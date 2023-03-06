####################################################################################
# Coding Python 3.11 UTF-8 [64-bit] (Python IDLE)
#
# PYAS Git: https://github.com/87owo/PYAS
# PYAS Web: https://pyantivirus.wixsite.com/pyas
#
# PYAS is managed by PYDT (Python Development Team)
# Copyright© 2020-2023 87owo (PYAS Security)
####################################################################################
#
##################################### 載入模組套件 ###################################

import os, sys, time, json, psutil, subprocess, requests
import win32api, win32con, socket, cryptocode, platform
from pefile import PE, DIRECTORY_ENTRY
from hashlib import md5, sha1, sha256
from PYAS_English import english_list
from win10toast import ToastNotifier
from threading import Thread
from random import randrange
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets, QtGui, QtCore
from PYAS_UI import Ui_MainWindow

###################################### 錯誤日誌 #####################################

def pyas_bug_log(e):
    try:
        print(f'[Error] {e}')
        with open('Library/PYAS/Temp/PYASB.log','a',encoding='utf-8') as ft:
            ft.write(f'{e}\n')
    except:
        pass

##################################### 移除暫存檔 ####################################

def remove_tmp():
    try:
        if os.path.isfile('Library/PYAS/Temp/PYASB.log'):
            os.remove('Library/PYAS/Temp/PYASB.log')
    except:
        pass

def remove_rtp():
    try:
        if os.path.isfile('Library/PYAS/Temp/PYASP.tmp'):
            os.remove('Library/PYAS/Temp/PYASP.tmp')
    except:
        pass

##################################### 資料庫檢查 ####################################

def pyas_lib():
    try:
        checkPath = ['Library/PYAS/Temp','Library/PYAS/Setup','Library/PYAS/Icon','Library/PYAE/Hashes']
        for i in checkPath:
            if not os.path.isdir(i):
                os.makedirs(i)
    except Exception as e:
        pyas_bug_log(e)

###################################### 密鑰認證 #####################################

def pyas_key():
    try:
        with open(sys.argv[0], 'rb') as f:
            file_md5 = str(md5(f.read()).hexdigest())
        try:
            response = requests.get("http://27.147.30.238:5001/pyas", params={'key': file_md5})
            if response.status_code == 200:
                if response.text == 'True':
                    with open('Library/PYAS/Setup/PYAS.key', 'w') as fc:
                        fc.write(file_md5)
                    return True
        except:
            if os.path.isfile('Library/PYAS/Setup/PYAS.key'):
                with open('Library/PYAS/Setup/PYAS.key', 'r') as fc:
                    if file_md5 == str(fc.read()):
                        return True
        return False
    except:
        return False

###################################### 主要程式 #####################################

