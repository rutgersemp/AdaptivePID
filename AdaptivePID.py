# Adaptive PID - Change hotend PID (M301) depending on material cooling fan (M106)
# Should theoretically allow for more dynamic use of fan during print, as hotend temperatures can anticipate changes

# Author:
# Rutger Semp

# Changelog:
# 13-05-2020 - 0.01
# . initial
#
# 13-05-2020 - 0.02
# . Added option to specify what PWM was used in testing
# .. fixed bug that prepended PID settings to total layer rather than directly before M106 command
# ... Added support for M107 as well

# ----

## Uses -
## M220 S<factor in percent> - set speed factor override percentage
## M221 S<factor in percent> - set flow factor override percentage
## M221 S<factor in percent> T<0-#toolheads> - set flow factor override percentage for single extruder
## M104 S<temp> T<0-#toolheads> - set extruder <T> to target temperature <S>
## M140 S<temp> - set bed target temperature
## M106 S<PWM> - set fan speed to target speed <S>
## M605/606 to save and recall material settings on the UM2

from ..Script import Script
import io
#from plugins.PostProcessingPlugin.Script import Script
#from UM.Logger import Logger

class AdaptivePID(Script):
    version = "0.02"
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name":"Adaptive PID """ + self.version + """ (Experimental)",
            "key":"AdaptivePID",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "PWM_max":
                {
                    "label": "Max. PWM",
                    "description": "Fan PWM at which PID was tuned",
                    "type": "int",
                    "defaut_value": 255,
                    "minimum_value": "1",
                    "minimum_value_warning": "20",
                    "maximum_value_warning": "255"
                },

                "PID_start_P":
                {
                    "label": "Kp at 0",
                    "description": "Kp value when fan is not running",
                    "type": "float"
                },

                "PID_start_I":
                {
                    "label": "Ki at 0",
                    "description": "Ki value when fan is not running",
                    "type": "float"
                },

                "PID_start_D":
                {
                    "label": "Kd at 0",
                    "description": "Kd value when fan is not running",
                    "type": "float"
                },

                "PID_end_P":
                {
                    "label": "Kp at 255",
                    "description": "Kp value when fan is at max PWM",
                    "type": "float"
                },

                "PID_end_I":
                {
                    "label": "Ki at 255",
                    "description": "Ki value when fan is at max PWM",
                    "type": "float"
                },

                "PID_end_D":
                {
                    "label": "Kd at 255",
                    "description": "Kd value when fan is at max PWM",
                    "type": "float"
                }
            }
        }"""


    def execute(self, data):
        PWM_max = self.getSettingValueByKey("PWM_max")

        startP = self.getSettingValueByKey("PID_start_P")
        startI = self.getSettingValueByKey("PID_start_I")
        startD = self.getSettingValueByKey("PID_start_D")

        endP = self.getSettingValueByKey("PID_end_P")
        endI = self.getSettingValueByKey("PID_end_I")
        endD = self.getSettingValueByKey("PID_end_D")

        for idx, layer in enumerate(data): # each layer is a single string of G/M codes
            splitlayer = layer.split('\n') # turn layer into list

            newlayer = "" # set up a blank layer
            for command in splitlayer:
                cmdval = self.getValue(command, 'M')
                if cmdval == 106 or cmdval == 107:
                    if cmdval == 106:
                        pwm = self.getValue(command, 'S') # get the PWM value

                    elif cmdval == 107:
                        pwm = 0 # 107 means kill fans, meaning PWM = 0

                    if 0 <= pwm <= 255: #safety check so we don't set insane PID factors
                        P = (pwm * ((endP - startP) / PWM_max)) + startP
                        I = (pwm * ((endI - startI) / PWM_max)) + startI
                        D = (pwm * ((endD - startD) / PWM_max)) + startD

                        entry = ";TYPE:CUSTOM\n"
                        entry += "; -- Adjusting hotend PID in anticipation of change in material cooling (M106)\n"
                        entry += "M301 E0 P{P:.2f} I{I:.2f} D{D:.2f} ; -- for fan PWM of {pwm:d}\n".format(P=P,I=I,D=D,pwm=pwm) #ugh, why no f-strings? it's 2020!!!!
                        entry += command

                else:
                    entry = command

                newlayer += entry + "\n"

            data[idx] = newlayer

        return data