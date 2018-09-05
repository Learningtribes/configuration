.PHONY: docker.build

SHARD=0
SHARDS=1

dockerfiles:=$(shell ls docker/build/*/Dockerfile)
#all_images:=$(patsubst docker/build/%/Dockerfile,%,$(dockerfiles))
all_images:=edxapp notes ecommerce credentials discovery forum devpi

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
	@echo '        $(docker_build)$$container   build $$container'
	@echo '        $(docker_push)$$container    push $$container to dockerhub '
	@echo ''
	@echo '        docker.build          build all defined docker containers (based on dockerhub base images)'
	@echo '        docker.push           push all defined docker containers'
	@echo ''

build: docker.build

clean: docker.clean

docker.clean:
	rm -rf .build

docker.test.shard: $(foreach image,$(shell echo $(images) | python util/balancecontainers.py $(SHARDS) | awk 'NR%$(SHARDS)==$(SHARD)'),$(docker_test)$(image))

docker.build: $(foreach image,$(images),$(docker_build)$(image))
docker.push: $(foreach image,$(images),$(docker_push)$(image))

$(docker_build)%: docker/build/%/Dockerfile
	docker build -t ltdps/$*:latest -f $< .

$(docker_push)%: $(docker_build)%
	docker push ltdps/$*:latest