class MainWindow_Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow_Controller, self).__init__()
        try:
            with open('Library/PYAE/Hashes/Viruslist.num', 'r') as f:
                self.vl = int(f.read())
        except:
            self.vl = 0
        self.ui = Ui_MainWindow() #繼承
        self.ui.pyas_opacity = 100
        self.setAttribute(Qt.WA_TranslucentBackground) #去掉邊框
        self.setWindowFlags(Qt.FramelessWindowHint) #取消使用Windows預設得窗口模式
        #self.setWindowFlags(Qt.WindowStaysOnTopHint|self.windowFlags()) #窗口置頂
        self.ui.setupUi(self)
        self.setup_control()
        
    def writeConfig(self, config):
        with open('Library/PYAS/Setup/PYAS.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(config, indent=4, ensure_ascii=False))
 
    def setup_control(self):
        self.init()#調用本地函數"init"
        self.ui.Close_Button.clicked.connect(self.close)#讓物件名稱"Close_Button"連接到函數"close"
        self.ui.Minimize_Button.clicked.connect(self.showMinimized)
        self.ui.Menu_Button.clicked.connect(self.ShowMenu)
        self.ui.State_Button.clicked.connect(self.Change_to_State_widget)
        self.ui.Protection_Button.clicked.connect(self.Change_to_Rrotection_widget)        
        self.ui.Virus_Scan_Button.clicked.connect(self.Change_to_Virus_Scan_widget)#Virus_Scan
        self.ui.Virus_Scan_Solve_Button.clicked.connect(self.Virus_Solve)
        self.ui.Virus_Scan_choose_Button.clicked.connect(self.Virus_Scan_Choose_Menu)
        self.ui.Virus_Scan_Break_Button.clicked.connect(self.Virus_Scan_Break)
        self.ui.File_Scan_Button.clicked.connect(self.File_Scan)#讓物件名稱"File_Scan_Button"連接到本地函數"File_Scan"
        self.ui.Path_Scan_Button.clicked.connect(self.Path_Scan)
        self.ui.Disk_Scan_Button.clicked.connect(self.pyas_scan_disk_init_en)
        self.ui.Tools_Button.clicked.connect(self.Change_to_Tools_widget)#More_Tools
        self.ui.System_Tools_Button.clicked.connect(lambda:self.Change_Tools(self.ui.System_Tools_widget))
        self.ui.System_Tools_Back.clicked.connect(lambda:self.Back_To_More_Tools(self.ui.System_Tools_widget))
        self.ui.Privacy_Tools_Button.clicked.connect(lambda:self.Change_Tools(self.ui.Privacy_Tools_widget))
        self.ui.Privacy_Tools_Back.clicked.connect(lambda:self.Back_To_More_Tools(self.ui.Privacy_Tools_widget))
        self.ui.Develop_Tools_Button.clicked.connect(lambda:self.Change_Tools(self.ui.Develop_Tools_widget))
        self.ui.Develop_Tools_Back.clicked.connect(lambda:self.Back_To_More_Tools(self.ui.Develop_Tools_widget))
        self.ui.More_Tools_Button.clicked.connect(lambda:self.Change_Tools(self.ui.More_Tools_widget))
        self.ui.More_Tools_Back.clicked.connect(lambda:self.Back_To_More_Tools(self.ui.More_Tools_widget))
        self.ui.System_Process_Manage_Button.clicked.connect(lambda:self.Change_Tools(self.ui.Process_widget))
        self.ui.Process_Tools_Back.clicked.connect(lambda:self.Back_To_More_Tools(self.ui.Process_widget))
        self.ui.System_Info_Button.clicked.connect(lambda:self.Change_Tools(self.ui.System_Info_widget))
        self.ui.System_Info_Back.clicked.connect(lambda:self.Back_To_More_Tools(self.ui.System_Info_widget))
        self.ui.Customize_CMD_Command_Button.clicked.connect(lambda:self.Change_Tools(self.ui.Customize_CMD_Command_widget))
        self.ui.Customize_CMD_Command_Back.clicked.connect(lambda:self.Back_To_More_Tools(self.ui.Customize_CMD_Command_widget))
        self.ui.Analyze_EXE_hash_Button.clicked.connect(lambda:self.Analyze_EXE(self.ui.Analyze_EXE_hash_Button))
        self.ui.Analyze_EXE_Back.clicked.connect(lambda:self.Back_To_More_Tools(self.ui.Analyze_EXE_widget))
        self.ui.Analyze_EXE_Bit_Button.clicked.connect(lambda:self.Analyze_EXE(self.ui.Analyze_EXE_Bit_Button))
        self.ui.Analyze_EXE_Funtion_Button.clicked.connect(lambda:self.Analyze_EXE(self.ui.Analyze_EXE_Funtion_Button))
        self.ui.Look_for_File_Button.clicked.connect(lambda:self.Change_Tools(self.ui.Look_for_File_widget))
        self.ui.Look_for_File_Back.clicked.connect(lambda:self.Back_To_More_Tools(self.ui.Look_for_File_widget))
        self.ui.Encryption_Text_Button.clicked.connect(lambda:self.Change_Tools(self.ui.Encryption_Text_widget))
        self.ui.Encryption_Text_Back.clicked.connect(lambda:self.Back_To_More_Tools(self.ui.Encryption_Text_widget))
        self.ui.Customize_REG_Command_Back.clicked.connect(lambda:self.Back_To_More_Tools(self.ui.Customize_REG_Command_widget))
        self.ui.Customize_REG_Command_Button.clicked.connect(lambda:self.Change_Tools(self.ui.Customize_REG_Command_widget))
        self.ui.Change_Users_Password_Button.clicked.connect(lambda:self.Change_Tools(self.ui.Change_Users_Password_widget))
        self.ui.Change_Users_Password_Back.clicked.connect(lambda:self.Back_To_More_Tools(self.ui.Change_Users_Password_widget))
        self.ui.About_Back.clicked.connect(self.ui.About_widget.hide)
        self.ui.Setting_Back.clicked.connect(self.Setting_Back)
        self.ui.Repair_System_Permission_Button.clicked.connect(self.Repair_System_Permission)
        self.ui.Repair_System_Files_Button.clicked.connect(self.Repair_System_Files)
        self.ui.Clean_System_Files_Button.clicked.connect(self.Clean_System_Files)
        self.ui.Enable_Safe_Mode_Button.clicked.connect(self.Enable_Safe_Mode)
        self.ui.Disable_Safe_Mode_Button.clicked.connect(self.Disable_Safe_Mode)
        self.ui.Delete_Private_File_Button.clicked.connect(self.Delete_Private_File)
        self.ui.Customize_CMD_Command_Run_Button.clicked.connect(self.Customize_CMD_Command)
        self.ui.Look_for_File_Run_Button.clicked.connect(self.Look_for_File)
        self.ui.Encryption_Text_Run_Button.clicked.connect(self.Encryption_Text)
        self.ui.Decrypt_Text_Run_Button.clicked.connect(self.Decrypt_Text)
        self.ui.Change_Users_Password_Run_Button.clicked.connect(self.Change_Users_Password)
        self.ui.Internet_location_Query_Button.clicked.connect(self.Internet_location_Query)
        self.ui.Rework_Network_Configuration_Button.clicked.connect(self.reset_network)
        self.ui.Customize_REG_Command_Run_Button.clicked.connect(self.Customize_REG_Command)
        self.ui.Process_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.Process_list.customContextMenuRequested.connect(self.Process_list_Menu)
        self.ui.Protection_switch_Button.clicked.connect(self.protect_threading_init)#Protection
        self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.clicked.connect(self.Show_Virus_Scan_Progress_Bar_switch)#Setting
        self.ui.Language_Traditional_Chinese.clicked.connect(self.Change_language)
        self.ui.Language_Simplified_Chinese.clicked.connect(self.Change_language)
        self.ui.Languahe_English.clicked.connect(self.Change_language)
        self.ui.Theme_White.clicked.connect(self.Change_Theme)
        self.ui.Theme_Black.clicked.connect(self.Change_Theme)
        self.ui.Theme_Green.clicked.connect(self.Change_Theme)
        self.ui.Theme_Pink.clicked.connect(self.Change_Theme)
        self.ui.Theme_Blue.clicked.connect(self.Change_Theme)
        self.ui.Theme_Red.clicked.connect(self.Change_Theme)

    def init(self):
        self.Safe = True
        self.Virus_Scan = False
        self.ui.widget_2.lower()
        self.ui.Navigation_Bar.raise_()
        self.ui.Window_widget.raise_()
        self.ui.Virus_Scan_choose_widget.raise_()
        self.Process_sim = QStringListModel()
        self.Process_quantity = []
        self.Process_Timer = QTimer()
        self.Process_Timer.timeout.connect(self.Process_list)
        if not os.path.exists('Library/PYAS/Setup/PYAS.json'):
            self.writeConfig({"high_sensitivity":0,"language":"english"})
        with open('Library/PYAS/Setup/PYAS.json', 'r', encoding='utf-8') as f:
            self.pyasConfig = json.load(f)
        try:
            self.ui.Theme_White.setChecked(True)
            if self.pyasConfig['language'] == "zh_TW":
                self.ui.Language_Traditional_Chinese.setChecked(True)
                self.lang_init_zh_tw()
            elif self.pyasConfig['language'] == "zh_CN":
                self.ui.Language_Simplified_Chinese.setChecked(True)
                self.lang_init_zh_cn()
            else:
                self.ui.Languahe_English.setChecked(True)
                self.lang_init_en()
        except:
            self.writeConfig({"high_sensitivity":0,"language":"english"})
            self.pyasConfig['language'] = "english"
            self.ui.Languahe_English.setChecked(True)
            self.lang_init_en()
        try:
            if self.pyasConfig['high_sensitivity'] == 1:
                self.show_virus_scan_progress_bar = 1
                self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.setText(self.text_Translate("已開啟"))
                self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.setStyleSheet("""
                QPushButton{border:none;background-color:rgba(20,200,20,100);border-radius: 15px;}
                QPushButton:hover{background-color:rgba(20,200,20,120);}""")
            else:
                self.show_virus_scan_progress_bar = 0
        except:
            self.show_virus_scan_progress_bar = 0
        self.ui.License_terms.setText('''Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.''')
        self.effect_shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow.setOffset(0,0) # 偏移
        self.effect_shadow.setBlurRadius(10) # 陰影半徑
        self.effect_shadow.setColor(QtCore.Qt.gray) # 陰影颜色
        self.ui.widget_2.setGraphicsEffect(self.effect_shadow)
        self.effect_shadow2 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow2.setOffset(0,0)
        self.effect_shadow2.setBlurRadius(10)
        self.effect_shadow2.setColor(QtCore.Qt.gray) 
        self.ui.Navigation_Bar.setGraphicsEffect(self.effect_shadow2)
        self.effect_shadow3 = QtWidgets.QGraphicsDropShadowEffect(self)
        self.effect_shadow3.setOffset(0,0)
        self.effect_shadow3.setBlurRadius(7)
        self.effect_shadow3.setColor(QtCore.Qt.gray) 
        self.ui.Window_widget.setGraphicsEffect(self.effect_shadow3)
        self.ui.Virus_Scan_choose_widget.hide()#hide()函數的用意是隱藏物件
        self.ui.Virus_Scan_widget.hide()
        self.ui.Tools_widget.hide()
        self.ui.Protection_widget.hide()
        self.ui.System_Tools_widget.hide()
        self.ui.Privacy_Tools_widget.hide()
        self.ui.Develop_Tools_widget.hide()
        self.ui.More_Tools_widget.hide()
        self.ui.Virus_Scan_Solve_Button.hide()
        self.ui.Virus_Scan_Break_Button.hide()
        self.ui.Virus_Scan_ProgressBar.hide()
        self.ui.Process_widget.hide()
        self.ui.System_Info_widget.hide()
        self.ui.Customize_CMD_Command_widget.hide()
        self.ui.Analyze_EXE_widget.hide()
        self.ui.Look_for_File_widget.hide()
        self.ui.Encryption_Text_widget.hide()
        self.ui.About_widget.hide()
        self.ui.Change_Users_Password_widget.hide()
        self.ui.Customize_REG_Command_widget.hide()
        self.ui.Setting_widget.hide()
        Thread(target = self.pyas_protect_init).start()
        Thread(target = self.pyas_vl_update).start()

##################################### 更新資料庫 ####################################

    def pyas_vl_update(self):
        for i in range(self.vl, 100000):
            try:
                y = f'VirusShare_{i:05}.md5'
                response = requests.get(f'https://virusshare.com/hashfiles/{y}', allow_redirects=True)
                if response.status_code == 200:
                    with open('Library/PYAE/Hashes/Viruslist.md5', 'a') as vlist:
                        lists_write = response.content.decode("utf-8").split('\n')[6:-1]
                        for list_write in lists_write:
                            vlist.write(str(list_write)[:10]+'\n')
                    self.vl = i + 1
                else:
                    self.vl = i
                    print(f'[INFO] Hashes Update Complete (V{self.vl - 1})')
                    break
                with open('Library/PYAE/Hashes/Viruslist.num', 'w') as f:
                    f.write(str(self.vl))
            except Exception as e:
                print(e)
                print(f'[INFO] Hashes Update Fail (V{self.vl - 1})')
                break

##################################### 英文初始化 ####################################
    
    def lang_init_en(self):
        _translate = QtCore.QCoreApplication.translate
        if self.Safe:
            self.ui.State_title.setText(_translate("MainWindow", "This device has been protected"))
        else:
            self.ui.State_title.setText(_translate("MainWindow", "This device is currently unsafe"))
        if pyas_key():
            self.ui.Window_title.setText(_translate("MainWindow", f"PYAS V{pyas_version}"))
        else:
            self.ui.Window_title.setText(_translate("MainWindow", f"PYAS V{pyas_version} (Security Key Error)"))
        cy = time.strftime('%Y')
        if int(cy) < 2020:
            cy = str('2020')
        self.ui.PYAS_CopyRight.setText(_translate("MainWindow", f"Copyright© 2020-{cy} 87owo (PYAS Security)"))
        if self.vl <= 0:
            self.ui.PYAE_Version.setText(_translate("MainWindow", f"PYAE V{pyae_version} (Downloading Library...)"))
        else:
            self.ui.PYAE_Version.setText(_translate("MainWindow", f"PYAE V{pyae_version} (Library Version: "+str(self.vl-1)+")"))
        self.ui.State_Button.setText(_translate("MainWindow", "State"))
        self.ui.Virus_Scan_Button.setText(_translate("MainWindow", "Scan"))
        self.ui.Tools_Button.setText(_translate("MainWindow", "Tools"))
        self.ui.Protection_Button.setText(_translate("MainWindow", "Protect"))
        self.ui.Virus_Scan_title.setText(_translate("MainWindow", "Virus Scan"))
        self.ui.Virus_Scan_text.setText(_translate("MainWindow", "Please select a scan method"))
        self.ui.Virus_Scan_choose_Button.setText(_translate("MainWindow", "Virus Scan"))
        self.ui.File_Scan_Button.setText(_translate("MainWindow", "File Scan"))
        self.ui.Path_Scan_Button.setText(_translate("MainWindow", "Path Scan"))
        self.ui.Disk_Scan_Button.setText(_translate("MainWindow", "Full Scan"))
        self.ui.Virus_Scan_Solve_Button.setText(_translate("MainWindow", "Solve Now"))
        self.ui.Virus_Scan_Break_Button.setText(_translate("MainWindow", "Stop Scan"))
        self.ui.Protection_title.setText(_translate("MainWindow", "Real-time protection"))
        self.ui.Protection_illustrate.setText(_translate("MainWindow", "Enable this option to monitor and remove malware in the system in real time."))
        self.ui.Protection_switch_Button.setText(self.text_Translate(self.ui.Protection_switch_Button.text()))
        self.ui.State_log.setText(_translate("MainWindow", "Log:"))
        self.ui.System_Tools_Button.setText(_translate("MainWindow", "System Tools"))
        self.ui.Privacy_Tools_Button.setText(_translate("MainWindow", "Privacy Tools"))
        self.ui.Develop_Tools_Button.setText(_translate("MainWindow", "Devs Tools"))
        self.ui.More_Tools_Button.setText(_translate("MainWindow", "More Tools"))
        self.ui.More_Tools_Back_Button.setText(_translate("MainWindow", "Tools>"))
        self.ui.System_Process_Manage_Button.setText(_translate("MainWindow", "Process Manager"))
        self.ui.Repair_System_Permission_Button.setText(_translate("MainWindow", "Repair Permission"))
        self.ui.Repair_System_Files_Button.setText(_translate("MainWindow", "Repair System Files"))
        self.ui.Clean_System_Files_Button.setText(_translate("MainWindow", "Clean System Files"))
        self.ui.Enable_Safe_Mode_Button.setText(_translate("MainWindow", "Enable Safe Mode"))
        self.ui.Disable_Safe_Mode_Button.setText(_translate("MainWindow", "Disable Safe Mode"))
        self.ui.System_Info_Button.setText(_translate("MainWindow", "System Information"))
        self.ui.System_Tools_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Privacy_Tools_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Delete_Private_File_Button.setText(_translate("MainWindow", "Private File Shred"))
        self.ui.Develop_Tools_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Customize_REG_Command_Button.setText(_translate("MainWindow", "Customize REG"))
        self.ui.Customize_CMD_Command_Button.setText(_translate("MainWindow", "Customize CMD"))
        self.ui.Analyze_EXE_hash_Button.setText(_translate("MainWindow", "Analyze File Hash"))
        self.ui.Analyze_EXE_Bit_Button.setText(_translate("MainWindow", "Analyze File Bits"))
        self.ui.Analyze_EXE_Funtion_Button.setText(_translate("MainWindow", "Analyze File Func"))
        self.ui.More_Tools_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Look_for_File_Button.setText(_translate("MainWindow", "Looking For Profiles"))
        self.ui.Encryption_Text_Button.setText(_translate("MainWindow", "Encrypt Decrypt Text"))
        self.ui.Change_Users_Password_Button.setText(_translate("MainWindow", "Change User Password"))
        self.ui.Internet_location_Query_Button.setText(_translate("MainWindow", "Internet Location Query"))
        self.ui.Rework_Network_Configuration_Button.setText(_translate("MainWindow", "Rework Network Config"))
        self.ui.Process_Tools_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Process_Total_title.setText(_translate("MainWindow", "Total process:"))
        self.ui.System_Info_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Customize_CMD_Command_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Customize_CMD_Command_Run_Button.setText(_translate("MainWindow", "Run"))
        self.ui.Customize_CMD_Command_output_title.setText(_translate("MainWindow", "Output:"))
        self.ui.Analyze_EXE_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Look_for_File_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Look_for_File_Run_Button.setText(_translate("MainWindow", "Search"))
        self.ui.Encryption_Text_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Encryption_Text_Run_Button.setText(_translate("MainWindow", "Encrypt"))
        self.ui.Encryption_Text_title2.setText(_translate("MainWindow", "After Encrypt & Decrypt"))
        self.ui.Encryption_Text_Password_title.setText(_translate("MainWindow", "Password:"))
        self.ui.Encryption_Text_title.setText(_translate("MainWindow", "Before Encrypt & Decrypt"))
        self.ui.Decrypt_Text_Run_Button.setText(_translate("MainWindow", "Decrypt"))
        self.ui.About_Back.setText(_translate("MainWindow", "Back"))
        self.ui.PYAS_Version.setText(_translate("MainWindow", f"PYAS V{pyas_version}"))
        self.ui.GUI_Made_title.setText(_translate("MainWindow", "GUI Make:"))
        self.ui.GUI_Made_Name.setText(_translate("MainWindow", "87owo"))
        self.ui.Core_Made_title.setText(_translate("MainWindow", "Core Make:"))
        self.ui.Core_Made_Name.setText(_translate("MainWindow", "87owo"))
        self.ui.Testers_title.setText(_translate("MainWindow", "Testers:"))
        self.ui.Testers_Name.setText(_translate("MainWindow", "87owo"))
        self.ui.PYAS_URL_title.setText(_translate("MainWindow", "Website:"))
        self.ui.PYAS_URL.setText(_translate("MainWindow", "<html><head/><body><p><a href=\"https://pyantivirus.wixsite.com/pyas?lang=en\"><span style= \" text-decoration: underline; color:#000000;\">https://pyantivirus.wixsite.com/pyas</span></a></p></body></html>"))
        self.ui.Change_Users_Password_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Change_Users_Password_New_Password_title.setText(_translate("MainWindow", "New password:"))
        self.ui.Change_Users_Password_User_Name_title.setText(_translate("MainWindow", "Username:"))
        self.ui.Change_Users_Password_Run_Button.setText(_translate("MainWindow", "Modify"))
        self.ui.Customize_REG_Command_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Value_Path_title.setText(_translate("MainWindow", "Value Path:"))
        self.ui.Value_Name_title.setText(_translate("MainWindow", "Value Name:"))
        self.ui.Value_Type_title.setText(_translate("MainWindow", "Value Type:"))
        self.ui.Value_Data_title.setText(_translate("MainWindow", "Value Data:"))
        self.ui.Customize_REG_Command_Run_Button.setText(_translate("MainWindow", "OK"))
        self.ui.Value_HEKY_title.setText(_translate("MainWindow", "Value HEKY:"))
        self.ui.Show_Virus_Scan_Progress_Bar_title.setText(_translate("MainWindow", "High Sensitivity Mode"))
        self.ui.Show_Virus_Scan_Progress_Bar_illustrate.setText(_translate("MainWindow", "Enable this option can improve scanning sensitivity,\nbut it can also cause manslaughter."))
        self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.setText(self.text_Translate(self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.text()))
        self.ui.Setting_Back.setText(_translate("MainWindow", "Back"))
        self.ui.Language_title.setText(_translate("MainWindow", "Language"))
        self.ui.Language_illustrate.setText(_translate("MainWindow", "Please select language"))
        self.ui.License_terms_title.setText(_translate("MainWindow", "License Terms:"))
        self.ui.Theme_title.setText(_translate("MainWindow", "Color Rendering Theme"))
        self.ui.Theme_illustrate.setText(_translate("MainWindow", "Please select a theme"))
        self.ui.Theme_White.setText(_translate("MainWindow", "White"))
        self.ui.Theme_Black.setText(_translate("MainWindow", "Black"))
        self.ui.Theme_Pink.setText(_translate("MainWindow", "Random"))
        self.ui.Theme_Red.setText(_translate("MainWindow", "Red"))
        self.ui.Theme_Green.setText(_translate("MainWindow", "Green"))
        self.ui.Theme_Blue.setText(_translate("MainWindow", "Blue"))

##################################### 簡中初始化 ####################################
    
    def lang_init_zh_cn(self):
        _translate = QtCore.QCoreApplication.translate
        if self.Safe:
            self.ui.State_title.setText(_translate("MainWindow", "这部装置已受到保护"))
        else:
            self.ui.State_title.setText(_translate("MainWindow", "这部装置目前不安全"))
        if pyas_key():
            self.ui.Window_title.setText(_translate("MainWindow", f"PYAS V{pyas_version}"))
        else:
            self.ui.Window_title.setText(_translate("MainWindow", f"PYAS V{pyas_version} (安全密钥错误)"))
        cy = time.strftime('%Y')
        if int(cy) < 2020:
            cy = str('2020')
        self.ui.PYAS_CopyRight.setText(_translate("MainWindow", f"Copyright© 2020-{cy} 87owo (PYAS Security)"))
        if self.vl <= 0:
            self.ui.PYAE_Version.setText(_translate("MainWindow", f"PYAE V{pyae_version} (正在下载数据庫...)"))
        else:
            self.ui.PYAE_Version.setText(_translate("MainWindow", f"PYAE V{pyae_version} (数据庫版本: "+str(self.vl-1)+")"))
        self.ui.State_Button.setText(_translate("MainWindow", "状态"))
        self.ui.Virus_Scan_Button.setText(_translate("MainWindow", "扫描"))
        self.ui.Tools_Button.setText(_translate("MainWindow", "工具"))
        self.ui.Protection_Button.setText(_translate("MainWindow", "防护"))
        self.ui.Virus_Scan_title.setText(_translate("MainWindow", "病毒扫描"))
        self.ui.Virus_Scan_text.setText(_translate("MainWindow", "请选择扫描方式"))
        self.ui.Virus_Scan_choose_Button.setText(_translate("MainWindow", "病毒扫描"))
        self.ui.File_Scan_Button.setText(_translate("MainWindow", "文件扫描"))
        self.ui.Path_Scan_Button.setText(_translate("MainWindow", "路径扫描"))
        self.ui.Disk_Scan_Button.setText(_translate("MainWindow", "全盘扫描"))
        self.ui.Virus_Scan_Solve_Button.setText(_translate("MainWindow", "立即解决"))
        self.ui.Virus_Scan_Break_Button.setText(_translate("MainWindow", "停止扫描"))
        self.ui.Protection_title.setText(_translate("MainWindow", "实时防护"))
        self.ui.Protection_illustrate.setText(_translate("MainWindow", "启用该选项可以实时监控进程中的恶意软体并清除。"))
        self.ui.Protection_switch_Button.setText(self.text_Translate(self.ui.Protection_switch_Button.text()))
        self.ui.State_log.setText(_translate("MainWindow", "日志:"))
        self.ui.System_Tools_Button.setText(_translate("MainWindow", "系统工具"))
        self.ui.Privacy_Tools_Button.setText(_translate("MainWindow", "隐私工具"))
        self.ui.Develop_Tools_Button.setText(_translate("MainWindow", "开发工具"))
        self.ui.More_Tools_Button.setText(_translate("MainWindow", "更多工具"))
        self.ui.More_Tools_Back_Button.setText(_translate("MainWindow", "工具>"))
        self.ui.System_Process_Manage_Button.setText(_translate("MainWindow", "系统进程管理"))
        self.ui.Repair_System_Permission_Button.setText(_translate("MainWindow", "系统权限修复"))
        self.ui.Repair_System_Files_Button.setText(_translate("MainWindow", "系统文件修复"))
        self.ui.Clean_System_Files_Button.setText(_translate("MainWindow", "系统垃圾清理"))
        self.ui.Enable_Safe_Mode_Button.setText(_translate("MainWindow", "启动安全模式"))
        self.ui.Disable_Safe_Mode_Button.setText(_translate("MainWindow", "关闭安全模式"))
        self.ui.System_Info_Button.setText(_translate("MainWindow", "系统版本资讯"))
        self.ui.System_Tools_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Privacy_Tools_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Delete_Private_File_Button.setText(_translate("MainWindow", "私密文件粉碎"))
        self.ui.Develop_Tools_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Customize_REG_Command_Button.setText(_translate("MainWindow", "自订REG指令"))
        self.ui.Customize_CMD_Command_Button.setText(_translate("MainWindow", "自订CMD指令"))
        self.ui.Analyze_EXE_hash_Button.setText(_translate("MainWindow", "分析文件哈希"))
        self.ui.Analyze_EXE_Bit_Button.setText(_translate("MainWindow", "分析文件位元"))
        self.ui.Analyze_EXE_Funtion_Button.setText(_translate("MainWindow", "分析文件函数"))
        self.ui.More_Tools_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Look_for_File_Button.setText(_translate("MainWindow", "寻找本机文件"))
        self.ui.Encryption_Text_Button.setText(_translate("MainWindow", "加密解密文字"))
        self.ui.Change_Users_Password_Button.setText(_translate("MainWindow", "变更用户密码"))
        self.ui.Internet_location_Query_Button.setText(_translate("MainWindow", "网路位置查询"))
        self.ui.Rework_Network_Configuration_Button.setText(_translate("MainWindow", "重置网路配置"))
        self.ui.Process_Tools_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Process_Total_title.setText(_translate("MainWindow", "进程总数:"))
        self.ui.System_Info_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Customize_CMD_Command_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Customize_CMD_Command_Run_Button.setText(_translate("MainWindow", "运行"))
        self.ui.Customize_CMD_Command_output_title.setText(_translate("MainWindow", "输出:"))
        self.ui.Analyze_EXE_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Look_for_File_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Look_for_File_Run_Button.setText(_translate("MainWindow", "寻找文件"))
        self.ui.Encryption_Text_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Encryption_Text_Run_Button.setText(_translate("MainWindow", "加密"))
        self.ui.Encryption_Text_title2.setText(_translate("MainWindow", "加密&解密后"))
        self.ui.Encryption_Text_Password_title.setText(_translate("MainWindow", "密码:"))
        self.ui.Encryption_Text_title.setText(_translate("MainWindow", "加密&解密前"))
        self.ui.Decrypt_Text_Run_Button.setText(_translate("MainWindow", "解密"))
        self.ui.About_Back.setText(_translate("MainWindow", "返回"))
        self.ui.PYAS_Version.setText(_translate("MainWindow", f"PYAS V{pyas_version}"))
        self.ui.GUI_Made_title.setText(_translate("MainWindow", "介面制作:"))
        self.ui.GUI_Made_Name.setText(_translate("MainWindow", "87owo"))
        self.ui.Core_Made_title.setText(_translate("MainWindow", "核心制作:"))
        self.ui.Core_Made_Name.setText(_translate("MainWindow", "87owo"))
        self.ui.Testers_title.setText(_translate("MainWindow", "测试人员:"))
        self.ui.Testers_Name.setText(_translate("MainWindow", "87owo"))
        self.ui.PYAS_URL_title.setText(_translate("MainWindow", "官方网站:"))
        self.ui.PYAS_URL.setText(_translate("MainWindow", "<html><head/><body><p><a href=\"https://pyantivirus.wixsite.com/pyas\"><span style=\" text-decoration: underline; color:#000000;\">https://pyantivirus.wixsite.com/pyas</span></a></p></body></html>"))
        self.ui.Change_Users_Password_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Change_Users_Password_New_Password_title.setText(_translate("MainWindow", "新密码:"))
        self.ui.Change_Users_Password_User_Name_title.setText(_translate("MainWindow", "用户名:"))
        self.ui.Change_Users_Password_Run_Button.setText(_translate("MainWindow", "修改"))
        self.ui.Customize_REG_Command_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Value_Path_title.setText(_translate("MainWindow", "值路径:"))
        self.ui.Value_Name_title.setText(_translate("MainWindow", "值名称:"))
        self.ui.Value_Type_title.setText(_translate("MainWindow", "值类型:"))
        self.ui.Value_Data_title.setText(_translate("MainWindow", "值资料:"))
        self.ui.Customize_REG_Command_Run_Button.setText(_translate("MainWindow", "确定"))
        self.ui.Value_HEKY_title.setText(_translate("MainWindow", "值HEKY:"))
        self.ui.Show_Virus_Scan_Progress_Bar_title.setText(_translate("MainWindow", "高灵敏度模式"))
        self.ui.Show_Virus_Scan_Progress_Bar_illustrate.setText(_translate("MainWindow", "启用该选项可以提高扫描灵敏度，但这也可能会造成误杀。"))
        self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.setText(self.text_Translate(self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.text()))
        self.ui.Setting_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Language_title.setText(_translate("MainWindow", "语言"))
        self.ui.Language_illustrate.setText(_translate("MainWindow", "请选择语言"))
        self.ui.License_terms_title.setText(_translate("MainWindow", "许可条款:"))
        self.ui.Theme_title.setText(_translate("MainWindow", "显色主题"))
        self.ui.Theme_illustrate.setText(_translate("MainWindow", "请选择主题"))
        self.ui.Theme_White.setText(_translate("MainWindow", "白色主题"))
        self.ui.Theme_Black.setText(_translate("MainWindow", "黑色主题"))
        self.ui.Theme_Pink.setText(_translate("MainWindow", "随机主题"))
        self.ui.Theme_Red.setText(_translate("MainWindow", "红色主题"))
        self.ui.Theme_Green.setText(_translate("MainWindow", "绿色主题"))
        self.ui.Theme_Blue.setText(_translate("MainWindow", "蓝色主题"))

##################################### 繁中初始化 ####################################
    
    def lang_init_zh_tw(self):
        _translate = QtCore.QCoreApplication.translate
        if self.Safe:
            self.ui.State_title.setText(_translate("MainWindow", "這部裝置已受到保護"))
        else:
            self.ui.State_title.setText(_translate("MainWindow", "這部裝置目前不安全"))
        if pyas_key():
            self.ui.Window_title.setText(_translate("MainWindow", f"PYAS V{pyas_version}"))
        else:
            self.ui.Window_title.setText(_translate("MainWindow", f"PYAS V{pyas_version} (安全密鑰錯誤)"))
        cy = time.strftime('%Y')
        if int(cy) < 2020:
            cy = str('2020')
        self.ui.PYAS_CopyRight.setText(_translate("MainWindow", f"Copyright© 2020-{cy} 87owo (PYAS Security)"))
        if self.vl <= 0:
            self.ui.PYAE_Version.setText(_translate("MainWindow", f"PYAE V{pyae_version} (正在下載資料庫...)"))
        else:
            self.ui.PYAE_Version.setText(_translate("MainWindow", f"PYAE V{pyae_version} (資料庫版本: "+str(self.vl-1)+")"))
        self.ui.State_Button.setText(_translate("MainWindow", "狀態"))
        self.ui.Virus_Scan_Button.setText(_translate("MainWindow", "掃描"))
        self.ui.Tools_Button.setText(_translate("MainWindow", "工具"))
        self.ui.Protection_Button.setText(_translate("MainWindow", "防護"))
        self.ui.Virus_Scan_title.setText(_translate("MainWindow", "病毒掃描"))
        self.ui.Virus_Scan_text.setText(_translate("MainWindow", "請選擇掃描方式"))
        self.ui.Virus_Scan_choose_Button.setText(_translate("MainWindow", "病毒掃描"))
        self.ui.File_Scan_Button.setText(_translate("MainWindow", "檔案掃描"))
        self.ui.Path_Scan_Button.setText(_translate("MainWindow", "路徑掃描"))
        self.ui.Disk_Scan_Button.setText(_translate("MainWindow", "全盤掃描"))
        self.ui.Virus_Scan_Solve_Button.setText(_translate("MainWindow", "立即解決"))
        self.ui.Virus_Scan_Break_Button.setText(_translate("MainWindow", "停止掃描"))
        self.ui.Protection_title.setText(_translate("MainWindow", "實時防護"))
        self.ui.Protection_illustrate.setText(_translate("MainWindow", "啟用該選項可以實時監控進程中的惡意軟體並清除。"))
        self.ui.Protection_switch_Button.setText(self.text_Translate(self.ui.Protection_switch_Button.text()))
        self.ui.State_log.setText(_translate("MainWindow", "日誌:"))
        self.ui.System_Tools_Button.setText(_translate("MainWindow", "系統工具"))
        self.ui.Privacy_Tools_Button.setText(_translate("MainWindow", "隱私工具"))
        self.ui.Develop_Tools_Button.setText(_translate("MainWindow", "開發工具"))
        self.ui.More_Tools_Button.setText(_translate("MainWindow", "更多工具"))
        self.ui.More_Tools_Back_Button.setText(_translate("MainWindow", "工具>"))
        self.ui.System_Process_Manage_Button.setText(_translate("MainWindow", "系統進程管理"))
        self.ui.Repair_System_Permission_Button.setText(_translate("MainWindow", "系統權限修復"))
        self.ui.Repair_System_Files_Button.setText(_translate("MainWindow", "系統檔案修復"))
        self.ui.Clean_System_Files_Button.setText(_translate("MainWindow", "系統垃圾清理"))
        self.ui.Enable_Safe_Mode_Button.setText(_translate("MainWindow", "啟動安全模式"))
        self.ui.Disable_Safe_Mode_Button.setText(_translate("MainWindow", "關閉安全模式"))
        self.ui.System_Info_Button.setText(_translate("MainWindow", "系統版本資訊"))
        self.ui.System_Tools_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Privacy_Tools_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Delete_Private_File_Button.setText(_translate("MainWindow", "私密檔案粉碎"))
        self.ui.Develop_Tools_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Customize_REG_Command_Button.setText(_translate("MainWindow", "自訂REG指令"))
        self.ui.Customize_CMD_Command_Button.setText(_translate("MainWindow", "自訂CMD指令"))
        self.ui.Analyze_EXE_hash_Button.setText(_translate("MainWindow", "分析文件哈希"))
        self.ui.Analyze_EXE_Bit_Button.setText(_translate("MainWindow", "分析文件位元"))
        self.ui.Analyze_EXE_Funtion_Button.setText(_translate("MainWindow", "分析文件函數"))
        self.ui.More_Tools_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Look_for_File_Button.setText(_translate("MainWindow", "尋找本機檔案"))
        self.ui.Encryption_Text_Button.setText(_translate("MainWindow", "加密解密文字"))
        self.ui.Change_Users_Password_Button.setText(_translate("MainWindow", "變更用戶密碼"))
        self.ui.Internet_location_Query_Button.setText(_translate("MainWindow", "網路位置查詢"))
        self.ui.Rework_Network_Configuration_Button.setText(_translate("MainWindow", "重置網路配置"))
        self.ui.Process_Tools_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Process_Total_title.setText(_translate("MainWindow", "進程總數:"))
        self.ui.System_Info_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Customize_CMD_Command_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Customize_CMD_Command_Run_Button.setText(_translate("MainWindow", "運行"))
        self.ui.Customize_CMD_Command_output_title.setText(_translate("MainWindow", "輸出:"))
        self.ui.Analyze_EXE_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Look_for_File_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Look_for_File_Run_Button.setText(_translate("MainWindow", "尋找檔案"))
        self.ui.Encryption_Text_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Encryption_Text_Run_Button.setText(_translate("MainWindow", "加密"))
        self.ui.Encryption_Text_title2.setText(_translate("MainWindow", "加密&解密後"))
        self.ui.Encryption_Text_Password_title.setText(_translate("MainWindow", "密碼:"))
        self.ui.Encryption_Text_title.setText(_translate("MainWindow", "加密&解密前"))
        self.ui.Decrypt_Text_Run_Button.setText(_translate("MainWindow", "解密"))
        self.ui.About_Back.setText(_translate("MainWindow", "返回"))
        self.ui.PYAS_Version.setText(_translate("MainWindow", f"PYAS V{pyas_version}"))
        self.ui.GUI_Made_title.setText(_translate("MainWindow", "介面製作:"))
        self.ui.GUI_Made_Name.setText(_translate("MainWindow", "87owo"))
        self.ui.Core_Made_title.setText(_translate("MainWindow", "核心製作:"))
        self.ui.Core_Made_Name.setText(_translate("MainWindow", "87owo"))
        self.ui.Testers_title.setText(_translate("MainWindow", "測試人員:"))
        self.ui.Testers_Name.setText(_translate("MainWindow", "87owo"))
        self.ui.PYAS_URL_title.setText(_translate("MainWindow", "官方網站:"))
        self.ui.PYAS_URL.setText(_translate("MainWindow", "<html><head/><body><p><a href=\"https://pyantivirus.wixsite.com/pyas\"><span style=\" text-decoration: underline; color:#000000;\">https://pyantivirus.wixsite.com/pyas</span></a></p></body></html>"))
        self.ui.Change_Users_Password_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Change_Users_Password_New_Password_title.setText(_translate("MainWindow", "新密碼:"))
        self.ui.Change_Users_Password_User_Name_title.setText(_translate("MainWindow", "用戶名:"))
        self.ui.Change_Users_Password_Run_Button.setText(_translate("MainWindow", "修改"))
        self.ui.Customize_REG_Command_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Value_Path_title.setText(_translate("MainWindow", "值路徑:"))
        self.ui.Value_Name_title.setText(_translate("MainWindow", "值名稱:"))
        self.ui.Value_Type_title.setText(_translate("MainWindow", "值類型:"))
        self.ui.Value_Data_title.setText(_translate("MainWindow", "值資料:"))
        self.ui.Customize_REG_Command_Run_Button.setText(_translate("MainWindow", "確定"))
        self.ui.Value_HEKY_title.setText(_translate("MainWindow", "值HEKY:"))
        self.ui.Show_Virus_Scan_Progress_Bar_title.setText(_translate("MainWindow", "高靈敏度模式"))
        self.ui.Show_Virus_Scan_Progress_Bar_illustrate.setText(_translate("MainWindow", "啟用該選項可以提高掃描靈敏度，但這也可能會造成誤殺。"))
        self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.setText(self.text_Translate(self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.text()))
        self.ui.Setting_Back.setText(_translate("MainWindow", "返回"))
        self.ui.Language_title.setText(_translate("MainWindow", "語言"))
        self.ui.Language_illustrate.setText(_translate("MainWindow", "請選擇語言"))
        self.ui.License_terms_title.setText(_translate("MainWindow", "許可條款:"))
        self.ui.Theme_title.setText(_translate("MainWindow", "顯色主題"))
        self.ui.Theme_illustrate.setText(_translate("MainWindow", "請選擇主題"))
        self.ui.Theme_White.setText(_translate("MainWindow", "白色主題"))
        self.ui.Theme_Black.setText(_translate("MainWindow", "黑色主題"))
        self.ui.Theme_Pink.setText(_translate("MainWindow", "隨機主題"))
        self.ui.Theme_Red.setText(_translate("MainWindow", "紅色主題"))
        self.ui.Theme_Green.setText(_translate("MainWindow", "綠色主題"))
        self.ui.Theme_Blue.setText(_translate("MainWindow", "藍色主題"))

####################################### 翻譯 #####################################

    def text_Translate(self, text):
        if self.pyasConfig['language'] == "zh_TW":
            translations = {"已开启": "已開啟","已关闭": "已關閉","On": "已開啟","Off": "已關閉"}
            for k, v in translations.items():
                text = text.replace(k, v)
            return text
        elif self.pyasConfig['language'] == "zh_CN":
            translations = {"嗎": "吗","項": "项","復": "复","攔": "拦","請": "请","後": "后","鑰": "钥","統": "统",
                            "當": "当","確定": "确认","掃描": "扫描","檔案": "文件","錯誤": "错误","實時": "实时",
                            "發現": "发现","權限": "权限","惡意": "恶意","設定": "设置","關於": "关于","防護": "保护",
                            "已開啟": "已开启","已關閉": "已关闭","On": "已开启","Off": "已关闭","軟體": "软件"}
            for k, v in translations.items():
                text = text.replace(k, v)
            return text
        elif self.pyasConfig['language'] == "english":
            return english_list[text]

################################### 視窗動畫特效 ####################################
    
    def Change_animation(self,widget):
        x = 170
        y = widget.pos().y()#獲取物件的y軸座標
        self.anim = QPropertyAnimation(widget, b"geometry")#動畫
        widget.setGeometry(QtCore.QRect(x - 100,y, 671,481))#設定物件"widget"的座標大小
        self.anim.setKeyValueAt(0.2, QRect(x - 60,y,671,481))
        self.anim.setKeyValueAt(0.4, QRect(x - 10,y,671,481))
        self.anim.setKeyValueAt(0.7, QRect(x - 3,y,671,481))
        self.anim.setKeyValueAt(1, QRect(x,y,671,481))
        self.anim.start()#動畫開始

    def Change_animation_2(self,nx,ny):
        x = self.ui.label.pos().x()
        y = self.ui.label.pos().y()
        self.anim2 = QPropertyAnimation(self.ui.label, b"geometry")
        if y > ny:
            self.anim2.setKeyValueAt(0.4, QRect(nx,ny + 25, 5, 35))
            self.anim2.setKeyValueAt(0.5, QRect(nx,ny + 12, 5, 34))
            self.anim2.setKeyValueAt(0.7, QRect(nx,ny + 6, 5, 33))
            self.anim2.setKeyValueAt(0.8, QRect(nx,ny + 4, 5, 32))
            self.anim2.setKeyValueAt(0.9, QRect(nx,ny + 2, 5, 31))
            self.anim2.setKeyValueAt(1, QRect(nx,ny, 5, 30))
        else:
            self.anim2.setKeyValueAt(0.4, QRect(nx,ny - 25, 5, 35))
            self.anim2.setKeyValueAt(0.5, QRect(nx,ny - 12, 5, 34))
            self.anim2.setKeyValueAt(0.7, QRect(nx,ny - 6, 5, 33))
            self.anim2.setKeyValueAt(0.8, QRect(nx,ny - 4, 5, 32))
            self.anim2.setKeyValueAt(0.9, QRect(nx,ny - 2, 5, 31))
            self.anim2.setKeyValueAt(1, QRect(nx,ny, 5, 30))
        self.anim2.start()
    
    def Change_animation_3(self,widget,time):#這裡是設定透明度
        self.opacity = QtWidgets.QGraphicsOpacityEffect()#if self.Virus_Scan != 1:
        self.opacity.setOpacity(0)
        widget.setGraphicsEffect(self.opacity)
        widget.setAutoFillBackground(True)
        self.draw(widget=widget,time=time)

    def Change_animation_4(self,widget,time,ny,ny2):
        x = widget.pos().x()
        y = widget.pos().y()
        self.anim4 = QPropertyAnimation(widget, b"geometry")
        self.anim4.setDuration(time)
        self.anim4.setStartValue(QRect(x, y, 141, ny))
        self.anim4.setEndValue(QRect(x, y, 141, ny2))
        self.anim4.start()

    def Change_animation5(self,widget,x1,y1,nx,ny):
        x = x1
        y = y1
        self.anim = QPropertyAnimation(widget, b"geometry")#動畫
        widget.setGeometry(QtCore.QRect(x,y - 45, nx,ny))#設定物件"widget"的座標大小
        self.anim.setKeyValueAt(0.2, QRect(x,y - 30,nx,ny))
        self.anim.setKeyValueAt(0.4, QRect(x,y - 10,nx,ny))
        self.anim.setKeyValueAt(0.7, QRect(x,y - 3,nx,ny))
        self.anim.setKeyValueAt(1, QRect(x,y,nx,ny))
        self.anim.start()#動畫開始


    def draw(self,widget,time):
        self.opacity.i = 1
        def timeout():
            self.opacity.setOpacity(self.opacity.i/100)
            widget.setGraphicsEffect(self.opacity)
            self.opacity.i += 1
            if self.opacity.i > 100:
                self.timer.stop()
                self.timer.deleteLater()
        self.timer = QTimer()
        self.timer.setInterval(0)
        self.timer.timeout.connect(timeout)
        self.timer.start()

    def Change_to_State_widget(self):
        if self.ui.State_widget.isHidden():#isHidden()函數用意是偵測物件是否在隱藏狀態
            self.Change_animation_2(25,41)
            self.Change_animation_3(self.ui.State_widget,0.5)
            self.Change_animation(self.ui.State_widget)
            self.ui.State_widget.show()#show()函數用意是讓隱藏函數顯示出來
            self.ui.Virus_Scan_widget.hide()
            self.ui.Tools_widget.hide()
            self.ui.Protection_widget.hide()
            self.ui.System_Tools_widget.hide()
            self.ui.Privacy_Tools_widget.hide()
            self.ui.Develop_Tools_widget.hide()
            self.ui.More_Tools_widget.hide()
            self.ui.Process_widget.hide()
            self.ui.System_Info_widget.hide()
            self.ui.Customize_CMD_Command_widget.hide()
            self.ui.Analyze_EXE_widget.hide()
            self.ui.Look_for_File_widget.hide()
            self.ui.Encryption_Text_widget.hide()
            self.ui.About_widget.hide()
            self.ui.Change_Users_Password_widget.hide()
            self.ui.Customize_REG_Command_widget.hide()
            self.ui.Setting_widget.hide()

    def Change_to_Virus_Scan_widget(self):
        if self.ui.Virus_Scan_widget.isHidden():
            self.Change_animation_2(25,164)
            self.Change_animation_3(self.ui.Virus_Scan_widget,0.5)
            self.Change_animation(self.ui.Virus_Scan_widget)
            self.ui.State_widget.hide()
            self.ui.Virus_Scan_widget.show()
            self.ui.Tools_widget.hide()
            self.ui.Protection_widget.hide()
            self.ui.System_Tools_widget.hide()
            self.ui.Privacy_Tools_widget.hide()
            self.ui.Develop_Tools_widget.hide()
            self.ui.More_Tools_widget.hide()
            self.ui.Process_widget.hide()
            self.ui.System_Info_widget.hide()
            self.ui.Customize_CMD_Command_widget.hide()
            self.ui.Analyze_EXE_widget.hide()
            self.ui.Look_for_File_widget.hide()
            self.ui.Encryption_Text_widget.hide()
            self.ui.About_widget.hide()
            self.ui.Change_Users_Password_widget.hide()
            self.ui.Customize_REG_Command_widget.hide()
            self.ui.Setting_widget.hide()

    def Change_to_Tools_widget(self):
        if self.ui.Tools_widget.isHidden():
            self.Change_animation_2(25,287)
            self.Change_animation_3(self.ui.Tools_widget,0.5)
            self.Change_animation(self.ui.Tools_widget)
            self.ui.State_widget.hide()
            self.ui.Virus_Scan_widget.hide()
            self.ui.Tools_widget.show()
            self.ui.Protection_widget.hide()
            self.ui.System_Tools_widget.hide()
            self.ui.Privacy_Tools_widget.hide()
            self.ui.Develop_Tools_widget.hide()
            self.ui.More_Tools_widget.hide()
            self.ui.Process_widget.hide()
            self.ui.System_Info_widget.hide()
            self.ui.Customize_CMD_Command_widget.hide()
            self.ui.Analyze_EXE_widget.hide()
            self.ui.Look_for_File_widget.hide()
            self.ui.Encryption_Text_widget.hide()
            self.ui.About_widget.hide()
            self.ui.Change_Users_Password_widget.hide()
            self.ui.Customize_REG_Command_widget.hide()
            self.ui.Setting_widget.hide()

    def Change_to_Rrotection_widget(self):
        if self.ui.Protection_widget.isHidden():
            self.Change_animation_2(25,410)
            self.Change_animation_3(self.ui.Protection_widget,0.5)
            self.Change_animation(self.ui.Protection_widget)
            self.ui.State_widget.hide()
            self.ui.Virus_Scan_widget.hide()
            self.ui.Tools_widget.hide()
            self.ui.Protection_widget.show()
            self.ui.System_Tools_widget.hide()
            self.ui.Privacy_Tools_widget.hide()
            self.ui.Develop_Tools_widget.hide()
            self.ui.More_Tools_widget.hide()
            self.ui.Process_widget.hide()
            self.ui.System_Info_widget.hide()
            self.ui.Customize_CMD_Command_widget.hide()
            self.ui.Analyze_EXE_widget.hide()
            self.ui.Look_for_File_widget.hide()
            self.ui.Encryption_Text_widget.hide()
            self.ui.About_widget.hide()
            self.ui.Change_Users_Password_widget.hide()
            self.ui.Customize_REG_Command_widget.hide()
            self.ui.Setting_widget.hide()

    def Change_Tools(self,widget):
        self.ui.Tools_widget.hide()
        self.ui.System_Tools_widget.hide()
        self.ui.Develop_Tools_widget.hide()
        self.ui.Analyze_EXE_widget.hide()
        self.ui.More_Tools_widget.hide()
        self.ui.Setting_widget.hide()
        self.ui.About_widget.hide()
        if widget == self.ui.Process_widget:
            self.Process_Timer.start(200)
        elif widget == self.ui.System_Info_widget:
            self.System_Info_update()
        self.Change_animation_3(widget,0.5)
        self.Change_animation(widget)
        widget.show()

    def Back_To_More_Tools(self,widget):
        widget.hide()
        if widget == self.ui.Process_widget:
            self.Process_Timer.stop()
        self.Change_animation_3(self.ui.Tools_widget,0.5)
        self.Change_animation(self.ui.Tools_widget)
        self.ui.Tools_widget.show()

##################################### 病毒掃描 #####################################
    
    def Virus_Scan_Break(self):
        self.Virus_Scan = False

    def Virus_Solve(self):
        try:
            for line in self.Virus_List:
                try:
                    if ':/Windows' not in str(line):
                        self.ui.Virus_Scan_text.setText(self.text_Translate('正在刪除: ')+str(line))
                        QApplication.processEvents()
                        os.remove(str(line))
                except:
                    continue
            self.Virus_List = []
            self.Virus_List_output.setStringList(self.Virus_List)
            self.ui.Virus_Scan_output.setModel(self.Virus_List_output)
            self.ui.Virus_Scan_text.setText(self.text_Translate('✔成功: 已執行成功。'))
            self.ui.Virus_Scan_Solve_Button.hide()
            self.ui.State_icon.setPixmap(QtGui.QPixmap(":/icon/Icon/check.png"))
            self.ui.State_title.setText(self.text_Translate("這部裝置已受到保護"))
            self.Safe = True
        except Exception as e:
            pyas_bug_log(e)
            self.Safe = False
            self.ui.Virus_Scan_text.setText(self.text_Translate("✖錯誤: 執行失敗。"))

    def api_scan(self, types, file):
        try:
            with open(file, "rb") as f:
                file_md5 = str(md5(f.read()).hexdigest())
            response = requests.get("http://27.147.30.238:5001/pyas", params={types: file_md5})
            if response.status_code == 200:
                if response.text == 'True':
                    return True
            return False
        except:
            return False

    def pyas_scan_start(self, file, rfp):
        try:
            with open(file, "rb") as f:
                file_md5 = str(md5(f.read()).hexdigest())[:10]
                return file_md5 in rfp
        except:
            return False

    def pyas_pe_start(self,file):
        try:
            pe = PE(file)
            pe.close()
            for entry in pe.DIRECTORY_ENTRY_IMPORT:#函數檢測
                for function in entry.imports:
                    if '_CorExeMain' in str(function.name):
                        return True
            return False
        except:
            return False
    
    def pyas_sign_start(self, file):  # 簽名檢查
        try:
            pe = PE(file, fast_load=True)
            pe.close()
            if pe.OPTIONAL_HEADER.DATA_DIRECTORY[DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_SECURITY']].VirtualAddress == 0:
                return True  # 未簽名
            return False  # 已簽名
        except:
            return True  # 未簽名

    #定義紀錄掃描
    def pyas_scan_write_en(self,file):
        try:
            self.Virus_List.append(file)
            self.Virus_List_output.setStringList(self.Virus_List)
            self.ui.Virus_Scan_output.setModel(self.Virus_List_output)
        except:
            pass

    #定義讀取紀錄
    def pyas_scan_answer_en(self):
        if self.Virus_List != []:
            print('[SCAN] Malware has been detected')
            self.Virus_List_output.setStringList(self.Virus_List)
            self.ui.Virus_Scan_output.setModel(self.Virus_List_output)
            self.ui.State_output.append(str(time.strftime('%Y/%m/%d %H:%M:%S')) + self.text_Translate(" > [病毒掃描] 掃描出") + str(len(self.Virus_List)) + self.text_Translate("個病毒"))
            self.ui.State_icon.setPixmap(QtGui.QPixmap(":/icon/Icon/X2.png"))
            self.ui.State_title.setText(self.text_Translate("這部裝置目前不安全"))
            self.ui.Virus_Scan_Solve_Button.show()
            self.ui.Virus_Scan_choose_Button.show()
            self.ui.Virus_Scan_Break_Button.hide()
            self.Virus_Scan = False
            self.Safe = False
            ToastNotifier().show_toast("PYAS Security",self.text_Translate("✖當前已發現惡意軟體共{}項。").format(len(self.Virus_List)),icon_path="Library/PYAS/Icon/ICON.ico",threaded=True)
            self.ui.Virus_Scan_text.setText(self.text_Translate("✖當前已發現惡意軟體共{}項。").format(len(self.Virus_List)))
        else:
            print('[SCAN] No malware currently found')
            self.ui.Virus_Scan_Break_Button.hide()
            self.ui.Virus_Scan_choose_Button.show()
            self.Virus_Scan = False
            self.Safe = True
            ToastNotifier().show_toast("PYAS Security",self.text_Translate('✔當前未發現惡意軟體。'),icon_path="Library/PYAS/Icon/ICON.ico",threaded=True)
            self.ui.Virus_Scan_text.setText(self.text_Translate('✔當前未發現惡意軟體。'))

##################################### 檔案掃描 #####################################
    
    def File_Scan(self):
        print('[SCAN] Start Scan Action (File Scan)')
        self.Virus_List = []
        self.ui.Virus_Scan_choose_widget.hide()
        self.ui.Virus_Scan_Solve_Button.hide()
        self.ui.Virus_Scan_ProgressBar.hide()
        self.Virus_List_output=QStringListModel()
        self.Virus_List_output.setStringList(self.Virus_List)
        self.ui.Virus_Scan_output.setModel(self.Virus_List_output)
        file, filetype= QFileDialog.getOpenFileName(self,self.text_Translate("病毒掃描"),"C:/",'')
        try:
            if file != "":
                self.ui.Virus_Scan_text.setText(self.text_Translate("正在初始化中，請稍後..."))
                self.Virus_Scan = True
                self.ui.Virus_Scan_choose_Button.hide()
                QApplication.processEvents()
                print('[INFO] Reading Viruslist Database')#讀取
                try:
                    with open('Library/PYAE/Hashes/Viruslist.md5','r') as fp:
                        rfp = fp.read()
                except:
                    rfp = ''
                if self.show_virus_scan_progress_bar == 0:#確認是否高靈敏
                    if self.pyas_sign_start(file):#簽名檢查
                        if self.pyas_scan_start(file,rfp):#MD5較驗
                            self.pyas_scan_write_en(file)#寫入發現病毒
                        elif self.pyas_pe_start(file):
                            self.pyas_scan_write_en(file)#寫入發現病毒
                        elif self.api_scan('md5', file):
                            self.pyas_scan_write_en(file)#寫入發現病毒
                else:
                    if self.pyas_scan_start(file,rfp):#MD5較驗
                        self.pyas_scan_write_en(file)#寫入發現病毒
                    elif self.pyas_pe_start(file):
                        self.pyas_scan_write_en(file)#寫入發現病毒
                    elif self.api_scan('md5', file):
                        self.pyas_scan_write_en(file)#寫入發現病毒
                self.pyas_scan_answer_en()
            else:
                self.ui.Virus_Scan_text.setText(self.text_Translate("請選擇掃描方式"))
        except Exception as e:
            QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+str(e),QMessageBox.Ok)

##################################### 路徑掃描 #####################################
    
    def Path_Scan(self):
        print('[SCAN] Start Scan Action (Path Scan)')
        self.ui.Virus_Scan_choose_widget.hide()
        self.ui.Virus_Scan_Solve_Button.hide()
        self.ui.Virus_Scan_ProgressBar.hide()
        self.Virus_List = []
        self.Virus_List_output=QStringListModel()
        self.Virus_List_output.setStringList(self.Virus_List)
        self.ui.Virus_Scan_output.setModel(self.Virus_List_output)
        file = QFileDialog.getExistingDirectory(self,self.text_Translate("病毒掃描"),"C:/")
        try:
            if file != "":
                self.ui.Virus_Scan_text.setText(self.text_Translate("正在初始化中，請稍後..."))
                self.Virus_Scan = True
                self.ui.Virus_Scan_choose_Button.hide()
                self.ui.Virus_Scan_Break_Button.show()
                QApplication.processEvents()
                print('[INFO] Reading Viruslist Database')#讀取
                try:
                    with open('Library/PYAE/Hashes/Viruslist.md5','r') as fp:
                        rfp = fp.read()
                except:
                    rfp = ''
                self.pyas_scan_path_en(file,rfp,False)
                self.pyas_scan_answer_en()
            else:
                self.ui.Virus_Scan_text.setText(self.text_Translate("請選擇掃描方式"))
        except Exception as e:
            QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+str(e),QMessageBox.Ok)

    def pyas_scan_path_en(self,path,rfp,fts):
        for fd in os.listdir(path):#遍歷檔案
            try:
                if not self.Virus_Scan:
                    self.ui.Virus_Scan_Break_Button.hide()
                    break
                else:
                    fullpath = str(os.path.join(path,fd)).replace("\\", "/")
                    if os.path.isdir(fullpath):#資料夾 深入遍歷
                        self.pyas_scan_path_en(fullpath,rfp,fts)
                    else:#檔案
                        self.ui.Virus_Scan_text.setText(self.text_Translate("正在掃描: ")+fullpath)
                        QApplication.processEvents()
                        if self.show_virus_scan_progress_bar == 0:#確認是否高靈敏
                            if self.pyas_sign_start(fullpath):#簽名檢查
                                if self.pyas_scan_start(fullpath,rfp):#MD5較驗
                                    self.pyas_scan_write_en(fullpath)#寫入發現病毒
                                elif self.pyas_pe_start(fullpath):
                                    self.pyas_scan_write_en(fullpath)#寫入發現病毒
                                elif self.api_scan('md5', fullpath):
                                    self.pyas_scan_write_en(fullpath)#寫入發現病毒
                        else:
                            if self.pyas_scan_start(fullpath,rfp):#MD5較驗
                                self.pyas_scan_write_en(fullpath)#寫入發現病毒
                            elif self.pyas_pe_start(fullpath):
                                self.pyas_scan_write_en(fullpath)#寫入發現病毒
                            elif self.api_scan('md5', fullpath):
                                self.pyas_scan_write_en(fullpath)#寫入發現病毒
            except:
                continue

