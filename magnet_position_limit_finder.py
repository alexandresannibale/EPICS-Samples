import epics
import matplotlib.pyplot as plt
from time import sleep
import numpy as np

#%% control loop
def linac_magnet_position_limit(current_step, HVmagnet_pos_epics, HVmagnet_set_current_epics,
                                HVmagnet_current):
    
    FC1_intensityM = epics.PV("alexandre:FC1:intensityM")
    reset_button = epics.PV("alexandre:autoC")
    P = epics.PV(HVmagnet_pos_epics)
    C = epics.PV(HVmagnet_set_current_epics)
    I = epics.PV(HVmagnet_current)
    
    reset_button.put(1)
    sleep(1)    
    while FC1_intensityM.get() <= 7:
        sleep(1)
    reset_button.put(0)
    
    position =[]
    set_current =[]
    mag_current = []
    beam_current = []
    
    while I.get() != 0:
       beam_current.append(FC1_intensityM.get())
       position.append(P.get())  
       set_current.append(C.get())
       mag_current.append(I.get())
       sleep(.5)
       C.put(set_current[-1] + current_step)
       
       print(position[-1], set_current[-1], mag_current[-1])
       
    reset_button.put(1)
    

    return position, set_current, mag_current, beam_current


#%%
def save_data(position, set_current, mag_current, beam_current, file_name):
    
    X = np.column_stack((set_current, position, mag_current, beam_current))
    np.savetxt(file_name, X)
    print(X)
    return X

    
#%%
def plot_linac_limits(position, set_current, mag_current, beam_current):
    
    fig , (ax1, ax2, ax3, ax4) = plt.subplots(4,1)
    ax1.plot(position)    
    ax1.set_ylabel("Tranverse position, $X_1$ [$mm $]")
    ax1.grid(True)
    
    ax2.plot(set_current)    
    ax2.set_ylabel("Set Magnet Slider, $I_s$ [AU]")
    ax2.grid(True)
    
    ax3.plot(mag_current)    
    ax3.set_ylabel("Magnet Current, $I$ [mA]")
    ax3.grid(True)
    
    ax4.plot(beam_current)    
    ax4.set_ylabel("Total Beam Current, $I_1$ [mA]")
    ax4.set_xlabel("time, t [s]")
    ax4.grid(True)
    return  fig , (ax1, ax2, ax3, ax4)


#%%
#PM1_position, PM1_set_current, mag_current, beam_current = linac_magnet_position_limit(-0.05, "alexandre:PM1:X:positionM",
                          #  "alexandre:H1:setCurrentC", "alexandre:PM1:intensityM")

#PM1_position, PM1_set_current, mag_current, beam_current = linac_magnet_position_limit(-0.05, "alexandre:PM1:Y:positionM",
#                            "alexandre:V1:setCurrentC", "alexandre:PM1:intensityM")

#PM2_position, PM2_set_current, mag_current, beam_current = linac_magnet_position_limit(-0.05, "alexandre:PM2:X:positionM",
#                            "alexandre:H2:setCurrentC", "alexandre:PM2:intensityM")

PM2_position, PM2_set_current, mag_current, beam_current = linac_magnet_position_limit(-0.05, "alexandre:PM2:Y:positionM",
                            "alexandre:V2:setCurrentC", "alexandre:PM2:intensityM")
plt.close("all")
plot_linac_limits(PM2_position, PM2_set_current, mag_current, beam_current)
save_data(PM2_position, PM2_set_current, mag_current, beam_current, "test.txt")
