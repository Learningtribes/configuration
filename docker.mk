.PHONY: docker.build

SHARD=0
SHARDS=1

dockerfiles:=$(shell ls docker/build/*/Dockerfile)
#all_images:=$(patsubst docker/build/%/Dockerfile,%,$(dockerfiles))
#all_images:=edxapp notes ecommerce credentials discovery forum devpi
all_images:=forum devpi

# Used in the test.mk file as well.
# set COMMIT_RANGE in CI environment for build on need
images:=$(if $(COMMIT_RANGE),$(shell git diff --name-only $(COMMIT_RANGE) | python util/parsefiles.py),$(all_images))
#images:=edxapp notes ecommerce credentials discovery forum devpi

docker_build=docker.build.
docker_push=docker.push.

help: docker.help

docker.help:
	@echo '    Docker:'
	@echo '        $$image: "images in $(images)"'
	@echo '        $$container: any container defined in docker/build/$$container/Dockerfile'
	@echo ''
	@echo '        $(docker_pull)$$image        pull $$image from dockerhub'
	@echo ''
	@echo '        $(docker_build)$$container   build $$container'
	@echo '        $(docker_push)$$container    push $$container to dockerhub '
	@echo ''
	@echo '        docker.build          build all defined docker containers (based on dockerhub base images)'
	@echo '        docker.push           push all defined docker containers'
	@echo ''

# N.B. / is used as a separator so that % will match the /
# in something like 'edxops/trusty-common:latest'
# Also, make can't handle ':' in filenames, so we instead '@'
# which means the same thing to docker
docker_pull=docker.pull/

build: docker.build

clean: docker.clean

docker.clean:
	rm -rf .build

docker.test.shard: $(foreach image,$(shell echo $(images) | python util/balancecontainers.py $(SHARDS) | awk 'NR%$(SHARDS)==$(SHARD)'),$(docker_test)$(image))

docker.build: $(foreach image,$(images),$(docker_build)$(image))
docker.push: $(foreach image,$(images),$(docker_push)$(image))


$(docker_pull)%:
	docker pull $(subst @,:,$*)

$(docker_build)%: docker/build/%/Dockerfile
	docker build -t ltdps/$*:test -f $< .

$(docker_push)%: $(docker_build)%
	docker push ltdps/$*:test


.build/%/Dockerfile.d: docker/build/%/Dockerfile Makefile
	@mkdir -p .build/$*
	$(eval FROM=$(shell grep "^\s*FROM" $< | sed -E "s/FROM //" | sed -E "s/:/@/g"))
	$(eval EDXOPS_FROM=$(shell echo "$(FROM)" | sed -E "s#edxops/([^@]+)(@.*)?#\1#"))
	@echo "$(docker_build)$*: $(docker_pull)$(FROM)" > $@

-include $(foreach image,$(images),.build/$(image)/Dockerfile.d)
