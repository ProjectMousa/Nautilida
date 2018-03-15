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
currentProfile = "None"       #Automatic or manual
wantedTimeInSeconds = 0
remainingTime = "0:00"          #Time running in seconds
remainingTimeInSeconds = 1
currentTime = "0:00"            #Current clock time
currentFlowRate = 0.0           #Current flow in GPM or LPM
totalWaterUsed = 0.0            #Total water used in Gallons or Liters
flowRateSystem = "GPM"          #GPM or LPM
waterUsedSystem = "Gallons"     #Gallons or Liters
currentRow = 0                  #Current Row
currentColumn = 0               #Current Column
inCreateShower = False          #In Create Shower or not
inputShowerLength = "1:00"      #Desired shower length
inputShowerLengthMinutes = 1    #Desired shower length in minutes
constantTemperature = True      #Constant temperature or not
currentIndex = 0
inShowerNameCreator = False
volumeCutoff = False            #Volume cutoff or not
volumeAtCutoff = 1              #Desired cutoff volume
inVariableTemperatureWizard = False
wizardMinutes = 0
inLoadShower = False
inEditShower = False
showerActive = False            #Shower active or not
wantedFlowRate = 1.0
currentHeatStep = 0
currentVolumeStep = 0
elapsedTime = 0
currentIndex = 0
TotLit = 0.0
currentTempIndex = 0

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
showerProfileVariableTemperature1 = []
showerProfileVariableTemperature2 = []
showerProfileVariableTemperature3 = []
showerProfileVariableTemperature4 = []

alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "␣", "'", "✓"]

### GUI DEFINITIONS ###
win = Tk()
win.title("Smart Shower")
win.geometry("480x320")
mainFont = tkinter.font.Font(family = "Helvetica", size = 35, weight = "bold")
subFont = tkinter.font.Font(family = "Helvetica", size = 18)
win.overrideredirect(True)
win.geometry("{0}x{1}+0+0".format(win.winfo_screenwidth(), win.winfo_screenheight()))

currentProfileLabel = Label()

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

loadShowerLabel0 = Label()

loadShowerLabel1 = Label()

loadShowerLabel2 = Label()

loadShowerLabel3 = Label()

loadShowerLabel4 = Label()

wantedFlowRateLabel = Label()

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
    currentProfileLabel.config(text = "Current Profile: " + currentProfile, font = subFont)
    wantedTemperatureLabel.config(text = "Wanted: " + str(wantedTemperature) + " °" + temperatureSystem, font = subFont)
    temperatureLabel.config(text = "Temperature", font = mainFont)
    timeLabel.config(text = "Time", font = mainFont)
    remainingTimeLabel.config(text = "Remaining: " + remainingTime, font = subFont)
    clockLabel.config(text = "Clock: " + currentTime, font = subFont)
    waterFlowLabel.config(text = "Water Flow", font = mainFont)
    currentFlowRateLabel.config(text = "Current Rate: " + str(currentFlowRate) + " " + flowRateSystem, font = subFont)
    totalWaterUsedLabel.config(text = "Total Used: " + str(totalWaterUsed) + " " + waterUsedSystem, font = subFont)
    
    screenLabel.place(x=250, y=0)
    currentProfileLabel.place(x=200, y=60)
    timeLabel.place(x=260, y=90)
    remainingTimeLabel.place(x=120, y=160)
    clockLabel.place(x=355, y=160)
    temperatureLabel.place(x=150, y=200)
    wantedTemperatureLabel.place(x=115, y=275)
    currentTemperatureLabel.place(x=355, y=275)
    waterFlowLabel.place(x=170, y=325)
    currentFlowRateLabel.place(x=35, y=395)
    totalWaterUsedLabel.place(x=345, y=395)
    if(showerActive == False):
        stopShowerButton.place_forget()
        startShowerButton.place(x=220, y=430)
    elif(showerActive == True):
        startShowerButton.place_forget()
        stopShowerButton.place(x=220, y=430)
    
    homeButton.place_forget()
    changeTemperatureSystemButton.place_forget()
    temperatureSystemLabel.place_forget()
    changeWaterSystemButton.place_forget()
    waterSystemLabel.place_forget()
    createNewShowerButton.place_forget()
    loadShowerButton.place_forget()
    editShowerButton.place_forget()
    wantedFlowRateLabel.place_forget()
    wantedFlowRateButton.place_forget()

    currentColumn = 0
    currentRow = 0
    os.system("xte 'mousemove 250 430'")
    
def myShowersPage():
    global currentScreen, currentColumn, currentRow
    currentScreen = "My Showers"
    screenLabel.config(text = currentScreen, font = mainFont)

    homeButton.place(x=10, y=10)
    screenLabel.place(x=150, y=90)
    createNewShowerButton.place(x=75, y=150)
    loadShowerButton.place(x=75, y=200)
    editShowerButton.place(x=75, y=250)
    
    currentProfileLabel.place_forget()
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
    loadShowerLabel0.place_forget()
    loadShowerLabel1.place_forget()
    loadShowerLabel2.place_forget()
    loadShowerLabel3.place_forget()
    loadShowerLabel4.place_forget()
    loadShowerButton0.place_forget()
    loadShowerButton1.place_forget()
    loadShowerButton2.place_forget()
    loadShowerButton3.place_forget()
    loadShowerButton4.place_forget()
    startShowerButton.place_forget()
    stopShowerButton.place_forget()

    currentColumn = 0
    currentRow = 0
    os.system("xte 'mousemove 20 20'")
    