##################################### 全盤掃描 #####################################
    
    def pyas_scan_disk_init_en(self):
        print('[SCAN] Start Scan Action (Disk Scan)')
        try:
            self.ui.Virus_Scan_choose_widget.hide()
            self.ui.Virus_Scan_text.setText(self.text_Translate("正在初始化中，請稍後..."))
            QApplication.processEvents()
            print('[INFO] Reading Viruslist Database')
            with open('Library/PYAE/Hashes/Viruslist.md5','r') as self.fp:
                rfp = self.fp.read()
            self.fp.close()
            self.Virus_Scan = True
            self.ui.Virus_Scan_Solve_Button.hide()
            self.ui.Virus_Scan_ProgressBar.hide()
            self.ui.Virus_Scan_choose_Button.hide()
            self.ui.Virus_Scan_Break_Button.show()
            self.Virus_List = []
            self.Virus_List_output=QStringListModel()
            self.Virus_List_output.setStringList(self.Virus_List)
            self.ui.Virus_Scan_output.setModel(self.Virus_List_output)
            self.scaning = self.text_Translate("正在掃描: ")
            for d in range(26):
                try:
                    self.pyas_scan_disk_en(str(chr(65+d))+':/',rfp)
                except:
                    pass
            self.pyas_scan_answer_en()
        except Exception as e:
            self.ui.Virus_Scan_text.setText(self.text_Translate("請選擇掃描方式"))
            QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+str(e),QMessageBox.Ok)

    def pyas_scan_disk_en(self,path,rfp):
        for fd in os.listdir(path):
            try:
                if not self.Virus_Scan:
                    self.ui.Virus_Scan_Break_Button.hide()
                    break
                else:
                    fullpath = str(os.path.join(path,fd)).replace("\\", "/")
                    QApplication.processEvents()
                    if self.show_virus_scan_progress_bar == 0:
                        if ':/Windows' in fullpath or ':/$Recycle.Bin' in fullpath or 'AppData' in fullpath:#路徑過濾
                            continue
                        elif ':/Program' in fullpath or ':/Users/Default' in fullpath:
                            sflist = ['.exe','.dll']
                        else:
                            sflist = ['.exe','.dll','.com','.bat','.vbs','.scr','.cpl','.htm','.html']
                        if os.path.isdir(fullpath):#資料夾 深入遍歷
                            self.ui.Virus_Scan_text.setText(self.scaning+fullpath)
                            self.pyas_scan_disk_en(fullpath,rfp)
                        else:#檔案
                            root, extension = os.path.splitext(fd)
                            if self.pyas_sign_start(fullpath) and str(extension).lower() in sflist:#簽名檢查+副檔名過濾檢測
                                self.ui.Virus_Scan_text.setText(self.scaning+fullpath)
                                if self.pyas_scan_start(fullpath,rfp):#MD5較驗
                                    self.pyas_scan_write_en(fullpath)#寫入發現病毒
                                elif self.pyas_pe_start(fullpath):
                                    self.pyas_scan_write_en(fullpath)#寫入發現病毒
                                elif self.api_scan('md5', fullpath):
                                    self.pyas_scan_write_en(fullpath)#寫入發現病毒
                    else:
                        if os.path.isdir(fullpath):#資料夾 深入遍歷
                            self.ui.Virus_Scan_text.setText(self.scaning+fullpath)
                            self.pyas_scan_disk_en(fullpath,rfp)
                        else:#檔案
                            root, extension = os.path.splitext(fd)
                            self.ui.Virus_Scan_text.setText(self.scaning+fullpath)
                            if self.pyas_scan_start(fullpath,rfp):#MD5較驗
                                self.pyas_scan_write_en(fullpath)#寫入發現病毒
                            elif self.pyas_pe_start(fullpath):
                                self.pyas_scan_write_en(fullpath)#寫入發現病毒
                            elif self.api_scan('md5', fullpath):
                                self.pyas_scan_write_en(fullpath)#寫入發現病毒
            except:
                continue

    def Virus_Scan_Choose_Menu(self):
        if self.ui.Virus_Scan_choose_widget.isHidden():
            self.ui.Virus_Scan_choose_widget.show()
            self.Change_animation_4(self.ui.Virus_Scan_choose_widget,100,0,101)
        else:
            self.ui.Virus_Scan_choose_widget.hide()

