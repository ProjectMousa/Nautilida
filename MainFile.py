from tkinter import *
import tkinter.font
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import time, sys
import threading
import os
import glob
from datetime import datetime

currentScreen = "Home"
currentTemperature = 0          #Current temperature from sensor
wantedTemperature = 40          #User-specified temperature
temperatureSystem = "F"         #F or C
direction = "Right"             #Right or Left
currentMode = "Automatic"       #Automatic or manual
wantedTime = "0:00"
remainingTime = "0:00"          #Time running in seconds
currentTime = "0:00"            #Current clock time
currentFlowRate = 0.0           #Current flow in GPM or LPM
totalWaterUsed = 0.0            #Total water used in Gallons or Liters
flowRateSystem = "GPM"          #GPM or LPM
waterUsedSystem = "Gallons"     #Gallons or Liters
currentRow = 0                  #Current Row
currentColumn = 0               #Current Column
inCreateShower = False          #In Create Shower or not
inputShowerLength = "1:00"      #Desired shower length
inputShowerLengthMinutes = 0    #Desired shower length in minutes
constantTemperature = True      #Constant temperature or not
currentIndex = 0
inShowerNameCreator = False
volumeCutoff = False            #Volume cutoff or not
volumeAtCutoff = 1              #Desired cutoff volume
inVariableTemperatureWizard = False
wizardMinutes = 0

showerProfile0 = {"name" : "Profile0", "active" : False, "current" : False, "length" : 1, "constant" : False, "tempIfConstant" : 0, "volumeCutoff" : False, "volumeIfCutoff" : 0}
showerProfile1 = {"name" : "Profile0", "active" : False, "current" : False, "length" : 1, "constant" : False, "tempIfConstant" : 0, "volumeCutoff" : False, "volumeIfCutoff" : 0}
showerProfile2 = {"name" : "Profile0", "active" : False, "current" : False, "length" : 1, "constant" : False, "tempIfConstant" : 0, "volumeCutoff" : False, "volumeIfCutoff" : 0}
showerProfile3 = {"name" : "Profile0", "active" : False, "current" : False, "length" : 1, "constant" : False, "tempIfConstant" : 0, "volumeCutoff" : False, "volumeIfCutoff" : 0}
showerProfile4 = {"name" : "Profile0", "active" : False, "current" : False, "length" : 1, "constant" : False, "tempIfConstant" : 0, "volumeCutoff" : False, "volumeIfCutoff" : 0}

showerProfileName0 = []
showerProfileName1 = []
showerProfileName2 = []
showerProfileName3 = []
showerProfileName4 = []

showerProfileVariableTemperature0 = []

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "␣", "'", "✓"]

### GUI DEFINITIONS ###
win = Tk()
win.title("Smart Shower")
win.geometry("480x320")
mainFont = tkinter.font.Font(family = "Helvetica", size = 35, weight = "bold")
subFont = tkinter.font.Font(family = "Helvetica", size = 18)
#win.overrideredirect(True)
#win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))

currentModeLabel = Label()

temperatureLabel = Label()

currentTemperatureLabel = Label()

wantedTemperatureLabel = Label()

temperatureSystemLabel = Label()

waterFlowLabel = Label()

currentFlowRateLabel = Label()

totalWaterUsedLabel = Label()

waterSystemLabel = Label()

timeLabel = Label()

remainingTimeLabel = Label()

clockLabel = Label()

inputShowerLengthLabel = Label()

constantTemperatureLabel = Label()

inputShowerNameLabel = Label()

volumeCutoffLabel = Label()

temperatureAtTimeLabel = Label()

### HARDWARE DEFINITIONS ###
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Left Button
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Select Button
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Right Button
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)   #Exit Button


### Event Functions ###

def close():
    GPIO.cleanup()
    win.destroy()

