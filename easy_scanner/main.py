#!/usr/bin/env python3
from PyQt6 import QtWidgets,QtCore,QtGui
from PyQt6.QtCore import QObject, pyqtSignal, QThread,Qt,QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog,QSizePolicy,QLineEdit
from PyQt6.QtGui import QScreen,QPalette,QColor
import sys
from appui import Ui_MainWindow   
import subprocess
import re
from datetime import datetime
import socket
import time 
from PyQt6.QtCore import Qt 
import requests
import os
from PyQt6.QtCore import QProcess
import signal
import json
import threading
import re

global filelogname
global folderlogproject
global file_full_nmap
global file_app_log
global temp_log_tosave
global temp_logapp
global should_exit
should_exit=False
temp_logapp=""
temp_log_tosave=""
file_full_nmap="full_nmap_output.txt"
file_app_log="app_log.txt"
filelogname=""
folderlogproject=""


 
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Initialize configuration
        self.config = self.init_config()

        self.center_on_screen()   
        self.new_button(self.ui.new_p)
        self.new_button(self.ui.run_nikto)
        self.new_button(self.ui.run_gbuster)
        self.new_button(self.ui.run_dirsearch)
        self.new_button(self.ui.run_enum)
        self.new_button(self.ui.run_wpscan)
        self.new_button(self.ui.run_sqlmap)
        self.new_button(self.ui.clean_notes)
        self.new_button(self.ui.openfile)

        self.styleButton(self.ui.run_dirsearch, "rgb(97, 227, 227)")
        self.styleButton(self.ui.run_enum, "rgb(187, 91, 116)")
        self.styleButton(self.ui.run_wpscan, "rgb(220, 138, 221)")
        self.styleButton(self.ui.run_sqlmap, "rgb(101, 136, 99)")
        self.styleButton(self.ui.openfile, "rgb(101, 136, 99)")
        self.styleButton(self.ui.run_nmap, "rgb(118, 64, 140)")
        self.styleButton(self.ui.run_nikto, "rgb(205, 171, 143)")
        self.styleButton(self.ui.run_gbuster, "rgb(153, 193, 241)")
        self.styleButton(self.ui.quit, "rgb(119, 118, 123)")        # Soft blue
        self.styleButton(self.ui.clean_all, "rgb(119, 118, 123)")   # Mild green
        self.styleButton(self.ui.clean_notes, "rgb(119, 118, 123)") # Light peach
        self.styleButton(self.ui.new_p, "rgb(119, 118, 123)")       # Pale yellow

        self.ui.run_nmap.clicked.connect(self.run_scan)
        self.ui.run_nikto.clicked.connect(self.run_nikto)
        self.ui.quit.clicked.connect(self.on_exit_button_clicked)
        self.ui.clean_all.clicked.connect(self.clean)
        self.ui.new_p.clicked.connect(self.new_pro)
        self.ui.clean_notes.clicked.connect(self.clean_notes)
        self.ui.run_gbuster.clicked.connect(self.gobuster)
        self.ui.run_dirsearch.clicked.connect(self.dirsearch)
        self.ui.run_enum.clicked.connect(self.enumlinux)
        self.ui.run_wpscan.clicked.connect(self.wpscan)
        self.ui.run_sqlmap.clicked.connect(self.sqlmap)
        self.ui.openfile.clicked.connect(self.open_file_dialog)

        self.ui.portServicef.setColumnWidth(0,130) 
        self.ui.portServicef.setColumnWidth(1,210) 
        self.ui.portServicef.setColumnWidth(2,1500)

        self.ui.run_nmap.setDefault(True)
        self.ui.ipf.setText("localhost") 
        self.ui.radio_url.setChecked(True)

        font = QtGui.QFont("Arial", 16)  # Use a standard size font
        self.ui.portServicef.setFont(font)
        font = QtGui.QFont("Arial", 12)  # Changed to a more common font as a test
        self.ui.textEdit.setFont(font)

        self.ui.portServicef.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        # store sudo password
        self.sudo_password = None

    def open_file_dialog(self):
        # Specify valid options for the QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a file",
            "",  # Start directory (empty uses the default home directory)
            "Text Files (*.txt)",  # Filter for file types
            options=QFileDialog.Option.DontUseNativeDialog)  # Valid option

        if file_path:
            print("File selected:", file_path)
            self.ui.lineEdit.setText(file_path)
 

    def check_exit(self):
        global should_exit
        exitornot=input("\rwould you like to exit ? Y/N   " )
        if exitornot.lower()=="y":
            should_exit=True
            sys.exit(0) 
        else:
            print("ok, we back to the main app")
            self.update_form()
            self.bring_them_home()
            return None
            
    def new_button(self,name):
        name.setEnabled(True)
        name.clearFocus()

    
    def load_tool_config(self, config_path='config.json'):
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
            
            # Ensure default sections
            config.setdefault('output_dir', 'reports')  
            config.setdefault('gobuster', {}).setdefault('timeout', 60)
            config['gobuster'].setdefault('wordlist', 'wordlists/directory-list-2.3-medium.txt')
            config.setdefault('nikto', {}).setdefault('timeout', 20)
            config.setdefault('nmap', {}).setdefault('tags', [])
            config.setdefault('sqlmap', {}).setdefault('options', ["--batch", "--level=1", "--risk=1", "--threads=4"])
            config.setdefault('dirsearch', {}).setdefault('extensions', 'html,php,txt,js,rar,zip,asp,jsp,sql,xml,json,config,bak,cgi,log')
            
            return config
        except FileNotFoundError:
            print("Configuration file not found. Using defaults.")
            return None
        except json.JSONDecodeError:
            print("Error decoding JSON. Using defaults.")
            return None

  
    def sqlmap(self):
        self.sqlanalyse()

    def sqlanalyse(self):
        output=self.scansql()
        print ("Done")
        self.logs("FINISHED sqlmap","") 
        folder="/sql_output"
        self.logs(f"full output of sqlmap save in folder: {folder}","")
    
    def scansql(self):
        global folderlogproject
        if folderlogproject=="":
             folderlogproject,time=self.get_folder()
        output=""
        allset=False
        ip = self.ui.ipf.text()
        file = self.ui.lineEdit.text()
        source=""
        folder="/sql_output"
        dir_outputsql=folderlogproject+folder
        print(dir_outputsql)
        
        # Create output directory if it doesn't exist
        os.makedirs(dir_outputsql, exist_ok=True)
        
        # Load configuration for sqlmap options
        config = self.config
        default_options = ["--batch", "--level=1", "--risk=1", "--threads=4"]
        
        if config and config.get('sqlmap') and 'options' in config['sqlmap']:
            sqlmap_options = config['sqlmap']['options']
        else:
            # Safe default options - not including aggressive options by default
            sqlmap_options = default_options
            
        if self.ui.radio_file.isChecked():
          if not file:
            print("you cant run sqlmap from file witout choosing file..")
            print("choose file from the main app")
          else:
            self.print_bold("Starting SQLmap from file...", "1;34")
            source="file"
            allset=True

        if self.ui.radio_url.isChecked():
          if not ip:
            print("you cant run sqlmap from url witout define url..")
            print("put url in the main app")
          else:
            self.print_bold("Starting SQLmap from url...", "1;34")
            source="url"
            allset=True

        if allset:
            if source=="url":
                cmd = ["sqlmap", "-u", ip, "--output-dir="+dir_outputsql]
                cmd.extend(sqlmap_options)
            if source=="file":
                cmd = ["sqlmap", "-r", file, "--output-dir="+dir_outputsql]
                cmd.extend(sqlmap_options)

            # Get timeout from config
            timeout = config.get('sqlmap', {}).get('timeout', 120) if config else 120
            print(f"Timeout set to: {timeout} seconds")
            self.logs("now i will run SQLmap","")
            output=self.runinshell(cmd,timeout=timeout,scanner="sqlmap",needs_sudo=False)
            if output:
                    output='\n'.join(output)
            return output
            


    def gobuster(self):
         self.gonalyse()
    
    def scan_buster(self, file):
        output=""  
        
        ip = self.ui.ipf.text()
        ports = self.ui.portf.text()
        
        # Get configuration values from config or use defaults
        config = self.config
        wordlist = config.get('gobuster', {}).get('wordlist', 'wordlists/directory-list-2.3-medium.txt') if config else 'wordlists/directory-list-2.3-medium.txt'
        timeout = config.get('gobuster', {}).get('timeout', 60) if config else 60
        ext = config.get('gobuster', {}).get('extensions', 'html,php,txt,js,rar,zip,asp,jsp,sql,xml,json,config,bak,cgi,log') if config else 'html,php,txt'
        
        port = ""
        if ports.strip() != "":
            port = "-p " + ports
            
        # Get custom tags from config
        custom_tags = config.get('gobuster', {}).get('tags', []) if config else []

        cmd = [
            "gobuster",
            "dir",
            "-u", ip,
            "-w", wordlist,
            "-e",
            "-x", ext,
            "-t", "40",
            "-q",
            "-z",
            "-o", file
        ]
        
        # Add any custom tags from config
        for tag in custom_tags:
            cmd.append(tag)

        self.logs("now i will run gobuster","")
        output = self.runinshell(cmd, timeout=timeout, scanner="gobuster", needs_sudo=False)
        return output

    def gonalyse(self):
        global folderlogproject
        file=""
        self.print_bold("Starting Gobuster...", "1;34")
        if folderlogproject=="":
            folderlogproject,time=self.get_folder()
        file=folderlogproject+"/gobuster_result.txt"
        output=self.scan_buster(file)
        #output='\n'.join(output)
        if output:
            redirect_urls = []

            # Iterate over each line in the output
            for line in output:
            # Check if there's a redirect arrow indicating a URL to capture
                if '-->' in line:
                    # Split the line on the redirect arrow and strip extra whitespace
                    parts = line.split('-->')
                    if len(parts) > 1:
                        url = parts[1].strip()
                        # Remove the trailing ']' if present
                        if url.endswith(']'):
                            url = url[:-1]
                        redirect_urls.append(url)

        # print("Collected redirect URLs:")
            if redirect_urls:
                self.logs(f"found intersting folder/files:","b")
                for url in redirect_urls:
                    self.logs(f"----{url}","b")

        print ("done")
        self.logs("FINISHED gobuster","") 
        self.logs(f"full report of gobuster save in file: {file}","")
       
    def dirsearch(self):
        self.diranalyse()
    
    def diranalyse(self):
        output=self.scan_dirsearch()
        #output='\n'.join(output)
        if output:
            urls = []
            urls = re.findall(r'->\s+(http[s]?://\S+)', output)
            if urls:
                self.logs(f"found intersting folder/files:","b")
                for url in urls:
                    self.logs(f"----{url}","b")
        print ("done")
        self.logs("FINISHED dirsearch","") 
         
    def scan_dirsearch(self):
        self.print_bold("Starting Dirsearch...", "1;34")
        ip = self.ui.ipf.text()
        ports = self.ui.portf.text()
        
        # Get extensions from config
        ext = self.config.get('dirsearch', {}).get('extensions', 
               "html,php,txt,js,rar,zip,asp,jsp,sql,xml,json,config,bak,cgi,log") if self.config else "html,php,txt"
        
        # Get timeout from config
        timeout = self.config.get('dirsearch', {}).get('timeout', 120) if self.config else 120
        
        # Get wordlist from config
        wordlist = self.config.get('dirsearch', {}).get('wordlist', 
                   "/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt") if self.config else ""
        
        codes = "404,403"  # "301,302,404,403"
        port = ""
        if ports.strip() != "":
            port = "-p " + ports

        # Prepare the command as a list of arguments
        cmd = [
            "dirsearch",
            "-u", ip,
            "-e", ext,
            "-q",
            "-x", codes
        ]
        
        # Add wordlist if specified in config
        if wordlist:
            cmd.extend(["-w", wordlist])

        self.logs("now i will run Dirsearch", "")
        output = self.runinshell(cmd, timeout=timeout, scanner="dirsearch", needs_sudo=False)
        if output:
            output = '\n'.join(output)
        return output
    
    def enumlinux(self):
        self.enumanalyse()

    def enumanalyse(self):
        output=self.scan_enum()
        print ("done")
        self.logs("FINISHED enum4linux","") 

    def scan_enum(self):
        self.print_bold("Starting Enum4linux...", "1;34")
        ip = self.ui.ipf.text()
        ports = self.ui.portf.text()
        
        # Get options and timeout from config
        config = self.config
        timeout = config.get('enum4linux', {}).get('timeout', 600) if config else 600
        enum_options = config.get('enum4linux', {}).get('options', ["-a"]) if config else ["-a"]
        
        port = ""
        if ports.strip() != "":
            port = "-p " + ports

        # Prepare the command as a list of arguments
        cmd = ["enum4linux"]
        
        # Add all options from config
        cmd.extend(enum_options)
        
        # Add target IP
        cmd.append(ip)
        
        self.logs("now i will run Enum4linux with options: " + " ".join(enum_options), "")
        output = self.runinshell(cmd, timeout=timeout, scanner="enum4linux", needs_sudo=False)
        if output:
            output = '\n'.join(output)
        return output

    def wpanalyse(self):
        output=self.scan_wpscan()
        print ("done")
        self.logs("FINISHED wpscan","") 
    
    def wpscan(self):
        self.wpanalyse()
    
    def scan_wpscan(self):
        self.print_bold("Starting WPscan...", "1;34")
        ip = self.ui.ipf.text()
        ports = self.ui.portf.text()
        
        # Get options and timeout from config
        config = self.config
        timeout = config.get('wpscan', {}).get('timeout', 600) if config else 600
        
        # Get enumeration options - default value matches current code's behavior
        wp_options = config.get('wpscan', {}).get('options', ["--enumerate", "vp,vt,u,cb,m"]) if config else ["--enumerate", "vp,vt,u,cb,m"]
        
        port = ""
        if ports.strip() != "":
            port = "-p " + ports

        # Prepare the command as a list of arguments
        cmd = [
            "wpscan",
            "--url", ip
        ]
        
        # Add all options from config
        cmd.extend(wp_options)
        
        self.logs("now i will run WPscan with options: " + " ".join(wp_options), "")
        output = self.runinshell(cmd, timeout=timeout, scanner="wpscan", needs_sudo=False)
        if output:
            output = '\n'.join(output)
        return output
        return output
 

    def run_nikto(self):
        self.niktoanalyse()

    def niktoanalyse(self):
        output=self.scan_nikto()
        print ("Done")
        self.logs("FINISHED nikto","") 
      
    def scan_nikto(self):
        self.print_bold("Starting Nikto...", "1;34")
        ip =  self.ui.ipf.text()
        ports=self.ui.portf.text()
        port=""
        if ports.strip()!="":
            port="-p "+ ports

        # Get timeout from config
        timeout = self.config.get('nikto', {}).get('timeout', 60) if self.config else 60

        cmd = [
            "nikto",
            "-h", ip,
            "-Tuning", "0123456789abcdex",
            port
            ]
      
        self.logs("now i will run NIKTO","")
        output=self.runinshell(cmd,timeout=timeout,scanner="nikto",needs_sudo=False)
        if output:
            output='\n'.join(output)
        return output
    
    def timeout_handler(self,signum, frame):
        raise TimeoutError
    
    def handle_output(self,stream, output_list,scanner,ex):
        in_traceback = False 
        while True:
            line = stream.readline()
            if not line:
                break
            if ex==True:
                break

            line = line.strip()
                
            if scanner=="wpscan":
                if "Trace:" in line or "/lib/" in line or in_traceback:
                    in_traceback = True  # Set flag to indicate we are in a traceback
                    if line.startswith('/usr/share/rubygems-integration'):
                        continue  # Continue to ignore lines until the end of the traceback
                    if line == '' or not line.startswith('/'):  # Heuristic to detect the end of the traceback
                        in_traceback = False  # Reset traceback flag if we reach an empty line or non-trace line
                    continue
                if "Scan Aborted: SIGTERM" in line:
                    continue  # Skip SIGTERM abort message
                if "/bin/wpscan" in line:
                    continue

            # Filter out common noise and undesired lines
            if "Failed to resolve \"\"." in line:
                continue  # Skip resolving errors
            if scanner == "gobuster" and "Progress:" in line:
                continue  # Skip Gobuster progress lines
            if scanner == "dirsearch" and ('%' in line or 'job:' in line):
                continue  # Skip Dirsearch progress bars
            if "[ERROR] context canceled" in line:
                continue
            if "context deadline exceeded " in line:
                continue
            

            # Print and store lines that are not filtered out
            if line and ex!=True:
                print(line)
                    
            output_list.append(line.strip())  # Store the line in the list

    def runinshell(self, cmd, timeout, scanner, needs_sudo):
        env = os.environ.copy()
        ex = False
        output_list = []  # List to capture all output for further analysis
        
        try:
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(timeout)
            if "nmap" in cmd:
                needs_sudo = True

            if needs_sudo:
                # Determine if we need to prompt for password
                if self.has_sudo_privileges():
                    cmd = ['sudo'] + cmd
                else:
                    # Reset password if attempting a scan after failure
                    if self.sudo_password is None or self.sudo_password == "":
                        ok = self.ask_sudo_password()
                        if not ok:
                            print("Sudo authentication failed - canceling scan")
                            self.ui.running.setText("")  # Clear running status
                            return []
                    
                    # Use -S to read password from stdin
                    cmd = ['sudo', '-S'] + cmd

            cmd = ['timeout', str(timeout)] + cmd
            print(f"Executing: {' '.join(cmd)}")

            # Allow sending password to stdin
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
            
            # Feed password only if using sudo -S
            if 'sudo' in cmd and '-S' in cmd and self.sudo_password:
                try:
                    process.stdin.write(self.sudo_password + '\n')
                    process.stdin.flush()
                except BrokenPipeError:
                    print("Failed to send password - pipe closed")
                    self.logs("Failed to authenticate with sudo", "b")
                    self.ui.running.setText("")  # Clear running status
                    return []

            stdout_thread = threading.Thread(target=self.handle_output, args=(process.stdout, output_list, scanner, ex), daemon=True)
            stderr_thread = threading.Thread(target=self.handle_output, args=(process.stderr, output_list, scanner, ex), daemon=True)
            stdout_thread.start()
            stderr_thread.start()
           
            # Wait for threads to complete
            stdout_thread.join()
            stderr_thread.join()

            # Ensure the process has ended
            returncode = process.poll()
            if returncode is None:  # Process still running
                process.terminate()
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    process.kill()

            signal.alarm(0)
            
            # Check for sudo authentication failure
            for line in output_list:
                if "Sorry, try again" in line:
                    print("Sudo authentication failed")
                    self.logs("Sudo authentication failed - wrong password", "b")
                    self.reset_sudo_password()  # Force new password prompt next time
                    self.ui.running.setText("")  # Clear running status
                    return []

            if process.returncode != 0 and process.returncode != 124:  # 124 is timeout's exit code
                stderr = process.communicate()
                self.logs(f"Command failed with return code {process.returncode}", "")
                self.ui.running.setText("")  # Ensure running status is cleared
                return output_list

            return output_list
              
        except KeyboardInterrupt:
            ex = True
            if 'process' in locals():
                process.kill()
            stdout_thread.join()
            self.check_exit()
            self.ui.running.setText("")  # Clear running status
            return output_list

        except TimeoutError:
            ex = True
            if 'process' in locals():
                process.kill()
            print(f"Terminated by timeout after {timeout} seconds\n")
            self.logs(f"Scan terminated by timeout after {timeout} seconds", "")
            self.ui.running.setText("")  # Clear running status
            return output_list
            
        except Exception as e:
            self.logs(f"Error executing command: {str(e)}", "")
            print(f"Error: {str(e)}")
            self.ui.running.setText("")  # Clear running status
            return output_list

    def update_form(self):
        self.update() 
        QApplication.processEvents()
        time.sleep(2) 

    def new_pro(self):
        folderlogproject=""
        self.clean()
       
    def on_exit_button_clicked(self):
        QApplication.quit()
 
    def run_scan(self):
        self.scan_nmap() 
        
    def clean_notes(self):
        self.ui.textEdit.clear()

    def clean(self):
        self.ui.portServicef.clearContents()
        self.ui.textEdit.clear()    
        self.ui.portf.clear()
    
    def styleButton(self, button, normal_color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {normal_color};
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 4px;
                padding: 5px;
                outline: none;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(normal_color, 20)};
                border: 2px solid #aaaaaa;
            }}
            QPushButton:pressed {{
                background-color: {self.lighten_color(normal_color, -20)};
                border: 2px solid #888888;
            }}
        """)


    def lighten_color(self, color, amount):
        """ Lighten a given RGB color. """
        # Use regular expression to find numbers in the RGB string
        numbers = re.findall(r'\d+', color)
        if len(numbers) == 3:
            r, g, b = map(int, numbers)
            r = max(min(r + amount, 255), 0)
            g = max(min(g + amount, 255), 0)
            b = max(min(b + amount, 255), 0)
            return f"rgb({r}, {g}, {b})"
        else:
            # Return the original color if parsing fails
            return color
 


 
    def is_any_cell_filled(self,table_widget,tex):
    #    print("check",tex)
        for row in range(table_widget.rowCount()):
            for column in range(table_widget.columnCount()):
                item = table_widget.item(row, column)
                if item:
                    if tex.lower() in item.text().lower(): #item and item.text():
                        return True
        return False


    def save_log_file(self,text,where):
        global folderlogproject,file_app_log,file_full_nmap
        base_path = folderlogproject
        # print(f"base path: {base_path}")
        # print(f"folder: {folderlogproject}")
        if where == "full":
            file_path = os.path.join(base_path, file_full_nmap)
       #     print(f"file path: {file_path}")
        elif where == "app":
        #    print(f"file path: {file_path}")
            file_path = os.path.join(base_path, file_app_log)
        else:
            return
        with open(file_path, 'a') as file:
            file.write(text + '\n')
        #print(f"file path: {file_path}")
        
    def logs(self,text,bold):
        global temp_log_tosave
        temp_log_tosave+=text+"\n"
        self.add_log(bold,text)
    
    def get_folder(self):
        global folderlogproject
        path=""
        original_ip = self.ui.ipf.text()
        resolved_ip = self.resolve_to_ip(original_ip)
        now = datetime.now()
        time_scan = now.strftime("%H:%M - %d/%m/%y")
        time_format = now.strftime("%d_%m_%y-%H:%M")

        # Use loaded config
        config = self.config
        base_output_dir = config.get('output_dir', 'reports') if config else 'reports'

        if folderlogproject=="":    
            folderlogproject = f"{resolved_ip}_{time_format}"      
            path = os.path.join(os.getcwd(), base_output_dir, folderlogproject)
            os.makedirs(path, exist_ok=True)
            file_names = [file_app_log, file_full_nmap]
            for file_name in file_names:
                file_path = os.path.join(path, file_name)
                with open(file_path, 'w') as file:
                    pass  
            self.logs(f"Created new project folder at: {path}","")
        folderlogproject = path
        return folderlogproject, time_scan

    def scan_nmap(self):
        global folderlogproject,file_app_log,file_full_nmap,temp_log_tosave,should_exit
        path = folderlogproject
        if should_exit:
            return
        try:
            original_ip =  self.ui.ipf.text()
            resolved_ip = self.resolve_to_ip(original_ip)
            folderlogproject,time_scan=self.get_folder()  
            self.logs(f"time of scan: {time_scan}","")
            print("starting..")
            port_option =[]       
            ip = None
            ports_p=""
            ports_only=[]
            services_only=[]
            ports=self.ui.portf.text()
            print ("IP: ",resolved_ip)
            self.logs(f"input target from user: {original_ip}","")
            self.logs(f"resolved ip: {resolved_ip}","")
            self.ui.running.setText('Running!  IP: '+ resolved_ip)
            self.update_form()
            all_ports=self.ui.allports.isChecked()
            self.logs(f"starting basic scan","")

            if ports:
                port_option = ports.split(',')  # Splitting by commas
                ports_p="-p"
                print("running ports: ", ports)
                self.logs(f"i will run only ports: {ports}","")
            elif all_ports:
                ports_p="-p-"
                print("running ALL ports")
                self.logs(f"i will run all ports","")
            else:
                ports_p=""
                print("running common ports")
                self.logs(f"i will run common ports","")   

            self.save_log_file(temp_log_tosave,"app")
            temp_log_tosave=""
            initial_output=self.run_nmap_initial(resolved_ip,ports_p, port_option)
            self.save_log_file(f"{initial_output}\n\n","full")

            if initial_output:
                open_ports = self.extract_ports(initial_output)
                os_details = self.extract_os_details(initial_output) 
                if os_details:
                    print(f"OS Name: {os_details[0]}, OS Version: {os_details[1]}")              
                    self.logs(f"first intial nmap identify OS Name: {os_details[0]}, OS Version: {os_details[1]}","b")
                # else:
                #     print("No OS guess found")

                next_line = 0
                correct_line = 0
                table = self.ui.portServicef
                next_line = table.rowCount()                
                for line in range(next_line):
                    item = table.item(line, 0)
                    if item is not None:
                        if item.text() != "":  # Changed from item.txt to item.text()
                            correct_line += 1

                if open_ports:   
                # print(f"{len(open_ports)} Open ports found:")
                    ports_only=[]
                    services_only=[]
                    for row_index, port_info in enumerate(open_ports):
                        if not self.is_any_cell_filled(self.ui.portServicef,port_info[0]):
                            for col_index, item in enumerate(port_info):
                                    self.add_item(self.ui.portServicef, correct_line, col_index, item) 
                            correct_line += 1     
                    for port_info in open_ports:
                        ports_only.append(port_info[0]) 
                    for port_info in open_ports:
                        services_only.append(port_info[1]) 
                    if not ports: 
                        self.logs(f"i found {len(open_ports)} ports open:","b")
                        formatp=",".join(ports_only)
                        self.logs(f"----{str(formatp)}","b")                  
                    self.logs(f"now i will run deep scan for each port","")
                    self.update() 
                    QApplication.processEvents()
                    time.sleep(5) 

                    self.save_log_file(temp_log_tosave,"app")
                    temp_log_tosave=""

                    self.run_nmap_detailed_per_port(resolved_ip, ports_only,open_ports)

                if not open_ports:
                    print("No open ports found.")
                    self.logs("i didn't found open ports","")
                    self.ui.running.setText("")
                    
        except KeyboardInterrupt:
            self.check_exit()
        
      

    def bring_them_home(self):
        subprocess.run(['wmctrl', '-a', 'NetworkScan'])
         
    def extract_domain(self,text):
        if text:
            match = re.search(r"Domain:\s*([^,\s]+)", text, re.IGNORECASE)
            if match:
                return match.group(1)
        else:
            return None

    def extract_dns_domain(self,text):
        if text:
            match = re.search(r"DNS_Domain_Name:\s*([^,\s]+)", text, re.IGNORECASE)
            if match:
                return match.group(1)
        else:
            return None
    def extract_dns_computer(self,text):
        if text:
            match = re.search(r"DNS_Computer_Name:\s*([^,\s]+)", text, re.IGNORECASE)
            if match:
                return match.group(1)
        else:
            return None


    def extract_nb_domain(self,text):
        if text:
        # Adjusted regular expression to handle variable spacing and ensure capture until end of line
            match = re.search(r"NetBIOS_Domain_Name:\s*([^\r\n]+)", text, re.IGNORECASE)
            if match:
                # Adding a strip to remove any trailing whitespace characters
                return match.group(1).strip()
        else:
            return None


    def extract_target_name(self,text):
        if text:
            match = re.search(r"Target_Name:\s*([^,\s]+)", text, re.IGNORECASE)
            if match:
                return match.group(1)
        else:
            return None


    def extract_computer_name(self,text):
        if text:
            match = re.search(r"Computer_Name:\s*([^,\s]+)", text, re.IGNORECASE)
            if match:
                return match.group(1)
        else:
            return None
  
    def extract_os_details(self, nmap_output):
        if nmap_output:
            # First, try to find the 'OS details' line
            os_details_pattern = r'OS details: (.*)'
            os_details_match = re.search(os_details_pattern, nmap_output)

            if os_details_match:
                os_details = os_details_match.group(1)
                # Regular expression to extract OS name and version
                match = re.search(r'([a-zA-Z ]+) (\d+(\.\d+)?( - \d+(\.\d+)?)?)', os_details)
                if match:
                    return [match.group(1).strip(), match.group(2).strip()]
            else:
                # If 'OS details' line isn't found or doesn't match, try 'Operating System' line
                os_details_pattern = r'Operating System: (.*)'
                os_details_match = re.search(os_details_pattern, nmap_output)

                if os_details_match:
                    os_details = os_details_match.group(1)
                    match = re.search(r'([a-zA-Z ]+) (\d+(\.\d+)?( - \d+(\.\d+)?)?)', os_details)
                    if match:
                        return [match.group(1).strip(), match.group(2).strip()]
                else:
                    # If 'Operating System' line isn't found, look for aggressive OS guesses
                    aggressive_guesses_pattern = r'Aggressive OS guesses: ([^,]+),'
                    aggressive_guesses_match = re.search(aggressive_guesses_pattern, nmap_output)

                    if aggressive_guesses_match:
                        first_guess = aggressive_guesses_match.group(1)
                        match = re.search(r'([a-zA-Z ]+) (\d+(\.\d+)?( - \d+(\.\d+)?)?)', first_guess)
                        if match:
                            return [match.group(1).strip(), match.group(2).strip()]
                    else:
                        # If no guesses found, check for a direct 'OS' line
                        os_pattern = r'OS: ([^;]+);'
                        os_match = re.search(os_pattern, nmap_output)
                        if os_match:
                            os_name = os_match.group(1).strip()
                            return [os_name, ""]  # The version is not specified directly in this case

        else:
            return None

    

    def add_item(self, widget, row, column, text):
        current_row_count = widget.rowCount()
        if row >= current_row_count:
            widget.setRowCount(row + 1)
        item = QtWidgets.QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignLeft)
        widget.setItem(row, column, item)

      
    def print_bold(self,msg, color_code):
        print(f"\033[{color_code}m{msg}\033[0m")
 
    def center_on_screen(self):
        # Get the geometry of the primary screen
        screen = QApplication.primaryScreen().geometry()
        center_x = int((screen.width() / 2) - (self.frameSize().width() / 2))
        center_y = int((screen.height() / 2) - (self.frameSize().height() / 2))
        self.move(center_x, center_y)   

    
    def run_nmap_initial(self, ip, ports_p, port_option):
        self.print_bold("Starting Initial Scan...", "1;34")
        ports = ','.join(port_option)
        
        # Base command - keep this exactly as it was originally
        cmd = ["nmap", "-Pn", "-O", "-sS","--min-rate", "3000"] + [ports_p] + [ports] + [ip]
        
        # Add additional tags from config without changing the base command
        additional_tags = self.config.get('nmap', {}).get('tags', []) if self.config else []
        if additional_tags:
            cmd.extend(additional_tags)
            self.logs(f"Adding additional nmap options from config: {' '.join(additional_tags)}", "")

        output = self.runinshell(cmd, timeout=9999, scanner="nmap", needs_sudo=True)
        if output:
            output = '\n'.join(output)
        return output
        
            
    def extract_ports(self, output):
        if output:
            fulls_ports = []
            port_info_list = []
            lines = output.split("\n")
            for line in lines:
                if "open" in line and not line.strip().startswith("Warning"):
                    match = re.search(r"(\d+)/tcp\s+open\s+(\S+)(?:\s+(.*))?", line)
                    fulls_ports.append(line)
                    if match:
                        port = match.group(1)
                        service = match.group(2)
                        version = match.group(3) if match.group(3) is not None else ''
                        port_info = [port, service, version]  # Use a list instead of a tuple
                        port_info_list.append(port_info)
            return port_info_list
        else:
            return None

        

    def resolve_to_ip(self,domain):
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            return domain  # Return the original if it's already an IP or couldn't be resolved

    
    def add_log(self,type,text):
        line_spacing = "100%" 
        if type == "b":
            pass
            self.ui.textEdit.append(f"<p style='line-height: {line_spacing};'><span style='font-size:15pt; color: red;'>{text}</span></p>")
        else:
            self.ui.textEdit.append(f"<p style='line-height: {line_spacing};'><span style='font-size:15pt; color: black;'>{text}</span></p>")
        self.update()
        QApplication.processEvents()
     
            
    def find_last_non_empty_row(self,table):
        last_non_empty_row = -1
        for row in range(table.rowCount()):
            row_has_data = False
            for column in range(table.columnCount()):
                item = table.item(row, column)
                if item and item.text().strip():
                    row_has_data = True
                    break
            if row_has_data:
                last_non_empty_row = row
        return last_non_empty_row


    def is_web_service(self,port, service):
        # List of common web service identifiers
        web_identifiers = ['http', 'https', 'web', 'www', '80', '443', '8080', '8000', '8081']
        # Check if the port or service description matches any of the web identifiers
        return service and any(web_id in service.lower() for web_id in web_identifiers) or str(port) in web_identifiers

    def run_nmap_detailed_per_port(self,ip, ports,full):
        global folderlogproject,file_app_log,file_full_nmap,temp_log_tosave,should_exit
        temp_log_tosave=""
        self.print_bold("Starting Detailed Scans...", "1;34")
      #  print(should_exit)
        if should_exit:
            return
        try:
        #  print(full)
            #self.update_text.emit("b","hey you")
            #detailed_outputs = []
            smb_related = ['smb', 'netbios-ssn', 'microsoft-ds', '139', '445','samba']
            rpc_related = ['rpcbind', '111','nfs','rpc','2049']
            ftp_r=['ftp','21']
            http_r=['80','http','httpd','https','443','8080','http-proxy']
            sip_r = ['sip']
            snmp_r = ['snmp', '161', '162']  
            xmpp_r = ['xmpp', 'jabber', '5222', '5223']  
            rdp_r = ['rdp', 'terminal services', 'ms-wbt-server', '3389']
            redis_r = ['redis', '6379']   
            sql_r = ['sql', 'mysql', '3306', '1433', '1521', 'postgres', 'postgresql', '5432']   
            smtp_r = ['smtp', '25', '587', '465']  
            mongodb_r = ['mongodb', 'mongo', '27017']  
            telnet_r = ['telnet', '23']   
            ad_r = ['active directory', '445', '3268', '3269','ldap', '389', '636','kerberos', '88', '464','domain','kpasswd5','globalcatLDAP','globalcatLDAPssl','ldapssl','kerberos-sec']
            ssh_r = ['ssh', '22']
            dns_r = ['dns', 'domain', '53']
            vnc_r = ['vnc', '5900', '5901', '5902', '5800']
            imap_r = ['imap', '143', '993']
            pop3_r = ['pop3', '110', '995']
            nntp_r = ['nntp', '119', '563']
            memcached_r = ['memcached', '11211']
            tftp_r = ['tftp', '69']
            irc_r = ['irc', '6667', '6697']
            rtsp_r = ['rtsp', '554']
            oracle_r = ['oracle', '1521', '1526']
            jdwp_r = ['jdwp', '8000']
            ipmi_r = ['ipmi', '623']
            afp_r = ['afp', 'apple-filing', '548']
            cassandra_r = ['cassandra', '9042', '9160']
            couchdb_r = ['couchdb', '5984']
            elasticsearch_r = ['elasticsearch', '9200', '9300']
            db2_r = ['db2', '50000']
            docker_r = ['docker', '2375', '2376']
            kubernetes_r = ['kubernetes', 'k8s', '6443', '8080', '10250']
            jenkins_r = ['jenkins', '8080']
            rabbitmq_r = ['rabbitmq', 'amqp', '5672', '15672']
            zookeeper_r = ['zookeeper', '2181']
            rsync_r = ['rsync', '873']
            git_r = ['git', '9418']
            hadoop_r = ['hadoop', '8020', '8088', '9000', '50070']    
            vmware_r = ['vmware', '902']
            zabbix_r = ['zabbix', '10050', '10051']
            nagios_r = ['nrpe', '5666']
            jmx_r = ['jmx', '1099']
            iot_r = ['iot', 'upnp', '1900', '5683', '1883', '8883']  # IoT, MQTT, CoAP
            api_r = ['api', 'rest', 'graphql', 'soap', 'grpc']
            nas_r = ['nas', 'storage', 'iscsi', '3260']
            ssl_r = ['ssl', 'tls', '443', '993', '995', '465']
            
            smbactive=False
            rpcactive=False
            ftpactive=False
            httpactive=False        
            countpo=0
            for port_loop in full:
                port, service, extra = port_loop
                copmuter=""
                domain=""
                os_item=""
                print(f"\033[35mScanning port {port}\033[0m")
                
                # Base nmap command (runinshell will handle sudo)
                cmd = ["nmap", "-sS", "-Pn", "-sC", "-A", "-sV", "--max-parallelism", "500", "-T4", "-p", port, ip]
                

                if service in smb_related or port in smb_related:
                    smbactive=True
                    cmd.extend(["--script=smb-enum-domains,smb-enum-shares,smb-enum-users,smb-ls,smb-os-discovery,smb-security-mode"])
                    cmd.extend(["--script=exploit"])
                    
                if service in rpc_related or port in rpc_related:
                    rpcactive=True
                    cmd.extend(["--script=nfs-ls,nfs-statfs,nfs-showmount"])
                    cmd.extend(["--script=exploit"])

                if service in ftp_r or port in ftp_r:
                    ftpactive=True
                    cmd.extend(["--script=ftp-anon.nse,ftp-libopie.nse"])
                    cmd.extend(["--script=exploit"])
                    
                if service in http_r or port in http_r:
                    httpactive=True
                    cmd.extend(["--script=http-headers.nse,http-methods.nse,http-sql-injection,http-barracuda-dir-traversal"])
                    cmd.extend(["--script=http-enum,http-title,http-server-header,http-robots.txt,http-cors,http-csrf,http-waf-detect"])
                    cmd.extend(["--script=exploit"])
                
                if service in ad_r or port in ad_r:
                    httpactive=True
                    cmd.extend(["--script=ldap-novell-getpass,ldap-rootdse,ldap-search,dns-srv-enum,krb5-enum-users"])
                    cmd.extend(["--script=exploit"])

                if service in rdp_r or port in rdp_r:
                    httpactive=True
                    cmd.extend(["--script=rdp-enum-encryption,rdp-ntlm-info"])
                    cmd.extend(["--script=exploit"])
    
                if service in sip_r or port in sip_r:
                    httpactive=True
                    cmd.extend(["--script=sip-call-spoof,sip-enum-users,sip-methods"])
                    cmd.extend(["--script=exploit"])

                if service in snmp_r or port in snmp_r:
                    httpactive=True
                    cmd.extend(["--script=snmp-hh3c-logins,snmp-info,snmp-interfaces,snmp-ios-config,snmp-win32-shares,snmp-win32-users"])
                    cmd.extend(["--script=exploit"])

                if service in telnet_r or port in telnet_r:
                    httpactive=True
                    cmd.extend(["--script=telnet-ntlm-info,telnet-encryption"])
                    cmd.extend(["--script=exploit"])

                if service in redis_r or port in redis_r:
                    httpactive=True
                    cmd.extend(["--script=redis-info"])
                    cmd.extend(["--script=exploit"])

                if service in xmpp_r or port in xmpp_r:
                    httpactive=True
                    cmd.extend(["--script=xmpp-info"])
                    cmd.extend(["--script=exploit"])

                if service in smtp_r or port in smtp_r:
                    httpactive=True
                    cmd.extend(["--script=smtp-commands,smtp-enum-users,smtp-ntlm-info,smtp-open-relay"])
                    cmd.extend(["--script=exploit"])

                if service in sql_r or port in sql_r:
                    httpactive=True
                    cmd.extend(["--script=mysql-audit,mysql-empty-password,mysql-info,mysql-query,mysql-variables,mysql-users"])
                    cmd.extend(["--script=ms-sql-config,ms-sql-dac,ms-sql-empty-password,ms-sql-info,ms-sql-ntlm-info,ms-sql-tables"])
                    cmd.extend(["--script=exploit"])
                
                if service in ssh_r or port in ssh_r:
                    httpactive=True
                    cmd.extend(["--script=ssh-auth-methods,ssh-hostkey,ssh-publickey-acceptance,ssh2-enum-algos,sshv1"])
                    cmd.extend(["--script=exploit"])

                if service in dns_r or port in dns_r:
                    httpactive=True
                    cmd.extend(["--script=dns-cache-snoop,dns-nsec-enum,dns-nsec3-enum,dns-nsid,dns-recursion,dns-service-discovery,dns-zone-transfer"])
                    cmd.extend(["--script=exploit"])

                if service in vnc_r or port in vnc_r:
                    httpactive=True
                    cmd.extend(["--script=realvnc-auth-bypass,vnc-info,vnc-title"])
                    cmd.extend(["--script=exploit"])

                if service in imap_r or port in imap_r:
                    httpactive=True
                    cmd.extend(["--script=imap-capabilities,imap-ntlm-info"])
                    cmd.extend(["--script=exploit"])

                if service in pop3_r or port in pop3_r:
                    httpactive=True
                    cmd.extend(["--script=pop3-capabilities,pop3-ntlm-info"])
                    cmd.extend(["--script=exploit"])

                if service in memcached_r or port in memcached_r:
                    httpactive=True
                    cmd.extend(["--script=memcached-info"])
                    cmd.extend(["--script=exploit"])

                if service in tftp_r or port in tftp_r:
                    httpactive=True
                    cmd.extend(["--script=tftp-enum"])
                    cmd.extend(["--script=exploit"])

                if service in irc_r or port in irc_r:
                    httpactive=True
                    cmd.extend(["--script=irc-info,irc-unrealircd-backdoor"])
                    cmd.extend(["--script=exploit"])

                if service in rtsp_r or port in rtsp_r:
                    httpactive=True
                    cmd.extend(["--script=rtsp-methods"])
                    cmd.extend(["--script=exploit"])

                if service in oracle_r or port in oracle_r:
                    httpactive=True
                    cmd.extend(["--script=oracle-enum-users,oracle-tns-version"])
                    cmd.extend(["--script=exploit"])

                if service in ipmi_r or port in ipmi_r:
                    httpactive=True
                    cmd.extend(["--script=ipmi-version,ipmi-cipher-zero"])
                    cmd.extend(["--script=exploit"])

                if service in afp_r or port in afp_r:
                    httpactive=True
                    cmd.extend(["--script=afp-ls,afp-serverinfo,afp-showmount"])
                    cmd.extend(["--script=exploit"])
                
                if service in mongodb_r or port in mongodb_r:
                    httpactive=True
                    cmd.extend(["--script=mongodb-databases,mongodb-info"])
                    cmd.extend(["--script=exploit"])
                
                if cassandra_r or port in cassandra_r:
                    httpactive=True
                    cmd.extend(["--script=cassandra-info"])
                    cmd.extend(["--script=exploit"])
                
                if service in couchdb_r or port in couchdb_r:
                    httpactive=True
                    cmd.extend(["--script=couchdb-databases,couchdb-stats"])
                    cmd.extend(["--script=exploit"])
                
                if service in elasticsearch_r or port in elasticsearch_r:
                    httpactive=True
                    cmd.extend(["--script=elasticsearch"])
                    cmd.extend(["--script=exploit"])
                
                if service in db2_r or port in db2_r:
                    httpactive=True
                    cmd.extend(["--script=db2-das-info,db2-discover"])
                    cmd.extend(["--script=exploit"])
                
                if service in docker_r or port in docker_r:
                    httpactive=True
                    cmd.extend(["--script=docker-registry-list-repositories"])
                    cmd.extend(["--script=exploit"])
                
                if service in kubernetes_r or port in kubernetes_r:
                    httpactive=True
                    cmd.extend(["--script=http-headers,ssl-cert"])
                    cmd.extend(["--script=exploit"])
                
                if service in jenkins_r or port in jenkins_r:
                    httpactive=True
                    cmd.extend(["--script=jenkins,jenkins-info"])
                    cmd.extend(["--script=exploit"])
                
                if service in rabbitmq_r or port in rabbitmq_r:
                    httpactive=True
                    cmd.extend(["--script=amqp-info"])
                    cmd.extend(["--script=exploit"])
                
                if service in zookeeper_r or port in zookeeper_r:
                    httpactive=True
                    cmd.extend(["--script=zookeeper-info"])
                    cmd.extend(["--script=exploit"])
                
                if service in rsync_r or port in rsync_r:
                    httpactive=True
                    cmd.extend(["--script=rsync-list-modules"])
                    cmd.extend(["--script=exploit"])
                
                if service in git_r or port in git_r:
                    httpactive=True
                    cmd.extend(["--script=git-info"])
                    cmd.extend(["--script=exploit"])
                
                if service in hadoop_r or port in hadoop_r:
                    httpactive=True
                    cmd.extend(["--script=hadoop-datanode-info,hadoop-jobtracker-info,hadoop-namenode-info,hadoop-secondary-namenode-info,hadoop-tasktracker-info"])
                    cmd.extend(["--script=exploit"])

                # New service types
                if service in ssl_r or port in ssl_r:
                    httpactive=True
                    cmd.extend(["--script=ssl-cert,ssl-enum-ciphers,ssl-heartbleed,ssl-dh-params,ssl-poodle"])
                    cmd.extend(["--script=exploit"])
                
                if service in iot_r or port in iot_r:
                    httpactive=True
                    cmd.extend(["--script=hnap-info,upnp-info,mqtt-subscribe"])
                    cmd.extend(["--script=exploit"])
                
                if service in api_r or port in api_r:
                    httpactive=True
                    cmd.extend(["--script=http-api-graphql,http-jsonp-detection,http-open-proxy"])
                    cmd.extend(["--script=exploit"])
                
                if service in nas_r or port in nas_r:
                    httpactive=True
                    cmd.extend(["--script=iscsi-info,nfs-showmount,nbd-info"])
                    cmd.extend(["--script=exploit"])
               
                result=self.runinshell(cmd,timeout=9999,scanner="nmap",needs_sudo=True)
                if result:
                    result='\n'.join(result)
                self.save_log_file(f"{result}\n","full")

                detail=self.extract_ports(result)
                if detail:
                    self.update_table_with_advanced_scan(detail)
            
                # noi=len(detail)
                # advan=detail[noi][1]
                # if self.is_web_service(port, service) or self.is_web_service(port,advan):                
                #         self.logs(f"port {port} is probably website","b")
            
                domain=self.extract_domain(result)
                computer=self.extract_computer_name(result)
                dnsdomain=self.extract_dns_domain(result)
                nbdomain=self.extract_nb_domain(result)
                dnscomputer=self.extract_dns_computer(result)
                targetn=self.extract_target_name(result)
                
                if targetn:
                    self.logs(f"on port {port} i got TARGET name: {targetn}","b")
                if nbdomain:
                    self.logs(f"on port {port} i got NETBIOS DOMAIN name: {nbdomain}","b")
                if dnsdomain:
                    self.logs(f"on port {port} i got DNS DOMAIN name: {dnsdomain}","b")

                if dnscomputer:
                    self.logs(f"on port {port} i got DNS COMPUTER name: {dnscomputer}","b")

                if domain and port!="3389" and port!=139 and port!= 445:
                    self.logs(f"on port {port} i got DOMAIN name: {domain}","b")

                # Initialize os_details before using it
                os_details = None
                if computer and port!="3389" and port!=139 and port!= 445:
                    self.logs(f"on port {port} i got COMPUTER name: {computer}","b")    
                    os_details = self.extract_os_details(result) 
                
                if os_details:
                    self.logs(f"on port {port} i got OS name: {os_details[0]} and OS version: {os_details[1]}","b")
                    print(f"OS Name: {os_details[0]}, OS Version: {os_details[1]}")
                # else:
                #     print("No OS guess found")
                
                if smbactive:
                    smbactive=False
                    smbd=self.extract_smb_oscomp(result)
                    # print(smbd)
                    # sys.exit(0)
                    if smbd:
                        os_info = smbd.get('OS_Info', {}) 
                        comp= os_info.get('Computer name', '')    
                        doma= os_info.get('Domain name', '')  
                        if comp:
                            self.logs(f"on port {port} i got Computer name: {comp}","b") 

                        if doma:
                            self.logs(f"on port {port} i got Domain name: {doma}","b") 

                    share_name=""
                    sharesi = self.smb_share(result,ip)
                    #    print(sharesi)
                    #  sys.exit(0)
                    if sharesi:
                        self.logs(f"found interesting files in SMB on port {port}:","b")
                        print (sharesi)
                        for share in sharesi:
                                share_name = share['Share Name']
                                comment = share.get('Comment', '')
                                path = share.get('Path', '')  # Check if 'Path' exists
                                access = share['Anonymous Access']   
                                self.logs(f"----share: {share_name}","b") 
                                self.logs(f"----path: {path}","b")
                                self.logs(f"----accss: {access}","b")
                                
                                
                if ftpactive:
                    ftpactive=False
                # last_row = self.find_last_non_empty_row(self.ui.ftptxt)
                # row=last_row+1
                    ftpd=self.parse_ftp_nmap_results(result)
                    print(ftpd)
                    if ftpd:           
                    #  self.ui.deepfindf.setCurrentIndex(0)
                        anon=ftpd['anonymous_login']
                        files=ftpd['files']
                        
                        if files:
                            self.logs("found interesting files in FTP:","b")
                            for f in files:
                                self.logs(f"----{str(f)}","b")
                
                if rpcactive: 
                    rpcactive=False
                    nfsd=self.parse_nfs_nmap_results(result)
                    if nfsd:
                        mount=nfsd['mount_shares']
                        files=nfsd['files']
                        if files:
                           self.logs("found interesting files in NFS","b")
                           for f in files:
                                self.logs(f"----{str(f)}","b")
                
                self.save_log_file(temp_log_tosave,"app")
                temp_log_tosave=""
                self.update() 
                QApplication.processEvents()
                time.sleep(5) 

            print("Done")
            self.logs("FINISHED nmap","") 
            print(f"full report of nmap save in file: {file_full_nmap}") 
            self.logs(f"full report of nmap save in file: {file_full_nmap}","") 
            self.save_log_file(temp_log_tosave,"app")
            temp_log_tosave=""
     
            self.ui.running.setText("")
            QApplication.processEvents()
            time.sleep(5)
            if result:
                result="\n".join(result)
                return result
            else:
                return None

        except KeyboardInterrupt:
            self.check_exit()

  
    def extract_smb_oscomp(self, nmap_output):
        os_info = {}
        # Adjusted pattern to match the output format
        os_pattern = r"\|\s*smb-os-discovery:\s*(.*?)\n\n"
        os_match = re.search(os_pattern, nmap_output, re.DOTALL)
        if os_match:
            os_details = os_match.group(1)
            # Adjusted pattern to match the output format for Computer name

            comp_name_match = re.search(r"\|\s*Computer name:\s*([^\r\n]+)", os_details)
            if comp_name_match:
                os_info['Computer name'] = comp_name_match.group(1).strip()
 
            # Adjusted pattern to match the output format for Domain name
            domain_name_match = re.search(r"\|\s*Domain name:\s*([^\\]+)", os_details)
            if domain_name_match:
                os_info['Domain name'] = domain_name_match.group(1).strip()

            # Return the structured data
            return {'OS_Info': os_info}
 
    def update_table_with_advanced_scan(self, advanced_results):
        for advanced_info in advanced_results:
            port, advanced_service, advanced_version = advanced_info
            row_to_update = self.find_row_by_port(port)

            if row_to_update is not None:
                self.update_table_cell(row_to_update, 2,advanced_service + " - " + advanced_version)
    def parse_ftp_nmap_results(self,nmap_output):
        if nmap_output:
            lines = nmap_output.split('\n')
            ftp_section = False
            files = []
            anon_login=""

            for line in lines:
                if 'ftp-anon:' in line:
                    ftp_section = True
                    anon_login = "Allowed" if "Anonymous FTP login allowed" in line else "Not Allowed"
                    continue

                av1 = ['/tcp','ftp-anon:','state']  
                if ftp_section:
                    if line.strip().startswith('|') and all(x not in line for x in av1):
                        parts = line.split()
                        print(parts)
                        
                        if parts[0] == '|':
                            permissions = parts[1]
                        else:
                            permissions = parts[0].lstrip('|_')
    

    
                        # Extract filename (assuming it's always the last part of the line)
                        filename = ' '.join(parts[-1:])
                        files.append({'permissions': permissions, 'filename': filename})

                    if line.startswith('|_'):
                            files_section = False

            return {
                "anonymous_login": anon_login,
                "files": files
            }
        else:
            return None
        
                
    def parse_nfs_nmap_results(self,nmap_output):
        if nmap_output:
            lines = nmap_output.split('\n')
            shares = set()  # Using a set to avoid duplicates
            files = []
            files_section = False  # Flag to indicate if we are in the file details section

            for line in lines:
                # Capture NFS mount share locations
                if line.strip().startswith('|_  /'):
                    share = line.strip('|_ ').split()[0]
                    shares.add(share)

                # Identify the start of the nfs-ls section
                if 'nfs-ls:' in line:
                    files_section = True

                # Process the file details section
                if files_section:
                    av1 = ['nfs-ls:','???', ' .', ' ..','PERMISSION','access:','|_']              
                    if line.strip().startswith('|') and all(x not in line for x in av1):
                            parts = line.split()
                          #  print (parts)
                            permission = parts[1]
                            uid = parts[2]
                            gid = parts[3]
                            filename = ' '.join(parts[6:])
                            files.append({
                                'permission': permission,
                                'uid': uid,
                                'gid': gid,
                                'filename': filename
                            })

                    # Break out of the loop if we reach the end of the NFS section
                    if line.startswith('|_'):
                        files_section = False

            return {
                "mount_shares": list(shares),
                "files": files
            }
        else:
            return None

  
    def smb_share(self, scan_result, ip_address):
        lines = scan_result.split('\n')
        smb_section = False
        shares = []
        share_info = {}


        # for line in lines:
        #     # Detect the start of the SMB share section
        #     if line.startswith('| smb-enum-shares:'):
        #         smb_section = True
        #         continue

        #     # Handle parsing within the SMB share section
        #     if smb_section:
        #         # Check for the end of the SMB section or individual share block
        #         if line.startswith('|_') or line.strip() == '|':
        #             smb_section = False
        #             if share_info:
        #                 shares.append(share_info)
        #                 share_info = None
        #             continue

        #         # Start parsing a new share that is not IPC$ or print$
        #         if line.strip().startswith('|   \\\\') and f'\\\\{ip_address}\\' in line:
        #             share_name = line.split('\\')[-1].split(':')[0].strip()
        #             # Skip unwanted shares
        #             if 'IPC$' in share_name or 'print$' in share_name:
        #                 share_info = None
        #             else:
        #                 if share_info:
        #                     shares.append(share_info)
        #                 share_info = {'Share Name': share_name}

        #         # Parse additional details of the share if it's being tracked
        #         if share_info:
        #             if 'Comment:' in line:
        #                 share_info['Comment'] = line.split('Comment:')[1].strip()
        #             elif 'Path:' in line:
        #                 share_info['Path'] = line.split('Path:')[1].strip()
        #             elif 'Anonymous access:' in line:
        #                 share_info['Anonymous Access'] = line.split('Anonymous access:')[1].strip()


        for line in lines:
            # if line.startswith('| smb-enum-shares:'):
            #     smb_section = True
            #     continue
            if line.startswith('|   \\\\') or line.startswith('|_'):
                # Before starting a new share or ending, save the current share if valid
                if share_info:
                    shares.append(share_info)
                    share_info = None

                if line.startswith('|_'):
                    smb_section = False
                    continue

            # Start parsing a new share that is not IPC$ or print$
            if line.startswith('|   \\\\') and f'\\\\{ip_address}\\' in line and 'IPC$' not in line and 'print$' not in line:
                share_name = line.split('\\')[-1].split(':')[0].strip()
                share_info = {'Share Name': share_name}  # Initialize a new share info dictionary

            # Collect additional details if currently processing a valid share
            if share_info:
                if 'Comment:' in line:
                    share_info['Comment'] = line.split('Comment:')[1].strip()
                elif 'Path:' in line:
                    share_info['Path'] = line.split('Path:')[1].strip()
                elif 'Anonymous access:' in line:
                    share_info['Anonymous Access'] = line.split('Anonymous access:')[1].strip()

                # if line.strip().startswith('|   \\\\') and f'\\\\{ip_address}\\' in line and 'IPC$' not in line and 'print$' not in line:
                #     if share_info:
                #         shares.append(share_info)
                #     share_name = line.split('\\')[-1].split(':')[0].strip()
                #     share_info = {'Share Name': share_name}
                #     if 'Comment:' in line and share_info:
                #         share_info['Comment'] = line.split('Comment:')[1].strip()
                #     elif 'Path:' in line and share_info:
                #         share_info['Path'] = line.split('Path:')[1].strip()
                #     elif 'Anonymous access:' in line and share_info:
                #         share_info['Anonymous Access'] = line.split('Anonymous access:')[1].strip()
                #     if line.startswith('|_'):
                #         smb_section = False
                #         if share_info:
                #             shares.append(share_info)
                #             share_info = {}

        return shares
    
 
    
    def smb_files(self,ip,scan_result, share_name):
        lines = scan_result.split('\n')
        files_section = False
        files = []
        found_files = False
        header_skipped = False
        start=f'| smb-ls: Volume \\\\{ip}\\{share_name}'

        for line in lines:
            if line.strip().startswith(start):
                files_section = True            
            if files_section:
                    if 'SIZE' not in line: 
                        if  not line.endswith(' .') and not line.endswith(' ..'):
                            if 'smb-ls:' not in line: 
                                if line !="|_":    
                                    found_files = True
                                    entry_name = line.split('  ')[-1].strip()
                                    entry_type = '<DIR>' if '<DIR>' in line else 'File'
                                    files.append({'Type': entry_type, 'Name': entry_name})
 
                    # Break out of the loop if we reach the end of the smb-ls section
                    if line.startswith('|_'):
                        break

        # If no files were found and we did enter the smb-ls section, return a message or handle accordingly
        if files_section and not found_files:
            return None

        return files

    def smb_security_mode(self,scan_result):
        lines = scan_result.split('\n')
        security_section = False
        security_info = {}

        for line in lines:
            # Check if we're in the smb-security-mode section
            if line.strip().startswith('| smb-security-mode:'):
                security_section = True
                continue

            # Once in the section, start parsing the specific elements
            if security_section:
                if 'account_used:' in line:
                    security_info['account_used'] = line.split('account_used:')[1].strip()
            if row_to_update is not None:
                self.update_table_cell(row_to_update, 2,advanced_service + " - " + advanced_version)
                
    def find_row_by_port(self, port):
        for row in range(self.ui.portServicef.rowCount()):
            if self.ui.portServicef.item(row, 0).text() == port:
                return row
        return None

    def update_table_cell(self, row, column, text):
        item = QtWidgets.QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignLeft)
        self.ui.portServicef.setItem(row, column, item)

    def init_config(self):
        """Initialize the application configuration from config.json or use defaults"""
        config = self.load_tool_config()
        
        # If config wasn't loaded, create a basic default configuration
        if not config:
            config = {
                "output_dir": "reports",
                "gobuster": {
                    "timeout": 60,
                    "wordlist": "/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt",
                    "extensions": "html,php,txt,js,rar,zip,asp,jsp,sql,xml,json,config,bak,cgi,log"
                },
                "nikto": {
                    "timeout": 60
                },
                "nmap": {
                    "tags": []
                },
                "sqlmap": {
                    "options": ["--batch", "--level=1", "--risk=1", "--threads=4"]
                },
                "dirsearch": {
                    "extensions": "html,php,txt,js,rar,zip,asp,jsp,sql,xml,json,config,bak,cgi,log",
                    "timeout": 120,
                    "wordlist": "/usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt"
                },
                "enum4linux": {
                    "timeout": 600,
                    "options": ["-a"]
                },
                "wpscan": {
                    "timeout": 600,
                    "options": ["--enumerate", "vp,vt,u,cb,m"]
                }
            }
            
        return config

    def has_sudo_privileges(self):
        """Check if sudo can be run without password"""
        try:
            result = subprocess.run(['sudo', '-n', 'true'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
            return result.returncode == 0
        except Exception:
            return False

    def reset_sudo_password(self):
        """Reset cached sudo password to force a new prompt"""
        self.sudo_password = None
        
    def ask_sudo_password(self):
        """Prompt user for sudo password via GUI input dialog"""
        pwd, ok = QtWidgets.QInputDialog.getText(
            self, "Sudo Password", "Enter sudo password:",
            QtWidgets.QLineEdit.EchoMode.Password)
        if ok and pwd.strip():  # Only accept non-empty passwords
            self.sudo_password = pwd
            return True
        elif ok and not pwd.strip():
            print("Empty password provided, aborting scan")
            self.logs("Empty sudo password provided. Scan aborted.", "b")
            self.ui.running.setText("Scan aborted - no password")
            return False
        else:
            print("Password dialog canceled, aborting scan")
            self.logs("Sudo password prompt canceled. Scan aborted.", "b")
            self.ui.running.setText("Scan aborted - canceled")
            return False

if __name__ == "__main__":
    title="EasyScanner"
    escape_sequence = f'\033]0;{title}\007'
    subprocess.run(f'echo "{escape_sequence}"', shell=True, check=True)   
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    exit_code = app.exec()
    app.processEvents()  # Process remaining events
    sys.exit(exit_code)
