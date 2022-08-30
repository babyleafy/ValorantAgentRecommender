import tkinter as tk
from tkinter import *
from bs4 import BeautifulSoup
import requests
import time
import os
import re
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

# Main Frame ------------------------------------------------------------------
root = tk.Tk()
root.title('Valorant Agent Composition Helper')  # Application Title
root.geometry("480x630")  # Application Window size
root.resizable(False, False)  # No resizing window
root.iconbitmap(r"icons/valorant.ico")  # Application Icon

canvas1 = tk.Canvas(root, width=480, height=630, bg='black')
bgPhoto = PhotoImage(file="icons/Bg.png")
canvas1.create_image(0, 0, image=bgPhoto, anchor=NW)
canvas1.pack()

global labelSelAgents
labelSelAgents = tk.Label(root, text='')
global labelResult
labelResult = tk.Label(root, text='')

labelTitle = tk.Label(root, text='Valorant Agent Recommender', bg='black')
labelTitle.config(font=('helvetica', 16, 'bold'), fg='white')
canvas1.create_window(240, 30, window=labelTitle)

labelDate = tk.Label(root, text='(July 2022)', bg='black')
labelDate.config(font=('helvetica', 11), fg='white')
canvas1.create_window(240, 52, window=labelDate)

labelDirection = tk.Label(root, text='Choose up to 4 agents:', bg='black')
labelDirection.config(font=('helvetica', 10, 'bold'), fg='white')
canvas1.create_window(240, 185, window=labelDirection)

labelResultMarker = tk.Label(root, text='Possible filler agents:', bg='black')
labelResultMarker.config(font=('helvetica', 11, 'bold'), fg='white')
canvas1.create_window(240, 520, window=labelResultMarker)

labelResult = tk.Label(root, text='', bg='black')
labelResult.config(font=('helvetica', 10), fg='white')
canvas1.create_window(240, 550, window=labelResult)

# Search bar
labelSearchTeam = tk.Label(root, text='Search a team:', bg='black')
labelSearchTeam.config(font=('helvetica', 10, 'bold'), fg='white')
canvas1.create_window(240, 390, window=labelSearchTeam)
entryBox = tk.Entry(root, font=('helvetica', 10), bg='black', fg='white', insertbackground='white')
canvas1.create_window(215, 410, window=entryBox)

# Update the search list for team search
teams = ['OpTic Gaming', 'FaZe Clan', 'Sentinels', 'Cloud9', 'FNATIC', 'FunPlus Phoenix', 'Guild Esports',
         'M3 Champions', 'Team Liquid', 'Paper Rex', 'DRX', 'XERXIA Esports', 'LOUD', 'KRU Esports', 'Zeta Division',
         'NRG', 'Acend', 'G2 Esports', 'Evil Geniuses', '100 Thieves', 'Ghost Gaming',
         'The Guard', 'Ninjas in Pyjamas', 'DAMWON Gaming']
