F4_WioTermianal_final_all.ino.bin       -- 所有功能测试固件
F3_WioTerminal_fianl_no_bt.bin		-- 不包含BT功能测试固件
F2_firmware_for_enduser.bin		-- 最终用户固件
F1_bootloader_unlocked.ino.bin		-- 解锁Bootloader不能烧录固件


F4_WioTermianal_final_all.ino_v2.bin	--功能测试追加模块是否校准步骤测试(读出E-Fuse内容，判断MAC地址是否写)
F3_WioTerminal_fianl_no_bt_v2.bin	--功能测试不包含BT，追加是否校准测试步骤


F4_WioTermianal_final_all.ino_v3.bin	--Pi Header GPIO测试FAIL处理(数组数量+1)
F3_WioTerminal_fianl_no_bt_v3.bin

F3_WioterminalTestCode20200529.bin      --2020.05.29日RTL8720DN模块固件更新(SPI通信)，测试固件适配更新
F3_WioterminalTestCode20200620.bin	     --2020.06.20日追加在焊接屏幕之前的三个开关功能测试
F3_WioterminalTestCode20200624.bin	     --2020.06.24日MP模式确认是否校准/WiFi扫描


F4_wifi_scan.ino.bin			     --2022.07.08日追加wifi扫描测试固件(只用于调试用)		

WioTerminalDebug.ino.bin		--2020.06.24日做成手动确认模块功能固件
					P 2 0 --> 设置模块进入MP模式
					P 2 1 --> 通过串口读取模块E-Fuse数据
					P 2 2 --> 通过串口发指令让模块扫描wifi
					P 3 0 --> 设置模块进入正常模式
					P 4   --> SPI模式下扫描WiFi
				   	P 5   --> SPI模式下读取模块固件版本