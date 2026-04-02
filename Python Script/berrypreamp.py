#  berrypreamp.py V0.7
#  Copyright (C) 2026 Roy Leith
#  For Python 3.13 & Bookworm.
#
#  This program is distributed under the terms of the GNU General Public License V3
#      see http://www.gnu.org/licenses/lgpl.txt
#
#  This program has been compiled for 64bit Bookworm and Python3.13 by pyinstaller
#
# If the script does not run in Python3.13, run it with Thonny to
# find out which modules you need to install.


import subprocess, os
import tkinter as tk

root = tk.Tk()
root.title('BerryPreamp')
root.option_add('*font', ('verdana', 10, 'bold'))
root.configure(bg="light yellow")
def statusquogain():
    result = subprocess.check_output("amixer -Dhw:sndrpihifiberry cget numid=21", shell=True)
    lines = result.splitlines()
    for line in lines:
        if line.find(b": values") > 0:
            Lgain = int(line[(line.find(b"=") + 1):(line.find(b",")):])
            Rgain = int(line[(line.find(b",") + 1):])
    return Lgain, Rgain

def statusquoLmode():
    result = subprocess.check_output("amixer -Dhw:sndrpihifiberry cget numid=22", shell=True)
    lines = result.splitlines()
    modeID = b"null"
    Lmode = b'null'
    for line in lines:
        if line.find(b": values=") > 0:
            modeID = (line[(line.find(b": values=") + 9):])
            for line in lines:
                if line.find(b"; Item #" + modeID) > 0:
                    Lmode = (line[(line.find(b"; Item #") + 10):])
    return Lmode

def statusquoRmode():
    result = subprocess.check_output("amixer -Dhw:sndrpihifiberry cget numid=23", shell=True)
    lines = result.splitlines()
    modeID = b"null"
    Rmode = b'null'
    for line in lines:
        if line.find(b": values=") > 0:
            modeID = (line[(line.find(b": values=") + 9):])
            for line in lines:
                if line.find(b"; Item #" + modeID) > 0:
                    Rmode = (line[(line.find(b"; Item #") + 10):])
    return Rmode

def statusquobias():
    result = subprocess.check_output("amixer -Dhw:sndrpihifiberry cget numid=24", shell=True)
    lines = result.splitlines()
    modeID = b"null"
    micbias = b'null'
    for line in lines:
        if line.find(b": values=") > 0:
            modeID = (line[(line.find(b": values=") + 9):])
            for line in lines:
                if line.find(b"; Item #" + modeID) > 0:
                    micbias = (line[(line.find(b"; Item #") + 10):])
    if micbias == b"'Mic Bias on'":
        micbiasval = "On"
    if micbias == b"'Mic Bias off'":
        micbiasval = "Off"
  
    return micbiasval
    
def statusquo():
    Lgain, Rgain = (statusquogain())
    print("Lgain", Lgain)
    print("Rgain", Rgain)
    print ("Left Mode ", statusquoLmode())
    print ("Right Mode ", statusquoRmode())
    print ("Bias", statusquobias())

def setgainL(val):
    os.system("amixer -q -Dhw:sndrpihifiberry cset numid=21 " + str(val) + ",")

def setlineL():
    leftvolvar.set(42)
    setgainL(42)
    
def setmicL():
    leftvolvar.set(104)
    setgainL(104)

def setgainR(val):
    os.system("amixer -q -Dhw:sndrpihifiberry cset numid=21 ," + str(val))

def setlineR():
    rightvolvar.set(42)
    setgainR(42)
    
def setmicR():
    rightvolvar.set(104)
    setgainR(104)

def setbias():
    val = micbiasvar.get()
    os.system("amixer -q -Dhw:sndrpihifiberry sset \"ADC Mic Bias\" \"Mic Bias \"" + str(val))
    if val == 'on':
        label4.config(text = 'Add Jumpers\nJ1  &  J3')
        
    else:
        label4.config(text = '              \n          ')

def setunbalanced():
    os.system("amixer -q -Dhw:sndrpihifiberry sset \"ADC Mic Bias\" \"Mic Bias off\"")
    os.system("amixer -q -Dhw:sndrpihifiberry sset \"ADC Left Input\" \"VINL1[SE]\"")
    os.system("amixer -q -Dhw:sndrpihifiberry sset \"ADC Right Input\" \"VINR1[SE]\"")
    os.system("amixer -q -Dhw:sndrpihifiberry sset ADC 42")

def setbalanced():

    os.system("amixer -q -Dhw:sndrpihifiberry sset \"ADC Left Input\" \"{VIN1P, VIN1M}[DIFF]\"")
    os.system("amixer -q -Dhw:sndrpihifiberry sset \"ADC Right Input\" \"{VIN2P, VIN2M}[DIFF]\"")


def exitreset():
    setunbalanced()
    root.destroy()

def exitasis():
    root.destroy()
    
# Initialisation

setbalanced()

