"""
Created on Wed Dec 14 22:11:37 2022

@author: alexandre
"""

import epics
import matplotlib.pyplot as plt
from time import sleep

"""
           PV Information

Object: Text Monitor
Thu Dec 15 06:49:54 CST 2022

alexandre:PM1:X:positionM
======================================
DESC: PM1:X
RTYP: calc
TYPE: DBF_DOUBLE
COUNT: 1
ACCESS: RW
IOC: localhost:5064
VALUE: -0.06
STAMP: Thu Dec 15, 2022 06:49:54.777
ALARM: NO

PRECISION: 2
HOPR: 5  LOPR: -5
"""


"""
           PV Information

Object: Slider
Thu Dec 15 11:37:31 CST 2022

alexandre:H1:setCurrentC
======================================
DESC: H1 current setpoint
RTYP: ao
TYPE: DBF_DOUBLE
COUNT: 1
ACCESS: RW
IOC: localhost:5064
VALUE: -1.28
STAMP: Thu Dec 15, 2022 08:34:18.962
ALARM: NO

PRECISION: 2
HOPR: 5  LOPR: -5
"""


#%% channels
PM1_X = epics.PV("alexandre:PM1:X:positionM")
PM1_X_current = epics.PV("alexandre:H1:setCurrentC")

#%% control parameters
PM1_X_set_point = 0.0
PM1_X_error     = 0.001

PM1_X_current_step = .1  

#%% control loop
PM1_Xvalues =[]
PM1_X_currentvalues =[]

PM1_X_current.put(6)
sleep(.2) 

for n in range(100):
    PM1_Xvalues.append(PM1_X.get())
    PM1_X_currentvalues.append(PM1_X_current.get())
    if   abs(PM1_Xvalues[-1] - PM1_X_set_point) <= PM1_X_error: break
    if   PM1_Xvalues[-1] > PM1_X_set_point                    : PM1_X_current.put(PM1_X_currentvalues[-1] - PM1_X_current_step)
    elif PM1_Xvalues[-1] < PM1_X_set_point                    : PM1_X_current.put(PM1_X_currentvalues[-1] + PM1_X_current_step)

    sleep(.2)        


#%%
plt.close("all")
fig , (ax1, ax2) = plt.subplots(2,1)
ax1.plot(PM1_Xvalues)    
ax1.set_ylabel("X tranverse position, $X_1$ [$\mu m$]")
ax1.grid(True)

ax2.plot(PM1_X_currentvalues)    
ax2.set_ylabel("Horizontal Magnet Current, $I_1$ [A]")
ax2.set_xlabel("time, t [s]")
ax2.grid(True)

