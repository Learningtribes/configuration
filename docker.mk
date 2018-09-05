.PHONY: docker.build docker.clean docker.push

SHARD=0
SHARDS=1
IMAGE_TAG?=latest
BUILD_TAG?=test
dockerfiles:=$(shell ls docker/build/*/Dockerfile)
#all_images:=$(patsubst docker/build/%/Dockerfile,%,$(dockerfiles))
all_images:=edxapp notes ecommerce credentials discovery forum devpi

# Used in the test.mk file as well.
# set COMMIT_RANGE in CI environment for build on need
images:=$(if $(COMMIT_RANGE),$(shell git diff --name-only $(COMMIT_RANGE) | python util/parsefiles.py),$(all_images))
#images:=edxapp notes ecommerce credentials discovery forum devpi

docker_build=docker.build.
docker_push=docker.push.
docker_clean=docker.clean.

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

<<<<<<< HEAD
build: docker.build

=======
# N.B. / is used as a separator so that % will match the /
# in something like 'edxops/trusty-common:latest'
# Also, make can't handle ':' in filenames, so we instead '@'
# which means the same thing to docker
>>>>>>> master
clean: docker.clean
build: docker.build

docker.test.shard: $(foreach image,$(shell echo $(images) | python util/balancecontainers.py $(SHARDS) | awk 'NR%$(SHARDS)==$(SHARD)'),$(docker_test)$(image))

docker.build: $(foreach image,$(images),$(docker_build)$(image))
docker.push: $(foreach image,$(images),$(docker_push)$(image))
<<<<<<< HEAD

$(docker_build)%: docker/build/%/Dockerfile
	docker build -t ltdps/$*:latest -f $< .

$(docker_push)%: $(docker_build)%
	docker push ltdps/$*:latest
=======
docker.clean: $(foreach image,$(images),$(docker_clean)$(image))

$(docker_build)%: docker/build/%/Dockerfile
	docker build -t ltdps/$*:$(BUILD_TAG) -f $< .

$(docker_push)%: $(docker_build)%
	docker tag ltdps/$*:$(BUILD_TAG) ltdps/$*:$(IMAGE_TAG)
	docker push ltdps/$*:$(IMAGE_TAG)

$(docker_clean)%:
	docker rmi ltdps/$*:$(BUILD_TAG) || true
	docker rmi `docker images -f "dangling=true" -q` || true
>>>>>>> master
