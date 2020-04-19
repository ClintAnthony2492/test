node {

    try {
        stage('GitHub Pull') { 
            // Get Code from GitHub
            git clean -fdx 
            git 'https://github.com/ClintAnthony2492/test'
        }

        stage('Pylint: SW Metrics') {
            sh '''#!/bin/bash
                  pylint add.py
                  echo "pylint complete"
            '''
        }

        stage('Unit Test') {
            sh '''#!/bin/bash
                  python3 -m unittest test_add.py
                  echo "Unittest complete"
            '''
            echo "Unit Test Complete"
        }

        stage('HWIL') {
            echo "Hardware in the Loop Testing complete"
        }

    } catch(err) {
        Test_Result = 'FAILED'
        throw err
    }

    finally {
        stage('Email') {

            //Jenkins by default will locate jelly script in JENKINS_HOME/email-templates
            //emailext attachLog: true, mimeType: 'text/html', body: '''${SCRIPT, template="groovy-html.template"}
            //Build artifacts can be found in:
            //''' + K_EmailArtDir, subject: "DOTC 17-28 Full Automated Test - Build ${VERSION}: ${Test_Result}" , to: 'Anthony.Deguzman@L3HARRIS.com'
        }
    }
}