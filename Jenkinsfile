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
  }
}
