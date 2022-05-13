import time
import random
import autoit
import undetected_chromedriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import scipy.interpolate as si

# Screen Width(X) = 1536-1
# Screen Height(Y) = 864-1


def TranslateCoordinates(xy: WebElement):
    listedXY = list(xy.location.values())
    listedXY[1] = listedXY[1] + 74
    return listedXY

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
        NatWait(True, 0.02, 0.05)
