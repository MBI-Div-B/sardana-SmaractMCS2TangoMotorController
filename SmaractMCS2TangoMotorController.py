from PyTango import DeviceProxy

from sardana.pool.controller import MotorController
from sardana.pool.controller import Type, Access, Description, DataAccess


class SmarActHCUController(MotorController):
    MaxDevice = 99

    axis_attributes = {
        'Tango_Device': {
            Type: str,
            Description: 'The Tango Device'
            ' (e.g. domain/family/member)',
            Access: DataAccess.ReadWrite
        },
    }

    def __init__(self, inst, props, *args, **kwargs):
        super().__init__(inst, props, *args, **kwargs)

        self._log.info('Initialized')
        # do some initialization
        self.axis_extra_pars = {}

    def AddDevice(self, axis):
        self._log.info('adding axis {:d}'.format(axis))
        self.axis_extra_pars[axis] = {}
        self.axis_extra_pars[axis]['Proxy'] = None
        self.axis_extra_pars[axis]['target_position'] = 0

    def DeleteDevice(self, axis):
        self._log.info('delete axis {:d}'.format(axis))
        del self.axis_extra_pars[axis]

    def StateOne(self, axis):
        state = self.axis_extra_pars[axis]['Proxy'].command_inout("State")
        status = self.axis_extra_pars[axis]['Proxy'].command_inout("Status")
        target_position = self.axis_extra_pars[axis]['target_position']
        switch_state = MotorController.NoLimitSwitch

        return state, status, switch_state

    def ReadOne(self, axis):
        ret = self.axis_extra_pars[axis]['Proxy'].read_attribute("position").value
        return ret

    def StartOne(self, axis, position):
        self.axis_extra_pars[axis]['target_position'] = position
        self.axis_extra_pars[axis]['Proxy'].write_attribute("position", position)

    def StopOne(self, axis):
        self.axis_extra_pars[axis]['Proxy'].command_inout("stop")

    def AbortOne(self, axis):
        self.axis_extra_pars[axis]['Proxy'].command_inout("stop")

    def SetAxisPar(self, axis, name, value):
        if self.axis_extra_pars[axis]['Proxy']:
            if name == 'velocity':
                self.axis_extra_pars[axis]['Proxy'].write_attribute("MaxFrequency", int(value))
            elif name in ['acceleration', 'deceleration']:
                pass
            elif name == 'step_per_unit':
                self.axis_extra_pars[axis]['Proxy'].write_attribute("Conversion", value)
            else:
                self._log.debug('Parameter %s is not set' % name)

    def GetAxisPar(self, axis, name):
        if self.axis_extra_pars[axis]['Proxy']:
            if name == 'velocity':
                result = self.axis_extra_pars[axis]['Proxy'].read_attribute("MaxFrequency").value
            elif name in ['acceleration', 'deceleration']:
                result = 0
            elif name == 'step_per_unit':
                result = self.axis_extra_pars[axis]['Proxy'].read_attribute("Conversion").value
            else:
                result = None
        else:
            result = None
        return result

    def SetAxisExtraPar(self, axis, name, value):
        if name == 'Tango_Device':
            self.axis_extra_pars[axis][name] = value
            try:
                proxy = DeviceProxy(value)
                self.axis_extra_pars[axis]['Proxy'] = proxy
                self.axis_extra_pars[axis]['target_position'] = proxy.read_attribute("position")
                self._log.info('axis {:d} DeviceProxy set to: {:s}'.format(axis, value))
            except Exception as e:
                self.axis_extra_pars[axis]['Proxy'] = None
                raise e
        else:
            result = None

    def GetAxisExtraPar(self, axis, name):
        result = self.axis_extra_pars[axis].get(name, None)
        return result

    def SendToCtrl(self, cmd):
        """
        Send custom native commands. The cmd is a space separated string
        containing the command information. Parsing this string one gets
        the command name and the following are the arguments for the given
        command i.e.command_name, [arg1, arg2...]

        :param cmd: string
        :return: string (MANDATORY to avoid OMNI ORB exception)
        """
        # Get the process to send
        mode = cmd.split(' ')[0].lower()
        args = cmd.strip().split(' ')[1:]

        if mode == 'homing':
            try:
                if len(args) == 1:
                    axis = int(args[0])
                else:
                    raise ValueError('Invalid number of arguments')
            except Exception as e:
                self._log.error(e)

            self._log.info('Starting homing for axis {:d}'.format(axis))
            try:
                self.axis_extra_pars[axis]['Proxy'].command_inout("Home")
            except Exception as e:
                self._log.error(e)