def musicPage():
    global currentScreen, currentColumn, currentRow
    currentScreen = "Music"
    screenLabel.config(text = currentScreen, font = mainFont)

    homeButton.place(x=10, y=10)
    screenLabel.place(x=250, y=90)
    
    currentProfileLabel.place_forget()
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
    editShowerButton.place_forget()
    wantedFlowRateLabel.place_forget()
    wantedFlowRateButton.place_forget()

    currentColumn = 0
    currentRow = 0
    os.system("xte 'mousemove 20 20'")
    
def settingsPage():
    global currentScreen, currentColumn, currentRow
    currentScreen = "Settings"
    screenLabel.config(text = currentScreen, font = mainFont)
    temperatureSystemLabel.config(text = "Current Temperature System: °" + temperatureSystem, font = subFont)
    waterSystemLabel.config(text = "Current Water System: " + waterUsedSystem, font = subFont)
    wantedFlowRateLabel.config(text = str(wantedFlowRate) + " " + flowRateSystem, font = subFont)

    homeButton.place(x=10, y=10)
    screenLabel.place(x=210, y=90)
    changeTemperatureSystemButton.place(x=80, y=160)
    temperatureSystemLabel.place(x=120, y=220)
    changeWaterSystemButton.place(x=80, y=270)
    waterSystemLabel.place(x=130, y=330)
    wantedFlowRateButton.place(x=80, y= 380)
    wantedFlowRateLabel.place(x=250, y=440)
    
    currentProfileLabel.place_forget()
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
    
    currentProfileLabel.place_forget()
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
    startShowerButton.place_forget()
    stopShowerButton.place_forget()
    wantedFlowRateLabel.place_forget()
    wantedFlowRateButton.place_forget()

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
            if(inLoadShower == False):
                if(currentRow == 3):
                    musicPage()
                elif(currentRow == 2):
                    os.system("xte 'mousemove 100 275'")
                    currentRow = 3
                elif(currentRow == 1):
                    os.system("xte 'mousemove 100 225'")
                    currentRow = 2
                elif(currentRow == 0):
                    os.system("xte 'mousemove 100 175'")
                    currentRow = 1
            elif(inLoadShower == True):
                if(currentRow == 0):
                    if(showerProfile1["active"] == True):
                        os.system("xte 'mousemove 100 100'")
                        currentRow = 1
                elif(currentRow == 1):
                    if(showerProfile2["active"] == True):
                        os.system("xte 'mousemove 100 150'")
                        currentRow = 2
                elif(currentRow == 2):
                    if(showerProfile3["active"] == True):
                        os.system("xte 'mousemove 100 200'")
                        currentRow = 3
                elif(currentRow == 3):
                    if(showerProfile4["active"] == True):
                        os.system("xte 'mousemove 100 250'")
                        currentRow = 4
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
    elif(currentScreen == "My Showers" and direction == "Left"):
        if(inCreateShower == False):
            if(inLoadShower == False):
                if(currentRow == 0):
                    homePage()
                elif(currentRow == 3):
                    os.system("xte 'mousemove 100 225'")
                    currentRow = 2
                elif(currentRow == 2):
                    os.system("xte 'mousemove 100 175'")
                    currentRow = 1
                elif(currentRow == 1):
                    os.system("xte 'mousemove 20 20'")
                    currentRow = 0
            elif(inLoadShower == True):
                if(currentRow == 4):
                    if(showerProfile3["active"] == True):
                        os.system("xte 'mousemove 100 200'")
                        currentRow = 3
                elif(currentRow == 3):
                    if(showerProfile2["active"] == True):
                        os.system("xte 'mousemove 100 150'")
                        currentRow = 2
                elif(currentRow == 2):
                    if(showerProfile1["active"] == True):
                        os.system("xte 'mousemove 100 100'")
                        currentRow = 1
                elif(currentRow == 1):
                    if(showerProfile0["active"] == True):
                        os.system("xte 'mousemove 100 50'")
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
    elif(currentScreen == "Music" and direction == "Right"):
        settingsPage()
    elif(currentScreen == "Music" and direction == "Left"):
        myShowersPage()
    elif(currentScreen == "Settings" and direction == "Right"):
        if(currentRow == 3):
            helpPage()
        elif(currentRow == 0):
            os.system("xte 'mousemove 100 175'")
            currentRow = 1
        elif(currentRow == 1):
            os.system("xte 'mousemove 100 275'")
            currentRow = 2
        elif(currentRow == 2):
            os.system("xte 'mousemove 100 400'")
            currentRow = 3
    elif(currentScreen == "Settings" and direction =="Left"):
        if(currentRow == 0):
            musicPage()
        elif(currentRow == 3):
            os.system("xte 'mousemove 100 275'")
            currentRow = 2
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
    wantedFlowRateLabel.config(text = str(wantedFlowRate) + " " + flowRateSystem, font = subFont)