def homePage():
    global currentScreen, currentColumn, currentRow
    currentScreen = "Home"
    screenLabel.config(text = currentScreen, font = mainFont)
    currentTemperatureLabel.config(text = "Current: " + str(currentTemperature) + " °" + temperatureSystem, font = subFont)
    currentModeLabel.config(text = "Current Mode: " + currentMode, font = subFont)
    wantedTemperatureLabel.config(text = "Wanted: " + str(wantedTemperature) + " °" + temperatureSystem, font = subFont)
    temperatureLabel.config(text = "Temperature", font = mainFont)
    timeLabel.config(text = "Time", font = mainFont)
    remainingTimeLabel.config(text = "Remaining: " + remainingTime, font = subFont)
    clockLabel.config(text = "Clock: " + currentTime, font = subFont)
    waterFlowLabel.config(text = "Water Flow", font = mainFont)
    currentFlowRateLabel.config(text = "Current Rate: " + str(currentFlowRate) + " " + flowRateSystem, font = subFont)
    totalWaterUsedLabel.config(text = "Total Used: " + str(totalWaterUsed) + " " + waterUsedSystem, font = subFont)
    
    screenLabel.place(x=250, y=0)
    currentModeLabel.place(x=180, y=60)
    timeLabel.place(x=260, y=90)
    remainingTimeLabel.place(x=120, y=160)
    clockLabel.place(x=355, y=160)
    temperatureLabel.place(x=150, y=200)
    wantedTemperatureLabel.place(x=115, y=275)
    currentTemperatureLabel.place(x=355, y=275)
    waterFlowLabel.place(x=170, y=325)
    currentFlowRateLabel.place(x=35, y=405)
    totalWaterUsedLabel.place(x=345, y=405)
    
    homeButton.place_forget()
    changeTemperatureSystemButton.place_forget()
    temperatureSystemLabel.place_forget()
    changeWaterSystemButton.place_forget()
    waterSystemLabel.place_forget()
    createNewShowerButton.place_forget()
    loadShowerButton.place_forget()

    currentColumn = 0
    currentRow = 0
    os.system("xte 'mousemove 100 100'")
    
def myShowersPage():
    global currentScreen, currentColumn, currentRow
    currentScreen = "My Showers"
    screenLabel.config(text = currentScreen, font = mainFont)

    homeButton.place(x=10, y=10)
    screenLabel.place(x=150, y=90)
    createNewShowerButton.place(x=75, y=150)
    loadShowerButton.place(x=75, y=200)
    
    currentModeLabel.place_forget()
    timeLabel.place_forget()
    remainingTimeLabel.place_forget()
    clockLabel.place_forget()
    temperatureLabel.place_forget()
    wantedTemperatureLabel.place_forget()
    currentTemperatureLabel.place_forget()
    waterFlowLabel.place_forget()
    currentFlowRateLabel.place_forget()
    totalWaterUsedLabel.place_forget()
    changeTemperatureSystemButton.place_forget()
    temperatureSystemLabel.place_forget()
    changeWaterSystemButton.place_forget()
    waterSystemLabel.place_forget()
    cancelNewShowerButton.place_forget()
    saveNewShowerButton.place_forget()
    createShowerLengthButton.place_forget()
    inputShowerLengthLabel.place_forget()
    constantTemperatureButton.place_forget()
    constantTemperatureLabel.place_forget()
    inputShowerNameLabel.place_forget()
    inputShowerNameButton.place_forget()
    volumeCutoffLabel.place_forget()
    volumeCutoffButton.place_forget()

    currentColumn = 0
    currentRow = 0
    os.system("xte 'mousemove 20 20'")
    
def musicPage():
    global currentScreen, currentColumn, currentRow
    currentScreen = "Music"
    screenLabel.config(text = currentScreen, font = mainFont)

    homeButton.place(x=10, y=10)
    screenLabel.place(x=250, y=90)
    
    currentModeLabel.place_forget()
    timeLabel.place_forget()
    remainingTimeLabel.place_forget()
    clockLabel.place_forget()
    temperatureLabel.place_forget()
    wantedTemperatureLabel.place_forget()
    currentTemperatureLabel.place_forget()
    waterFlowLabel.place_forget()
    currentFlowRateLabel.place_forget()
    totalWaterUsedLabel.place_forget()
    changeTemperatureSystemButton.place_forget()
    temperatureSystemLabel.place_forget()
    changeWaterSystemButton.place_forget()
    waterSystemLabel.place_forget()
    createNewShowerButton.place_forget()
    loadShowerButton.place_forget()

    currentColumn = 0
    currentRow = 0
    os.system("xte 'mousemove 20 20'")
    
