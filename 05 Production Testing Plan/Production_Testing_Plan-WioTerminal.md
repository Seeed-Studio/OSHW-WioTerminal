# Wio Terminal Testplan

## 1. Flash Bootloader

### Firmware flash tool

[J-Link BASE Debug Probe](https://www.segger.com/products/debug-probes/j-link/models/j-link-base/)

![](https://files.seeedstudio.com/wiki/Wio-Terminal/OSHW/Aspose.Words.404a1889-d01e-409a-8ee3-e39eb935ba1e.001.png) ![](https://files.seeedstudio.com/wiki/Wio-Terminal/OSHW/Aspose.Words.404a1889-d01e-409a-8ee3-e39eb935ba1e.002.png)

## Wio Terminal port for program firmware

|No. |JLink |Wio Terminal |
| - | - | - |
|1 |Pin-1 |VTref |J7-6 |VCC3V3\_MCU |
|2 |Pin-7 |SWDIO |J7-2 |SWDIO |
|3 |Pin-9 |SWCLK |J7-1 |SWDCLK |
|4 |Pin-12 |GND |J7-5 |GND |

![](https://files.seeedstudio.com/wiki/Wio-Terminal/OSHW/Aspose.Words.404a1889-d01e-409a-8ee3-e39eb935ba1e.003.png) ![](https://files.seeedstudio.com/wiki/Wio-Terminal/OSHW/Aspose.Words.404a1889-d01e-409a-8ee3-e39eb935ba1e.004.png)

### Flash Script

```
@ECHO OFF
ECHO start to auto processing and exit
cd bootloader_upload_script_samd51
JFlash.exe -openprjDefault.jflash -openbootloader-wio_terminal-v3.7.0-79-gd73dd64.bin -auto -exit
IF ERRORLEVEL 1 goto ERROR
goto END


:ERROR
ECHO J-Flash program Error!!
cd ..
pause


:END
```

[bootloader_upload_script_samd51.zip](https://drive.weixin.qq.com/s?k=AGEAZwfLABEDLAviEXAb8ACQYAAEM)

## 2. Flash test firmware

After flash the bootloader, connect Wio Terminal 's type C port to PC. Flash test firmware to Wio Terminal.

### Flash Script 

```
cd firmware_upload_script_usb
python2 0.testcode_flash.py 6
python2 1.ReceiveSerial.py
cd..
```

[firmware_upload_script_usb.zip](https://drive.weixin.qq.com/s?k=AGEAZwfLABEoCiyPPIAb8ACQYAAEM)

## 3. Function test

### a. Screen Test

![](https://files.seeedstudio.com/wiki/Wio-Terminal/OSHW/Aspose.Words.404a1889-d01e-409a-8ee3-e39eb935ba1e.007.png)![](https://files.seeedstudio.com/wiki/Wio-Terminal/OSHW/Aspose.Words.404a1889-d01e-409a-8ee3-e39eb935ba1e.008.png)![](https://files.seeedstudio.com/wiki/Wio-Terminal/OSHW/Aspose.Words.404a1889-d01e-409a-8ee3-e39eb935ba1e.009.png)

### b. Function Test

Hardware connection when testing-fpc connector

![](https://files.seeedstudio.com/wiki/Wio-Terminal/OSHW/Aspose.Words.404a1889-d01e-409a-8ee3-e39eb935ba1e.010.png)

Hardware connection when testing-Raspberry Pi Header

![](https://files.seeedstudio.com/wiki/Wio-Terminal/OSHW/Aspose.Words.404a1889-d01e-409a-8ee3-e39eb935ba1e.011.png)

![](https://files.seeedstudio.com/wiki/Wio-Terminal/OSHW/Aspose.Words.404a1889-d01e-409a-8ee3-e39eb935ba1e.012.png)

## 4. Flash End User Firmware

After complete the function test, flash the end user firmware to Wio Terminal 

### Flash Script 

```
echo %time%
cd ambd_flash_tool
:ambd_flash_tool.exe flash
python ambd_flash_tool.py erase
if %errorlevel% NEQ 0 goto error


timeout /t 1
python ambd_flash_tool.py flash
if %errorlevel% NEQ 0 goto error


timeout /t 2
cd ..
echo %time%
cd firmware_upload_script_usb
python2 0.testcode_flash.py 2
cd..
pause


:error
echo command failed
pause
```

[ambd_flash_tool.zip](https://drive.weixin.qq.com/s?k=AGEAZwfLABEfeMBB1KAb8ACQYAAEM)

After flash the firware, the screen will show as below

![](https://files.seeedstudio.com/wiki/Wio-Terminal/OSHW/Aspose.Words.404a1889-d01e-409a-8ee3-e39eb935ba1e.014.png)
