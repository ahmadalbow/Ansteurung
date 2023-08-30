from jds6600 import jds6600

j = jds6600("/dev/ttyUSB0")
j.setwaveform(1,"sinc")
j.setfrequency(1,1000)