def settingsPage():
    global currentScreen, currentColumn, currentRow
    currentScreen = "Settings"
    screenLabel.config(text = currentScreen, font = mainFont)
    temperatureSystemLabel.config(text = "Current Temperature System: °" + temperatureSystem, font = subFont)
    waterSystemLabel.config(text = "Current Water System: " + waterUsedSystem, font = subFont)

    homeButton.place(x=10, y=10)
    screenLabel.place(x=210, y=90)
    changeTemperatureSystemButton.place(x=80, y=160)
    temperatureSystemLabel.place(x=120, y=220)
    changeWaterSystemButton.place(x=80, y=270)
    waterSystemLabel.place(x=130, y=330)
    
    currentModeLabel.place_forget()
    timeLabel.place_forget()
    remainingTimeLabel.place_forget()
    clockLabel.place_forget()
    temperatureLabel.place_forget()
    wantedTemperatureLabel.place_forget()
    currentTemperatureLabel.place_forget()
    waterFlowLabel.place_forget()
    currentFlowRateLabel.place_forget()
    totalWaterUsedLabel.place_forget()
    createNewShowerButton.place_forget()
    loadShowerButton.place_forget()

    currentColumn = 0
    currentRow = 0
    os.system("xte 'mousemove 20 20'")
    
def helpPage():
    global currentScreen, currentColumn, currentRow
    currentScreen = "Help"
    screenLabel.config(text = currentScreen, font = mainFont)

    homeButton.place(x=10, y=10)
    screenLabel.place(x=270, y=90)
    
    currentModeLabel.place_forget()
    timeLabel.place_forget()
    remainingTimeLabel.place_forget()
    clockLabel.place_forget()
    temperatureLabel.place_forget()
    wantedTemperatureLabel.place_forget()
    currentTemperatureLabel.place_forget()
    waterFlowLabel.place_forget()
    currentFlowRateLabel.place_forget()
    totalWaterUsedLabel.place_forget()
    changeTemperatureSystemButton.place_forget()
    temperatureSystemLabel.place_forget()
    changeWaterSystemButton.place_forget()
    waterSystemLabel.place_forget()
    createNewShowerButton.place_forget()
    loadShowerButton.place_forget()

    currentColumn = 0
    currentRow = 0
    os.system("xte 'mousemove 20 20'")
    
def changeScreen():
    global currentScreen, currentColumn, currentRow
    if(currentScreen == "Home" and direction == "Right"):
        myShowersPage()
    elif(currentScreen == "Home" and direction == "Left"):
        helpPage()
    elif(currentScreen == "My Showers" and direction == "Right"):
        if(inCreateShower == False):
            if(currentRow == 2):
                musicPage()
            elif(currentRow == 1):
                os.system("xte 'mousemove 100 225'")
                currentRow = 2
            elif(currentRow == 0):
                os.system("xte 'mousemove 100 175'")
                currentRow = 1
        elif(inCreateShower == True):
            if(currentRow == 0):
                if(inShowerNameCreator == False):
                    os.system("xte 'mousemove 100 100'")
                    currentRow = 1
            elif(currentRow == 1):
                os.system("xte 'mousemove 100 150'")
                currentRow = 2
            elif(currentRow == 2):
                os.system("xte 'mousemove 100 200'")
                currentRow = 3
            elif(currentRow == 3):
                os.system("xte 'mousemove 150 400'")
                currentRow = 4
            elif(currentRow == 4):
                os.system("xte 'mousemove 350 400'")
                currentRow = 5
            print(currentRow)
    elif(currentScreen == "My Showers" and direction == "Left"):
        if(inCreateShower == False):
            if(currentRow == 0):
                homePage()
            elif(currentRow == 2):
                os.system("xte 'mousemove 100 175'")
                currentRow = 1
            elif(currentRow == 1):
                os.system("xte 'mousemove 20 20'")
                currentRow = 0
        elif(inCreateShower == True):
            if(currentRow == 5):
                os.system("xte 'mousemove 150 400'")
                currentRow = 4
            elif(currentRow == 4):
                os.system("xte 'mousemove 100 200'")
                currentRow = 3
            elif(currentRow == 3):
                os.system("xte 'mousemove 100 150'")
                currentRow = 2
            elif(currentRow == 2):
                os.system("xte 'mousemove 100 100'")
                currentRow = 1
            elif(currentRow == 1):
                os.system("xte 'mousemove 100 50'")
                currentRow = 0
            print(currentRow)
    elif(currentScreen == "Music" and direction == "Right"):
        settingsPage()
    elif(currentScreen == "Music" and direction == "Left"):
        myShowersPage()
    elif(currentScreen == "Settings" and direction == "Right"):
        if(currentRow == 2):
            helpPage()
        elif(currentRow == 0):
            os.system("xte 'mousemove 100 175'")
            currentRow = 1
        elif(currentRow == 1):
            os.system("xte 'mousemove 100 275'")
            currentRow = 2
    elif(currentScreen == "Settings" and direction =="Left"):
        if(currentRow == 0):
            musicPage()
        elif(currentRow == 2):
            os.system("xte 'mousemove 100 175'")
            currentRow = 1
        elif(currentRow == 1):
            os.system("xte 'mousemove 20 20'")
            currentRow = 0
    elif(currentScreen == "Help" and direction == "Right"):
        homePage()
    elif(currentScreen == "Help" and direction == "Left"):
        settingsPage()
        
