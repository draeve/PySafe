from pygame import *
from time import *
from random import *
import serial

font.init()                                             #important init stuff
page = "menu"

#SETTING VARIABLES
black = (0,0,0)                     #colours
white = (255, 255, 255)
grey = (211,211,211)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
purple = (255, 0, 255)
cyan = (0, 255, 255)

pastelB = (204,229,255)             #BLUES
lightGreyB = (0,153,153)
skyB = (0,204,204)
colombianB = (153,221,255)
discoB = (51, 187, 255)
capriB = (0, 170, 255)


cardinalR = (196, 30, 58)           #REDS
turkeyR = (169, 17, 1)

screenW = 1000                                          #screen
screenH = 600
screen = display.set_mode((screenW, screenH))

DIN170 = font.Font("fonts1/DINAlternate-Bold.ttf", 170)   #fonts
DIN45 = font.Font("fonts1/DINAlternate-Bold.ttf", 45)
DIN36 = font.Font("fonts1/DINAlternate-Bold.ttf", 36)
DIN24 = font.Font("fonts1/DINAlternate-Bold.ttf", 24)

ser = serial.Serial('COM4')                             #serial

pwInput = ""                                            #pw encryption

#HELPER FUNCTIONS

def centered(image1,image2,y):       #horizontally centering
    w1, h1 = image1.get_width(), image1.get_height()
    w2, h2 = image2.get_width(), image2.get_height()
    x = (screenW - (w1 + w2 + 10))//2
    screen.blit(image1, (x, y - h1//2)) 
    screen.blit(image2, (x + w1 + 10, y - h2//2))

def testAuth(passW):                 #checks from file and gives authorization
    f = open("key/password.key", "r")
    master_pw = f.readline()
    if passW == master_pw:
        return True
    else:
        return False

#MAIN PAGES

def menu():
    screen.fill(white)

    background = transform.scale(image.load("images/background.png"),(screenW,screenH))     #loading images in
    psLogo = transform.scale(image.load("images/sneklogo.png"),(170,170))
    psTitle = DIN170.render("PySafe", True, white)
    pwLabel = DIN45.render("Password:", True, white)

    pwIn_X, pwIn_Y = pwLabel.get_width(), pwLabel.get_height()                                     #vals for password label and input
    totalW_In = pwIn_X + 400 + 10
    startPosX_In = screenW - totalW_In//2
    pwInputRect = Rect(pwIn_X*2 + 10, (400 - pwIn_X//2), 400, pwIn_Y)

    screen.blit(background, (0,0))
    screen.blit(pwLabel, (pwIn_X, 320 - pwIn_Y//2))
    centered(psLogo, psTitle, 90)

    pwInput = ""

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "quit"
            if evt.type == KEYDOWN: #if a key on the keyboard is pressed down
                keyVal = evt.unicode
                draw.rect(screen, white, pwInputRect, 0)
                if keyVal != "\r" and keyVal != "\t":
                    pwInput += keyVal
                    if keyVal == "\b":
                        pwInput = pwInput[0:-2]
                        draw.rect(screen, white, pwInputRect, 0)
                if keyVal == "\r": #when entered/returned, the it runs through the testing authorization (uses the password.key file)
                    if testAuth(pwInput) == True:
                        return "lockUnlock"
                    else:
                        wrongPasswordPic = DIN45.render("Wrong Password. Please try again.", True, white)
                        screen.blit(wrongPasswordPic, (250, 400))
            screen.set_clip(pwInputRect)                                #showing the last/end part to the picture of the password input
            draw.rect(screen, white, pwInputRect, 0)
            pwPic = DIN45.render(pwInput, True, black)
            if pwPic.get_width() > pwInputRect[2]:
                x,y = pwInputRect[0] - (pwPic.get_width() - pwInputRect[2]), pwInputRect[1]
                screen.blit(pwPic,(x,y))
            else:
                screen.blit(pwPic, (pwInputRect[0], pwInputRect[1]))
            screen.set_clip(None)
        display.flip()

def lockUnlock():
    lockunlockBack = transform.scale(image.load("images/lockunlock.jpg"), (screenW, screenH))
    screen.blit(lockunlockBack, (0,0))

    lockRect = Rect(50, 225, 425, 200)
    unlockRect = Rect(525, 225, 425, 200)
    resetRect = Rect(50, 50, 320, 60)
    
    rects = [lockRect, unlockRect, resetRect]
    draw.rect(screen, pastelB, lockRect)
    draw.rect(screen, pastelB, unlockRect)
    draw.rect(screen, cardinalR, resetRect)
    
    values = ["lock", "unlock", "resetPass"]   
    labels = ["Lock PySafe", "Unlock Pysafe", "Reset Password"]
    
    txtlockPic = DIN45.render("Lock PySafe", True, black)
    txtunlockPic = DIN45.render("Unlock Pysafe", True, black)
    txtresetPic = DIN36.render("Unlock Pysafe", True, black)

    screen.blit(txtlockPic, (lockRect[0] + (lockRect[2] - txtlockPic.get_width())//2, lockRect[1] + (lockRect[3] - txtlockPic.get_height())//2))
    screen.blit(txtunlockPic, (unlockRect[0] + (unlockRect[2] - txtunlockPic.get_width())//2, unlockRect[1] + (unlockRect[3] - txtunlockPic.get_height())//2))
    screen.blit(txtresetPic, (resetRect[0] + (resetRect[2] - txtresetPic.get_width())//2, resetRect[1] + (resetRect[3] - txtresetPic.get_height())//2))
    
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "quit"

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
            
        if lockRect.collidepoint(mx,my):
            draw.rect(screen, pastelB, lockRect)
            screen.blit(txtlockPic, (lockRect[0] + (lockRect[2] - txtlockPic.get_width())//2, lockRect[1] + (lockRect[3] - txtlockPic.get_height())//2))
            if mb[0] == 1:
                ser.write(b'lock')
                sleep(1.25)
                draw.rect(screen, colombianB, lockRect,4)
                screen.blit(txtlockPic, (lockRect[0] + (lockRect[2] - txtlockPic.get_width())//2, lockRect[1] + (lockRect[3] - txtlockPic.get_height())//2))
        if unlockRect.collidepoint(mx,my):
            draw.rect(screen, pastelB, unlockRect)
            screen.blit(txtunlockPic, (unlockRect[0] + (unlockRect[2] - txtunlockPic.get_width())//2, unlockRect[1] + (unlockRect[3] - txtunlockPic.get_height())//2))
            if mb[0] == 1:
                ser.write(b'unlock')
                sleep(1.25)
                draw.rect(screen, colombianB, unlockRect,4)
                screen.blit(txtunlockPic, (unlockRect[0] + (unlockRect[2] - txtunlockPic.get_width())//2, unlockRect[1] + (unlockRect[3] - txtunlockPic.get_height())//2))
        if resetRect.collidepoint(mx,my):
            draw.rect(screen, cardinalR, resetRect)
            screen.blit(txtresetPic, (resetRect[0] + (resetRect[2] - txtresetPic.get_width())//2, resetRect[1] + (resetRect[3] - txtresetPic.get_height())//2))
            if mb[0] == 1:
                draw.rect(screen, cardinalR, resetRect,4)
                screen.blit(txtresetPic, (resetRect[0] + (resetRect[2] - txtresetPic.get_width())//2, resetRect[1] + (resetRect[3] - txtresetPic.get_height())//2))
                return "resetPass"
        display.flip()

def resetPass():
    resetPassBack = transform.scale(image.load("images/resetPass.jpg"), (screenW, screenH))
    screen.blit(resetPassBack, (0,0))

    pwLabel = DIN45.render("New Password:", True, white)

    pwIn_X, pwIn_Y = pwLabel.get_width(), pwLabel.get_height()                                     #vals for password label and input
    totalW_In = pwIn_X + 400 + 10
    startPosX_In = screenW - totalW_In//2
    newPassInputRect = Rect(pwIn_X + pwLabel.get_width()//2, (320- pwIn_Y//2), 400, pwIn_Y)
    screen.blit(pwLabel, (pwIn_X - 200, 320 - pwIn_Y//2))

    lockUnlockReturnPic = DIN36.render("Back", True, black)
    returnRect = Rect(50, 475, lockUnlockReturnPic.get_width(), lockUnlockReturnPic.get_height())
    draw.rect(screen, cardinalR, returnRect)
    screen.blit(lockUnlockReturnPic, (returnRect[0], returnRect[1]))
    newPass = ""

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "quit"
            if evt.type == KEYDOWN: #if a key on the keyboard is pressed down
                keyVal = evt.unicode
                draw.rect(screen, white, newPassInputRect, 0)
                if keyVal != "\r" and keyVal != "\t":
                    newPass += keyVal
                    if keyVal == "\b":
                        newPass = newPass[0:-2]
                        draw.rect(screen, white, newPassInputRect, 0)
                if keyVal == "\r":
                    with open("key/password.key", "w") as fileKey:
                        fileKey.write(newPass)
                    confirmedChangePic = DIN36.render("Your password has now been changed.", True, white)
                    screen.blit(confirmedChangePic, (200, 400))
            mx,my = mouse.get_pos()
            mb = mouse.get_pressed()

            if returnRect.collidepoint(mx,my):
                draw.rect(screen, cardinalR, returnRect, 3)
                if mb[0] == 1:
                    return "lockUnlock"
            screen.set_clip(newPassInputRect)
            draw.rect(screen, white, newPassInputRect, 0)
            newPassPic = DIN45.render(newPass, True, black)
            if newPassPic.get_width() > newPassInputRect[2]:
                x,y = newPassInputRect[0] - (newPassPic.get_width() - newPassInputRect[2]), newPassInputRect[1]
                screen.blit(newPassPic,(x,y))
            else:
                screen.blit(newPassPic, (newPassInputRect[0], newPassInputRect[1]))
            screen.set_clip(None)

        display.flip()

running = True
while page != "quit":
    if page == "menu":
        page = menu()
    if page == "lockUnlock":
        page = lockUnlock()
    if page == "resetPass":
        page = resetPass()
    display.flip()

ser.write(b'lock')
sleep(1.25)
quit()
