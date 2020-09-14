# sardana-SmaractMCS2TangoMotorController
Sardana contoller for SmarAct MCS2 Controller with multiple axis.

## Compatible Devices

http://svn.code.sf.net/p/tango-ds/code/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Motor/
http://svn.code.sf.net/p/tango-ds/code/DeviceClasses/Motion/MotorControllers/Smaract/SmarActMCS2Ctrl/

## Configuration

You need to set the Tango device name for each axis of this generic controller by the axis_attribute: Tango_Device

The state and status of the Tango device are direclty mapped as state and status of the sardana motor.

The Position is read by the Tango attribute: Position

The Sardana Stop and Abort methods both call the Tango Stop command.