# Listbox and scroll frame
scrollFrame = tk.Frame(root)
scrollbar = tk.Scrollbar(scrollFrame, orient=VERTICAL)
listBox = tk.Listbox(scrollFrame, width=20, height=4, bg='black', fg='white', yscrollcommand=scrollbar.set)
scrollbar.config(command=listBox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listBox.pack(fill=Y)
canvas1.create_window(215, 455, window=scrollFrame)


# Scrollbar and search helper functions
def update(data):  # updates listbox
    listBox.delete(0, END)
    for item in data:
        listBox.insert(END, item)


def fillout(e):  # fills entry when listbox item is clicked
    entryBox.delete(0, END)
    entryBox.insert(0, listBox.get(ANCHOR))


def check(e):  # updates listbox when typing
    typed = entryBox.get()
    if typed == '':
        data = teams
        buttonFull['state'] = 'normal'
        buttonFill['state'] = 'normal'
    else:
        data = []
        for item in teams:
            if typed.lower() in item.lower():
                data.append(item)
    update(data)


update(teams)
listBox.bind('<<ListboxSelect>>', fillout)
entryBox.bind('<KeyRelease>', check)


# Secondary Frames -------------------------------------------------------------
def disable_event():
    pass


# update check Window
updateWindow = Toplevel(root, bg='black')
updateWindow.title("[Update]")
tUpdate = "A newer version has been detected. Please update to the latest version."
mFill = Message(updateWindow, text=tUpdate, width=380,
                bg="black", font=('helvetica', 12, 'bold'), fg='white').pack(side=TOP, anchor=N)
okButtonUpdate = tk.Button(updateWindow, height=1, width=8, text='Ok',
                           bg='red', fg='white', font=('helvetica', 9, 'bold'), activebackground="#292929",
                           command=lambda: [helpMenuOnclicks(""), updateWindow.withdraw(), os.system(
                               "start \"\" https://github.com/babyleafy/ValorantAgentRecommender")])
okButtonUpdate.pack(side=BOTTOM, anchor=S)

# fillButton Help Dropdown Window
fillWindow = Toplevel(root, bg='black')
fillWindow.title('[Help] Fill Button')
tFill = "• The fill button will recommend the remaining agents in a composition based off pro teams." \
        "\n\n• A map, region, and at least one agent must be selected"
mFill = Message(fillWindow, text=tFill, width=380, bg="black", font=('helvetica', 12, 'bold'), fg='white')
mFill.pack(side=TOP, anchor=N)
okButtonFill = tk.Button(fillWindow, height=1, width=8, text='Ok', bg='red', fg='white', font=('helvetica', 9, 'bold'),
                         activebackground="#292929", command=lambda: [helpMenuOnclicks("")])
okButtonFill.pack(side=BOTTOM, anchor=S)

# fullButton Help Dropdown Window
fullWindow = Toplevel(root, bg='black')
fullWindow.title("[Help] Full Button")
tFull = "• The full button will return a full team composition based on the selected team."
mFull = Message(fullWindow, text=tFull, width=380, bg="black", font=('helvetica', 12, 'bold'), fg='white').pack(
    side=TOP, anchor=N)
okButtonFull = tk.Button(fullWindow, height=1, width=8, text='Ok', bg='red', fg='white', font=('helvetica', 9, 'bold'),
                         activebackground="#292929", command=lambda: [helpMenuOnclicks("")])
okButtonFull.pack(side=BOTTOM, anchor=S)


# Help Menu Dropdown Functionality
def helpMenuOnclicks(string):
    x = root.winfo_rootx() + 380
    y = root.winfo_rooty() - 50
    for menuButton in menuButtons:
        menuButton.withdraw()
        menuButton.protocol("WM_DELETE_WINDOW", disable_event)
        menuButton.resizable(False, False)
        menuButton.transient(root)
        menuButton.iconbitmap("icons/valorant.ico")
        menuButton.geometry(f'400x150+{x}+{y}')
    match string:
        case "Fill":
            fillWindow.deiconify()
        case "Full":
            fullWindow.deiconify()
        case "Link":
            os.system("start \"\" https://github.com/babyleafy/ValorantAgentRecommender")


# Creating the Help Menu Widget
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Fill button", command=lambda: [helpMenuOnclicks("Fill")])
filemenu.add_command(label="Full button", command=lambda: [helpMenuOnclicks("Full")])
filemenu.add_command(label="Take me to the Instructions on GitHub", command=lambda: [helpMenuOnclicks("Link")])
menubar.add_cascade(label="Help", menu=filemenu)


# MAP, REGION, AGENT BUTTONS -------------------------------------------------------------------------------
# Select Map (Disables the pressed map button and re-enables the rest)
def selectMap(mapz, button):
    map.clear()
    map.append(mapz)
    recommended.clear()
    labelResult.destroy()
    buttonFull['state'] = 'normal'
    buttonFill['state'] = 'normal'
    for mapx in maps:
        eval(f'button{mapx}')['state'] = 'normal'  # Sets the state of maps buttons to normal
    button['state'] = 'disabled'


# ASCENT
buttonAscent = tk.Button(height=1, width=8, text='Ascent', font=('helvetica', 9, 'bold'),
                         command=lambda: [selectMap("Ascent", buttonAscent)], bg='#044738', fg='#bfffd2',
                         disabledforeground='#00f245')
buttonAscent.bind("<Enter>", lambda e: buttonAscent.config(bg='#037058'))
buttonAscent.bind("<Leave>", lambda e: buttonAscent.config(bg='#044738'))
canvas1.create_window(131, 82, window=buttonAscent)
# BIND
buttonBind = tk.Button(height=1, width=8, text='Bind', font=('helvetica', 9, 'bold'),
                       command=lambda: [selectMap("Bind", buttonBind)], bg='#044738', fg='#bfffd2',
                       disabledforeground='#00f245')
buttonBind.bind("<Enter>", lambda e: buttonBind.config(bg='#037058'))
buttonBind.bind("<Leave>", lambda e: buttonBind.config(bg='#044738'))
canvas1.create_window(203, 82, window=buttonBind)
# BREEZE
buttonBreeze = tk.Button(height=1, width=8, text='Breeze', font=('helvetica', 9, 'bold'),
                         command=lambda: [selectMap("Breeze", buttonBreeze)], bg='#044738', fg='#bfffd2',
                         disabledforeground="#00f245")
buttonBreeze.bind("<Enter>", lambda e: buttonBreeze.config(bg='#037058'))
buttonBreeze.bind("<Leave>", lambda e: buttonBreeze.config(bg='#044738'))
canvas1.create_window(275, 82, window=buttonBreeze)
# FRACTURE
buttonFracture = tk.Button(height=1, width=8, text='Fracture', font=('helvetica', 9, 'bold'),
                           command=lambda: [selectMap("Fracture", buttonFracture)], bg='#044738', fg='#bfffd2',
                           disabledforeground="#00f245")
buttonFracture.bind("<Enter>", lambda e: buttonFracture.config(bg='#037058'))
buttonFracture.bind("<Leave>", lambda e: buttonFracture.config(bg='#044738'))
canvas1.create_window(347, 82, window=buttonFracture)
# HAVEN
buttonHaven = tk.Button(height=1, width=8, text='Haven', font=('helvetica', 9, 'bold'),
                        command=lambda: [selectMap("Haven", buttonHaven)], bg='#044738', fg='#bfffd2',
                        disabledforeground="#00f245")
buttonHaven.bind("<Enter>", lambda e: buttonHaven.config(bg='#037058'))
buttonHaven.bind("<Leave>", lambda e: buttonHaven.config(bg='#044738'))
canvas1.create_window(168, 114, window=buttonHaven)
# ICEBOX
buttonIcebox = tk.Button(height=1, width=8, text='Icebox', font=('helvetica', 9, 'bold'),
                         command=lambda: [selectMap("Icebox", buttonIcebox)], bg='#044738', fg='#bfffd2',
                         disabledforeground="#00f245")
buttonIcebox.bind("<Enter>", lambda e: buttonIcebox.config(bg='#037058'))
buttonIcebox.bind("<Leave>", lambda e: buttonIcebox.config(bg='#044738'))
canvas1.create_window(240, 114, window=buttonIcebox)
# PEARL
buttonPearl = tk.Button(height=1, width=8, text='Pearl', font=('helvetica', 9, 'bold'),
                        command=lambda: [selectMap("Pearl", buttonPearl)], bg='#044738', fg='#bfffd2',
                        disabledforeground="#00f245")
buttonPearl.bind("<Enter>", lambda e: buttonPearl.config(bg='#037058'))
buttonPearl.bind("<Leave>", lambda e: buttonPearl.config(bg='#044738'))
canvas1.create_window(312, 114, window=buttonPearl)


# Select Region
def selectRegion(reg, button):
    region.clear()
    region.append(reg)
    labelResult.destroy()
    buttonFull['state'] = 'normal'
    buttonFill['state'] = 'normal'
    for regionx in regions:
        eval(f'button{regionx}')['state'] = 'normal'  # Sets the state of maps buttons to normal
    button['state'] = 'disabled'


# NORTH AMERICA
buttonNA = tk.Button(height=1, width=9, text='N. America', font=('helvetica', 9, 'bold'),
                     command=lambda: [selectRegion("NA", buttonNA)], bg='#012f52', fg='#add9ff',
                     disabledforeground="#00d0ff")
buttonNA.bind("<Enter>", lambda e: buttonNA.config(bg='#00467d'))
buttonNA.bind("<Leave>", lambda e: buttonNA.config(bg='#012f52'))
canvas1.create_window(120, 155, window=buttonNA)
# EUROPE
buttonEU = tk.Button(height=1, width=9, text='Europe', font=('helvetica', 9, 'bold'),
                     command=lambda: [selectRegion("EU", buttonEU)], bg='#012f52', fg='#add9ff',
                     disabledforeground="#00d0ff")
buttonEU.bind("<Enter>", lambda e: buttonEU.config(bg='#00467d'))
buttonEU.bind("<Leave>", lambda e: buttonEU.config(bg='#012f52'))
canvas1.create_window(200, 155, window=buttonEU)
# ASIA-PACIFIC
buttonAPAC = tk.Button(height=1, width=9, text='Asia-Pacific', font=('helvetica', 9, 'bold'),
                       command=lambda: [selectRegion("APAC", buttonAPAC)], bg='#012f52', fg='#add9ff',
                       disabledforeground="#00d0ff")
buttonAPAC.bind("<Enter>", lambda e: buttonAPAC.config(bg='#00467d'))
buttonAPAC.bind("<Leave>", lambda e: buttonAPAC.config(bg='#012f52'))
canvas1.create_window(280, 155, window=buttonAPAC)
# SOUTH AMERICA
buttonSA = tk.Button(height=1, width=9, text='S. America', font=('helvetica', 9, 'bold'),
                     command=lambda: [selectRegion("SA", buttonSA)], bg='#012f52', fg='#add9ff',
                     disabledforeground="#00d0ff")
buttonSA.bind("<Enter>", lambda e: buttonSA.config(bg='#00467d'))
buttonSA.bind("<Leave>", lambda e: buttonSA.config(bg='#012f52'))
canvas1.create_window(360, 155, window=buttonSA)


# Select Agents
def appendAgent(name, button, five):
    buttonFill['state'] = 'normal'
    buttonFull['state'] = 'normal'
    labelResult.destroy()
    if name in agents:  # If the button is clicked again, reset the button
        agents.remove(name)
        nameLower = name[0].lower() + name[1:]
        button.config(bg='white', height=21, width=63, image=eval(f'{nameLower}Photo'.replace(r'/', '')))
        buttons.remove(button)
    elif len(agents) < 4 or five == 1:
        button.config(height=1, width=7, image='', bg='#e04252')  # formats the clicked agent button
        agents.append(name)  # appends the clicked agent

    delLabel()  # Resets the selected agents list
    global labelSelAgents
    labelSelAgents = tk.Label(root, width=55, text=agents, bg='black',
                              fg='white')  # Label indicating the selected agents
    canvas1.create_window(240, 354, window=labelSelAgents)
    buttons.append(button)


# ASTRA
astraPhoto = PhotoImage(file="icons/Astra_icon.png")
buttonAstra = tk.Button(height=21, width=63, text='Astra', command=lambda: [appendAgent("Astra", buttonAstra, 0)],
                        image=astraPhoto, bg='white', borderwidth=0, activebackground="white",
                        disabledforeground='black', font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(100, 210, window=buttonAstra)
# BREACH2
breachPhoto = PhotoImage(file="icons/Breach_icon.png")
buttonBreach = tk.Button(height=21, width=63, text='Breach', command=lambda: [appendAgent("Breach", buttonBreach, 0)],
                         image=breachPhoto, bg='white', borderwidth=0, activebackground="white",
                         disabledforeground='black', font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(170, 210, window=buttonBreach)
# BRIM3
brimstonePhoto = PhotoImage(file="icons/Brimstone_icon.png")
buttonBrimstone = tk.Button(height=21, width=63, text='Brimstone',
                            command=lambda: [appendAgent("Brimstone", buttonBrimstone, 0)], image=brimstonePhoto,
                            bg='white', borderwidth=0, activebackground="white", disabledforeground='black',
                            font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(240, 210, window=buttonBrimstone)
# CHAMBER4
chamberPhoto = PhotoImage(file="icons/Chamber_icon.png")
buttonChamber = tk.Button(height=21, width=63, text='Chamber',
                          command=lambda: [appendAgent("Chamber", buttonChamber, 0)], image=chamberPhoto, bg='white',
                          borderwidth=0, activebackground="white", disabledforeground='black',
                          font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(310, 210, window=buttonChamber)
# CYPHER5
cypherPhoto = PhotoImage(file="icons/Cypher_icon.png")
buttonCypher = tk.Button(height=21, width=63, text='Cypher', command=lambda: [appendAgent("Cypher", buttonCypher, 0)],
                         image=cypherPhoto, bg='white', borderwidth=0, activebackground="white",
                         disabledforeground='black', font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(380, 210, window=buttonCypher)
# JETT6
jettPhoto = PhotoImage(file="icons/Jett_icon.png")
buttonJett = tk.Button(height=21, width=63, text='Jett', command=lambda: [appendAgent("Jett", buttonJett, 0)],
                       image=jettPhoto, bg='white', borderwidth=0, activebackground="white", disabledforeground='black',
                       font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(100, 240, window=buttonJett)
# KO7
kAYOPhoto = PhotoImage(file="icons/KAYO_icon.png")
buttonKAYO = tk.Button(height=21, width=63, text='KAY/O', command=lambda: [appendAgent("KAY/O", buttonKAYO, 0)],
                       image=kAYOPhoto, bg='white', borderwidth=0, activebackground="white", disabledforeground='black',
                       font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(170, 240, window=buttonKAYO)
# KJ8
killjoyPhoto = PhotoImage(file="icons/Killjoy_icon.png")
buttonKilljoy = tk.Button(height=21, width=63, text='Killjoy',
                          command=lambda: [appendAgent("Killjoy", buttonKilljoy, 0)], image=killjoyPhoto, bg='white',
                          borderwidth=0, activebackground="white", disabledforeground='black',
                          font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(240, 240, window=buttonKilljoy)
# NEON9
neonPhoto = PhotoImage(file="icons/Killjoy1.png")
buttonNeon = tk.Button(height=21, width=63, text='Neon', command=lambda: [appendAgent("Neon", buttonNeon, 0)],
                       image=neonPhoto, bg='white', borderwidth=0, activebackground="white", disabledforeground='black',
                       font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(310, 240, window=buttonNeon)
# OMEN10
omenPhoto = PhotoImage(file="icons/Omen_icon.png")
buttonOmen = tk.Button(height=21, width=63, text='Omen', command=lambda: [appendAgent("Omen", buttonOmen, 0)],
                       image=omenPhoto, bg='white', borderwidth=0, activebackground="white", disabledforeground='black',
                       font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(380, 240, window=buttonOmen)
# PHOENIX11
phoenixPhoto = PhotoImage(file="icons/Phoenix_icon.png")
buttonPhoenix = tk.Button(height=21, width=63, text='Phoenix',
                          command=lambda: [appendAgent("Phoenix", buttonPhoenix, 0)], image=phoenixPhoto, bg='white',
                          borderwidth=0, activebackground="white", disabledforeground='black',
                          font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(100, 270, window=buttonPhoenix)
# RAZE12
razePhoto = PhotoImage(file="icons/Raze_icon.png")
buttonRaze = tk.Button(height=21, width=63, text='Raze', command=lambda: [appendAgent("Raze", buttonRaze, 0)],
                       image=razePhoto, bg='white', borderwidth=0, activebackground="white", disabledforeground='black',
                       font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(170, 270, window=buttonRaze)
# REYNA13
reynaPhoto = PhotoImage(file="icons/Reyna_icon.png")
buttonReyna = tk.Button(height=21, width=63, text='Reyna', command=lambda: [appendAgent("Reyna", buttonReyna, 0)],
                        image=reynaPhoto, bg='white', borderwidth=0, activebackground="white",
                        disabledforeground='black', font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(240, 270, window=buttonReyna)
# SAGE14
sagePhoto = PhotoImage(file="icons/Sage_icon.png")
buttonSage = tk.Button(height=21, width=63, text='Sage', command=lambda: [appendAgent("Sage", buttonSage, 0)],
                       image=sagePhoto, bg='white', borderwidth=0, activebackground="white", disabledforeground='black',
                       font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(310, 270, window=buttonSage)
# SKYE15
skyePhoto = PhotoImage(file="icons/Skye_icon.png")
buttonSkye = tk.Button(height=21, width=63, text='Skye', command=lambda: [appendAgent("Skye", buttonSkye, 0)],
                       image=skyePhoto, bg='white', borderwidth=0, activebackground="white", disabledforeground='black',
                       font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(380, 270, window=buttonSkye)
# SOVA16
sovaPhoto = PhotoImage(file="icons/Sova_icon.png")
buttonSova = tk.Button(height=21, width=63, text='Sova', command=lambda: [appendAgent("Sova", buttonSova, 0)],
                       image=sovaPhoto, bg='white', borderwidth=0, activebackground="white", disabledforeground='black',
                       font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(100, 300, window=buttonSova)
# VIPER17
viperPhoto = PhotoImage(file="icons/Viper_icon.png")
buttonViper = tk.Button(height=21, width=63, text='Viper', command=lambda: [appendAgent("Viper", buttonViper, 0)],
                        image=viperPhoto, bg='white', borderwidth=0, activebackground="white",
                        disabledforeground='black', font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(170, 300, window=buttonViper)
# YORU18
yoruPhoto = PhotoImage(file="icons/Yoru_icon.png")
buttonYoru = tk.Button(height=21, width=63, text='Yoru', command=lambda: [appendAgent("Yoru", buttonYoru, 0)],
                       image=yoruPhoto, bg='white', borderwidth=0, activebackground="white", disabledforeground='black',
                       font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(240, 300, window=buttonYoru)
# FADE19
fadePhoto = PhotoImage(file="icons/Fade_icon.png")
buttonFade = tk.Button(height=21, width=63, text='Fade', command=lambda: [appendAgent("Fade", buttonFade, 0)],
                       image=fadePhoto, bg='white', borderwidth=0, activebackground="white", disabledforeground='black',
                       font=('helvetica', 11, 'bold'), fg='black')
canvas1.create_window(310, 300, window=buttonFade)


# Helper functions for selecting buttons
# Deletes the selected agents label
def delLabel():
    labelSelAgents.destroy()


# FUNCTIONAL BUTTONS ----------------------------------------------------------------------------------------------
# CLEARS
def clear1():
    agents.clear()  # clears agents selected array
    recommended.clear()  # clears agents recommended array
    labelSelAgents.destroy()  # clears selected agents label list
    labelResult.destroy()  # clears result
    # for loop each agent button selected and reset it
    for button in buttons:
        agentx = button['text']
        agentx = agentx[0].lower() + agentx[1:]
        button.config(bg='white', height=21, width=63, image=eval(f'{agentx}Photo'.replace(r'/', '')))
    buttons.clear()  # clears agents button array
    buttonFill['state'] = 'normal'


def clear2():
    entryBox.delete(0, END)
    buttonFull['state'] = 'normal'


# Clear1 button
clearPhoto = PhotoImage(file="icons/clear.png")
buttonClear1 = tk.Button(height=22, width=63, text='Clear', command=clear1, image=clearPhoto, bg='black', borderwidth=0,
                         activebackground="black")
canvas1.create_window(275, 330, window=buttonClear1)
# Clear 2button
buttonClear2 = tk.Button(height=22, width=63, text='Clear', command=clear2, image=clearPhoto, bg='black', borderwidth=0,
                         activebackground="black")
canvas1.create_window(320, 440, window=buttonClear2)


# Helper function for recommend()
def getID(thingToID):  # Converts agent or map into ID format for rib.gg searching purposes
    match thingToID:
        case "Astra":
            return 15
        case "Breach" | "Ascent" | "EU":
            return 1
        case "Brimstone" | "Breeze":
            return 8
        case "Chamber":
            return 17
        case "Cypher" | "Bind" | "APAC":
            return 3
        case "Fade":
            return 19
        case "Jett":
            return 12
        case "KAY/O":
            return 16
        case "Killjoy":
            return 5
        case "Neon":
            return 18
        case "Omen":
            return 11
        case "Phoenix" | "Haven":
            return 7
        case "Raze" | "NA":
            return 2
        case "Reyna" | "Pearl":
            return 10
        case "Sage" | "Fracture":
            return 9
        case "Skye":
            return 13
        case "Sova" | "Icebox" | "SA":
            return 4
        case "Viper":
            return 6
        case "Yoru":
            return 14


# Recommend based on pro compositions
def recommend():
    recommended.clear()
    topAgentsPrint = []
    agentsList = agents.copy()
    # MAP DETECTED AND 4 AGENTS
    if len(agentsList) > 0 and map[0] != 'noMap' and region[0] != 'noRegion':
        # Creating the url
        copyAgentsList = agentsList.copy()
        temp = agentsList.pop(0)
        newURL = ''
        tempIndex = 0
        url = f'https://rib.gg/analytics/comps/picks?agents={getID(temp)}&map=1&patch=23&region=2&tab=comps&view=picks'
        if len(agentsList) > 0:
            for agent in agentsList:
                index = url.find('&', tempIndex + 1)
                newURL = url[:index + 1] + f'agents={getID(agent)}' + url[index:]
                tempIndex = index
                url = newURL
            newestURL = (newURL.replace('map=1', f'map={getID(map[0])}')).replace('region=2',
                                                                                  f'region={getID(region[0])}')
        else:
            newestURL = (url.replace('map=1', f'map={getID(map[0])}')).replace('region=2', f'region={getID(region[0])}')

        # Driver chrome options
        options = Options()
        options.headless = True
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(newestURL)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'image'))
        )
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        driver.quit()

        # Retrieve and parse the agents
        images = soup.find_all('image')
        topCompList = []
        if len(images) != 0:
            if len(images) > 15:
                images2 = images[-15:]
            else:
                images2 = images[-len(images):]
            for image in images2:
                href = image.attrs['href']
                agentExtract = re.findall('^/assets/agents/(\w+)\.webp', href)[0]
                if (agentExtract == 'kayo'):
                    finalAgent = 'KAY/O'
                else:
                    finalAgent = agentExtract.capitalize()
                topCompList.append(finalAgent)
            finalComp1 = topCompList[len(topCompList) - 5:len(topCompList)]
            # Handles cases where 1, 2, or 3 comps are found
            if len(topCompList) == 15:
                finalComp2 = topCompList[len(topCompList) - 10:len(topCompList) - 5]
                finalComp3 = topCompList[len(topCompList) - 15:len(topCompList) - 10]
            elif len(topCompList) == 10:
                finalComp2 = topCompList[len(topCompList) - 10:len(topCompList) - 5]
                finalComp3 = 'No more pro comps found'
            elif len(topCompList) == 5:
                finalComp2 = 'No more pro comps found'
                finalComp3 = 'No more pro comps found'
            for agent in copyAgentsList:
                finalComp1.remove(agent)
                if finalComp2 != 'No more pro comps found':
                    finalComp2.remove(agent)
                if finalComp3 != 'No more pro comps found':
                    finalComp3.remove(agent)

            # Retrieve and parse times the comp was picked
            numbers = soup.find_all('text')
            topNumbers = []
            if len(numbers) > 3:
                numbers2 = numbers[-3:]
            else:
                numbers2 = numbers[-len(numbers):]
            for number in numbers2:
                text = number.string
                topNumbers.append(text)
            finalNumber1 = topNumbers[len(topNumbers) - 1]
            # Handles cases where 1, 2, or 3 comps are found
            if len(topNumbers) == 3:
                finalNumber2 = topNumbers[len(topNumbers) - 2]
                finalNumber3 = topNumbers[len(topNumbers) - 3]
            elif len(topNumbers) == 2:
                finalNumber2 = topNumbers[len(topNumbers) - 2]
                finalNumber3 = ''
            elif len(topNumbers) == 1:
                finalNumber2 = ''
                finalNumber3 = ''

            topAgentsPrint.append(f'#1: {finalComp1} - {finalNumber1}\n'
                                  f'#2: {finalComp2} - {finalNumber2}\n'
                                  f'#3: {finalComp3} - {finalNumber3}')
        else:
            topAgentsPrint.append('No pro comps found,\n'
                                  'requests may be rate-limited, please clear and try again in 30 seconds')
    # NOMAP
    elif map[0] == 'noMap':
        topAgentsPrint.append('Select_a_Map')
    # NOREGION
    elif region[0] == 'noRegion':
        topAgentsPrint.append('Select_a_Region')
    # NOAGENTS
    elif len(agentsList) == 0:
        topAgentsPrint.append('Select_at_least_1_agent')

    buttonFill['state'] = 'disabled'
    buttonFull['state'] = 'disabled'
    global labelResult  # GUI update
    labelResult = tk.Label(root, width=43, text=topAgentsPrint[0], bg='black', fg='white')
    labelResult.config(font=('helvetica', 11))
    canvas1.create_window(240, 560, window=labelResult)


fillPhoto = PhotoImage(file="icons/ill.png")
buttonFill = tk.Button(height=22, width=63, text='Fill', command=recommend, image=fillPhoto, bg='black',
                       borderwidth=0, activebackground="black")
canvas1.create_window(205, 330, window=buttonFill)


# Suggest Full Composition
def suggestFull():
    recommended.clear()
    topAgentsPrint = []
    team = entryBox.get()
    if map[0] != 'noMap' and team != '':
        options = Options()
        options.headless = True
        options.add_argument("start-maximized")
        options.add_experimental_option("detach", True)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get('https://www.vlr.gg')
        ## Navigation to the proper stats page
        try:
            searchBar = driver.find_element(By.NAME, 'q')
            searchBar.send_keys(team)
            searchBar.send_keys(Keys.RETURN)
            select = Select(driver.find_element(By.NAME, 'type'))
            select.select_by_visible_text('Teams')
            driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[1]/div/form/div/div[2]/input').click()
            driver.find_element(By.XPATH, '//a[@class="wf-module-item search-item mod-first"]').click()
            driver.find_element(By.XPATH, '//a[@class="wf-nav-item  mod-stats"]').click()
            # Extracting agent information
            html = driver.page_source
            driver.quit()
            soup = BeautifulSoup(html, 'html.parser')
            mapComp = soup.find_all('div', attrs={'class': 'agent-comp-agg mod-first', 'data-map': map[0]})
            images = mapComp[0].find_all('img',
                                         attrs={'style': 'width: 25px; margin-left: 8px; display: inline-block;'})
            topCompList = []

            for image in images:
                src = image.attrs['src']
                agentExtract = re.findall('^/img/vlr/game/agents/(\w+)\.png', src)[0]
                if (agentExtract == 'kayo'):
                    finalAgent = 'KAY/O'
                else:
                    finalAgent = agentExtract.capitalize()
                topCompList.append(finalAgent)
            topAgentsPrint.append(f'Most recent {team} composition on {map[0]}:\n {topCompList}')
        except:
            topAgentsPrint.append('Unable to find agent comp, \n'
                                  'please double check team name.')
    elif map[0] == 'noMap':
        topAgentsPrint.append('Select_a_map')
    elif team == '':
        topAgentsPrint.append('Select_a_team')

    buttonFill['state'] = 'disabled'
    buttonFull['state'] = 'disabled'
    global labelResult  # GUI update
    labelResult = tk.Label(root, width=43, text=topAgentsPrint[0], bg='black', fg='white')
    labelResult.config(font=('helvetica', 11))
    canvas1.create_window(240, 560, window=labelResult)


fullPhoto = PhotoImage(file="icons/ill2.png")
buttonFull = tk.Button(height=22, width=63, text='FullSuggest', command=suggestFull, image=fullPhoto, bg='black',
                       borderwidth=0, activebackground="black")
canvas1.create_window(320, 410, window=buttonFull)


# UPDATE CHECK
# Checks for update
def updateCheck():
    updateWindow.withdraw()
    locallastedit = os.path.getmtime('./icons')
    locallastedit = datetime.fromtimestamp(locallastedit).strftime('%Y-%m-%d')
    locallastedit = locallastedit.split('-')
    locallastedit = int(locallastedit[0]), int(locallastedit[1]), int(locallastedit[2])
    html_text = requests.get('https://github.com/babyleafy/ValorantAgentRecommender').text
    soup = BeautifulSoup(html_text, 'lxml')
    try:
        time.sleep(.5)
        templastedit = soup.find("time-ago", class_='no-wrap').get('datetime')
        lastedit = ''
        for x in range(0, 10):
            lastedit = f'{lastedit}{templastedit[x]}'
        lastedit = lastedit.split('-')
        lastedit = int(lastedit[0]), int(lastedit[1]), int(lastedit[2])
    except:
        print('gitHub did not load...')
        lastedit = locallastedit
    if (lastedit[0] + lastedit[1] > locallastedit[0] + locallastedit[1]) or (
            (lastedit[0] + lastedit[1] == locallastedit[0] + locallastedit[1]) and lastedit[2] > locallastedit[2]):
        x = root.winfo_rootx() - 8
        y = root.winfo_rooty() - 35
        updateWindow.resizable(False, False)
        updateWindow.transient(root)
        updateWindow.iconbitmap("icons/valorant.ico")
        updateWindow.geometry(f'400x80+{x}+{y}')
        updateWindow.deiconify()


# MAIN CODE / VARIABLES ---------------------------------------------------------------------------------
if __name__ == '__main__':
    menuButtons = [fillWindow, fullWindow]  # help menu windows
    buttons = []  # agent buttons
    maps = ['Ascent', 'Bind', 'Breeze', 'Fracture', 'Haven', 'Icebox', 'Pearl']  # maps in Valorant
    regions = ['NA', 'EU', 'APAC', 'SA']
    agents = []  # agents selected
    agentID = []  # IDs of the selected agents
    map = []  # map selected
    map.append('noMap')  # default map not selected
    region = []  # region selected
    region.append('noRegion')
    recommended = []  # results
    dict = {}  # dictionary for agent pick rate per map

    helpMenuOnclicks('')
    updateCheck()

    # AGENTS
    controllerS = ['Astra', 'Brimstone', 'Omen', 'Viper']
    initiatorS = ['Breach', 'KAY/O', 'Skye', 'Sova', 'Fade']
    sentinelS = ['Chamber', 'Cypher', 'Killjoy', 'Sage']
    duelistS = ['Jett', 'Neon', 'Phoenix', 'Raze', 'Reyna', 'Yoru']

    # COMPS
    asc = []
    bin = []
    bre = []
    fra = []
    hav = []
    ice = []
    pea = []
    mapList = [asc, bin, bre, fra, hav, ice, pea]

root.config(menu=menubar)
root.mainloop()
