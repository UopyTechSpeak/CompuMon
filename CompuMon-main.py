#                                                   ,----,                                                                                     #
#                                                 ,/   .`|                                                                                     #
#                                               ,`   .'  :                    ,---,      .--.--.                                          ,-.  #
#          ,--,          ,-.----.             ;    ;     /                  ,--.' |     /  /    '. ,-.----.                           ,--/ /|  #
#        ,'_ /|   ,---.  \    /  \          .'___,/    ,'                   |  |  :    |  :  /`. / \    /  \                        ,--. :/ |  #
#   .--. |  | :  '   ,'\ |   :    |         |    :     |                    :  :  :    ;  |  |--`  |   :    |                       :  : ' /   #
# ,'_ /| :  . | /   /   ||   | .\ :     .--,;    |.';  ;   ,---.     ,---.  :  |  |,--.|  :  ;_    |   | .\ :   ,---.     ,--.--.   |  '  /    #
# |  ' | |  . ..   ; ,. :.   : |: |   /_ ./|`----'  |  |  /     \   /     \ |  :  '   | \  \    `. .   : |: |  /     \   /       \  '  |  :    #
# |  | ' |  | |'   | |: :|   |  \ :, ' , ' :    '   :  ; /    /  | /    / ' |  |   /' :  `----.   \|   |  \ : /    /  | .--.  .-. | |  |   \   #
# :  | | :  ' ;'   | .; :|   : .  /___/ \: |    |   |  '.    ' / |.    ' /  '  :  | | |  __ \  \  ||   : .  |.    ' / |  \__\/: . . '  : |. \  #
# |  ; ' |  | '|   :    |:     |`-'.  \  ' |    '   :  |'   ;   /|'   ; :__ |  |  ' | : /  /`--'  /:     |`-''   ;   /|  ," .--.; | |  | ' \ \ #
# :  | : ;  ; | \   \  / :   : :    \  ;   :    ;   |.' '   |  / |'   | '.'||  :  :_:,''--'.     / :   : :   '   |  / | /  /  ,.  | '  : |--'  #
# '  :  `--'   \ `----'  |   | :     \  \  ;    '---'   |   :    ||   :    :|  | ,'      `--'---'  |   | :   |   :    |;  :   .'   \;  |,'     #
# :  ,      .-./         `---'.|      :  \  \            \   \  /  \   \  / `--''                  `---'.|    \   \  / |  ,     .-./'--'       #
#  `--`----'               `---`       \  ' ;             `----'    `----'                           `---`     `----'   `--`---'               #
#                                       `--`                                                                                                   #

import tkinter as tk
import tkinter.ttk as ttk
import platform
import psutil
import subprocess
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import wmi

# —————————————————————————Copyright Information——————————————————————————————————— #
# Kind reminder: Please keep the copyright information and do not delete this area! #
# Copyright (c) 2024 UopyTechSpeak                                                  #
# This project is developed by UopyTechSpeak                                        #
# Project Address: https://github.com/UopyTechSpeak/CompuMon                        #
# Open source license: Apache-2.0 license                                           #
# This project uses AI tools to fix bugs that developers cannot fix                 #
# ————————————————————————————————————————————————————————————————————————————————— #

# Obtain detailed CPU model
def get_cpu_model():
    system = platform.system()
    if system == "Windows":
        try:
            command = "wmic cpu get Name"
            result = subprocess.check_output(command, shell=True).decode("utf-8").strip().split("\n")[1]
            return result
        except Exception as e:
            print(e)
            return "Failed to obtain CPU model"
    elif system == "Linux":
        try:
            command = "cat /proc/cpuinfo | grep 'model name' | head -n 1"
            result = subprocess.check_output(command, shell=True).decode("utf-8").strip().split(":")[1].strip()
            return result
        except Exception as e:
            print(e)
            return "Failed to obtain CPU model"
    return "Unsupported operating system"


# Get memory frequency
def get_memory_frequency():
    system = platform.system()
    if system == "Linux":
        try:
            command = "cat /proc/meminfo | grep 'MemSpeed'"
            result = subprocess.check_output(command, shell=True).decode("utf-8").strip().split(":")[1].strip()
            return result + " MHz"
        except Exception as e:
            print(e)
            return "Failed to obtain memory frequency"
    return "The current operating system is temporarily unable to obtain the memory frequency"