def changeTemperatureSystem():
    global temperatureSystem
    global wantedTemperature
    if(temperatureSystem == "F"):
        temperatureSystem = "C"
        if(wantedTemperature > 50):
            wantedTemperature = 50
        elif(wantedTemperature < 5):
            wantedTemperature = 5
        temperatureSystemLabel.config(text = "Current Temperature System: °" + temperatureSystem, font = subFont)
    elif(temperatureSystem == "C"):
        temperatureSystem = "F"
        if(wantedTemperature > 120):
            wantedTemperature = 120
        elif(wantedTemperature < 40):
            wantedTemperature = 40
        temperatureSystemLabel.config(text = "Current Temperature System: °" + temperatureSystem, font = subFont)

def changeWaterSystem():
    global flowRateSystem
    global waterUsedSystem
    if(flowRateSystem == "GPM" and waterUsedSystem == "Gallons"):
        flowRateSystem = "LPM"
        waterUsedSystem = "Liters"
        waterSystemLabel.config(text = "Current Water System: " + waterUsedSystem, font = subFont)
    elif(flowRateSystem == "LPM" and waterUsedSystem == "Liters"):
        flowRateSystem = "GPM"
        waterUsedSystem = "Gallons"
        waterSystemLabel.config(text = "Current Water System: " + waterUsedSystem, font = subFont)

def createNewShower():
    global inCreateShower, inputShowerLength, currentRow
    inputShowerLengthLabel.config(text = inputShowerLength, font = subFont)
    constantTemperatureLabel.config(text = "Yes: " + str(wantedTemperature) + " °" + temperatureSystem, font = subFont)
    inputShowerNameLabel.config(text = "a", font = subFont)
    volumeCutoffLabel.config(text = "No", font = subFont)

    createShowerLengthButton.place(x=50, y=100)
    inputShowerLengthLabel.place(x=300, y=105)
    constantTemperatureButton.place(x=50, y=150)
    constantTemperatureLabel.place(x=400, y=155)
    cancelNewShowerButton.place(x=50, y=400)
    saveNewShowerButton.place(x=335, y=400)
    inputShowerNameLabel.place(x=300, y=55)
    inputShowerNameButton.place(x=50, y=50)
    volumeCutoffLabel.place(x=300, y=205)
    volumeCutoffButton.place(x=50, y=200)

    homeButton.place_forget()
    screenLabel.place_forget()
    createNewShowerButton.place_forget()
    loadShowerButton.place_forget()

    inCreateShower = True
    os.system("xte 'mousemove 100 50'")
    currentRow = 0

    if(showerProfile0["active"] == False):
        showerProfile0["active"] = True
        showerProfile0["current"] = True
    elif(showerProfile1["active"] == False):
        showerProfile1["active"] = True
        showerProfile1["current"] = True
    elif(showerProfile2["active"] == False):
        showerProfile2["active"] = True
        showerProfile2["current"] = True
    elif(showerProfile3["active"] == False):
        showerProfile3["active"] = True
        showerProfile3["current"] = True
    elif(showerProfile4["active"] == False):
        showerProfile4["active"] = True
        showerProfile4["current"] = True
    
def cancelNewShower():
    global inCreateShower
    myShowersPage()
    inCreateShower = False