def createNewShower():
    global inCreateShower, inputShowerLength, currentRow
    if(showerProfile0["active"] == False or showerProfile1["active"] == False or showerProfile2["active"] == False or showerProfile3["active"] == False or showerProfile4["active"] == False):
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
        editShowerButton.place_forget()

        inCreateShower = True
        os.system("xte 'mousemove 100 50'")
        currentRow = 0

        if(showerProfile0["active"] == False):
            showerProfile0["current"] = True
        elif(showerProfile1["active"] == False):
            showerProfile1["current"] = True
        elif(showerProfile2["active"] == False):
            showerProfile2["current"] = True
        elif(showerProfile3["active"] == False):
            showerProfile3["current"] = True
        elif(showerProfile4["active"] == False):
            showerProfile4["current"] = True
    else:
        myShowersPage()
    
def cancelNewShower():
    global inCreateShower
    myShowersPage()
    inCreateShower = False

def saveNewShower():
    global wantedTemperature, inCreateShower, showerProfile0, showerProfile1, showerProfile2, showerProfile3, showerProfile4
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
        showerProfile0["active"] = True
    elif(showerProfile1["active"] == False):
        if(constantTemperature == True):
            showerProfile1["constant"] = True
            showerProfile1["tempIfConstant"] = wantedTemperature
        elif(constantTemperature == False):
            showerProfile1["constant"] = False
        showerProfile1["name"] = "".join(showerProfileName1)
        showerProfile1["length"] = inputShowerLengthMinutes
        if(volumeCutoff == True):
            showerProfile1["volumeCutoff"] = True
            showerProfile1["volumeIfCutoff"] = volumeAtCutoff
        elif(volumeCutoff == False):
            showerProfile1["volumeCutoff"] = False
        showerProfile1["active"] = True
    elif(showerProfile2["active"] == False):
        if(constantTemperature == True):
            showerProfile2["constant"] = True
            showerProfile2["tempIfConstant"] = wantedTemperature
        elif(constantTemperature == False):
            showerProfile2["constant"] = False
        showerProfile2["name"] = "".join(showerProfileName2)
        showerProfile2["length"] = inputShowerLengthMinutes
        if(volumeCutoff == True):
            showerProfile2["volumeCutoff"] = True
            showerProfile2["volumeIfCutoff"] = volumeAtCutoff
        elif(volumeCutoff == False):
            showerProfile2["volumeCutoff"] = False
        showerProfile2["active"] = True
    elif(showerProfile3["active"] == False):
        if(constantTemperature == True):
            showerProfile3["constant"] = True
            showerProfile3["tempIfConstant"] = wantedTemperature
        elif(constantTemperature == False):
            showerProfile3["constant"] = False
        showerProfile3["name"] = "".join(showerProfileName3)
        showerProfile3["length"] = inputShowerLengthMinutes
        if(volumeCutoff == True):
            showerProfile3["volumeCutoff"] = True
            showerProfile3["volumeIfCutoff"] = volumeAtCutoff
        elif(volumeCutoff == False):
            showerProfile3["volumeCutoff"] = False
        showerProfile3["active"] = True
    elif(showerProfile4["active"] == False):
        if(constantTemperature == True):
            showerProfile4["constant"] = True
            showerProfile4["tempIfConstant"] = wantedTemperature
        elif(constantTemperature == False):
            showerProfile4["constant"] = False
        showerProfile4["name"] = "".join(showerProfileName4)
        showerProfile4["length"] = inputShowerLengthMinutes
        if(volumeCutoff == True):
            showerProfile4["volumeCutoff"] = True
            showerProfile4["volumeIfCutoff"] = volumeAtCutoff
        elif(volumeCutoff == False):
            showerProfile4["volumeCutoff"] = False
        showerProfile4["active"] = True
    showerProfile0["current"] = False
    showerProfile1["current"] = False
    showerProfile2["current"] = False
    showerProfile3["current"] = False
    showerProfile4["current"] = False
    myShowersPage()
    inCreateShower = False

