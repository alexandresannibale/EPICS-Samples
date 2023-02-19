"""
Created on Wed Dec 14 22:11:37 2022

@author: alexandre
"""

import epics
import matplotlib.pyplot as plt
from time import sleep

"""
           PV Information

Object: Bar Monitor
Wed Dec 14 22:12:26 CST 2022

alexandre:cathodeTempM
======================================
DESC: Cathode Measured Temp
RTYP: calc
TYPE: DBF_DOUBLE
COUNT: 1
ACCESS: RW
IOC: localhost:5064
VALUE: 158.4
STAMP: Wed Dec 14, 2022 22:12:25.488
ALARM: NO

PRECISION: 1
HOPR: 200  LOPR: 0
"""

PV_name = "alexandre:cathodeTempM"
catodeTemp = epics.PV(PV_name)

print(" %s connected :" % PV_name, catodeTemp.connected )

catodeTempvalues =[]
for n in range(1000):
    catodeTempvalues.append(catodeTemp.get())
    print("\rcatode temperature %14.5f C" % catodeTempvalues[-1], end="")
    sleep(1)


#%%
plt.plot(catodeTempvalues)    
plt.xlabel("time, t [s]")
plt.ylabel("Catode Temperature, T [C]")
plt.grid(True)
