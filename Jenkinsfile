node {

    Test_Result = 'SUCCESSFUL'
    GitHub_Pull = 'PASS'
    Pylint_SW_Metrics = 'PASS'
    GitHubPull = 'PASS'
    Unit_Test = 'PASS'
    HWIL_Test = 'PASS'
    Post_Process = 'PASS'


    try {
       
        stage('GitHub Pull') { 
            try {
                // Get Code from GitHub
                step([$class: 'WsCleanup'])
                git 'https://github.com/ClintAnthony2492/test'
            } catch(err) {
                GitHub_Pull = 'FAILED'
                echo "<FAIL> GitHub Pull FAILED"
            }
        }

        stage('Pylint: SW Metrics') {
            try {
                sh '''#!/bin/bash
                      pylint hwil_gps_v002.py
                      echo "pylint complete"
                '''
            } catch(err) {
                Pylint_SW_Metrics = 'FAILED'
                echo "<FAIL> Pylint SW Metrics FAILED"
            }
        }

        stage('Unit Test') {
            try {
                sh '''#!/bin/bash
                      python3 -m unittest -v test_format_date.py
                      echo "Unittest complete"
                '''
                echo "Unit Test Complete"
            } catch(err) {
                Unit_Test = 'FAILED'
                echo "<FAIL> Unit Test  FAILED"
            }
        }

        stage('HWIL') {
            try {
                sh '''#!/bin/bash
                      python3 pyboard.py --device /dev/tty.usbmodem2085348F344D2 hwil_gps_v002.py
                      sleep 10
                '''
                echo "Necessary Board Reset"

                echo "Hardware in the Loop Testing complete"
            } catch(err) {
                HWIL_Test = 'FAILED'
                echo "<FAIL> HWIL FAILED"
            }
        }

        stage('Post-Process & Analysis') {
            try {
                sh '''#!/bin/bash
                      python3 pyboard.py --device /dev/tty.usbmodem2085348F344D2 post_process_logs.py
                      sleep 5
                      python3 pyboard.py --device /dev/tty.usbmodem2085348F344D2 send_standby.py
                '''
                echo "Post-Process and Analysis complete"
            } catch(err) {
                Post_Process = 'FAILED'
                echo "<FAIL> Post_Process & Analysis FAILED"
            }
        }

    } catch(err) {
        Test_Result = 'FAILED'
        throw err
    }

    finally {
        stage('Email Notify') {
            emailext body: "GitHub PULL: ${GitHub_Pull} \n Pylint: SW Metrics: ${Pylint_SW_Metrics} \n \
                            Unit Test: ${Unit_Test} \n HWIL: ${HWIL_Test}  \n Post-Process & Analysis: ${Post_Process}"
                            , to: 'ant.dg24@gmail.com', subject: "Test Results: ${Test_Result}"
        }
    }
}