import os
import sys
import platform
import shutil
import struct
import re
import time

try:
    import pathlib
except ImportError:
    print("Installing pathlib module")
    res = os.system("pip3 install pathlib")
    if res != 0:
        print("pathlib module installation failed")
        sys.exit(1)
    import pathlib

from pathlib import Path

try:
    import click
except ImportError:
    print("Installing click module")
    res = os.system("pip3 install click")
    if res != 0:
        print("click module installation failed")
        sys.exit(1)
    import click

try:
    import colorama
except ImportError:
    print("Installing colorama module")
    res = os.system("pip3 install colorama")
    if res != 0:
        print("Colorama module installation failed")
        sys.exit(1)
    import colorama

from colorama import init, Fore, Back, Style

try:
    import serial
except ImportError:
    print("Installing pyserial module")
    res = os.system("pip3 install pyserial")
    if res != 0:
        print("pyserial module installation failed")
        sys.exit(1)
    import serial

if os.name == 'nt':  # sys.platform == 'win32':
    from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports
else:
    raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))

# List of supported board USB IDs.  Each board is a tuple of unique USB vendor
# ID, USB product ID.
BOARD_IDS = \
    [{
        "name": "wio terminal",
        "info": ("2886", "802D"),
        "isbootloader": False
    },
    {
        "name": "wio terminal",
        "info": ("2886", "002D"),
        "isbootloader": True
    }]

def getAllPortInfo():
    return comports(include_links=False)
    
def getAvailableBoard():
    for info in getAllPortInfo():
        port, desc, hwid = info 
        ii = hwid.find("VID:PID")
        #hwid: USB VID:PID=2886:002D SER=4D68990C5337433838202020FF123244 LOCATION=7-3.1.3:1.
        if ii != -1:
            for b in  BOARD_IDS:
                (vid, pid) = b["info"]
                if vid == hwid[ii + 8: ii + 8 + 4] and pid == hwid[ii + 8 + 5 :ii + 8 + 5 + 4 ]:
                    if b["isbootloader"] == True :
                        return port, True
                    else:
                        return port, False
    return None, False

def stty(port):
    
    if port == None:
        _port, _isbootloader = getAvailableBoard()
        if _port == None:
            print(Fore.RED + "Sorry, the device you should have is not plugged in.")
            sys.exit(1)
    else:
        _port = port

    if os.name == "posix":
        if platform.uname().system == "Darwin":
            return "stty -f " + _port + " %d"
        return "stty -F " + _port + " %d"
    elif os.name == "nt":
        return "MODE " + _port + ":BAUD=%d PARITY=N DATA=8"
    
    return "echo not support"

def get_flash_tool():
    _tool = str(Path(os.path.split(os.path.realpath(__file__))[0], 'tool'))
    _platform = platform.platform()
    if _platform.find('Windows') >= 0:
        _tool = str(Path(_tool, 'windows', "amebad_image_tool.exe"))
    elif _platform.find('Linux') >= 0:
        _tool = str(Path(_tool, 'linux', 'amebad_image_tool'))
    elif _platform.find('Darwin') >= 0:
        _tool = str(Path(_tool, 'macos', 'amebad_image_tool'))
    elif _platform.find('macOS') >= 0:
        _tool = str(Path(_tool, 'macos', 'amebad_image_tool'))
    else:
        _tool = ""
        print(Fore.RED, "No support yet!")
        sys.exit(1)
    return _tool

def get_bossac_tool():
    _tool = str(Path(os.path.split(os.path.realpath(__file__))[0], 'tool'))
    _platform = platform.platform()
    if _platform.find('Windows') >= 0:
        _tool = str(Path(_tool, 'windows', "bossac.exe"))
    elif _platform.find('Linux') >= 0:
        _tool = str(Path(_tool, 'linux', 'bossac'))
    elif _platform.find('Darwin') >= 0:
        _tool = str(Path(_tool, 'macos', 'bossac'))
    elif _platform.find('macOS') >= 0:
        _tool = str(Path(_tool, 'macos', 'bossac'))
    else:
        _tool = ""
        print(Fore.RED, "No support yet!")
        sys.exit(1)
    return _tool


def make_empty_img(length):
    _empty = struct.pack('B', 0xFF)
    with open("km0_boot_all.bin", "wb") as _km0_boot_all_bin:
        for i in range(8192):
            i
            _km0_boot_all_bin.write(_empty)
    _km0_boot_all_bin.close()

    with open("km4_boot_all.bin", "wb") as _km4_boot_all_bin:
        for i in range(4096):
            i
            _km4_boot_all_bin.write(_empty)
    _km4_boot_all_bin.close()

    with open("km0_km4_image2.bin", "wb") as _km0_km4_image2_bin:
        for i in range(length - 12):
            i
            for j in range(1024):
                j
                _km0_km4_image2_bin.write(_empty)
    _km0_km4_image2_bin.close()