##################################### 實用工具 #####################################

    def Repair_System_Permission(self):
        #QMessageBox跟tkinter.messagebox是差不多的東西 yes的回傳值為16384
        question = QMessageBox.warning(self,self.text_Translate('修復系統權限'),self.text_Translate("您確定要修復系統權限嗎?"),QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384 and self.pyas_protect_repair():
            QMessageBox.information(self,self.text_Translate('完成'),self.text_Translate("修復完成!"),QMessageBox.Ok,QMessageBox.Ok)
        else:
            QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+self.text_Translate("修復失敗"),QMessageBox.Ok)

    def Repair_System_Files(self):
        try:
            question = QMessageBox.warning(self,self.text_Translate("修復系統檔案"),self.text_Translate("您確定要修復系統檔案嗎?"),QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            if question == 16384:
                runc = os.system('start sfc /scannow')
                if runc != 0:
                    QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+self.text_Translate("修復失敗"),QMessageBox.Ok)
        except Exception as e:
            pyas_bug_log(e)

    def Clean_System_Files(self):
        try:
            question = QMessageBox.warning(self,self.text_Translate('清理系統檔案'),self.text_Translate("您確定要清理系統檔案嗎?"),QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            if question == 16384:
                runc = os.system('start cleanmgr')
                if runc != 0:
                    QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+self.text_Translate("清理失敗"),QMessageBox.Ok)
        except Exception as e:
            pyas_bug_log(e)

    def Enable_Safe_Mode(self):
        question = QMessageBox.warning(self,self.text_Translate('啟用安全模式'),self.text_Translate("您確定啟用安全模式嗎?"),QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            runc = os.system('bcdedit /set {default} safeboot minimal')
            if runc == 0:
                question = QMessageBox.warning(self,'reboot',self.text_Translate("使用該選項後需要重啟，現在要重啟嗎?"),QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
                if question == 16384:
                    os.system('shutdown -r -t 0')
            else:
                QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+self.text_Translate("啟用失敗"),QMessageBox.Ok)  

    def Disable_Safe_Mode(self):
        question = QMessageBox.warning(self,self.text_Translate('禁用安全模式'),self.text_Translate("您確定禁用安全模式嗎?"),QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            runc = os.system('bcdedit /deletevalue {current} safeboot')
            if runc == 0:
                question = QMessageBox.warning(self,'reboot',self.text_Translate("使用該選項後需要重啟，現在要重啟嗎?"),QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
                if question == 16384:
                    os.system('shutdown -r -t 0')
            else:
                QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+self.text_Translate("禁用失敗"),QMessageBox.Ok)  

    def System_Info_update(self):
        self.ui.System_Info_View.setText(f'System information:\nCore version: {platform.platform()}\nMachine type: {platform.machine()}\nSystem Info: {platform.architecture()}\nComputer Name: {platform.node()}\nProcessor Name: {platform.processor()}')

    def Delete_Private_File(self):
        file, filetype= QFileDialog.getOpenFileName(self,self.text_Translate("刪除檔案"),"C:/",'')
        if file =="":
            pass
        elif file == str(sys.argv[0]):
            QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+self.text_Translate('存取被拒'),QMessageBox.Ok)
            pass
        else:
            question = QMessageBox.warning(self,self.text_Translate('刪除檔案'),self.text_Translate("您確定刪除該檔案嗎?"),QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            if question == 16384:
                try:
                    os.remove(file)
                    QMessageBox.information(self,self.text_Translate("刪除成功"),self.text_Translate("刪除成功"),QMessageBox.Ok)
                except Exception as e:
                    pyas_bug_log(e)
                    QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+self.text_Translate("刪除失敗"),QMessageBox.Ok)
     
    def Customize_CMD_Command(self):
        CMD_Command = self.ui.Customize_CMD_Command_lineEdit.text()
        if CMD_Command == '':
            return
        else:
            if CMD_Command.split()[0].lower() == "/add" or CMD_Command.split()[0].lower() == "/a":
                if CMD_Command.split()[1].lower() == "--virus" or CMD_Command.split()[1].lower() == "-v":
                    if CMD_Command.split()[2].lower() == "--md5" or CMD_Command.split()[2].lower() == "-m":
                        try:
                            value = str(CMD_Command.split()[3])
                            with open('Library/PYAE/Hashes/Viruslist.md5','a') as vm:
                                vm.write(str(value)[:10]+'\n')
                            self.ui.Customize_CMD_Command_output.setText("Successfully added MD5 to the database!")
                        except:
                            self.ui.Customize_CMD_Command_output.setText("Error: Add MD5 database failed")
                        return
                    elif CMD_Command.split()[2].lower() == "--file" or CMD_Command.split()[2].lower() == "-f":
                        try:
                            file, filetype= QFileDialog.getOpenFileName(self,self.text_Translate("添加數據庫"),"C:/",'All File *.*')
                            if file != '':
                                with open('Library/PYAE/Hashes/Viruslist.md5','a') as vm:
                                    vm.write(str(md5(open(file,'rb').read()).hexdigest())[:10]+'\n')
                                self.ui.Customize_CMD_Command_output.setText("Successfully added MD5 to the database!")
                        except:
                            self.ui.Customize_CMD_Command_output.setText("Error: Add MD5 database failed")
                        return
            else:
                try:
                    si = subprocess.STARTUPINFO()
                    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    p = subprocess.Popen(CMD_Command,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
                    out = p.stdout.read()
                    try:
                        self.ui.Customize_CMD_Command_output.setText(str(out.decode('utf-8')))
                    except:
                        self.ui.Customize_CMD_Command_output.setText(str(out))
                    QMessageBox.information(self,self.text_Translate("完成"),self.text_Translate("運行成功"),QMessageBox.Ok,QMessageBox.Ok)
                except Exception as e:
                    pyas_bug_log(e)
                    QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+ '\"' + CMD_Command + '\"' + self.text_Translate("不是有效命令"),QMessageBox.Ok,QMessageBox.Ok)
        
    def Customize_REG_Command(self):
        continue_v = True
        Value_name = str(self.ui.Value_Name_input.text())
        Value_Path = str(self.ui.Value_Path_input.text())
        Value_Data = str(self.ui.Value_Data_input.text())
        Value_Type = str(self.ui.Value_Type_input.text())
        Value_HEKY = str(self.ui.Value_HEKY_input.text())
        if Value_HEKY == "HKEY_CLASSES_ROOT":
            Value_HEKY = win32con.HKEY_LOCAL_MACHINE
        elif Value_HEKY == "HKEY_CURRENT_USER":
            Value_HEKY = win32con.HKEY_CURRENT_USER
        elif Value_HEKY == "HKEY_LOCAL_MACHINE":
            Value_HEKY = win32con.HKEY_LOCAL_MACHINE
        elif Value_HEKY == "HKEY_USERS":
            Value_HEKY = win32con.HKEY_USERS
        elif Value_HEKY == "HKEY_CURRENT_CONFIG":
            Value_HEKY = win32con.HKEY_CURRENT_CONFIG
        else:
            QMessageBox.critical(self,self.text_Translate("錯誤"),self.text_Translate('錯誤: ')+self.text_Translate("您輸入了錯誤的HEKY"),QMessageBox.Ok)
            continue_v = False
        if Value_Type == "REG_BINARY":
            Value_Type = win32con.REG_BINARY
        elif Value_Type == "REG_DWORD":
            Value_Type = win32con.REG_DWORD
        elif Value_Type == "REG_DWORD_LITTLE_ENDIAN":
            Value_Type = win32con.REG_DWORD_LITTLE_ENDIAN
        elif Value_Type == "REG_DWORD_BIG_ENDIAN":
            Value_Type = win32con.REG_DWORD_BIG_ENDIAN
        elif Value_Type == "REG_EXPAND_SZ":
            Value_Type = win32con.REG_EXPAND_SZ
        elif Value_Type == "REG_LINK":
            Value_Type = win32con.REG_LINK
        elif Value_Type == "REG_MULTI_SZ":
            Value_Type = win32con.REG_MULTI_SZ
        elif Value_Type == "REG_NONE":
            Value_Type = win32con.REG_NONE
        elif Value_Type == "REG_QWORD":
            Value_Type = win32con.REG_QWORD
        elif Value_Type == "REG_QWORD_LITTLE_ENDIAN":
            Value_Type = win32con.REG_QWORD_LITTLE_ENDIAN
        elif Value_Type == "REG_SZ":
            Value_Type = win32con.REG_SZ
        else:
            QMessageBox.critical(self,self.text_Translate("錯誤"),self.text_Translate('錯誤: ')+self.text_Translate("您輸入了錯誤的TYPE"),QMessageBox.Ok)
            continue_v = False
        if continue_v:
            if QMessageBox.warning(self,self.text_Translate("警告"),self.text_Translate("您確定要新增值或是修改值嗎?"),QMessageBox.Yes|QMessageBox.No) == 16384:
                try:
                    key = win32api.RegOpenKey(Value_HEKY,Value_Path,0,win32con.KEY_ALL_ACCESS)
                    win32api.RegSetValueEx(key, Value_name,0,Value_Type,Value_Data)
                    win32api.RegCloseKey(key)
                    QMessageBox.information(self,self.text_Translate("完成"),self.text_Translate("成功的創建或修改註冊表值"),QMessageBox.Ok)
                except Exception as e:
                    QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+str(e),QMessageBox.Ok)

    def Analyze_EXE(self,button):
        if button == self.ui.Analyze_EXE_Funtion_Button:
            file, filetype= QFileDialog.getOpenFileName(self,self.text_Translate("分析文件函數"),"C:/",'EXE OR DLL File *.exe *.dll')
            if file != '':
                pe = PE(file)
                self.ui.Analyze_EXE_Output.setText("")
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    for function in entry.imports:
                        try:
                            self.ui.Analyze_EXE_Output.append(str(function.name.decode('utf-8')))
                        except:
                            self.ui.Analyze_EXE_Output.append(str(function.name))
                pe.close()
                self.Change_Tools(self.ui.Analyze_EXE_widget)
                QApplication.processEvents()
            else:
                pass
        elif button == self.ui.Analyze_EXE_hash_Button:
            file, filetype= QFileDialog.getOpenFileName(self,self.text_Translate("分析文件哈希值"),"C:/",'All File *.*')
            if file != '':
                self.ui.Analyze_EXE_Output.setText("")
                with open(file,"rb") as f:
                    bytes = f.read()
                    readable_hash = str(md5(bytes).hexdigest())
                    readable_hash2 = str(sha1(bytes).hexdigest())
                    readable_hash3 = str(sha256(bytes).hexdigest())
                    self.ui.Analyze_EXE_Output.append(f'MD5: {readable_hash}\nSHA1: {readable_hash2}\nSHA256: {readable_hash3}')
                self.Change_Tools(self.ui.Analyze_EXE_widget)
                QApplication.processEvents()
                f.close()
            else:
                pass
        else:
            file, filetype= QFileDialog.getOpenFileName(self,self.text_Translate("分析文件位元"),"C:/",'EXE OR DLL File *.exe *.dll')
            if file != '':
                pe = PE(file,fast_load=True)
                self.ui.Analyze_EXE_Output.setText("")
                for section in pe.sections:
                    try:
                        self.ui.Analyze_EXE_Output.append(str(section.Name.decode('utf-8')) + str(hex(section.VirtualAddress)) + str(hex(section.Misc_VirtualSize)) + str(section.SizeOfRawData))
                    except:
                        self.ui.Analyze_EXE_Output.append(str(section.Name) + str(hex(section.VirtualAddress)) + str(hex(section.Misc_VirtualSize)) + str(section.SizeOfRawData))
                pe.close()
                self.Change_Tools(self.ui.Analyze_EXE_widget)
                QApplication.processEvents()

    def Look_for_File(self):
        try:
            File_Name = self.ui.Look_for_File_input.text()
            if File_Name != "":
                self.find_files_info_zh(File_Name)
            else:
                QMessageBox.information(self,self.text_Translate("提示"),'['+self.text_Translate("提示")+'] '+self.text_Translate("請輸入需要尋找的檔案"),QMessageBox.Ok)
        except Exception as e:
            pyas_bug_log(e)

    def find_files_info_zh(self,ffile):
        self.find_files = []
        try:
            for d in range(26):
                try:
                    self.findfile_zh(str(chr(65+d))+':/',ffile)
                except:
                    pass
            if self.find_files != []:
                self.ui.Look_for_File_output.setText('')
                for find_file in self.find_files:
                    self.ui.Look_for_File_output.append(find_file)
                QApplication.processEvents()
                self.Change_Tools(self.ui.Look_for_File_widget)
            else:
                QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+self.text_Translate('未找到檔案'),QMessageBox.Ok)
        except:
            pass

    def findfile_zh(self,path,ffile):
        self.ui.Look_for_File_output.setText(self.text_Translate('正在尋找: ')+str(path))
        QApplication.processEvents()
        for fd in os.listdir(path):
            try:
                fullpath = str(os.path.join(path,fd)).replace("\\", "/")
                if ':/Windows' in fullpath or ':/$Recycle.Bin' in fullpath or ':/ProgramData' in fullpath or 'AppData' in fullpath or 'PerfLogs' in fullpath:
                    continue
                elif os.path.isdir(fullpath):
                    self.findfile_zh(fullpath,ffile)
                elif ffile in str(fd):
                    date = time.ctime(os.path.getmtime(fullpath))
                    self.find_files.append(str(self.text_Translate('找到檔案: ')+str(fullpath)+'\n'+self.text_Translate('創建日期: ')+str(date)+'\n'))
            except:
                continue

    def Process_list(self):
        try:
            self.Process_quantity = []
            self.Process_list_app = []
            self.Process_list_app_exe = []
            self.Process_list_app_pid = []
            self.Process_list_app_name = []
            self.Process_list_app_user = []
            for p in psutil.process_iter():
                if p.name() == '' or p.name() == 'System' or p.name() == 'System Idle Process' or p.name() == 'Registry':
                    pass
                else:
                    try:
                        self.Process_list_app.append(f"{p.name()} ({p.pid}) > {p.exe()}")
                        self.Process_list_app_pid.append(p.pid)
                        self.Process_list_app_exe.append(p.exe())
                        self.Process_list_app_name.append(p.name())
                        self.Process_list_app_user.append(p.username())
                    except:
                        self.Process_list_app.append(f"{p.name()} ({p.pid})")
                        self.Process_list_app_pid.append(p.pid)
                        self.Process_list_app_exe.append('None')
                        self.Process_list_app_name.append(p.name())
                        self.Process_list_app_user.append(p.username())
            if len(self.Process_list_app_name) != self.Process_quantity:
                self.Process_quantity = len(self.Process_list_app_name)
                self.ui.Process_Total_View.setText(str(self.Process_quantity))
                self.Process_sim.setStringList(self.Process_list_app)
                self.ui.Process_list.setModel(self.Process_sim)
        except Exception as e:
            if str(type(e)) == "<class 'psutil.AccessDenied'>":
                print('[Error] Psutil Permission Denied')
            else:
                pyas_bug_log(e)

    def Encryption_Text(self):
        input_text = self.ui.Encryption_Text_input.toPlainText()
        password = self.ui.Encryption_Text_Password_input.text()
        self.encrypt_zh(input_text,password)
    
    def Decrypt_Text(self):
        input_text = self.ui.Encryption_Text_input.toPlainText()
        password = self.ui.Encryption_Text_Password_input.text()
        self.decrypt_zh(input_text,password)

    def encrypt_zh(self,e,e2):
        self.ui.Encryption_Text_output.setText(str(cryptocode.encrypt(e,e2)))

    def decrypt_zh(self,e,e2):
        self.ui.Encryption_Text_output.setText(str(cryptocode.decrypt(e,e2)))

    def Change_Users_Password(self):
        username = self.ui.Change_Users_Password_User_Name_input.text()
        password = self.ui.Change_Users_Password_New_Password_input.text()
        if QMessageBox.warning(self,self.text_Translate("警告"),self.text_Translate("您確定要修改用戶密碼嗎?"),QMessageBox.Yes|QMessageBox.No) == 16384:
            try:
                if password == "":
                    subprocess.call("net user {} {}".format(username,'""'))
                else:
                    subprocess.call("net user {} {}".format(username,password))
            except Exception as e:
                QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+str(e),QMessageBox.Ok)

    def Internet_location_Query(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            QMessageBox.information(self,self.text_Translate("IP查詢"),self.text_Translate("您的ip地址為:{}").format(s.getsockname()[0]),QMessageBox.Ok)
            s.close()
        except Exception as e:
            pyas_bug_log(e)

    def reset_network(self):
        if QMessageBox.warning(self,self.text_Translate("警告"),self.text_Translate("您確定要重置網路配置嗎?"),QMessageBox.Yes|QMessageBox.No) == 16384:
            try:
                subprocess.call("netsh winsock reset", shell=True)
                QMessageBox.information(self,self.text_Translate("完成"),self.text_Translate("重置網路配置成功"),QMessageBox.Ok)
            except Exception as e:
                QMessageBox.critical(self,self.text_Translate('錯誤'),self.text_Translate('錯誤: ')+str(e),QMessageBox.Ok)

    def Setting_Back(self):
        self.ui.Navigation_Bar.show()
        self.ui.Setting_widget.hide()

    def Process_list_Menu(self,pos):
        try:
            self.item = self.ui.Process_list.selectedIndexes()
            for i in self.item:
                item = i.row()
                self.pid = self.Process_list_app_pid[item]
                self.exefile = self.Process_list_app_exe[item]
                self.exename = self.Process_list_app_name[item]
            self.Process_popMenu = QMenu()
            self.kill_Process = QAction(self.text_Translate("結束進程"),self)
            self.Process_popMenu.addAction(self.kill_Process)
            ques = self.Process_popMenu.exec_(self.ui.Process_list.mapToGlobal(pos))
            if ques == self.kill_Process:
                for p in psutil.process_iter():
                    if p.pid == self.pid:
                        p.kill()
        except Exception as e:
            pyas_bug_log(e)

##################################### 實時防護 #####################################
    
    def protect_threading_init(self):
        self.ui.State_output.clear()
        if self.ui.Protection_switch_Button.text() == self.text_Translate("已開啟"):
            remove_rtp()
            self.ui.Protection_switch_Button.setText(self.text_Translate("已關閉"))
            self.ui.Protection_switch_Button.setStyleSheet("""
            QPushButton{border:none;background-color:rgba(20,20,20,30);border-radius: 15px;}
            QPushButton:hover{background-color:rgba(20,20,20,50);}""")
            self.ui.State_output.append(str(time.strftime('%Y/%m/%d %H:%M:%S')) + self.text_Translate(' > [提示] 尚未啟用實時防護'))
            QApplication.processEvents()
        else:
            self.ui.Protection_illustrate.setText(self.text_Translate("正在初始化中，請稍後..."))
            QApplication.processEvents()
            Thread(target = self.pyas_protect_init).start()

    def pyas_protect_repair(self):
        rp_reg = False
        try:
            Permission = ['NoControlPanel', 'NoDrives', 'NoControlPanel', 'NoFileMenu', 'NoFind', 'NoRealMode', 'NoRecentDocsMenu','NoSetFolders', \
            'NoSetFolderOptions', 'NoViewOnDrive', 'NoClose', 'NoRun', 'NoDesktop', 'NoLogOff', 'NoFolderOptions', 'RestrictRun', \
            'NoViewContexMenu', 'HideClock', 'NoStartMenuMorePrograms', 'NoStartMenuMyGames', 'NoStartMenuMyMusic' 'NoStartMenuNetworkPlaces', \
            'NoStartMenuPinnedList', 'NoActiveDesktop', 'NoSetActiveDesktop', 'NoActiveDesktopChanges', 'NoChangeStartMenu', 'ClearRecentDocsOnExit', \
            'NoFavoritesMenu', 'NoRecentDocsHistory', 'NoSetTaskbar', 'NoSMHelp', 'NoTrayContextMenu', 'NoViewContextMenu', 'NoWindowsUpdate', \
            'NoWinKeys', 'StartMenuLogOff', 'NoSimpleNetlDList', 'NoLowDiskSpaceChecks', 'DisableLockWorkstation', 'NoManageMyComputerVerb']
            try:#開啟註冊表鍵
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'Explorer')#創建鍵
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
            for i in Permission:
                try:
                    win32api.RegDeleteValue(key,i)#刪除值
                    rp_reg = True
                except:
                    pass
            win32api.RegCloseKey(key)#關閉已打開的鍵
            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'Explorer')
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
            key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
            for i in Permission:
                try:
                    win32api.RegDeleteValue(key,i)
                    rp_reg = True
                except:
                    pass
            win32api.RegCloseKey(key)
            Permission = ['DisableTaskMgr', 'DisableRegistryTools', 'DisableChangePassword', 'Wallpaper']
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'System')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',0,win32con.KEY_ALL_ACCESS)
            for i in Permission:
                try:
                    win32api.RegDeleteValue(key,i)
                    rp_reg = True
                except:
                    pass
            win32api.RegCloseKey(key)
            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'System')
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',0,win32con.KEY_ALL_ACCESS)
            for i in Permission:
                try:
                    win32api.RegDeleteValue(key,i)
                    rp_reg = True
                except:
                    pass
            win32api.RegCloseKey(key)
            Permission = ['NoComponents', 'NoAddingComponents']
            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'ActiveDesktop')
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop',0,win32con.KEY_ALL_ACCESS)
            for i in Permission:
                try:
                    win32api.RegDeleteValue(key,i)
                    rp_reg = True
                except:
                    pass
            win32api.RegCloseKey(key)
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Policies\Microsoft\Windows\System',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Policies\Microsoft\Windows',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'System')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Policies\Microsoft\Windows\System',0,win32con.KEY_ALL_ACCESS)
            try:
                win32api.RegDeleteValue(key, 'DisableCMD')
                rp_reg = True
            except:
                pass
            win32api.RegCloseKey(key)
            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Policies\Microsoft\Windows\System',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Policies\Microsoft\Windows',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'System')
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Policies\Microsoft\Windows\System',0,win32con.KEY_ALL_ACCESS)
            try:
                win32api.RegDeleteValue(key, 'DisableCMD')
                rp_reg = True
            except:
                pass
            win32api.RegCloseKey(key)
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Policies\Microsoft\MMC\{8FC0B734-A0E1-11D1-A7D3-0000F87571E3}',0,win32con.KEY_ALL_ACCESS)
            except:
                try:
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Policies\Microsoft\MMC',0,win32con.KEY_ALL_ACCESS)
                except:
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Policies\Microsoft',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegCreateKey(key,'MMC')
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Policies\Microsoft\MMC',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'{8FC0B734-A0E1-11D1-A7D3-0000F87571E3}')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Policies\Microsoft\MMC\{8FC0B734-A0E1-11D1-A7D3-0000F87571E3}',0,win32con.KEY_ALL_ACCESS)
            try:
                win32api.RegDeleteValue(key, 'Restrict_Run')
                rp_reg = True
            except:
                pass
            win32api.RegCloseKey(key)
        except:
            rp_reg = False
        return rp_reg

    def pyas_protect_init(self):
        try:
            print('[INFO] Start Action (Real-time Protect)')
            open('Library/PYAS/Temp/PYASP.tmp','w',encoding='utf-8').write('Protect temp file, dont remove it')
            if self.ui.Protection_switch_Button.text() == self.text_Translate("已關閉"):
                self.ui.Protection_illustrate.setText(self.text_Translate("啟用該選項可以實時監控進程中的惡意軟體並清除。"))
                self.ui.Protection_switch_Button.setText(self.text_Translate("已開啟"))
                self.ui.Protection_switch_Button.setStyleSheet("""
                QPushButton{border:none;background-color:rgba(20,200,20,100);border-radius: 15px;}
                QPushButton:hover{background-color:rgba(20,200,20,120);}""")
            while os.path.isfile('Library/PYAS/Temp/PYASP.tmp'):
                for p in psutil.process_iter():
                    try:
                        time.sleep(0.00001)
                        QApplication.processEvents()
                        file, name = str(p.exe()), str(p.name())
                        if '' == file or str(sys.argv[0]) == file or ':\Windows' in file or ':\Program' in file or ':\XboxGames' in file or 'mem' in file.lower() or 'Registry' in file or 'AppData' in file:
                            continue
                        elif self.pyas_sign_start(file) or self.api_scan('md5', file):
                            if subprocess.call(f'taskkill /f /im "{name}" /t',shell=True) == 0:
                                text = self.text_Translate('{} > [實時防護] 成功攔截了一個惡意軟體:').format(time.strftime('%Y/%m/%d %H:%M:%S'))+name
                            else:
                                if not self.pyas_protect_repair():
                                    text = self.text_Translate('{} > [實時防護] 惡意軟體攔截失敗:').format(time.strftime('%Y/%m/%d %H:%M:%S'))+name
                            self.ui.State_output.append(text)
                            ToastNotifier().show_toast("PYAS Security",text,icon_path="Library/PYAS/Icon/ICON.ico",duration=10,threaded=True)
                    except:
                        continue
        except Exception as e:
            pyas_bug_log(e)

