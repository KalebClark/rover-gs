import pygame
import time
from numpy import interp
import math

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print 'Initialized Joystick : %s' % j.get_name()

"""
Returns a vector of the following form:
[LThumbstickX, LThumbstickY, Unknown Coupled Axis???, 
RThumbstickX, RThumbstickY, 
Button 1/X, Button 2/A, Button 3/B, Button 4/Y, 
Left Bumper, Right Bumper, Left Trigger, Right Triller,
Select, Start, Left Thumb Press, Right Thumb Press]

Note:
No D-Pad.
Triggers are switches, not variable. 
Your controller may be different
"""

def get():
    out = {} 
    pygame.event.pump()

    buttons = {
        0:  'lx',
        1:  'ly',
        2:  'ry',
        3:  'rx',
        4:  '?',
        5:  '?',
        6:  '?',
        7:  '?',
        8:  'du',
        9:  'dr',
        10:  '10',
        11:  '11',
        12:  'B',
        13:  'B',
        14:  'B',
        15:  'B',
        16:  'B',
        17:  'B',
        18:  'B',
        19:  'B',
        20:  'B',
        21:  'B',
        22:  'B',
        23:  'B',
        24:  'B',
        25:  'B',
        26:  'B',
        27:  'B',
        28:  'B'
    }

    
    #Read input from the two joysticks       
    for i in range(0, j.get_numaxes()):
        val = interp(j.get_axis(i), [-1, 0.9], [0, 255])
        out[buttons[i]] = int(val)


#    for i in range(0, j.get_numbuttons()):
#        out.append(j.get_button(i))
        #out[it] = j.get_button(i)
        #it+=1
    return out

def test():
    while True:
        print get()
        time.sleep(.1)
