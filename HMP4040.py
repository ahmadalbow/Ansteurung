import math
import time
import requests
import urllib.parse
class HMP4040:

    enabled_channels = []
    channels_power = {}
    def __init__(self, ipaddresse):

        self.url = f"http://{ipaddresse}/scpi_response.txt"
    def query(self,command):
        command = urllib.parse.quote(command)
        body = f"request={command}"
        response = requests.post(self.url, data=body)
        return response.text

    def set_volt(self,channel,volt):
        self.query(f"INST OUT{channel}")
        self.query(f"volt {volt}")

    def read_volt(self,channel):
        self.query(f"INST OUT{channel}")
        return float(self.query("MEAS:volt?"))

    def read_volt_limit(self, channel):
        self.query(f"INST OUT{channel}")
        return float(self.query("volt?"))

    def set_curr(self, channel, curr):
        self.query(f"INST OUT{channel}")
        self.query(f"CURR {curr}")
    def read_curr(self, channel):
        self.query(f"INST OUT{channel}")
        return float(self.query("MEAS:CURR?"))

    def read_curr_limit(self, channel):
        self.query(f"INST OUT{channel}")
        return float(self.query("CURR?"))

    def enable_Channel(self,channel):

        self.query(f"INST OUT{channel}")
        self.query(f"OUTP:SEL 1")
        if (self.enabled_channels.__contains__(channel)):
            return
        self.enabled_channels.append(channel)

    def disable_Channel(self, channel):

        self.query(f"INST OUT{channel}")
        self.query("OUTP:SEL 0")
        if (not self.enabled_channels.__contains__(channel)):
            return
        self.enabled_channels.remove(channel)

    def disable_output(self):
        self.query(f"OUTP:GEN 0")

    def enable_output(self):
        self.query(f"OUTP:GEN 1")

    def set_power(self,channel, power):
        self.channels_power[channel] = power
        self.query(f"INST OUT{channel}")
        self.set_volt(channel,0.1)
        time.sleep(0.7)
        R = self.read_volt(channel) / self.read_curr(channel)
        self.set_volt(channel,math.sqrt(power*R/2))
        time.sleep(0.7)
        R = self.read_volt(channel) / self.read_curr(channel)
        self.set_volt(channel,math.sqrt((3/4)*power * R ))
        time.sleep(0.7)
        R = self.read_volt(channel) / self.read_curr(channel)
        self.set_volt(channel,math.sqrt(power * R ))
    def read_power(self,channel):

        return self.read_curr(channel)*self.read_volt(channel)
    def power_correcter(self):
        while(True):
            for channel in self.enabled_channels:
                must_power = self.channels_power[channel]
                curr_power = self.read_power(channel)
                error = abs(must_power - curr_power) / must_power * 100
                while (error > 1):
                    R = self.read_volt(channel) / self.read_curr(channel)
                    if(self.read_curr_limit(channel) < math.sqrt(must_power / R)):
                        self.set_curr(channel,math.sqrt(must_power / R))
                    self.set_volt(channel, math.sqrt(must_power * R))
                    error = abs(must_power - curr_power) / must_power * 100
                    time.sleep(0.7)
    def start_up(self):
        channels = [1,2,3,4]
        self.disable_output()
        for channel in channels:
            self.disable_Channel(channel)
            self.set_volt(channel,1)