######################################################################
def loadShower():
    global inLoadShower, currentRow, showerProfile0, showerProfile1, showerProfile2, showerProfile3, showerProfile4
    inLoadShower = True
    if(showerProfile0["active"] == True):
        loadShowerButton0.place(x=50, y=50)
        loadShowerLabel0.config(text = showerProfile0["name"], font = subFont)
        loadShowerLabel0.place(x=300, y=55)
    if(showerProfile1["active"] == True):
        loadShowerButton1.place(x=50, y=100)
        loadShowerLabel1.config(text = showerProfile1["name"], font = subFont)
        loadShowerLabel1.place(x=300, y=105)
    if(showerProfile2["active"] == True):
        loadShowerButton2.place(x=50, y=150)
        loadShowerLabel2.config(text = showerProfile2["name"], font = subFont)
        loadShowerLabel2.place(x=300, y=155)
    if(showerProfile3["active"] == True):
        loadShowerButton3.place(x=50, y=200)
        loadShowerLabel3.config(text = showerProfile3["name"], font = subFont)
        loadShowerLabel3.place(x=300, y=205)
    if(showerProfile4["active"] == True):
        loadShowerButton4.place(x=50, y=250)
        loadShowerLabel4.config(text = showerProfile4["name"], font = subFont)
        loadShowerLabel4.place(x=300, y=255)

    os.system("xte 'mousemove 100 50'")
    currentRow = 0

    showerProfile0["current"] = False
    showerProfile1["current"] = False
    showerProfile2["current"] = False
    showerProfile3["current"] = False
    showerProfile4["current"] = False
    
    homeButton.place_forget()
    screenLabel.place_forget()
    createNewShowerButton.place_forget()
    loadShowerButton.place_forget()
    editShowerButton.place_forget()

def loadShower0():
    global inLoadShower, constantTemperature, wantedTemperature, volumeCutoff, volumeAtCutoff, showerProfile0, wantedTimeInSeconds, currentProfile
    if(showerProfile0["constant"] == True):
        constantTemperature = True
        wantedTemperature = showerProfile0["tempIfConstant"]
    elif(showerProfile0["constant"] == False):
        constantTemperature = False
        wantedTemperature = showerProfileVariableTemperature0[0]
    if(showerProfile0["volumeCutoff"] == True):
        volumeCutoff = True
        volumeAtCutoff = showerProfile0["volumeIfCutoff"]
    elif(showerProfile0["volumeCutoff"] == False):
        volumeCutoff = False
    currentProfile = showerProfile0["name"]
    currentProfileLabel.config(text = "Current Profile: " + currentProfile, font = subFont)
    wantedTimeInSeconds = (showerProfile0["length"] * 60)
    showerProfile0["current"] = True
    inLoadShower = False
    myShowersPage()
    print(showerProfileVariableTemperature0)
    print("Load Shower 0")

def loadShower1():
    global inLoadShower, constantTemperature, wantedTemperature, volumeCutoff, volumeAtCutoff, showerProfile1, wantedTimeInSeconds, currentProfile
    if(showerProfile1["constant"] == True):
        constantTemperature = True
        wantedTemperature = showerProfile1["tempIfConstant"]
    elif(showerProfile1["constant"] == False):
        constantTemperature = False
        wantedTemperature = showerProfileVariableTemperature1[0]
    if(showerProfile1["volumeCutoff"] == True):
        volumeCutoff = True
        volumeAtCutoff = showerProfile1["volumeIfCutoff"]
    elif(showerProfile1["volumeCutoff"] == False):
        volumeCutoff = False
    currentProfile = showerProfile1["name"]
    currentProfileLabel.config(text = "Current Profile: " + currentProfile, font = subFont)
    wantedTimeInSeconds = (showerProfile1["length"] * 60)
    showerProfile1["current"] = True
    inLoadShower = False
    myShowersPage()
    print("Load Shower 1")

def loadShower2():
    global inLoadShower, constantTemperature, wantedTemperature, volumeCutoff, volumeAtCutoff, showerProfile2, wantedTimeInSeconds, currentProfile
    if(showerProfile2["constant"] == True):
        constantTemperature = True
        wantedTemperature = showerProfile2["tempIfConstant"]
    elif(showerProfile2["constant"] == False):
        constantTemperature = False
        wantedTemperature = showerProfileVariableTemperature2[0]
    if(showerProfile2["volumeCutoff"] == True):
        volumeCutoff = True
        volumeAtCutoff = showerProfile2["volumeIfCutoff"]
    elif(showerProfile2["volumeCutoff"] == False):
        volumeCutoff = False
    currentProfile = showerProfile2["name"]
    currentProfileLabel.config(text = "Current Profile: " + currentProfile, font = subFont)
    wantedTimeInSeconds = (showerProfile2["length"] * 60)
    showerProfile2["current"] = True
    inLoadShower = False
    myShowersPage()
    print("Load Shower 2")

def loadShower3():
    global inLoadShower, constantTemperature, wantedTemperature, volumeCutoff, volumeAtCutoff, showerProfile3, wantedTimeInSeconds, currentProfile
    if(showerProfile3["constant"] == True):
        constantTemperature = True
        wantedTemperature = showerProfile3["tempIfConstant"]
    elif(showerProfile3["constant"] == False):
        constantTemperature = False
        wantedTemperature = showerProfileVariableTemperature3[0]
    if(showerProfile3["volumeCutoff"] == True):
        volumeCutoff = True
        volumeAtCutoff = showerProfile3["volumeIfCutoff"]
    elif(showerProfile3["volumeCutoff"] == False):
        volumeCutoff = False
    currentProfile = showerProfile3["name"]
    currentProfileLabel.config(text = "Current Profile: " + currentProfile, font = subFont)
    wantedTimeInSeconds = (showerProfile3["length"] * 60)
    showerProfile3["current"] = True
    inLoadShower = False
    myShowersPage()
    print("Load Shower 3")