maxvalue = b"104"
minvalue = b"0"

# Input Panel
widgetrelief = 'raised'
widgetborderwidth = 2
background = 'light yellow'
titlelabel = 'royal blue'
blackfont = 'Arial Black'
stdfont = 'Arial'


Master = tk.Frame(root, width=80, height=800, relief='flat', bg=background, borderwidth=1)
Master.pack(side='top', pady=0, padx=0)

Lgainval, Rgainval = (statusquogain())


label1 = tk.Label(Master, text=' Input Gain ', fg=titlelabel, font=(blackfont, 16), bg='gray90',
                  borderwidth=3, relief='ridge') .pack(side='top', pady=0, padx=0)
label2 = tk.Label(Master, text='Mode: balanced', fg=titlelabel, font=(blackfont, 12, 'normal'),
                  bg=background) .pack(side='top', pady=0, padx=0)

label3 = tk.Label(Master, text='Mic Bias', bg='white', fg='red', font=(stdfont, 12, 'bold'))
label3.pack(side='top', pady=0, padx=0)

# Mic Bias
micbiasvar = tk.StringVar()
biasq=(statusquobias())

rb1 = tk.Radiobutton(Master, text="off", borderwidth=3, variable=micbiasvar, value="off",
                     command=setbias, indicatoron=0, cursor='hand2')
rb1.pack(side='top', pady=0, padx=0)

rb2 = tk.Radiobutton(Master, fg='white', bg='gray50', text="ON", borderwidth=3, variable=micbiasvar, value="on",
                                command=setbias, indicatoron=0, selectcolor='red', cursor='hand2')
rb2.pack(side='top', pady=0, padx=0)

label4 = tk.Label(Master, bg=background, fg='red', font=(blackfont, 10))
label4.pack(side='top', pady=0, padx=0)

if biasq == 'Off':
    rb1.select()
    label4.config(text = '           \n               ')

else:
    rb2.select()
    label4.config(text = 'Add Jumpers\nJ1  &  J3')

#Left
left = tk.Frame(Master, width=10, height=220, relief='flat', bg= background, borderwidth=1)
left.pack(side='left', pady=0, padx=0)

# label5 = tk.Label(left, text='          L    ', bg=background) .pack(side='top')

leftvolvar = tk.IntVar()       
leftvolvar.set(Lgainval)
leftvol = tk.Scale(left, from_=maxvalue, to=minvalue, label='L', orient='vertical', length=250, width=14,
                   borderwidth=widgetborderwidth, relief=widgetrelief, bg='gray90', cursor='hand2',
                   variable=leftvolvar, command= setgainL,) .pack(side='top')

b1 = tk.Button(left, text='MIC', font=(blackfont, 11, 'bold'), relief=widgetrelief, fg=titlelabel,
               bg='gray90', command=setmicL) .pack(side='top')
b2 = tk.Button(left, text='LINE', font=(blackfont, 11, 'bold'), relief=widgetrelief, fg=titlelabel,
               bg='gray90', command=setlineL) .pack(side='top')

#Right
right = tk.Frame(Master, width=10, height=220, relief='flat', bg= background, borderwidth=1)
right.pack(side='right', pady=0, padx=0)
# label6 = tk.Label(right, text='          R    ', bg=background) .pack(side='top')

rightvolvar = tk.IntVar()       
rightvolvar.set(Rgainval)
rightvol = tk.Scale(right, from_=maxvalue, to=minvalue, label='R', orient='vertical', length=250, width=14,
                    borderwidth=widgetborderwidth, relief=widgetrelief, bg='gray90', cursor='hand2',
                    variable=rightvolvar, command= setgainR,)
rightvol.pack(side='top')

b3 = tk.Button(right, text='MIC', font=(blackfont, 11, 'bold'), relief=widgetrelief,
               fg=titlelabel, bg='gray90', command=setmicR) .pack(side='top')
b4 = tk.Button(right, text='LINE', font=(blackfont, 11, 'bold'), relief=widgetrelief,
               fg=titlelabel, bg='gray90', command=setlineR) .pack(side='top')

Leave = tk.Frame(root, width=60, height=100, relief='raised', borderwidth=3, bg='light yellow')
Leave.pack(side='top', pady=0, padx=0)

label7 = tk.Label(Leave, text=' Exit Mode ', font=(blackfont, 14), fg='red', borderwidth=0, relief='flat', bg=background)
label7.pack(side='top')

b5 = tk.Button(Leave, text='Unbalanced\nLINE IN', font=(blackfont, 8), relief=widgetrelief,
               borderwidth=widgetborderwidth, bg='gray90', command=exitreset) .pack(side='top')
b6 = tk.Button(Leave, text='Keep Preamp\nSettings', font=(blackfont, 8), relief=widgetrelief,
               borderwidth=widgetborderwidth, bg='gray90', command=exitasis) .pack(side='top')


root.mainloop()

   
   
   
        
