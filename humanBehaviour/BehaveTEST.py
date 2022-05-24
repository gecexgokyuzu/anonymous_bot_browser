import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium_stealth import stealth
import login_check
import autoit
import Behave
import time
from pyHM import mouse


Behave.RandomMovement(True, True)


"""
if __name__=="__main__":
    optionsUserAgent = login_check.SetProxy_SetUserAgent()
    driver = uc.Chrome(options=optionsUserAgent[0])
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # ------------- STEALTH DRIVER ------------- #
    stealth(driver, fix_hairline=True, hardware_concurrency=12, run_on_insecure_origins=False, platform="Win32", webgl_vendor="WebKit", renderer="WebKit WebGL", languages=["tr-TR" , "tr", "en-US", "en"])
    driver.get("about:blank")
"""