def saveNewShower():
    global wantedTemperature, wantedTime, inCreateShower, showerProfile0, showerProfile1, showerProfile2, showerProfile3, showerProfile4
    global showerProfileName0, showerProfileName1, showerProfileName2, showerProfileName3, showerProfileName4  
    if(showerProfile0["active"] == False):
        if(constantTemperature == True):
            showerProfile0["constant"] = True
            showerProfile0["tempIfConstant"] = wantedTemperature
        elif(constantTemperature == False):
            showerProfile0["constant"] = False
        showerProfile0["name"] = "".join(showerProfileName0)
        showerProfile0["length"] = inputShowerLengthMinutes
        if(volumeCutoff == True):
            showerProfile0["volumeCutoff"] = True
            showerProfile0["volumeIfCutoff"] = volumeAtCutoff
        elif(volumeCutoff == False):
            showerProfile0["volumeCutoff"] = False
        print(showerProfile0["active"])
        print(showerProfile0["constant"])
        print(showerProfile0["tempIfConstant"])
        print(showerProfile0["name"])
        print(showerProfile0["length"])
        print(showerProfile0["volumeCutoff"])
        print(showerProfile0["volumeIfCutoff"])
    elif(showerProfile1["active"] == False):
        if(constantTemperature == True):
            showerProfile1["constant"] = True
            showerProfile1["tempIfConstant"] = wantedTemperature
        elif(constantTemperature == False):
            showerProfile1["constant"] = False
        showerProfile1["name"] = "".join(showerProfileName1)
        showerProfile1["length"] = inputShowerLengthMinutes
    elif(showerProfile2["active"] == False):
        if(constantTemperature == True):
            showerProfile2["constant"] = True
            showerProfile2["tempIfConstant"] = wantedTemperature
        elif(constantTemperature == False):
            showerProfile2["constant"] = False
        showerProfile2["name"] = "".join(showerProfileName2)
        showerProfile2["length"] = inputShowerLengthMinutes
    elif(showerProfile3["active"] == False):
        if(constantTemperature == True):
            showerProfile3["constant"] = True
            showerProfile3["tempIfConstant"] = wantedTemperature
        elif(constantTemperature == False):
            showerProfile3["constant"] = False
        showerProfile3["name"] = "".join(showerProfileName3)
        showerProfile3["length"] = inputShowerLengthMinutes
    elif(showerProfile4["active"] == False):
        if(constantTemperature == True):
            showerProfile4["constant"] = True
            showerProfile4["tempIfConstant"] = wantedTemperature
        elif(constantTemperature == False):
            showerProfile4["constant"] = False
        showerProfile4["name"] = "".join(showerProfileName4)
        showerProfile4["length"] = inputShowerLengthMinutes
    else:
        print("All Profiles Taken")
    showerProfile0["current"] = False
    showerProfile1["current"] = False
    showerProfile2["current"] = False
    showerProfile3["current"] = False
    showerProfile4["current"] = False
    myShowersPage()
    inCreateShower = False

def loadShower():
    print("Load Shower")

def changeConstantTemperature():
    global constantTemperature, wizardMinutes
    if(inVariableTemperatureWizard == False):
        if(constantTemperature == True):
            constantTemperature = False
            constantTemperatureLabel.config(text = "No", font = subFont)
            wizardMinutes = 1
            variableTemperatureWizard()
        ########################################################################################
        elif(constantTemperature == False):
            constantTemperature = True
            constantTemperatureLabel.config(text = "Yes: " + str(wantedTemperature) + " °" + temperatureSystem, font = subFont)
    elif(inVariableTemperatureWizard == True):
        wizardMinutes += 1
        variableTemperatureWizard()
    print(inVariableTemperatureWizard)
        
def variableTemperatureWizard():
    global wizardMinutes, inVariableTemperatureWizard
    if(wizardMinutes != (inputShowerLengthMinutes + 1)):
        inVariableTemperatureWizard = True
        if(wizardMinutes == 1):
            temperatureAtTimeLabel.config(text = "Temperature at " + str(wizardMinutes) + " Minute: " + str(wantedTemperature), font = subFont)
        else:
            temperatureAtTimeLabel.config(text = "Temperature at " + str(wizardMinutes) + " Minutes: " + str(wantedTemperature), font = subFont)
            if(showerProfile0["current"] == True):
                showerProfileVariableTemperature0.append(wantedTemperature)
        temperatureAtTimeLabel.place(x=50, y=300)
    elif(wizardMinutes == (inputShowerLengthMinutes + 1)):
        showerProfileVariableTemperature0.append(wantedTemperature)
        inVariableTemperatureWizard = False
        temperatureAtTimeLabel.place_forget()
        print("Wizard Done")

