import ast
import threading
import tkinter as tk
from tkinter import ttk
from arp_spoofer import arp_spoofer

import nmap.nmapper as nmap


class Main_Screen:
    def __init__(self):
        self.window = tk.Tk()
        self.window.grid_propagate(False)
        self.host_frame = tk.LabelFrame(self.window, width=256, height=312, text='Host selection')
        self.info_frame = tk.LabelFrame(self.window, width=256, height=312, text='Host information')
        self.center_grid_frames()
        self.host_box = tk.Listbox(self.host_frame)
        self.host_box.grid(row=2, column=0)
        self.host_box.bind('<<ListboxSelect>>', self.onselect)
        self.start_button = tk.Button(self.host_frame, text="Detect network \n devices",
                                      command=self.start_get_hosts_thread)
        self.start_button.grid(row=0, column=0)
        self.host_box_label = tk.Label(self.host_frame, text="Detected Hosts")
        self.host_box_label.grid(row=1, column=0)
        self.progressbar = ttk.Progressbar(self.host_frame, mode='indeterminate')
        self.progressbar.grid(row=5, column=0, sticky='n', ipady=3, ipadx=10, pady=20)
        self.progress_label = tk.Label(self.host_frame, text='')
        self.progress_label.config(font=("Arial", 11))
        self.progress_label.grid()
        self.window.geometry("563x453")
        # self.create_entry_label_pairs(self.info_frame, 'ip', 'os', 'type')  //OPTIONAL CLEAN PAIR GENERATION

        self.host_ip_entry_label = tk.Label(self.info_frame, text='Host IP:')  # creating IP entry/label pair
        self.host_ip_entry_label.grid()
        self.host_ip_entry = tk.Entry(self.info_frame)
        self.host_ip_entry.grid()
        self.set_entry_text(self.host_ip_entry, "192.168.1.15") # testing purposes
        self.host_ip_entry.config(state='disabled')

        self.host_os_entry_label = tk.Label(self.info_frame, text='Host OS:')  # creating OS entry/label pair
        self.host_os_entry_label.grid()
        self.host_os_entry = tk.Entry(self.info_frame)
        self.host_os_entry.grid()
        self.host_os_entry.config(state='disabled')

        self.host_type_entry_label = tk.Label(self.info_frame, text='Host TYPE:')  # creating TYPE entry/label pair
        self.host_type_entry_label.grid()
        self.host_type_entry = tk.Entry(self.info_frame)
        self.host_type_entry.grid()
        self.host_type_entry.config(state='disabled')
        mock_attack = ['spoof', 'sniffer']

        self.attack_label = tk.Label(self.info_frame, text='Choose an attack:')
        self.attack_label.grid()
        self.attack_combobox = ttk.Combobox(self.info_frame, value=mock_attack)  # creating the attack combobox
        self.attack_combobox.grid()

        self.arp_spoof_button = tk.Button(self.info_frame, text="Start ARP \n spoofer", # creating the spoof button
                                          command=self.start_arp_spoof_thread)
        self.arp_spoof_button.grid(pady=30) # for testing purposes, should be disabled

        self.arp_spoof_stop_button = tk.Button(self.info_frame, text="Stop ARP \n spoofer",  # creating the spoof button
                                          state='disabled')
        self.arp_spoof_stop_button.grid(pady=30)  # for testing purposes, should be disabled

        self.window.mainloop() # start Main GUI loop
    # def create_entry_label_pairs(self, frame, *fields):
    #     tk.Label(frame, text='').grid()
    #
    #     for field in fields:
    #         globals()['host_' + field + '_entry_label'] = tk.Label(frame, text=f'Host {field.upper()}:')
    #         globals()['host_' + field + '_entry_label'].grid()
    #         globals()['host_' + field + '_entry'] = tk.Entry(frame)
    #         globals()['host_' + field + '_entry'].grid()

    def onselect(self, evt):
        w = evt.widget

        index = int(w.curselection()[0])
        value = w.get(index)
        dict_value = ast.literal_eval(value)  # transforming the listbox string to a dictionary

        self.host_ip_entry.config(state='normal')
        self.set_entry_text(self.host_ip_entry, dict_value["ip"])
        self.host_ip_entry.config(state='disabled')

        self.host_os_entry.config(state='normal')
        self.set_entry_text(self.host_os_entry, dict_value["os"])
        self.host_os_entry.config(state='disabled')

        self.host_type_entry.config(state='normal')
        self.set_entry_text(self.host_type_entry, dict_value["type"])
        self.host_type_entry.config(state='disabled')

    def set_entry_text(self, entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)

    def center_grid_frames(self):
        self.host_frame.grid(row=0, column=0, sticky="nesw")
        self.host_frame.grid_rowconfigure(0, weigh=1)
        self.host_frame.grid_columnconfigure(0, weigh=1)
        self.info_frame.grid(row=0, column=1, sticky="nesw")
        # self.info_frame.grid_rowconfigure(0, weigh=1)
        self.info_frame.grid_columnconfigure(0, weigh=1)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_propagate(False)
        self.host_frame.grid_propagate(False)

    def get_hosts(self):
        self.host_box.delete(0, 'end')
        self.progress_label.configure(text='Searching for hosts...')
        [self.host_box.insert('end', x) for x in nmap.discover_hosts()]
        self.progress_label.config(text='Hosts found')

    def arp_spoof(self):
        print(self.host_ip_entry.get())
        arp_spoofer.main(self.host_ip_entry.get())


    # unique thread starter?
    def start_get_hosts_thread(self):
        global get_hosts_thread
        get_hosts_thread = threading.Thread(target=self.get_hosts)
        get_hosts_thread.daemon = True
        self.progressbar.start()
        get_hosts_thread.start()
        self.window.after(20, self.check_get_host_thread)

    def start_arp_spoof_thread(self):
        global arp_spoof_thread
        arp_spoof_thread = threading.Thread(target=self.arp_spoof)
        arp_spoof_thread.daemon = True
        arp_spoof_thread.start()
        self.arp_spoof_stop_button.configure(state='active')
        self.arp_spoof_button.configure(state='disabled')



    # unique thread checker?
    def check_get_host_thread(self):
        if get_hosts_thread.is_alive():
            self.window.after(20, self.check_get_host_thread)
        else:
            self.progressbar.stop()
            #self.arp_spoof_button.grid(pady=30) # do this in the final version
            self.progressbar.grid_forget()

if __name__ == '__main__':
    app = Main_Screen()
