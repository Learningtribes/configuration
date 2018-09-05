.PHONY: ci.build ci.push

ci.build:
	docker build -t ltdps/configuration:latest -f ci/Dockerfile .

ci.push: ci.build
	docker push ltdps/configuration:latest
