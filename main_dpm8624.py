import serial
import time,re,sys
import commands
import dpm8624

##------------------------------------<< main >>---------------------------------------------------------------------###

power_bench = dpm8624.DPM8624()

print(f"Device Temperature: {power_bench.read_temperature()} °C.")
print(f"Set the Device Output voltage: {power_bench.set_voltage(7.0)}")
print(f"Set the output current to: {power_bench.set_current(0.5)}")

power_bench.read_output_status()

settings = power_bench.read_all_settings()
print("-"*30)
print("\033[0;33m" + f"Starting with the following settings:")
print("\033[0;33m" + f"Voltage: {settings[1]} V")
print("\033[0;33m" + f"Current: {settings[2]} A")
print("\033[0;33m" + f"Mode   : {settings[3]}")
print("-"*30)
power_bench.enable_output()

for i in range(10):
    print(power_bench.read_current_measurement()," | ",power_bench.read_voltage_measurement()," | ",power_bench.read_cc_cv_mode())
    time.sleep(1)

power_bench.disable_output()

del power_bench
