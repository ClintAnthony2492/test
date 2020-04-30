node {

    // declare variables for emailing purposes
    Test_Result = 'SUCCESSFUL'
    GitHub_Pull = 'FAIL'
    Pylint_SW_Metrics = 'FAIL'
    GitHubPull = 'FAIL'
    Unit_Test = 'FAIL'
    HWIL_Test = 'FAIL'
    Post_Process = 'FAIL'


    try {
        // Stage GitHub Pull - This pulls a latest build from the main repository
        stage('GitHub Pull') { 
            echo "----------------------------------------------------------------------"
            echo "GitHub Pull in proress..."
            echo "----------------------------------------------------------------------"
            // Get build from GitHub
            step([$class: 'WsCleanup'])
            git 'https://github.com/ClintAnthony2492/test'

            GitHub_Pull = 'PASS'
            echo "GitHub Pull Complete"
        }
        // Stage Pylint SW Metrics - This conducts basic software metrics the main 
        // python script hwil_gps.py. Powered by a third party python library called Pylint.
        stage('Pylint: SW Metrics') {
            echo "----------------------------------------------------------------------"
            echo "Pylint: Software Metrics in progress..."
            echo "----------------------------------------------------------------------"
            // Need to utilize bash shell to call pylint
            sh '''#!/bin/bash
                  pylint hwil_gps.py
                  echo "pylint complete"
            '''
            Pylint_SW_Metrics = 'PASS'
        }
        // Stage Unit Test  - This conducts 1 simple unit test on a module that formats
        // a 'date' for easier reading. Powered by Unittest which is already integrated
        // in the python3 libraries
        stage('Unit Test') {
            echo "----------------------------------------------------------------------"
            echo "Unit Testing in progress..."
            echo "----------------------------------------------------------------------"
            // Need to utilize bash shell to call python3 
            sh '''#!/bin/bash
                  python3 -m unittest -v test_format_date.py
                  echo "Unittest on test_format_date.py complete"
            '''
            echo "Unit Test Complete"
            Unit_Test = 'PASS'
        }
        // Stage HWIL - This is the main stage that conduct hardware in the loop testing.
        // This pytest test commminicates with the MicroPython Pyboard that communicates 
        // the Adafruit GPS Module. 
        stage('HWIL') {
            echo "----------------------------------------------------------------------"
            echo "Hardware in the Loop Testing in progress..."
            echo "----------------------------------------------------------------------"
            // Need to utilize bash shell to call python3 
            sh '''#!/bin/bash
                  python3 pyboard.py --device /dev/tty.usbmodem2085348F344D2 hwil_gps.py
            '''
            sh '''#!/bin/bash
                  sleep 10
            '''

            echo "Necessary Board Reset"

            echo "Hardware in the Loop Testing complete"
            HWIL_Test = 'PASS'
        }
        // Stage Post-Process and Analysis - This stage post-processes the the logs created in
        // the HWIL stage. post_process_logs.py parses throught the logs and analyzes the test
        // data. It calculates the Time to First Fix and outputs satalite from the GPS Sentences.
        stage('Post-Process & Analysis') {
            echo "----------------------------------------------------------------------"
            echo "Post-Process & Analysis' in progress... "
            echo "----------------------------------------------------------------------"
            // Need to utilize bash shell to call python3 
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
        // Stage Email Notify: Final Stage that notifies the  developer a test has finished
        // along with test results and a build log.
        stage('Email Notify') {
            emailext attachLog: true, body: "This is an automated email by Jenkins. \
            \nA Jenkins pipeline has been triggerd from a repository change. \
            \nIt coducted a pipeline test on MicroPython Pyboard GPS Project \
            \nSee below and build.log attached for results. \
            \n\n\nGitHub PULL:    ${GitHub_Pull}\nPylint SW Metrics:    ${Pylint_SW_Metrics} \
            \nUnit Test:    ${Unit_Test} \nHWIL:    ${HWIL_Test} \nPost-Process & Analysis:    ${Post_Process}", 
            to: 'ant.dg24@gmail.com', subject: "Test Results: ${Test_Result}"
        }
    }
}