# AdaptivePID
## Adaptive PID G-code postprocessor plugin for Cura

Postprocessing script that looks at changes to material cooling fan (M106, M107) and adjusts hotend PID settings according to it.

Requires user to autotune PID (M303) without fan and with fan at highest (anticipated) PWM, and enter these PID values manually.
Script will then linearly interpolate between these PID values and set them using M301 directly before any call to M106/M107.

## TODO

* Fix potential bug with decimal PWM values
CURA seems to output decimal values (such as 127.5 at 50% fan) that the scripts does not pick up on

* Add functionality to anticipate cooldown

Add the option to temporarily increase the temperature setpoint some time ahead of the M106 call to further negate sudden temperature drops