def update_system_info():
    """Update system information display"""
    system_info_text.delete(1.0, tk.END)
    system_info_text.insert(tk.END, "operating system: {}\n".format(platform.system()))
    system_info_text.insert(tk.END, "system version: {}\n".format(platform.release()))
    system_info_text.insert(tk.END, "computer name: {}\n".format(platform.node()))
    system_info_text.insert(tk.END, "Detailed system information: {}\n".format(platform.platform()))
    system_info_text.insert(tk.END, "System Architecture: {}\n".format(platform.architecture()))


def update_cpu_info():
    """Update CPU information display"""
    cpu_info_text.delete(1.0, tk.END)
    cpu_info_text.insert(tk.END, "Number of CPU logical cores: {}\n".format(psutil.cpu_count(logical=True)))
    cpu_info_text.insert(tk.END, "Number of physical CPU cores: {}\n".format(psutil.cpu_count(logical=False)))
    cpu_info_text.insert(tk.END, "CPU model: {}\n".format(get_cpu_model()))
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_info_text.insert(tk.END, "Current CPU usage rate: {} %\n".format(cpu_percent))
    cpu_progress_bar["value"] = cpu_percent
    update_cpu_usage_data(cpu_percent)
    update_cpu_usage_chart()


def update_memory_info():
    """Update memory information display"""
    memory_info_text.delete(1.0, tk.END)
    memory = psutil.virtual_memory()
    memory_info_text.insert(tk.END, "total memory: {} GB\n".format(round(memory.total / (1024 ** 3), 2)))
    memory_info_text.insert(tk.END, "Used memory: {} GB\n".format(round(memory.used / (1024 ** 3), 2)))
    memory_info_text.insert(tk.END, "Memory usage rate: {} %\n".format(memory.percent))
    memory_info_text.insert(tk.END, "Memory frequency: {}\n".format(get_memory_frequency()))
    memory_progress_bar["value"] = memory.percent
    update_memory_usage_data(memory.percent)
    update_memory_usage_chart()


def update_disk_info():
    """Update disk information display"""
    disk_info_text.delete(1.0, tk.END)
    partitions = psutil.disk_partitions()
    for partition in partitions:
        disk_info_text.insert(tk.END, "Disk partition: {}\n".format(partition.device))
        disk_info_text.insert(tk.END, "file system type: {}\n".format(partition.fstype))
        disk_usage = psutil.disk_usage(partition.mountpoint)
        disk_info_text.insert(tk.END, "Total capacity: {} GB\n".format(round(disk_usage.total / (1024 ** 3), 2)))
        disk_info_text.insert(tk.END, "Used capacity: {} GB\n".format(round(disk_usage.used / (1024 ** 3), 2)))
        disk_info_text.insert(tk.END, "Disk utilization rate: {} %\n".format(disk_usage.percent))


