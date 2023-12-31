
#Write
SET_VOLTAGE =":01w10="
SET_CURRENT = ":01w11="
SET_POWER_OUTPUT = ":01w20="
ENABLE_OUTPUT = ":01w12=1,,\n"
DISABLE_OUTPUT = ":01w12=0,,\n"

#Read
READ_TEMPERATURE = ":01r33=0,,\n"
READ_MAXIMUM_VOLTAGE = ":01r00=0,,\n"
READ_MAXIMUM_CURRENT = ":01r01=0,,\n"
READ_VOLTAGE_SETTING = ":01r10=0,,\n"
READ_CURRENT_SETTING = ":01r11=0,,\n"
READ_OUTPUT_STATUS = ":01r12=0,,\n"
READ_VOLTAGE_MEASUREMENT = ":01r30=0,,\n"
READ_OUTPUT_CURRENT = ":01r31=0,,\n"
READ_CC_CV_MODE = ":01r32=0,,\n"
