node {

    Test_Result = 'SUCCESSFUL'
    GitHub_Pull = 'FAIL'
    Pylint_SW_Metrics = 'FAIL'
    GitHubPull = 'FAIL'
    Unit_Test = 'FAIL'
    HWIL_Test = 'FAIL'
    Post_Process = 'FAIl'


    try {
       
        stage('GitHub Pull') { 
            // Get Code from GitHub
            step([$class: 'WsCleanup'])
            git 'https://github.com/ClintAnthony2492/test'
            GitHub_Pull = 'PASS'
        }

        stage('Pylint: SW Metrics') {
            sh '''#!/bin/bash
                  pylint hwil_gps_v002.py
                  echo "pylint complete"
            '''
            Pylint_SW_Metrics = 'PASS'
        }

        stage('Unit Test') {
            sh '''#!/bin/bash
                  python3 -m unittest -v test_format_date.py
                  echo "Unittest complete"
            '''
            echo "Unit Test Complete"
            Unit_Test = 'PASS'
        }

        stage('HWIL') {
            sh '''#!/bin/bash
                  python3 pyboard.py --device /dev/tty.usbmodem2085348F344D2 hwil_gps_v002.py
                  sleep 10
            '''
            echo "Necessary Board Reset"

            echo "Hardware in the Loop Testing complete"
            HWIL_Test = 'PASS'
        }

        stage('Post-Process & Analysis') {
            sh '''#!/bin/bash
                  python3 pyboard.py --device /dev/tty.usbmodem2085348F344D2 post_process_logs.py
                  sleep 5
                  python3 pyboard.py --device /dev/tty.usbmodem2085348F344D2 send_standby.py
            '''
            echo "Post-Process and Analysis complete"
            Post_Process = 'PASS'
        }

    } catch(err) {
        Test_Result = 'FAILED'
        throw err
    }

    finally {
        stage('Email Notify') {
            emailext attachLog: true, body: "GitHub PULL:    ${GitHub_Pull}\nPylint SW Metrics:    ${Pylint_SW_Metrics} \
                     \nUnit Test:    ${Unit_Test} \nHWIL:    ${HWIL_Test} \nPost-Process & Analysis:    ${Post_Process}", 
                     to: 'ant.dg24@gmail.com', subject: "Test Results: ${Test_Result}"
        }
    }
}