##################################### 系統設置 #####################################

    def ShowMenu(self):
        self.WindowMenu = QMenu()
        Main_Settings = QAction(self.text_Translate("設定"),self)
        Main_About = QAction(self.text_Translate("關於"),self)
        self.WindowMenu.addAction(Main_Settings)
        self.WindowMenu.addAction(Main_About)
        pos = QtCore.QPoint(0, 30)
        Qusetion = self.WindowMenu.exec_(self.ui.Menu_Button.mapToGlobal(pos))
        if Qusetion == Main_About:
            if self.ui.About_widget.isHidden():
                self.ui.About_widget.show()
                self.ui.About_widget.raise_()
                self.ui.Navigation_Bar.raise_()
                self.ui.Window_widget.raise_()
                self.Change_animation_3(self.ui.About_widget,0.5)
                self.Change_animation5(self.ui.About_widget,170,50,671,481)
                self.Setting_Back()
        if Qusetion == Main_Settings:
            if self.ui.Setting_widget.isHidden():
                self.ui.Setting_widget.show()
                self.ui.About_widget.hide()
                self.ui.Setting_widget.raise_()
                self.ui.Window_widget.raise_()
                self.Change_animation_3(self.ui.Setting_widget,0.5)
                self.Change_animation5(self.ui.Setting_widget,10,50,831,481)

    def Show_Virus_Scan_Progress_Bar_switch(self):
        try:
            sw_state = self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.text()
            if sw_state == self.text_Translate("已關閉"):
                self.pyasConfig['high_sensitivity'] = 1
                self.writeConfig(self.pyasConfig)
                self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.setText(self.text_Translate("已開啟"))
                self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.setStyleSheet("""
                QPushButton{border:none;background-color:rgba(20,200,20,100);border-radius: 15px;}
                QPushButton:hover{background-color:rgba(20,200,20,120);}""")
                self.show_virus_scan_progress_bar = 1
            elif sw_state == self.text_Translate("已開啟"):
                self.pyasConfig['high_sensitivity'] = 0
                self.writeConfig(self.pyasConfig)
                self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.setText(self.text_Translate("已關閉"))
                self.ui.Show_Virus_Scan_Progress_Bar_switch_Button.setStyleSheet("""
                QPushButton{border:none;background-color:rgba(20,20,20,30);border-radius: 15px;}
                QPushButton:hover{background-color:rgba(20,20,20,50);}""")
                self.show_virus_scan_progress_bar = 0
            else:
                pass
        except:
            try:
                config = {'high_sensitivity': 0,'language': 'english'}
                self.writeConfig(config)
            except Exception as e:
                pyas_bug_log(e)

