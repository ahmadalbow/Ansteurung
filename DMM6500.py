import pyvisa
from enum import Enum
class DMM6500:
    rm = pyvisa.ResourceManager()
    def __init__(self, ipaddresse):
        self.inst = self.rm.open_resource(f'TCPIP::{ipaddresse}::INSTR')
        self.ranges = {}

    def measure(self,function, bufferName = 'defbuffer1' ):
        return float(self.inst.query(f'MEAS:{function.value}? "{bufferName}"'))


    def query(self,command):
        self.inst.query(command)

    def write(self,command):
        self.inst.write(command)

    def rest_trigger(self):
        self.inst.write("TRIG:CONT REST")


    def startup(self):
        for func in list(Function_With_Range):
            self.ranges[func.name] = 'AUTO'
            self.write(f'SENS:{func.value}:RANG:AUTO ON')

    def set_Range(self,function,value):
        if (function.name in [e.name for e in list(Function_With_Range)]):
            if (value == 'auto' or value == 'AUTO' or value == 'Auto' ):
                self.write(f'SENS:{function.value}:RANG:AUTO ON')
                self.ranges[function.name] = 'AUTO'
                return
            elif (function.name == 'VOLTDC' and value in [0.1,1,10,100,1000]):
                self.write(f'{function.value}:RANGE {value}')
            elif (function.name == 'VOLTAC' and value in [0.1,1,10,100,750]):
                self.write(f'{function.value}:RANGE {value}')
            elif (function.name == 'CURRDC' and value in [0.00001,0.0001,0.001,0.01,0.1,1]):
                self.write(f'{function.value}:RANGE {value}')
            elif (function.name == 'CURRAC' and value in [0.0001,0.001,0.01,0.1,1,3]):
                self.write(f'{function.value}:RANGE {value}')
            elif (function.name == 'RES' and value in [10,100,1000,10000,100000,1000000,10000000,100000000]):
                self.write(f'{function.value}:RANGE {value}')
            elif (function.name == 'CAPACITANCE' and value in [0.000000001,0.000000010,0.000000100,0.000001,0.000010,0.000100]):
                self.write(f'{function.value}:RANGE {value}')
            else:
                print('falsche Funktion oder Range eingegeben ')
                return
            self.ranges[function.name] = value

    def get_range(self,function):
        if (function.name in [e.name for e in list(Function_With_Range)]):
            return self.ranges[function.name]
        return 'this function has no range'


class Function(Enum):
    VOLTDC = 'VOLT'
    VOLTAC = 'VOLT:AC'
    CURRDC = 'CURR'
    CURRAC = 'CURR:AC'
    RES = 'RES'
    FRES = 'FRES'
    DIOD = 'DIOD'
    CAPACITANCE = 'CAPacitance'
    TEMP = 'TEMP'
    CONT = 'CONT'
    FREQ = 'FREQ'
    PERIOD = 'PER'

class Function_With_Range(Enum):
    VOLTDC = 'VOLT'
    VOLTAC = 'VOLT:AC'
    CURRDC = 'CURR'
    CURRAC = 'CURR:AC'
    RES = 'RES'
    CAPACITANCE = 'CAPacitance'
