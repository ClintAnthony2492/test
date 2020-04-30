node {

    Test_Result = 'PASS'

    try {

        stage('GitHub Pull') { 
            echo "----------------------------------------------------------------------"
            echo "GitHub Pull in progress..."
            echo "----------------------------------------------------------------------"
            // Get Code from GitHub
            step([$class: 'WsCleanup'])
            git 'https://github.com/ClintAnthony2492/test'

            echo "GitHub Pull Complete"
        }

        stage('Pylint: SW Metrics') {
            try {
            echo "----------------------------------------------------------------------"
            echo "Pylint: Software Metrics in progress..."
            echo "----------------------------------------------------------------------"
            sh '''#!/bin/bash
                  pylint hwil_gps.py
            '''
            echo "Pylint: SW Metrics Complete"
            } catch(err) {
                echo "<FAIL> Pylint FAILED"
            }
        }

        stage('Unit Test') {
            echo "----------------------------------------------------------------------"
            echo "Unit Testing in progress..."
            echo "----------------------------------------------------------------------"

            echo "Unit Test is not implemented"
        }

        stage('HWIL') {
            echo "----------------------------------------------------------------------"
            echo "Hardware in the Loop Testing in progress..."
            echo "----------------------------------------------------------------------"

            sh '''#!/bin/bash
                  python3 pyboard.py --device /dev/tty.usbmodem2085348F344D2 hwil_gps.py
                  sleep 10
            '''
            echo "Necessary Board Reset..."
            
            echo "Hardware in the Loop Testing complete"
        }
        stage('Post-Process & Analysis') {
            echo "----------------------------------------------------------------------"
            echo "Post-Process & Analysis' in progress... "
            echo "----------------------------------------------------------------------"

            echo "Post-Process & Analysis is not implemented"
        }


    } catch(err) {
        Test_Result = 'FAILED'
        throw err
    }

    finally {
        stage('Email Notify') {
            emailext attachLog: true, body: "This is an automated email by Jenkins. \
            \nA Jenkins pipeline has been triggerd from a repository change. \
            \nIt coducted a pipeline test on MicroPython Pyboard GPS Project. \
            \nSee build.log attached for results.", to: 'ant.dg24@gmail.com', subject: "Test Results: ${Test_Result}"
        }
    }
}