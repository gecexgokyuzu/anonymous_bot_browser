import time
import autoit
import undetected_chromedriver
from selenium.webdriver.remote.webelement import WebElement
import numpy as np
import scipy.interpolate as si
import pyautogui
from pyHM import mouse
import math
import matplotlib.pyplot as plt


def TranslateMousetoDriver(driver, xy):
    listedXY = list(xy)
    panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
    listedXY[1] = listedXY[1] - panel_height
    print("Panel Height: " + str(panel_height))
    driverScreenSize = list([driver.execute_script("return window.screen.width"), driver.execute_script("return window.screen.height")])
    screenSize = pyautogui.size()
    pageYOffset = driver.execute_script('return window.pageYOffset;')
    isScrollBar = driver.execute_script('return document.documentElement.scrollHeight>document.documentElement.clientHeight;')
    print("isScrollBar: " + str(isScrollBar))
    listedXY[0] = round((listedXY[0] * driverScreenSize[0]) / screenSize[0])
    listedXY[1] = round(((listedXY[1] * driverScreenSize[1]) / screenSize[1]))
    listedXY[1] = listedXY[1] - pageYOffset
    if isScrollBar:
        listedXY[0] = listedXY[0] + 25
    return listedXY

def TranslateElementSize(xy, size):
    
    return xy



def TranslateCoordinates(xy: WebElement, driver, isCenter = True):
    panel_height = driver.execute_script('return window.outerHeight - window.innerHeight;')
    driverScreenSize = list([driver.execute_script("return window.screen.width"), driver.execute_script("return window.screen.height")])
    screenSize = pyautogui.size()
    pageYOffset = driver.execute_script('return window.pageYOffset;')
    isScrollBar = driver.execute_script('return document.documentElement.scrollHeight>document.documentElement.clientHeight;')
    listedXY = list(xy.location.values())
    if isCenter:
        print(xy.size)
        xySize = list(xy.size.values())
        listedXY[0] = listedXY[0] + int(xySize[1] / 2)
        listedXY[1] = listedXY[1] + int(xySize[0] / 2)
    if isScrollBar:
        listedXY[0] = listedXY[0] + 10
    listedXY[0] = (round((listedXY[0] * screenSize[0]) / driverScreenSize[0]))
    listedXY[1] = listedXY[1] - pageYOffset
    listedXY[1] = ((round((listedXY[1] * screenSize[1]) / driverScreenSize[1])) + panel_height)
    return listedXY

def OffsetDegree(data, index, arrayLength):
    arrayLength = arrayLength - 2
    index = index + 1
    print("DATA: " + str(data) + " -- INDEX: " + str(index) + " -- Array Length :" + str(arrayLength))
    if index % 2 == 0:
        data = data + np.random.randint(15, 30)
    else:
        data = data - np.random.randint(15, 30)
    print("Data after offset = " + str(data))
    return data

def CurvedMouseOffset(dataArray: np.ndarray):
    for idx, data in enumerate(dataArray[1:-1]):
        dataArray[dataArray == data] = OffsetDegree(data, idx, dataArray.size)
    return dataArray

def KnotCount(mousePos, mouseTarget):
    knotCount = mousePos - mouseTarget
    knotCount = round(knotCount / 200)
    print("knotCount = " + str(knotCount) + " -- knotCount Absolute = " + str(abs(knotCount)) + " -- knotCount Integer = " + str(int(abs(knotCount))))
    return abs(knotCount)

def CurvedMouse(element: WebElement, driver, isCenter = False):
    mousePosX = autoit.mouse_get_pos()[0]
    mousePosY = autoit.mouse_get_pos()[1]
    elementXY = TranslateCoordinates(element, driver, isCenter)
    mouseTargetX = elementXY[0]
    mouseTargetY = elementXY[1]
    absXDiff = mousePosX - mouseTargetX 
    absYDiff = mousePosY - mouseTargetY
    
    if abs(absXDiff) > abs(absYDiff):
        x_data = np.linspace(mousePosX, mouseTargetX, dtype=int, num=int(KnotCount(mousePosX, mouseTargetX)))
        y_data = np.linspace(mousePosY, mouseTargetY, dtype=int, num=int(KnotCount(mousePosX, mouseTargetX)))
    else:
        x_data = np.linspace(mousePosX, mouseTargetX, dtype=int, num=int(KnotCount(mousePosY, mouseTargetY)))
        y_data = np.linspace(mousePosY, mouseTargetY, dtype=int, num=int(KnotCount(mousePosY, mouseTargetY)))

    x_data = CurvedMouseOffset(x_data)
    y_data = CurvedMouseOffset(y_data)
    print(x_data)
    print(y_data)
    knots = x_data.size
    speedChanges = []
    speedChangesIndex = []

    ####--------relative speed---------------------------------------------------------------------

    for i in range(knots):
        if knots - i == 0 or knots - i == 1 or knots - i == knots or knots - i == knots - 1:
            speed = np.random.uniform(0.7, 0.8)
            speedChanges.append(speed)
            speedChangesIndex.append(i)
            print("INDEX: {} || SPEED: {}".format(i, speed))
        elif round(knots / 2) - 1 > i:
            speed = np.random.uniform(0.6, 0.7)
            speedChanges.append(speed)
            speedChangesIndex.append(i)
            print("INDEX: {} || SPEED: {}".format(i, speed))
        elif round(knots / 2) == i or (knots / 2) -1 == i or (knots / 2) + 1 == i:
            speed = np.random.uniform(0.5, 0.6)
            speedChanges.append(speed)
            speedChangesIndex.append(i)
            print("INDEX: {} || SPEED: {}".format(i, speed))
        elif round(knots / 2) + 1 < i:
            speed = np.random.uniform(0.6, 0.7)
            speedChanges.append(speed)
            speedChangesIndex.append(i)
            print("INDEX: {} || SPEED: {}".format(i, speed))
    relativeSpeed = list(zip(speedChangesIndex, speedChanges))
    relativeSpeed = dict(relativeSpeed)

    ####-----move mouse----------------------------------------------------------------------------

    for i, (x, y) in enumerate(zip(x_data, y_data)):
        mouse.move(x, y, relativeSpeed[i])

