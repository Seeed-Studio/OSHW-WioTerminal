import subprocess
import datetime
import sys
import os
import time
import shlex
import serial
from serial.tools import list_ports
from time import sleep

Model = sys.argv[1]

if Model == "1":
    TEST_PROGRAM = "F1_bootloader_unlocked.ino.bin"
if Model == "2":
    TEST_PROGRAM = "F2_firmware_for_enduser.bin"
if Model == "3":
    TEST_PROGRAM = "F3_WioTerminal_fianl_no_bt_v3.bin"
if Model == "4":
    TEST_PROGRAM = "F4_WioTermianal_final_all.ino_v3.bin"
if Model == "5":
    TEST_PROGRAM = "TEST_SAMD51.ino.bin" 
if Model == "6":
    TEST_PROGRAM = "F3_WioterminalTestCode20200624.bin"
    
if Model == "7":
    TEST_PROGRAM = "WioTerminalDebug.ino.bin"    
    
if Model == "8":
    TEST_PROGRAM = "F4_wifi_scan.ino.bin"    


tool = 'bossac.exe'
#TEST_PROGRAM = 'mp_bootloader_wio_terminal.bin'

def timeout_command(command, timeout=10):
    """
    call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None
    """

    if type(command) == type(''):
        command = shlex.split(command)
    start = datetime.datetime.now()
    process = subprocess.Popen(command)  # , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    resultcode = process.poll()
    while resultcode is None:
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            process.kill()
            return -1
        sleep(0.01)
        resultcode = process.poll()
    return resultcode

def find_device():
    timeout = 50
    while timeout != 0:
        port = None
        for p in list_ports.comports():
            print p[2]
            if p[2].upper().startswith('USB VID:PID=2886:002D'):
                port = p[0]
                print('find port: ' + port)
                return port

            if p[2].upper().startswith('USB VID:PID=2886:802D'):
                port = p[0]
                os.system("MODE %s:1200,N,8,1" %port)
                time.sleep(1)
            

        sleep(0.1)
        timeout -= 1

    print('No test board found')
    return None

def write_test():
    print('Write  test program to test board')
    sleep(0.1)
    port = find_device()
    if not port:
        return -1

    cmd = '%s -i -d --port=%s -U -i --offset=0x4000 -w -v %s -R' % (tool, port, TEST_PROGRAM)
    return timeout_command(cmd)


port=find_device()
write_test() 
time.sleep(2) 