def inputShowerName():
    if(showerProfile0["current"] == True):
        inputShowerNameLabel.config(text = "".join(showerProfileName0) + alphabet[currentIndex], font = subFont)
    elif(showerProfile1["current"] == True):
        inputShowerNameLabel.config(text = "".join(showerProfileName1) + alphabet[currentIndex], font = subFont)
    elif(showerProfile2["current"] == True):
        inputShowerNameLabel.config(text = "".join(showerProfileName2) + alphabet[currentIndex], font = subFont)
    elif(showerProfile3["current"] == True):
        inputShowerNameLabel.config(text = "".join(showerProfileName3) + alphabet[currentIndex], font = subFont)
    elif(showerProfile4["current"] == True):
        inputShowerNameLabel.config(text = "".join(showerProfileName4) + alphabet[currentIndex], font = subFont)

def appendShowerName():
    global inShowerNameCreator, direction
    global showerProfileName0, showerProfileName1, showerProfileName2, showerProfileName3, showerProfileName4
    if(inShowerNameCreator == False):
        inShowerNameCreator = True
    elif(currentIndex == 28):
        inShowerNameCreator = False
        direction = "Right"
        changeScreen()
    elif(inShowerNameCreator == True):
        if(showerProfile0["current"] == True):
            if(currentIndex == 26):
                showerProfileName0.append(" ")
            else:
                showerProfileName0.append(alphabet[currentIndex])
        elif(showerProfile1["current"] == True):
            if(currentIndex == 26):
                showerProfileName1.append(" ")
            else:
                showerProfileName1.append(alphabet[currentIndex])
        elif(showerProfile2["current"] == True):
            if(currentIndex == 26):
                showerProfileName2.append(" ")
            else:
                showerProfileName2.append(alphabet[currentIndex])
        elif(showerProfile3["current"] == True):
            if(currentIndex == 26):
                showerProfileName3.append(" ")
            else:
                showerProfileName3.append(alphabet[currentIndex])
        elif(showerProfile4["current"] == True):
            if(currentIndex == 26):
                showerProfileName4.append(" ")
            else:
                showerProfileName4.append(alphabet[currentIndex])
        inputShowerName()

def changeVolumeCutoff():
    global volumeCutoff
    if(volumeCutoff == True):
        volumeCutoff = False
        volumeCutoffLabel.config(text = "No", font = subFont)
    elif(volumeCutoff == False):
        volumeCutoff = True
        volumeCutoffLabel.config(text = "Yes: " + str(volumeAtCutoff) + " " + waterUsedSystem, font = subFont)

### WIDGETS ###

# Button, triggers the connected command when it is pressed

homeButton = Button(win, text='Home', font=mainFont, command=homePage, bg='dim gray', height=1, width=10)

win.protocol("WM_DELETE_WINDOW", close) # cleanup GPIO when user closes window

changeTemperatureSystemButton = Button(win, text = "Change Temperature System", font = subFont, command = changeTemperatureSystem, bg='dim gray', height=1, width=30)

changeWaterSystemButton = Button(win, text = "Change Water System", font = subFont, command = changeWaterSystem, bg='dim gray', height=1, width=30)

createNewShowerButton = Button(win, text = "Create New Shower", font = subFont, command = createNewShower, bg="dim gray", height=1, width=30)

cancelNewShowerButton = Button(win, text = "Cancel", font = subFont, command = cancelNewShower, bg="dim gray", height=1, width=15)

saveNewShowerButton = Button(win, text = "Save", font = subFont, command = saveNewShower, bg="dim gray", height=1, width=15)

loadShowerButton = Button(win, text = "Load Shower", font = subFont, command = loadShower, bg="dim gray", height=1, width=30)

createShowerLengthButton = Button(win, text = "Shower Length:", font = subFont, bg="dim gray", height=1, width=12)

constantTemperatureButton = Button(win, text = "Constant Temperature:", font = subFont, command = changeConstantTemperature, bg="dim gray", height=1, width=18)

inputShowerNameButton = Button(win, text = "Name:", font = subFont, command = appendShowerName, bg="dim gray", height=1, width=12)

volumeCutoffButton = Button(win, text = "Volume Cutoff:", font = subFont, command=changeVolumeCutoff, bg="dim gray", height=1, width=12)

