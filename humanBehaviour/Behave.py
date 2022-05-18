import time
import random
import autoit
import undetected_chromedriver
from selenium.webdriver.remote.webelement import WebElement
import numpy as np
import scipy.interpolate as si
from pyHM import mouse

# Screen Width(X) = 1536-1
# Screen Height(Y) = 864-1


def TranslateCoordinates(xy: WebElement):
    listedXY = list(xy.location.values())
    listedXY[1] = listedXY[1] + 74
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
    knotCount = knotCount / 200
    print("knotCount = " + str(knotCount) + " -- knotCount Absolute = " + str(abs(knotCount)) + " -- knotCount Integer = " + str(int(abs(knotCount))))
    return abs(knotCount)

def CurvedMouse(xAxisTarget=0, yAxisTarget=0, speed=10):
    mousePosX = autoit.mouse_get_pos()[0]
    mousePosY = autoit.mouse_get_pos()[1]
    mouseTargetX = 200
    mouseTargetY = 800
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

#--------relative speed----------------------------------------------------------------------------

    for i in range(knots):
        if knots - i == 0 or knots - i == 1 or knots - i == knots or knots - i == knots - 1:
            speed = np.random.uniform(0.7, 0.8)
            speedChanges.append(speed)
            speedChangesIndex.append(i)
            print("INDEX: {} || SPEED: {}".format(i, speed))
        elif (knots / 2) - 1 > i:
            speed = np.random.uniform(0.6, 0.7)
            speedChanges.append(speed)
            speedChangesIndex.append(i)
            print("INDEX: {} || SPEED: {}".format(i, speed))
        elif (knots / 2) == i or (knots / 2) -1 == i or (knots / 2) + 1 == i:
            speed = np.random.uniform(0.5, 0.6)
            speedChanges.append(speed)
            speedChangesIndex.append(i)
            print("INDEX: {} || SPEED: {}".format(i, speed))
        elif (knots / 2) + 1 < i:
            speed = np.random.uniform(0.6, 0.7)
            speedChanges.append(speed)
            speedChangesIndex.append(i)
            print("INDEX: {} || SPEED: {}".format(i, speed))
    relativeSpeed = list(zip(speedChangesIndex, speedChanges))
    relativeSpeed = dict(relativeSpeed)

#-----move mouse-----------------------------------------------------------------------------------

    for i, (x, y) in enumerate(zip(x_data, y_data)):
        mouse.move(x, y, relativeSpeed[i])
        

        


def RandomMovement(isLoad = False, iCount: int = 1):
    if not isLoad:
        x = random(500,1000)
        y = random(500,1000)
        z = random(10,30)
        autoit.mouse_move(x,y,z)
    else:
        centerX = 750
        centerY = 430
        iCount += 1

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

def NatWait(isLoad=False, min: float = 0.5, max: float = 2):
    if isLoad:
        time.sleep(round(random.uniform(min, max), 4))
    else:
        time.sleep(round(random.uniform(min, max), 3))

def NatWaitLoad(driver: undetected_chromedriver.Chrome, element: WebElement):
    while not is_element_visible_in_viewpoint(driver, element):
        NatWait(True, 0.1, 0.)
        RandomMovement(True)