def copy_img(dir):
    _local_dir = str(Path(os.path.split(os.path.realpath(__file__))[0]))
    _km0_boot_all_bin = str(Path(dir, "km0_boot_all.bin"))
    _km4_boot_all_bin = str(Path(dir, "km4_boot_all.bin"))
    _km0_km4_image2_bin = str(Path(dir, "km0_km4_image2.bin"))
    if not os.path.exists(_km0_boot_all_bin):
        print(Fore.RED + _km0_boot_all_bin + " not exists!")
        sys.exit(1)
    if not os.path.exists(_km4_boot_all_bin):
        print(Fore.RED + _km4_boot_all_bin + " not exists!")
        sys.exit(1)
    if not os.path.exists(_km0_km4_image2_bin):
        print(Fore.RED + _km0_km4_image2_bin + " not exists!")
        sys.exit(1)
    print(Fore.GREEN + "copy img to workspace...")
    shutil.copyfile(_km0_boot_all_bin, str(Path(_local_dir, "km0_boot_all.bin")))
    shutil.copyfile(_km4_boot_all_bin, str(Path(_local_dir, "km4_boot_all.bin")))
    shutil.copyfile(_km0_km4_image2_bin, str(Path(_local_dir, "km0_km4_image2.bin")))

    
@click.group()
@click.version_option(version='0.6.0')
def cli():
    """RTL872XD Flash tool

    This tool is used to burn rtl8720d firmware.
    """
    init(autoreset=True)
    pass

@cli.command()
@click.option(
    "--length",
    "-l",
    default=2048,
    type=click.INT,
    help="Length(kB) (default 2048kB).",
    metavar="DELAY",
)
@click.option(
    "--port",
    "-p",
    required=False,
    type=click.STRING,
    help="Name of serial port for connected board.",
    metavar="PORT",
)
def erase(length, port):
    if port == None:
        _port, _isbootloader = getAvailableBoard()
        if _port == None:
            print(Fore.RED + "Sorry, the device you should have is not plugged in.")
            sys.exit(1)
    else:
        _port = port
    
    if _isbootloader == False:
        _cmd = stty(_port)
        print(_cmd)
        if _cmd != "echo not support":
            os.system(_cmd%1200)
        time.sleep(2)
    _port, _isbootloader = getAvailableBoard()
    if _isbootloader == True:
        _tool = get_bossac_tool()
        _cmd = _tool + " -i -d --port=" + _port + " -U -i --offset=0x4000 -w -v " + str(Path(os.getcwd(), 'firmware')) + "/WioTerminal_USB2Serial_Burn8720.ino.bin -R" 
        os.system(_cmd)
   
    for i in range(0, 3):
        print(Fore.GREEN + "wait...")
        time.sleep(1)

    _port, _isbootloader = getAvailableBoard()
    if _port == None:
        print(Fore.RED + "Sorry, the device you should have is not plugged in.")
        sys.exit(1)

    make_empty_img(length)

    _tool = get_flash_tool()
    
    _cmd = _tool + " " + _port 

    print(Fore.GREEN + "Flashing...")
    obj = os.popen(_cmd)
    ret = obj.read()
    print(ret)
    if ret.find('successfully') >= 0:
        print(Fore.GREEN + "Success!")
    else:
        print(Fore.RED + "Error!")
        sys.exit(2)

@cli.command()
@click.option(
    "--port",
    "-p",
    required=False,
    type=click.STRING,
    help="Name of serial port for connected board.",
    metavar="PORT",
)
@click.option(
    "--dir",
    "-d",
    required=False,
    type=click.STRING,
    help="Specifies the location of the directory where the firmware is located",
    metavar="DIR",
)
def flash(port, dir):
    if port == None:
        _port, _isbootloader = getAvailableBoard()
        if _port == None:
            print(Fore.RED + "Sorry, the device you should have is not plugged in.")
            sys.exit(1)
    else:
        _port = port

    print(_port)
    
    if _isbootloader == False:
        _cmd = stty(_port)
        print(_cmd)
        if _cmd != "echo not support":
            os.system(_cmd%1200)
        time.sleep(2)
    _port, _isbootloader = getAvailableBoard()
    if _isbootloader == True:
        _tool = get_bossac_tool()
        _cmd = _tool + " -i -d --port=" + _port + " -U -i --offset=0x4000 -w -v " + str(Path(os.getcwd(), 'firmware')) + "/WioTerminal_USB2Serial_Burn8720.ino.bin -R" 
        os.system(_cmd)

    for i in range(0, 3):
        print(Fore.GREEN + "wait...")
        time.sleep(1)

    _port, _isbootloader = getAvailableBoard()

    if _port == None:
        print(Fore.RED + "Sorry, the device you should have is not plugged in.")
        sys.exit(1)

    if dir == None:
        dir = str(Path(os.getcwd(), 'firmware'))
  
    copy_img(dir)

    _tool = get_flash_tool()
    
    _cmd = _tool + " " + _port 

    print(Fore.GREEN + "Flashing...")
    obj = os.popen(_cmd)
    ret = obj.read()
    print(ret)
    if ret.find('successfully') >= 0:
        print(Fore.GREEN + "Success!")
    else:
        print(Fore.RED + "Error!")
        sys.exit(3)

if __name__ == "__main__":
    try:
        cli()
    except OSError:
        print("error")
        sys.exit(4)
   