#------------random movement-----------------------------------------------------------------------

def RandomMovement(isCircle = False):
    if isCircle:
        mousePosX = autoit.mouse_get_pos()[0]
        mousePosY = autoit.mouse_get_pos()[1]
        #right:
        mouseRightTargetX = mousePosX + np.random.randint(100, 200)
        mouseRightTargetY = mousePosY + np.random.randint(100, 150)
        #bottom:
        mouseBottomTargetY = mousePosY + np.random.randint(100,200)
        mouseBottomTargetX = mousePosX + np.random.randint(-50, 100)
        #left:
        mouseLeftTargetX = mousePosX - np.random.randint(100, 200)
        mouseLeftTargetY = mousePosY - np.random.randint(50, 100)
        #top:
        mouseTopTargetX = np.random.randint(550, 750)
        mouseTopTargetY = np.random.randint(300, 400)

        x = np.array([mouseRightTargetX, mouseBottomTargetX, mouseLeftTargetX, mouseTopTargetX])
        y = np.array([mouseRightTargetY, mouseBottomTargetY, mouseLeftTargetY, mouseTopTargetY])

        print("X array values = " + str(x))
        print("Y array values = " + str(y))

        #append the starting x,y coordinates
        x = np.r_[x, x[0]]
        y = np.r_[y, y[0]]

        #fit splines to x=f(u) and y=g(u), treating both as periodic. also note that s=0
        #is needed in order to force the spline fit to pass through all the input points.
        tck, u = si.splprep([x, y], s=0, per=True)

        #evaluate the spline fits for 1000 evenly spaced distance values
        xi, yi = si.splev(np.linspace(0, 1, 150), tck)

        for x, y in zip(xi, yi):
            autoit.mouse_move(round(x), round(y), 1)

    elif isCircle == False:
        mousePosX = autoit.mouse_get_pos()[0]
        mousePosY = autoit.mouse_get_pos()[1]
        if mousePosX < 1300 or mousePosY < 600:
            mouse.move(mousePosX + np.random.randint(50, 100), mousePosY + np.random.randint(15, 30), 2)
        else:
            mouse.move(mousePosX - np.random.randint(50, 100), mousePosY - np.random.randint(15, 30), 2)


#-----------element visibility---------------------------------------------------------------------

def is_element_visible_in_viewpoint(driver, element) -> bool:
    return driver.execute_script("var elem = arguments[0],                 " 
                                 "  box = elem.getBoundingClientRect(),    " 
                                 "  cx = box.left + box.width / 2,         " 
                                 "  cy = box.top + box.height / 2,         " 
                                 "  e = document.elementFromPoint(cx, cy); " 
                                 "for (; e; e = e.parentElement) {         " 
                                 "  if (e === elem)                        " 
                                 "    return true;                         " 
                                 "}                                        " 
                                 "return false;                            "
                                 , element)

def NatWaitLoad():
    RandomMovement(isCircle=True)

def Pause(isRead: bool = False):
    if isRead:
        time.sleep(np.random.uniform(1,3))
        RandomMovement()
    else:
        time.sleep(np.random.uniform())


def ScrollIntoView(driver, element, direction = 'down'):
    while not is_element_visible_in_viewpoint(driver, element):
        autoit.mouse_wheel(direction, 1)
        RandomMovement()
        Pause()

def HumanRead(driver: undetected_chromedriver.Chrome, element: WebElement):
    xy = TranslateCoordinates(driver=driver, xy=element)
    print(str(xy[0])+", "+str(xy[1]))
    mouse.move(xy[0], xy[1])
    print("Mouse Location after moving" + str(autoit.mouse_get_pos()))
    mouse.down(button='left')
    mouse.move(mouse.get_current_position()[0] + 1200, mouse.get_current_position()[1] + 150, 1)
    mouse.up(button='left')
    mouse.double_click()

def HumanWrite(text, speed = 2):
    for i, char in enumerate(text):
        if i % speed == 0:
            Pause()
        autoit.send(char)
        