# sardana-SmaractMCS2TangoMotorController
Sardana contoller for SmarAct MCS2 Controller with up to three axis.

You need to set the Tango device name for each axis of this generic controller by the axis_attribute: Tango_Device

The state and status of the Tango device are direclty mapped as state and status of the sardana motor.

The Position is read by the Tango attribute: Position
To set the position the same Tango attribute is used.

The Sardana Stop and Abort methods both call the Tango Stop command.

Velocity, Acceleration, and Step_Per_Unit can be directly set.

