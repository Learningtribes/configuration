pipeline {
  agent any
  stages {
    stage('Syntax Checking') {
      agent {
        docker {
          image 'python:2'
          args '-u root:root'
        }
      }
      steps {
        sh 'make requirements'
        sh 'make test'
        sh 'make test.clean'
      }
    }
    stage('Build Image') {
        sh 'make docker.build'
    }
    stage('Push Image') {
        sh 'make docker.push'
    }
  }
}