def loadShower4():
    global inLoadShower, constantTemperature, wantedTemperature, volumeCutoff, volumeAtCutoff, showerProfile4, wantedTimeInSeconds, currentProfile
    if(showerProfile4["constant"] == True):
        constantTemperature = True
        wantedTemperature = showerProfile4["tempIfConstant"]
    elif(showerProfile4["constant"] == False):
        constantTemperature = False
        wantedTemperature = showerProfileVariableTemperature4[0]
    if(showerProfile4["volumeCutoff"] == True):
        volumeCutoff = True
        volumeAtCutoff = showerProfile4["volumeIfCutoff"]
    elif(showerProfile4["volumeCutoff"] == False):
        volumeCutoff = False
    currentProfile = showerProfile4["name"]
    currentProfileLabel.config(text = "Current Profile: " + currentProfile, font = subFont)
    wantedTimeInSeconds = (showerProfile4["length"] * 60)
    showerProfile4["current"] = True
    inLoadShower = False
    myShowersPage()
    print("Load Shower 4")

def editShower():
    global inEditShower
    inEditShower = True
    print("Edit Shower")

    homeButton.place_forget()
    screenLabel.place_forget()
    createNewShowerButton.place_forget()
    loadShowerButton.place_forget()
    editShowerButton.place_forget()

def changeConstantTemperature():
    global constantTemperature, wizardMinutes, showerProfileVariableTemperature0, showerProfileVariableTemperature1, showerProfileVariableTemperature2, showerProfileVariableTemperature3, showerProfileVariableTemperature4
    if(inVariableTemperatureWizard == False):
        if(constantTemperature == True):
            constantTemperature = False
            if(showerProfile0["current"] == True):
                showerProfileVariableTemperature0 = []
                print("yes")
            elif(showerProfile1["current"] == True):
                showerProfileVariableTemperature1 = []
            elif(showerProfile2["current"] == True):
                showerProfileVariableTemperature2 = []
            elif(showerProfile3["current"] == True):
                showerProfileVariableTemperature3 = []
            elif(showerProfile4["current"] == True):
                showerProfileVariableTemperature4 = []
            constantTemperatureLabel.config(text = "No", font = subFont)
            wizardMinutes = 1
            variableTemperatureWizard()
        elif(constantTemperature == False):
            constantTemperature = True
            constantTemperatureLabel.config(text = "Yes: " + str(wantedTemperature) + " °" + temperatureSystem, font = subFont)
    elif(inVariableTemperatureWizard == True):
        wizardMinutes += 1
        variableTemperatureWizard()
        
def variableTemperatureWizard():
    global wizardMinutes, inVariableTemperatureWizard
    if(wizardMinutes != (inputShowerLengthMinutes + 1)):
        inVariableTemperatureWizard = True
        if(wizardMinutes == 1):
            temperatureAtTimeLabel.config(text = "Temperature at " + str(wizardMinutes) + " Minute: " + str(wantedTemperature) + " °" + temperatureSystem, font = subFont)
        else:
            temperatureAtTimeLabel.config(text = "Temperature at " + str(wizardMinutes) + " Minutes: " + str(wantedTemperature) + " °" + temperatureSystem, font = subFont)
            if(showerProfile0["current"] == True):
                showerProfileVariableTemperature0.append(wantedTemperature)
            elif(showerProfile1["current"] == True):
                showerProfileVariableTemperature1.append(wantedTemperature)
            elif(showerProfile2["current"] == True):
                showerProfileVariableTemperature2.append(wantedTemperature)
            elif(showerProfile3["current"] == True):
                showerProfileVariableTemperature3.append(wantedTemperature)
            elif(showerProfile4["current"] == True):
                showerProfileVariableTemperature4.append(wantedTemperature)
        temperatureAtTimeLabel.place(x=50, y=300)
        print(showerProfileVariableTemperature0)
        print(showerProfileVariableTemperature1)
    elif(wizardMinutes == (inputShowerLengthMinutes + 1)):
        showerProfileVariableTemperature0.append(wantedTemperature)
        inVariableTemperatureWizard = False
        temperatureAtTimeLabel.place_forget()
#############################################################################################
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
##########################################################################
def appendShowerName():
    global inShowerNameCreator, direction
    global showerProfileName0, showerProfileName1, showerProfileName2, showerProfileName3, showerProfileName4
    if(inShowerNameCreator == False):
        inShowerNameCreator = True
        if(showerProfile0["current"] == True):
            showerProfileName0 = []
        elif(showerProfile1["current"] == True):
            showerProfileName1 = []
        elif(showerProfile2["current"] == True):
            showerProfileName2 = []
        elif(showerProfile3["current"] == True):
            showerProfileName3 = []
        elif(showerProfile4["current"] == True):
            showerProfileName4 = []
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

