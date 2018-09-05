pipeline {
    agent {
<<<<<<< HEAD
        docker {
            image 'ltdps/configuration:latest'
            args '''
            -u root:root
=======
        dockerfile {
          filename 'ci/Dockerfile'
          args '''
            -u 'root:root'
>>>>>>> master
            -v /var/run/docker.sock:/var/run/docker.sock
            -v /usr/bin/docker:/usr/bin/docker
            '''
        }
    }
    environment {
        COMMIT_RANGE = "HEAD~1"
        BUILD_DIR = "${env.WORKSPACE}"
        BUILD_TAG = "${env.GIT_COMMIT}"
    }
    stages {
<<<<<<< HEAD
        stage('Syntax Check') {
=======
        stage('Test') {
>>>>>>> master
            steps {
                sh 'make test'
            }
            post {
                always {
                    sh 'make test.clean'
                }
            }
        }
        stage ('Try Build Image') {
            steps {
                sh "make docker.build"
            }
            post {
                always {
                    sh 'make docker.clean'
                }
            }
        }
    }
}
