# AdaptivePID
## Adaptive PID G-code postprocessor plugin for Cura

Postprocessing script that looks at changes to material cooling fan (M106, M107) and adjusts hotend PID settings according to it.

Requires user to autotune PID (M303) without fan and with fan at highest (anticipated) PWM, and enter these PID values manually.
Script will then linearly interpolate between these PID values and set them using M301 directly before any call to M106/M107.

## Installation and usage
### Installation
The script can be placed either in "%appdata%\Cura\-version-\Scripts" or in the installation folder directly "\Program Files\Ultimaker Cura\plugins\PostProcessingPlugin\scripts"

## usage
First you must figure out the PID values required. To get these, it's easiest to simply autotune the hotend using a call to M103.
Using a serial terminal of choice (Arduino, RealTerm, PuTTY, etc.) run M103 with your hotend set at your usual printing temperature.
Do this once with the fan completely off (M106 S0) and once with the fan fully on (M106 S255) or optionally at whatever PWM you run your fan at most often.

Write down the Kp Ki and Kd settings reported by your printer for both scenarios.

In Cura, find the script in the top menu > Extensions > Post processing > Modify GCode.
Enter the PWM with which you tuned your PID, and the PID values you wrote down for both scenarios



## TODO

* Fix potential bug with decimal PWM values

CURA seems to output decimal values (such as 127.5 at 50% fan) that the scripts does not pick up on

* Add functionality to anticipate cooldown

Add the option to temporarily increase the temperature setpoint some time ahead of the M106 call to further negate sudden temperature drops