##################################### 更改語言 #####################################
    
    def Change_language(self):
        try:
            self.ui.State_output.clear()
            if self.ui.Language_Traditional_Chinese.isChecked():
                self.pyasConfig['language'] = "zh_TW"
                self.writeConfig(self.pyasConfig)
                self.lang_init_zh_tw()
            elif self.ui.Language_Simplified_Chinese.isChecked():
                self.pyasConfig['language'] = "zh_CN"
                self.writeConfig(self.pyasConfig)
                self.lang_init_zh_cn()
            else:
                self.pyasConfig['language'] = "english"
                self.writeConfig(self.pyasConfig)
                self.lang_init_en()
        except Exception as e:
            pyas_bug_log(e)

##################################### 主題顏色 #####################################
    
    def Change_Theme(self):
        if self.ui.Theme_Red.isChecked():
            self.ui.Window_widget.setStyleSheet("""QWidget#Window_widget {background-color:rgba(255,140,140,200);}""")
            self.ui.Navigation_Bar.setStyleSheet("""QWidget#Navigation_Bar {background-color:rgba(255,130,130,200);}""")
            return
        elif self.ui.Theme_White.isChecked():
            self.ui.Window_widget.setStyleSheet("""QWidget#Window_widget {background-color:rgb(240,240,240);}""")
            self.ui.Navigation_Bar.setStyleSheet("""QWidget#Navigation_Bar {background-color:rgb(230,230,230);}""")
            return
        elif self.ui.Theme_Black.isChecked():
            self.ui.Window_widget.setStyleSheet("""QWidget#Window_widget {background-color:rgba(90,90,90,130);}""")
            self.ui.Navigation_Bar.setStyleSheet("""QWidget#Navigation_Bar {background-color:rgba(80,80,80,150);}""")
            return
        elif self.ui.Theme_Green.isChecked():
            self.ui.Window_widget.setStyleSheet("""QWidget#Window_widget {background-color:rgba(120,240,130,180);}""")
            self.ui.Navigation_Bar.setStyleSheet("""QWidget#Navigation_Bar {background-color:rgba(100,240,110,200);}""")
            return
        elif self.ui.Theme_Pink.isChecked():
            r,g,b = randrange(50, 250),randrange(50, 250),randrange(50, 250)
            self.ui.Window_widget.setStyleSheet("""QWidget#Window_widget {background-color:rgba("""+str(r)+""","""+str(g)+""","""+str(b)+""",240);}""")
            self.ui.Navigation_Bar.setStyleSheet("""QWidget#Navigation_Bar {background-color:rgba("""+str(r-20)+""","""+str(g-20)+""","""+str(b-20)+""",240);}""")
            return
        elif self.ui.Theme_Blue.isChecked():
            self.ui.Window_widget.setStyleSheet("""QWidget#Window_widget {background-color:rgba(0,120,240,100);}""")
            self.ui.Navigation_Bar.setStyleSheet("""QWidget#Navigation_Bar {background-color:rgba(0,120,240,120);}""")
            return
        