def startShower():
    global showerActive, constantTemperature, remainingTimeInSeconds
    showerActive = True
    homePage()
    remainingTimeInSeconds = wantedTimeInSeconds
    if(currentProfile == "None"):
        constantTemperature = False
        checkTemperature()
        checkFlowRate()
    elif(constantTemperature == True):
        checkTemperature()
        checkFlowRate()
        updateRemainingTime()
    else:
        checkVariableTemperature()
        checkFlowRate()
        updateRemainingTime()
    print("Start Shower")

def stopShower():
    global showerActive, constantTemperature, remainingTime, currentIndex, currentFlowRate, totalWaterUsed, TotLit, tot_cnt
    currentIndex = 0
    showerActive = False
    shutOffHeat()
    shutOffVolume()
    remainingTime = "0:00"
    remainingTimeLabel.config(text = "Remaining: " + remainingTime, font = subFont)
    homePage()
    constantTemperature = True
    currentFlowRate = 0.0
    totalWaterUsed = 0.0
    TotLit = 0.0
    tot_cnt = 0
    print("Stop Shower")    

def checkFlowRate():
    global showerActive
    if(showerActive == True):
        if(inCreateShower == False):
            getWaterFlow()
            if(currentFlowRate < wantedFlowRate):
                volumeValve("Higher")
            elif(currentFlowRate > wantedFlowRate):
                volumeValve("Lower")
            if(totalWaterUsed >= volumeAtCutoff):
                if(currentProfile != "None"):
                    stopShower()
            win.after(1000, checkFlowRate)
  
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

editShowerButton = Button(win, text = "Edit Shower", font = subFont, command=editShower, bg="dim gray", height=1, width=30)

loadShowerButton0 = Button(win, text = "Load", font = subFont, command=loadShower0, bg="dim gray", height=1, width=10)

loadShowerButton1 = Button(win, text = "Load", font = subFont, command=loadShower1, bg="dim gray", height=1, width=10)

loadShowerButton2 = Button(win, text = "Load", font = subFont, command=loadShower2, bg="dim gray", height=1, width=10)

loadShowerButton3 = Button(win, text = "Load", font = subFont, command=loadShower3, bg="dim gray", height=1, width=10)

loadShowerButton4 = Button(win, text = "Load", font = subFont, command=loadShower4, bg="dim gray", height=1, width=10)

startShowerButton = Button(win, text = "Start Shower", font = subFont, command=startShower, bg="dim gray", height=1, width=12)

stopShowerButton = Button(win, text = "Stop Shower", font = subFont, command=stopShower, bg="dim gray", height=1, width=12)

wantedFlowRateButton = Button(win, text = "Wanted Flow Rate:", font = subFont, bg="dim gray", height=1, width=30)

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
    global wantedTemperature, inputShowerLengthMinutes, inputShowerLength, wantedFlowRate
    global Rotary_counter, LockRotary, NewCounter, currentIndex, volumeAtCutoff							# Current Volume
    LockRotary.acquire()					# get lock for rotary switch
    NewCounter = Rotary_counter			# get counter value
    Rotary_counter = 0						# RESET IT TO 0
    LockRotary.release()					# and release lock					
    if (NewCounter !=0):
        if(currentScreen == "Home"):
            if(currentProfile == "None"):
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
                    if(wizardMinutes == 1):
                        temperatureAtTimeLabel.config(text = "Temperature at " + str(wizardMinutes) + " Minute: " + str(wantedTemperature) + " °" + temperatureSystem, font = subFont)
                    elif(wizardMinutes > 1):
                        temperatureAtTimeLabel.config(text = "Temperature at " + str(wizardMinutes) + " Minutes: " + str(wantedTemperature) + " °" + temperatureSystem, font = subFont)
                elif(currentRow == 3 and volumeCutoff == True):
                    volumeAtCutoff += NewCounter
                    if(volumeAtCutoff < 1):
                        volumeAtCutoff = 1
                    elif(volumeAtCutoff > 100):
                        volumeAtCutoff = 100
                    volumeCutoffLabel.config(text = "Yes: " + str(volumeAtCutoff) + " " + waterUsedSystem, font = subFont)
        elif(currentScreen == "Settings"):
            if(currentRow == 3):
                wantedFlowRate += (NewCounter * 0.5)
                if(wantedFlowRate < 0.5):
                    wantedFlowRate = 0.5
                elif(wantedFlowRate > 20.0):
                    wantedFlowRate = 20.0
                wantedFlowRateLabel.config(text = str(wantedFlowRate) + " " + flowRateSystem, font = subFont)
    win.after(100, rotaryInput)

###Temperature Probe###

os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-0417c1c235ff')[0]
device_file = device_folder + '/w1_slave'
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    global currentTemperature
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
    if(showerActive == True):
        if(inCreateShower == False):
            if(currentTemperature < wantedTemperature):
                heatValve("Hot")
            elif(currentTemperature > wantedTemperature):
                heatValve("Cold")
        win.after(3000, checkTemperature)