### MAIN CODE ###
screenLabel = Label()
homePage()
def MainCode():
    Close = False
    global direction
    leftInput = GPIO.input(11)
    selectInput = GPIO.input(13)
    rightInput = GPIO.input(15)
    exitInput = GPIO.input(12)
    if leftInput == False:
        direction = "Left"
        changeScreen()
    elif selectInput == False:
        os.system("xte 'mouseclick 1'")
    elif rightInput == False:
        direction = "Right"
        changeScreen()
    elif exitInput == False: 
        Close = True
    if Close == False:
        win.after(150, MainCode)
    if Close == True:
        close()

###Rotary Encoder###

Enc_A = 37
Enc_B = 38
Rotary_counter = 0
Current_A = 1
Current_B = 1
LockRotary = threading.Lock()
GPIO.setwarnings(True)
GPIO.setup(Enc_A, GPIO.IN) 				
GPIO.setup(Enc_B, GPIO.IN)
def rotary_interrupt(A_or_B):
    global Rotary_counter, Current_A, Current_B, LockRotary
    Switch_A = GPIO.input(Enc_A)
    Switch_B = GPIO.input(Enc_B)													# now check if state of A or B has changed													
    if Current_A == Switch_A and Current_B == Switch_B:		
        return										
    Current_A = Switch_A								
    Current_B = Switch_B								
    if (Switch_A and Switch_B):						
        LockRotary.acquire()
        if A_or_B == Enc_B:							
            Rotary_counter += 1						
        else:										
            Rotary_counter -= 1						
        LockRotary.release()						
    return

GPIO.add_event_detect(Enc_A, GPIO.RISING, callback=rotary_interrupt) 				# NO bouncetime 
GPIO.add_event_detect(Enc_B, GPIO.RISING, callback=rotary_interrupt)
NewCounter = 0
def rotaryInput():
    global wantedTemperature, inputShowerLengthMinutes, inputShowerLength
    global Rotary_counter, LockRotary, NewCounter, currentIndex, volumeAtCutoff							# Current Volume
    LockRotary.acquire()					# get lock for rotary switch
    NewCounter = Rotary_counter			# get counter value
    Rotary_counter = 0						# RESET IT TO 0
    LockRotary.release()					# and release lock					
    if (NewCounter !=0):
        if(currentScreen == "Home"):                # Counter has CHANGED
            wantedTemperature += NewCounter	# Decrease or increase volume 
            if(temperatureSystem == "F"):
                if wantedTemperature < 40:						# limit volume to 0...100
                    wantedTemperature = 40
                elif wantedTemperature > 120:					# limit volume to 0...100
                    wantedTemperature = 120
            elif(temperatureSystem == "C"):
                if wantedTemperature < 5:						# limit volume to 0...100
                    wantedTemperature = 5
                elif wantedTemperature > 50:					# limit volume to 0...100
                    wantedTemperature = 50
            wantedTemperatureLabel.config(text = "Wanted: " + str(wantedTemperature) + " °" + temperatureSystem, font = subFont)
        elif(currentScreen == "My Showers"):
            if(inCreateShower == True):
                if(currentRow == 0):
                    if(inShowerNameCreator == True):
                        currentIndex += NewCounter
                        if(currentIndex < 0):
                            currentIndex = 28
                        elif(currentIndex > 28):
                            currentIndex = 0
                        inputShowerName()
                elif(currentRow == 1):
                    inputShowerLengthMinutes += NewCounter
                    if(inputShowerLengthMinutes > 60):
                        inputShowerLengthMinutes = 60
                    elif(inputShowerLengthMinutes < 1):
                        inputShowerLengthMinutes = 1
                    inputShowerLength = "%s:00" % (str(inputShowerLengthMinutes))
                    inputShowerLengthLabel.config(text = inputShowerLength, font = subFont)
                elif(currentRow == 2 and constantTemperature == True):
                    wantedTemperature += NewCounter
                    if(temperatureSystem == "F"):
                        if wantedTemperature < 40:						# limit volume to 0...100
                            wantedTemperature = 40
                        elif wantedTemperature > 120:					# limit volume to 0...100
                            wantedTemperature = 120
                    elif(temperatureSystem == "C"):
                        if wantedTemperature < 5:						# limit volume to 0...100
                            wantedTemperature = 5
                        elif wantedTemperature > 50:					# limit volume to 0...100
                            wantedTemperature = 50
                    constantTemperatureLabel.config(text = "Yes: " + str(wantedTemperature) + " °" + temperatureSystem, font = subFont)
                elif(currentRow == 2 and constantTemperature == False):
                    wantedTemperature += NewCounter
                    if(temperatureSystem == "F"):
                        if wantedTemperature < 40:						# limit volume to 0...100
                            wantedTemperature = 40
                        elif wantedTemperature > 120:					# limit volume to 0...100
                            wantedTemperature = 120
                    elif(temperatureSystem == "C"):
                        if wantedTemperature < 5:						# limit volume to 0...100
                            wantedTemperature = 5
                        elif wantedTemperature > 50:					# limit volume to 0...100
                            wantedTemperature = 50
                    temperatureAtTimeLabel.config(text = "Temperature at " + str(wizardMinutes) + " Minutes: " + str(wantedTemperature), font = subFont)
                    ###########################################################
                elif(currentRow == 3 and volumeCutoff == True):
                    volumeAtCutoff += NewCounter
                    if(volumeAtCutoff < 1):
                        volumeAtCutoff = 1
                    elif(volumeAtCutoff > 100):
                        volumeAtCutoff = 100
                    volumeCutoffLabel.config(text = "Yes: " + str(volumeAtCutoff) + " " + waterUsedSystem, font = subFont)
    win.after(100, rotaryInput)

