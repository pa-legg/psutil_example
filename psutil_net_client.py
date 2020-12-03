import socket
import psutil
import datetime
import time
import json
import pprint
import pickle

all_data = []
pp = pprint.PrettyPrinter(indent=4)
out_file = str(datetime.datetime.now())
out_file = out_file.replace('-','').replace(':','').split('.')[0].replace(' ','_')
out_file = out_file + '.json'
print(out_file)
show_output = False

def get_data():
    entry = {}
    entry['dt'] = str(datetime.datetime.now())
    entry['boot_dt'] = str(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))
    entry['cpu'] = psutil.cpu_times()
    entry['cpu_percent'] = psutil.cpu_percent()
    entry['network'] = psutil.net_io_counters(pernic=True)
    entry['network_conns'] = psutil.net_connections()
    entry['disk_io_counters'] = psutil.disk_io_counters(perdisk=True)
    entry['memory'] = psutil.virtual_memory()
    entry['swap'] = psutil.swap_memory()
    entry['processes_info'] = []

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
            entry['processes_info'].append(pinfo)
        except psutil.NoSuchProcess:
            pass
        
    if show_output:
        pp.pprint(entry)
        print ("\n")
    all_data.append(entry)

def get_single_data():
    entry = {}
    entry['dt'] = str(datetime.datetime.now())
    entry['machine'] = 'machine1'
    entry['boot_dt'] = str(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))
    entry['cpu'] = psutil.cpu_times()
    entry['cpu_percent'] = psutil.cpu_percent()
    entry['network'] = psutil.net_io_counters(pernic=True)
    entry['network_conns'] = psutil.net_connections()
    entry['disk_io_counters'] = psutil.disk_io_counters(perdisk=True)
    entry['memory'] = psutil.virtual_memory()
    entry['swap'] = psutil.swap_memory()
    entry['processes_info'] = []

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
            entry['processes_info'].append(pinfo)
        except psutil.NoSuchProcess:
            pass
        
    if show_output:
        pp.pprint(entry)
        print ("\n")
    return entry

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 12346)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)





while(True):
    try:
        # Send data
        print ("Get data...")
        data=pickle.dumps( get_single_data() )
        print ("Send data...")
        sock.send(data)
        print ("Wait...")
        time.sleep(5)
    finally:
        pass

sock.close()