def checkVariableTemperature():
    global currentTemperature, elapsedTime, currentTempIndex, wantedTemperature
    read_temp()
    if(showerActive == True):
        if(elapsedTime >= 60):
            elapsedTime = 0
            currentTempIndex += 1
        if(showerProfile0["current"] == True):
            if(currentTemperature < showerProfileVariableTemperature0[currentTempIndex]):
                heatValve("Hot")
            elif(currentTemperature > showerProfileVariableTemperature0[currentTempIndex]):
                heatValve("Cold")
            wantedTemperature = showerProfileVariableTemperature0[currentTempIndex]
        elif(showerProfile1["current"] == True):
            if(currentTemperature < showerProfileVariableTemperature1[currentTempIndex]):
                heatValve("Hot")
            elif(currentTemperature > showerProfileVariableTemperature1[currentTempIndex]):
                heatValve("Cold")
            wantedTemperature = showerProfileVariableTemperature1[currentTempIndex]
        elif(showerProfile2["current"] == True):
            if(currentTemperature < showerProfileVariableTemperature2[currentTempIndex]):
                heatValve("Hot")
            elif(currentTemperature > showerProfileVariableTemperature2[currentTempIndex]):
                heatValve("Cold")
            wantedTemperature = showerProfileVariableTemperature2[currentTempIndex]
        elif(showerProfile3["current"] == True):
            if(currentTemperature < showerProfileVariableTemperature3[currentTempIndex]):
                heatValve("Hot")
            elif(currentTemperature > showerProfileVariableTemperature3[currentTempIndex]):
                heatValve("Cold")
            wantedTemperature = showerProfileVariableTemperature3[currentTempIndex]
        elif(showerProfile0["current"] == True):
            if(currentTemperature < showerProfileVariableTemperature4[currentTempIndex]):
                heatValve("Hot")
            elif(currentTemperature > showerProfileVariableTemperature4[currentTempIndex]):
                heatValve("Cold")
            wantedTemperature = showerProfileVariableTemperature4[currentTempIndex]
        win.after(3000, checkVariableTemperature)

def updateTemperature():
    global currentTemperature
    if(currentScreen == "Home"):
        wantedTemperatureLabel.config(text = "Wanted: " + str(wantedTemperature) + " °" + temperatureSystem, font = subFont)
        currentTemperatureLabel.config(text = "Current: " + str(currentTemperature) + " °" + temperatureSystem, font = subFont)
    win.after(100, updateTemperature)
    
###Valve Turning###
    
DIR_H = 32   # Direction GPIO Pin
DIR_V = 36
STEP_H = 31  # Step GPIO Pin
STEP_V = 35
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 48   # Steps per Revolution (360 / 7.5)

GPIO.setup(DIR_H, GPIO.OUT)
GPIO.setup(STEP_H, GPIO.OUT)
GPIO.setup(DIR_V, GPIO.OUT)
GPIO.setup(STEP_V, GPIO.OUT)

step_count = SPR
step_count_H = 0
step_count_V = 0
delay = .001

heatValveMinimum = 0
heatValveMaximum = 1200
volumeValveMinimum = 0
volumeValveMaximum = 200

