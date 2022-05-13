import time
import random
import autoit
import undetected_chromedriver
from selenium.webdriver.remote.webelement import WebElement


def TranslateCoordinates(xy: WebElement):
    listedXY = list(xy.location.values())
    listedXY[1] = listedXY[1] + 74
    return listedXY

def RandomMovement():
    x = random(500,1000)
    y = random(500,1000)
    autoit.mouse_move(x,y)

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

def NaturalWait(min: float, max: float, isLoad=False):
    if isLoad:
        time.sleep(round(random.uniform(min, max),3))
    else:
        time.sleep