##################################### 操作事件 #####################################

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        if event.button()==Qt.LeftButton and x >= 10 and x <= 841 and y >= 10 and y <= 49:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #獲取鼠標相對窗口的位置
            event.accept()
            while self.ui.pyas_opacity > 60 and self.m_flag == True:
                time.sleep(0.003)
                self.ui.pyas_opacity -= 1
                window.setWindowOpacity(self.ui.pyas_opacity/100)
                QApplication.processEvents()
        
    def mouseMoveEvent(self, QMouseEvent):
        try:
            if Qt.LeftButton and self.m_flag:
                self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
                QApplication.processEvents()
                QMouseEvent.accept()
        except:
            pass
        
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))
        while self.ui.pyas_opacity < 100 and self.m_flag == False:
            time.sleep(0.003)
            self.ui.pyas_opacity += 1
            window.setWindowOpacity(self.ui.pyas_opacity/100)
            QApplication.processEvents()

    def paintEvent(self, event):# 圓角
        pat2 = QPainter(self)
        pat2.setRenderHint(QPainter.Antialiasing)
        pat2.setBrush(Qt.white)
        pat2.setPen(Qt.transparent)
        rect = self.rect()
        rect.setLeft(10)
        rect.setTop(10)
        rect.setWidth(rect.width()-10)
        rect.setHeight(rect.height()-10)
        pat2.drawRoundedRect(rect, 1, 1)

    def closeEvent(self, event):
        while self.ui.pyas_opacity > 0:
            time.sleep(0.001)
            self.ui.pyas_opacity -= 1
            window.setWindowOpacity(self.ui.pyas_opacity/100)
            QApplication.processEvents()
        window.hide()

##################################### 主初始化 #####################################

if __name__ == '__main__':
    try:
        pyas_lib()
        remove_tmp()
        remove_rtp()
        pyas_version, pyae_version = "2.6.1", "2.2.5"
        QtCore.QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)# 自適應窗口縮放
        QtGui.QGuiApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)# 自適應窗口縮放
        app = QtWidgets.QApplication(sys.argv)
        window = MainWindow_Controller()
        window.show()
        for i in range(101):
            time.sleep(0.001)
            window.setWindowOpacity(i/100)
            QApplication.processEvents()
        print(f'[INFO] PYAS V{pyas_version} , PYAE V{pyae_version}')
        sys.exit(app.exec_())
    except Exception as e:
        pyas_bug_log(e)

####################################################################################
#Copyright© 2020-2023 87owo (PYAS Security)
