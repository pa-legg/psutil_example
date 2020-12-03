import psutil
import datetime
import time
import json
import pprint

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
    
while(True):
    get_data()
    with open(out_file, 'w') as fd:
        json.dump(all_data, fd, sort_keys=True, indent=4)