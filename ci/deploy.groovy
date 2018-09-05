pipeline {
    agent any
    environment {
        COMMIT_RANGE = "HEAD~1"
        DOCKER = credentials("docker_hub")
        BUILD_TAG = "${env.GIT_COMMIT}"
    }
    parameters {
        string(name: "image_tag", defaultValue: "latest", description: "Tag of this image?")
    }
    stages {
        stage ('Build Image') {
            steps {
                sh "make docker.build"
            }
        }
        stage('Push Image') {
            steps {
                sh "docker login -u${DOCKER_USR} -p${DOCKER_PSW}"
                sh "IMAGE_TAG=${params.image_tag} make docker.push"
            }
            post {
                always {
                    sh 'make docker.clean'
                }
            }
        }
    }
}