###Temperature Probe###

os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")
base_dir = '/sys/bus/w1/devices/'
#device_folder = glob.glob(base_dir + '28-0417c1c235ff')[0]
#device_file = device_folder + '/w1_slave'
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    global currentTemperature
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        if(temperatureSystem == "F"):
            currentTemperature = round(temp_f)
        elif(temperatureSystem == "C"):
            currentTemperature = round(temp_c)

def checkTemperature():
    global currentTemperature
    read_temp()
    if(inCreateShower == False):
        if(currentTemperature < wantedTemperature):
            heatValve("Hot")
        elif(currentTemperature > wantedTemperature):
            heatValve("Cold")
    win.after(3000, checkTemperature)
    
def updateTemperature():
    global currentTemperature
    if(currentScreen == "Home"):
        currentTemperatureLabel.config(text = "Current: " + str(currentTemperature) + " °" + temperatureSystem, font = subFont)
    win.after(100, updateTemperature)
    
###Valve Turning###
    
DIR = 36   # Direction GPIO Pin
STEP = 35  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 48   # Steps per Revolution (360 / 7.5)

GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

step_count = SPR
delay = .001

def heatValve(hotORcold):
    if(hotORcold == "Hot"):
        GPIO.output(DIR, CW)
        for x in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            time.sleep(delay)
    elif(hotORcold == "Cold"):
        GPIO.output(DIR, CCW)
        for x in range(step_count):
            GPIO.output(STEP, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            time.sleep(delay)

def volumeValve(higherORlower):
    if(higherORlower == "Higher"):
        print("Higher volume")
    elif(higherORlower == "Lower"):
        print("Lower volume")
        
###Flow Meter###
        
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
rate_cnt = 0
tot_cnt = 0
minutes = 0
constant = 0.10
time_new = 0.0
def getWaterFlow():
    global rate_cnt, tot_cnt, minutes, constant, time_new
    if(currentScreen == "Home"):
        time_new = time.time() + 10
        rate_cnt = 0
        while time.time() <= time_new:
            if GPIO.input(16) != 0:
                rate_cnt += 1
                tot_cnt += 1
            try:
                pass
                #print(GPIO.input(16), end="")
            except:
                pass
        minutes += 1
        print("\nLiters / min ", round(rate_cnt * constant, 4))
        print("Total Liters ", round(tot_cnt * constant, 4))
    win.after(1000, getWaterFlow)

###Time Functions###
def updateClock():
    global currentTime
    if(currentScreen == "Home"):
        currentHour = datetime.now().hour
        currentMinute = datetime.now().minute
        if(currentMinute < 10):
            currentTime = "%s:0%s" % (str(currentHour), str(currentMinute))
        elif(currentMinute >= 10):
            currentTime = "%s:%s" % (str(currentHour), str(currentMinute))
        clockLabel.config(text = "Clock: " + currentTime, font = subFont)
    win.after(5000, updateClock)
    
win.after(100, MainCode)
win.after(50, rotaryInput)
#win.after(100, checkTemperature)
#win.after(100, updateTemperature)
win.after(1000, updateClock)
#win.after(1000, getWaterFlow)
win.mainloop() # Loops forever
