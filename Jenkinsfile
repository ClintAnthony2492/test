//Build 002
node {

    Test_Result = 'SUCCESSFUL'

    try {
        
        stage('GitHub Pull') { 
            echo "----------------------------------------------------------------------"
            echo "GitHub Pull in proress..."
            echo "----------------------------------------------------------------------"
            // Get Code from GitHub
            step([$class: 'WsCleanup'])
            git 'https://github.com/ClintAnthony2492/test'

            echo "GitHub Pull Complete"
        }

        stage('Pylint: SW Metrics') {
            echo "----------------------------------------------------------------------"
            echo "Pylint: Software Metrics in proress..."
            echo "----------------------------------------------------------------------"
            sh '''#!/bin/bash
                  pylint hwil_gps.py
                  echo "hwil_gps.py metrics complete"
            '''
            echo "Pylint: SW Metrics Complete"
        }

        stage('Unit Test') {
            echo "----------------------------------------------------------------------"
            echo "Unit Testing in proress..."
            echo "----------------------------------------------------------------------"

            echo "Unit Test is not implemented"
        }

        stage('HWIL') {
            sh '''#!/bin/bash
                  python3 pyboard.py --device /dev/tty.usbmodem2085348F344D2 hwil_gps.py
                  sleep 10
            '''
            echo "Necessary Board Reset..."

            echo "Hardware in the Loop Testing complete"
        }

        stage('Post-Process & Analysis') {
            sh '''#!/bin/bash
                  python3 pyboard.py --device /dev/tty.usbmodem2085348F344D2 post_process_logs.py
                  sleep 5
                  python3 pyboard.py --device /dev/tty.usbmodem2085348F344D2 send_standby.py
            '''
            echo "Post-Process and Analysis complete"
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