def heatValve(hotORcold):
    global step_count_H, currentHeatStep, currentVolumeStep
    valveDirection = "CW"
    if((currentTemperature - wantedTemperature) > 0):
        valveDirection = "CCW"
    elif((currentTemperature - wantedTemperature) < 0):
        valveDirection = "CW"
    difference = abs(currentTemperature - wantedTemperature)
    if(difference > 10):
        step_count_H = 200
    elif(difference <= 10):
        step_count_H = 50
    if((currentHeatStep + step_count_H) >= heatValveMinimum and (currentHeatStep + step_count_H) <= heatValveMaximum and valveDirection == "CW"):
        if(hotORcold == "Hot"):
            GPIO.output(DIR_H, CCW)
            for x in range(step_count_H):
                GPIO.output(STEP_H, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(STEP_H, GPIO.LOW)
                time.sleep(delay)
                currentHeatStep += 1
    elif((currentHeatStep - step_count_H) >= heatValveMinimum and (currentHeatStep - step_count_H) <= heatValveMaximum and valveDirection == "CCW"):
        if(hotORcold == "Cold"):
            GPIO.output(DIR_H, CW)
            for x in range(step_count_H):
                GPIO.output(STEP_H, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(STEP_H, GPIO.LOW)
                time.sleep(delay)
                currentHeatStep -= 1

def shutOffHeat():
    global currentHeatStep
    GPIO.output(DIR_H, CW)
    for x in range((currentHeatStep) + 200):
        GPIO.output(STEP_H, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_H, GPIO.LOW)
        time.sleep(delay)
    currentHeatStep = 0

def shutOffVolume():
    global currentVolumeStep
    GPIO.output(DIR_V, CCW)
    for x in range((currentVolumeStep) + 200):
        GPIO.output(STEP_V, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_V, GPIO.LOW)
        time.sleep(delay)
    currentVolumeStep = 0

def volumeValve(higherORlower):
    global step_count_V, currentHeatStep, currentVolumeStep
    valveDirection = "CW"
    if((currentFlowRate - wantedFlowRate) > 0):
        valveDirection = "CCW"
    elif((currentFlowRate - wantedFlowRate) < 0):
        valveDirection = "CW"
    difference = abs(currentFlowRate - wantedFlowRate)
    if(difference > 2.0):
        step_count_V = 50
    elif(difference <= 2.0):
        step_count_V = 20
    if((currentVolumeStep + step_count_V) >= volumeValveMinimum and (currentVolumeStep + step_count_V) <= volumeValveMaximum and valveDirection == "CW"):
        if(higherORlower == "Higher"):
            GPIO.output(DIR_V, CW)
            for x in range(step_count_V):
                GPIO.output(STEP_V, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(STEP_V, GPIO.LOW)
                time.sleep(delay)
                currentVolumeStep += 1
    elif((currentVolumeStep - step_count_V) >= volumeValveMinimum and (currentVolumeStep - step_count_V) <= volumeValveMaximum and valveDirection == "CCW"):
        if(higherORlower == "Lower"):
            GPIO.output(DIR_V, CCW)
            for x in range(step_count_V):
                GPIO.output(STEP_V, GPIO.HIGH)
                time.sleep(delay)
                GPIO.output(STEP_V, GPIO.LOW)
                time.sleep(delay)
                currentVolumeStep -= 1

        
###Flow Meter###
        
inpt = 33
GPIO.setup(inpt, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
minutes = 0
constant = 0.006
time_new = 0.0
rpt_int = 1

global rate_cnt, tot_cnt
rate_cnt = 0
tot_cnt = 0

def getWaterFlow():
    global rate_cnt, tot_cnt, minutes, constant, time_new, rpt_int, currentFlowRate, totalWaterUsed, TotLit
    time_new = time.time() + rpt_int
    rate_cnt = 0
    while time.time() <= time_new:

        minutes += 1

    LperM = round(((rate_cnt * constant)/(rpt_int/60)),2)
    TotLit = round(tot_cnt * constant,1)

    if(flowRateSystem == "LPM" and waterUsedSystem == "Liters"):
        currentFlowRate = round(LperM,1)
        totalWaterUsed = round(TotLit,1)
        currentFlowRateLabel.config(text = "Current Rate: " + str(currentFlowRate) + " " + flowRateSystem, font = subFont)
        totalWaterUsedLabel.config(text = "Total Used: " + str(totalWaterUsed) + " " + waterUsedSystem, font = subFont)
    elif(flowRateSystem == "GPM" and waterUsedSystem == "Gallons"):
        currentFlowRate = round(LperM * 0.26417287472922,1)
        totalWaterUsed = round(TotLit * 0.26417287472922,1)
        currentFlowRateLabel.config(text = "Current Rate: " + str(currentFlowRate) + " " + flowRateSystem, font = subFont)
        totalWaterUsedLabel.config(text = "Total Used: " + str(totalWaterUsed) + " " + waterUsedSystem, font = subFont)
        
def Pulse_cnt(inpt_pin):
    global rate_cnt, tot_cnt
    rate_cnt += 1
    tot_cnt += 1

GPIO.add_event_detect(inpt, GPIO.FALLING, callback = Pulse_cnt, bouncetime = 10)


###Time Functions###
def updateClock():
    global currentTime
    if(currentScreen == "Home"):
        if(datetime.now().hour <= 12):
            currentHour = datetime.now().hour
        elif(datetime.now().hour > 12):
            currentHour = (datetime.now().hour - 11)
        if(datetime.now().hour == 0):
            currentHour = 12
        currentMinute = datetime.now().minute
        if(currentMinute < 10):
            currentTime = "%s:0%s" % (str(currentHour), str(currentMinute))
        elif(currentMinute >= 10):
            currentTime = "%s:%s" % (str(currentHour), str(currentMinute))
        clockLabel.config(text = "Clock: " + currentTime, font = subFont)
    win.after(5000, updateClock)
    
def updateRemainingTime():
    global remainingTimeInSeconds, remainingTime, showerActive, elapsedTime
    if(currentProfile != "None"):
        if(showerActive == True):
            if((remainingTimeInSeconds % 60) != 0):
                if((remainingTimeInSeconds % 60) >= 10):
                    remainingTime = "%s:%s" % (str(int(((remainingTimeInSeconds - (remainingTimeInSeconds % 60)) / 60))), str((remainingTimeInSeconds % 60)))
                else:
                    remainingTime = "%s:0%s" % (str(int(((remainingTimeInSeconds - (remainingTimeInSeconds % 60)) / 60))), str((remainingTimeInSeconds % 60)))
            else:
                remainingTime = "%s:0%s" % (str(int(((remainingTimeInSeconds - (remainingTimeInSeconds % 60)) / 60))), str((remainingTimeInSeconds % 60)))
            remainingTimeLabel.config(text = "Remaining: " + remainingTime, font = subFont)
            remainingTimeInSeconds -= 1
            elapsedTime += 1
        if(remainingTimeInSeconds <= 0):
            stopShower()
        if(showerActive == True):
            win.after(1000, updateRemainingTime)
win.after(100, MainCode)
win.after(50, rotaryInput)
win.after(100, updateTemperature)
win.after(1000, updateClock)
win.mainloop() # Loops forever
