import serial
import time,re,sys
import commands
import dpm8624
import yaml
import csv
from datetime import datetime
##------------------------------------<< main >>---------------------------------------------------------------------###
power_bench = dpm8624.DPM8624()
with open("li-ion-profile.yaml","r") as file:
    charging_profile = yaml.safe_load(file)

logfilename = datetime.now().isoformat() + ".csv"
f = open(logfilename,"w")
csvwriter = csv.writer(f)
csvwriter.writerow(["charging_voltage","charging_current","charging_mode","timestamp"])

power_bench.set_voltage(charging_profile['profile']['max_voltage'])
power_bench.set_current(charging_profile['profile']['max_current'])

settings = power_bench.read_all_settings()

print("-"*30)
print("\033[0;33m" + f"Starting with the following settings:")
print("\033[0;33m" + f"Voltage: {settings[1]} V")
print("\033[0;33m" + f"Current: {settings[2]} A")
print("\033[0;33m" + f"Mode   : {settings[3]}")
print("-"*30)

power_bench.enable_output()
time.sleep(2)
print("\033[0;31m" + f"Start Charging")
print("\033[0;32m")
start_time = time.time()
current_time = 0
try:
    while current_time <= start_time + charging_profile['profile']['max_charging_time']:
        current_time = time.time()
        current = power_bench.read_current_measurement()
        voltage = power_bench.read_voltage_measurement()
        mode = power_bench.read_cc_cv_mode()
        remaining_time = charging_profile['profile']['max_charging_time'] - (time.time()-start_time)
        print(voltage," | ",current," | ",mode," | ",remaining_time)
        run_time = time.time()-start_time
        csvwriter.writerow([voltage,current,mode,run_time])

        if mode == "CV-Mode":
            if current <= charging_profile['profile']['max_current'] * charging_profile['profile']['shutoff_threshold']:
                power_bench.disable_output()
                print("Charging is done")
                charging_time = time.time() - start_time
                print(f"The charging took {charging_time} seconds.")
                break
        time.sleep(2)

    power_bench.disable_output()
    del power_bench
    f.close()
except KeyboardInterrupt:
    power_bench.disable_output()
    del power_bench
    f.close()
finally:
    f.close()
    sys.exit()