def update_running_processes():
    processes_text.delete(1.0, tk.END)
    for proc in psutil.process_iter():
        try:
            process_info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent'])
            processes_text.insert(tk.END, "PID: {} - Name: {} - CPU Usage: {}%\n".format(
                process_info['pid'], process_info['name'], process_info['cpu_percent']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass


def update_graphics_card_info():
    graphics_info_text.delete(1.0, tk.END)
    try:
        w = wmi.WMI(namespace="root\\CIMV2")
        for gpu in w.Win32_VideoController():
            graphics_info_text.insert(tk.END, "Graphics card name: {}\n".format(gpu.Name))
            graphics_info_text.insert(tk.END, "Graphics card driver version: {}\n".format(gpu.DriverVersion))
            graphics_info_text.insert(tk.END, "memory size: {} MB\n".format(int(gpu.AdapterRAM/1024/1024)))
    except Exception as e:
        print(e)
        graphics_info_text.insert(tk.END, "Failed to obtain graphics card information\n")


def update_all_info():
    update_system_info()
    update_cpu_info()
    update_memory_info()
    update_disk_info()
    update_running_processes()
    update_graphics_card_info()
    root.after(1000, update_all_info)


# Used to store CPU usage data
cpu_usage_data = []


def update_cpu_usage_data(cpu_percent):
    cpu_usage_data.append(cpu_percent)
    if len(cpu_usage_data) > 60:  # Only retain data from the last 60 seconds
        cpu_usage_data.pop(0)


# Define canvas_cpu as a global variable
canvas_cpu = None


def update_cpu_usage_chart():
    global canvas_cpu
    fig_cpu = plt.Figure(figsize=(4, 3), dpi=100)
    ax_cpu = fig_cpu.add_subplot(111)
    ax_cpu.clear()
    ax_cpu.plot(cpu_usage_data, label='CPU Usage')
    ax_cpu.set_xlabel('Time (s)')
    ax_cpu.set_ylabel('CPU Usage (%)')
    ax_cpu.set_title('CPU Usage Over Time')
    ax_cpu.legend()
    if canvas_cpu:
        canvas_cpu.get_tk_widget().destroy()
    canvas_cpu = FigureCanvasTkAgg(fig_cpu, master=root)
    canvas_cpu.draw()
    canvas_cpu.get_tk_widget().grid(row=5, column=1, sticky=tk.N + tk.S + tk.E + tk.W)


# Used to store memory usage data
memory_usage_data = []


def update_memory_usage_data(memory_percent):
    memory_usage_data.append(memory_percent)
    if len(memory_usage_data) > 60:  # Only retain data from the last 60 seconds
        memory_usage_data.pop(0)


def update_memory_usage_chart():
    global canvas_memory
    fig_memory = plt.Figure(figsize=(4, 3), dpi=100)
    ax_memory = fig_memory.add_subplot(111)
    ax_memory.clear()
    ax_memory.plot(memory_usage_data, label='Memory Usage')
    ax_memory.set_xlabel('Time (s)')
    ax_memory.set_ylabel('Memory Usage (%)')
    ax_memory.set_title('Memory Usage Over Time')
    ax_memory.legend()
    if canvas_memory:
        canvas_memory.get_tk_widget().destroy()
    canvas_memory = FigureCanvasTkAgg(fig_memory, master=root)
    canvas_memory.draw()
    canvas_memory.get_tk_widget().grid(row=5, column=2, sticky=tk.N + tk.S + tk.E + tk.W)


root = tk.Tk()
root.title("Computer dynamic hardware monitoring dashboard")

# Configure the weights of rows and columns to enable components to automatically resize
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)
root.grid_columnconfigure(2, weight=3)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=3)

# System information display area
system_info_label = tk.Label(root, text="system information")
system_info_label.grid(row=0, column=0, sticky=tk.W)
system_info_text = tk.Text(root, height=5, width=40)
system_info_text.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

# CPU information display area
cpu_info_label = tk.Label(root, text="CPU information")
cpu_info_label.grid(row=0, column=1, sticky=tk.W)
cpu_info_text = tk.Text(root, height=5, width=40)
cpu_info_text.grid(row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)
cpu_progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
cpu_progress_bar.grid(row=2, column=1, sticky=tk.E + tk.W)

# Memory information display area
memory_info_label = tk.Label(root, text="Memory Information")
memory_info_label.grid(row=0, column=2, sticky=tk.W)
memory_info_text = tk.Text(root, height=5, width=40)
memory_info_text.grid(row=1, column=2, sticky=tk.N + tk.S + tk.E + tk.W)
memory_progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
memory_progress_bar.grid(row=2, column=2, sticky=tk.E + tk.W)

# Disk information display area
disk_info_label = tk.Label(root, text="Disk Information")
disk_info_label.grid(row=3, column=0, sticky=tk.W)
disk_info_text = tk.Text(root, height=6, width=40)
disk_info_text.grid(row=4, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

# Display area for process information during operation
processes_label = tk.Label(root, text="Running processes")
processes_label.grid(row=3, column=1, sticky=tk.W)
processes_text = tk.Text(root, height=6, width=40)
processes_text.grid(row=4, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

# Graphics card information display area
graphics_info_label = tk.Label(root, text="Graphics card information")
graphics_info_label.grid(row=3, column=2, sticky=tk.W)
graphics_info_text = tk.Text(root, height=6, width=40)
graphics_info_text.grid(row=4, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

# CPU Usage Chart Area
fig_cpu = plt.Figure(figsize=(4, 3), dpi=100)
ax_cpu = fig_cpu.add_subplot(111)
canvas_cpu = FigureCanvasTkAgg(fig_cpu, master=root)
canvas_cpu.draw()
canvas_cpu.get_tk_widget().grid(row=5, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

# Memory Usage Chart Area
fig_memory = plt.Figure(figsize=(4, 3), dpi=100)
ax_memory = fig_memory.add_subplot(111)
canvas_memory = FigureCanvasTkAgg(fig_memory, master=root)
canvas_memory.draw()
canvas_memory.get_tk_widget().grid(row=5, column=2, sticky=tk.N + tk.S + tk.E + tk.W)

update_all_info()
root.mainloop()
