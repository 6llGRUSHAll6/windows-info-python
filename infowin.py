import os
import platform
import datetime
import socket
import psutil
import requests
from screeninfo import get_monitors
import win32com.client
import winreg

def get_gradient_colors(start_rgb, end_rgb, steps):
    colors = []
    for i in range(steps):
        r = round(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / (steps - 1))
        g = round(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / (steps - 1))
        b = round(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / (steps - 1))
        colors.append(f"{r};{g};{b}")
    return colors
logo = r"""
__        __  ___   _   _ 
\ \      / / |_ _| | \ | |
 \ \ /\ / /   | |  |  \| |
  \ V  V /    | |  | |\  |
   \_/\_/    |___| |_| \_|"""

start_rgb = (0, 255, 255)
end_rgb = (100, 130, 255)
for line in logo.split('\n'):
    if len(line.strip()) == 0:
        continue
    colors = get_gradient_colors(start_rgb, end_rgb, len(line))
    colored_line = []
    for i, char in enumerate(line):
        r, g, b = colors[i].split(';')
        colored_line.append(f"\033[38;2;{r};{g};{b}m{char}")
    print(''.join(colored_line) + '\033[0m')
def get_uptime():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m"
def get_os_info():
    try:
        wmi = win32com.client.GetObject("winmgmts:")
        os_info = wmi.ExecQuery("SELECT Caption FROM Win32_OperatingSystem")[0]
        caption = os_info.Caption.strip()
        
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
        release_id = winreg.QueryValueEx(key, "DisplayVersion")[0]
        return caption, release_id
    except Exception as e:
        return platform.system(), "Unknown"
def get_memory():
    mem = psutil.virtual_memory()
    used = mem.used // (1024**2)
    total = mem.total // (1024**2)
    return f"{used}/{total} MB"
def get_cpu():
    try:
        wmi = win32com.client.GetObject("winmgmts:")
        cpus = wmi.ExecQuery("SELECT Name FROM Win32_Processor")
        return cpus[0].Name.strip()
    except:
        return platform.processor()
def get_gpu():
    try:
        wmi = win32com.client.GetObject("winmgmts:")
        gpus = wmi.ExecQuery("SELECT Name FROM Win32_VideoController")
        return gpus[0].Name.strip() if gpus else "Unknown"
    except:
        return "Unknown"
def get_ip():
    addrs = psutil.net_if_addrs()
    for interface in addrs.values():
        for addr in interface:
            if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                return addr.address
    return "Not Available"
def get_public_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=5).text
    except:
        return "Not Available"
def get_resolution():
    try:
        return f"{get_monitors()[0].width}x{get_monitors()[0].height}"
    except:
        return "Unknown"
uptime = get_uptime()
os_caption, release_id = get_os_info()  # Изменено здесь
memory = get_memory()
cpu = get_cpu()
gpu = get_gpu()
ipv4 = get_ip()
public_ip = get_public_ip()
resolution = get_resolution()
info = f"""
Uptime:     {uptime}
OS:         {os_caption} ({release_id})
Hostname:   {socket.gethostname()}
User:       {os.getlogin()}
Python:     {platform.python_version()}
IP:         {ipv4}
Public IP:  {public_ip}
CPU:        {cpu}
GPU:        {gpu}
RAM:        {memory}
Resolution: {resolution}
""" 
print(info)