import serial
import time,re,sys
import commands

class DPM8624:
    def __init__(self):
        try:
            self.ser = serial.Serial('/dev/ttyUSB0')
            print(self.ser.name)
            print("")
        except:
            print("Can not open Serial interface")
            sys.exit()
    def __del__(self):
        self.ser.close()

    def set_voltage(self,voltage):
        #set the new voltage limit
        voltage = int(voltage * 100)
        cmd = (commands.SET_VOLTAGE + str(voltage) + ",,\n").encode()
        self.ser.write(cmd)
        return self.clean_output(self.ser.readline().decode(),[":01","\r\n"])

    def set_current(self,current):
        #set the new current limit
        current_milliampere = int(current * 1000)
        cmd = (commands.SET_CURRENT + str(current_milliampere) + ",,\n").encode()
        self.ser.write(cmd)
        return self.clean_output(self.ser.readline().decode(),[":01","\r\n"])

    def set_power_output(self,voltage,current):
        voltage_mv = int(voltage*100)
        current_ma = int(current*1000)
        cmd = (commands.SET_POWER_OUTPUT + str(voltage_mv) + "," + str(current_ma) + ",\n").encode()
        self.ser.write(cmd)
        return self.clean_output(self.ser.readline().decode(),[":01","\r\n"])

    def enable_output(self):
        cmd = commands.ENABLE_OUTPUT.encode()
        self.ser.write(cmd)
        return self.clean_output(self.ser.readline().decode(), [":01", "\r\n"])

    def disable_output(self):
        cmd = commands.DISABLE_OUTPUT.encode()
        self.ser.write(cmd)
        return self.clean_output(self.ser.readline().decode(), [":01", "\r\n"])

    def read_temperature(self):
        cmd = commands.READ_TEMPERATURE.encode()
        self.ser.write(cmd)
        return int(self.clean_output(self.ser.readline().decode(), [":01r33=",".\r\n"]))

    def read_maximum_voltage(self):
        cmd = commands.READ_MAXIMUM_VOLTAGE.encode()
        self.ser.write(cmd)
        return self.clean_output(self.ser.readline().decode(), [":01r00=", ".\r\n"])

    def read_maximum_current(self):
        cmd = commands.READ_MAXIMUM_CURRENT.encode()
        self.ser.write(cmd)
        return self.clean_output(self.ser.readline().decode(), [":01r01=", ".\r\n"])

    def read_voltage_setting(self):
        cmd = commands.READ_VOLTAGE_SETTING.encode()
        self.ser.write(cmd)
        return int(self.clean_output(self.ser.readline().decode(), [":01r10=", ".\r\n"])) * 0.01

    def read_current_setting(self):
        cmd = commands.READ_CURRENT_SETTING.encode()
        self.ser.write(cmd)
        return int(self.clean_output(self.ser.readline().decode(), [":01r11=", ".\r\n"])) * 0.001

    def read_output_status(self):
        cmd = commands.READ_OUTPUT_STATUS.encode()
        self.ser.write(cmd)
        ret = self.clean_output(self.ser.readline().decode(), [":01r12=", ".\r\n"])
        if ret == 0:
            return "OFF"
        elif ret == 1:
            return "ON"

    def read_voltage_measurement(self):
        cmd = commands.READ_VOLTAGE_MEASUREMENT.encode()
        self.ser.write(cmd)
        voltage_v = int(self.clean_output(self.ser.readline().decode(), [":01r30=", ".\r\n"]))*0.01
        return round(voltage_v,3)

    def read_current_measurement(self):
        cmd = commands.READ_OUTPUT_CURRENT.encode()
        self.ser.write(cmd)
        current_a = int(self.clean_output(self.ser.readline().decode(),[":01r31=",",",".\r\n"])) * 0.001
        return round(current_a,3)

    def read_cc_cv_mode(self):
        cmd = commands.READ_CC_CV_MODE.encode()
        self.ser.write(cmd)
        ret = int(self.clean_output(self.ser.readline().decode(), [":01r32=", ",", ".\r\n"]))
        if ret == 0:
            return "CV-Mode"
        elif ret == 1:
            return "CC_Mode"

    def clean_output(self,input_string,substrings):
        for _ in substrings:
            input_string = input_string.replace(_,"")
        output_string = input_string
        return output_string

    def read_all_settings(self):
        temp = self.read_temperature()
        voltage = self.read_voltage_setting()
        current = self.read_current_setting()
        mode = self.read_cc_cv_mode()
        return temp,voltage,current,mode