import time
import autoit
import pyautogui
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium_stealth import stealth
import login_check
import humanBehaviour.Behave as Behave
from pyHM import mouse

if __name__=="__main__":
    optionsUserAgent = login_check.SetProxy_SetUserAgent()
    driver = uc.Chrome(options=optionsUserAgent[0])
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # ------------- STEALTH DRIVER ------------- #
    stealth(driver, fix_hairline=True, hardware_concurrency=12, run_on_insecure_origins=False, platform="Win32", webgl_vendor="WebKit", renderer="WebKit WebGL", languages=["tr-TR" , "tr", "en-US", "en"])
    #driver.get("https://gologin.com/check-browser")
    #driver.get("https://bot.incolumitas.com/")
    #driver.get("https://google.com/")
    #driver.get("https://bot.sannysoft.com/")
    #driver.get("https://amiunique.org")
    #driver.get("https://whatsmyscreenresolution.com/")
    driver.get("https://facebook.com")
    """
    time.sleep(5)

    print("Screen Size: " + str(pyautogui.size()))
    print("Client X: " + str(driver.execute_script("return document.documentElement.clientWidth")))
    print("Client Y: " + str(driver.execute_script("return document.documentElement.clientHeight")))
    print("Driver Size: " + str(driver.get_window_size()))
    print("Driver Position: " + str(driver.get_window_position()))
    print("Window Size: " + str(driver.execute_script("var e = window, a = 'inner';if ( !( 'innerWidth' in window ) ){a = 'client';e = document.documentElement || document.body;}return {  height : e[ a+'Height' ] , width : e[ a+'Width' ] }")))
    print("Window Screen X: " + str(driver.execute_script("return window.screen.width")) + "\n" + "Window Screen Y: " + str(driver.execute_script("return window.screen.height")))

    testControl = driver.find_element(By.XPATH, '/html/body/section[1]/div/div/div[1]/button[5]')

    print("testControl Driver Location: " + str(testControl.location))
    print("testControl Driver Location Translated: " + str(Behave.TranslateCoordinates(testControl, driver, True)))

    xy = Behave.TranslateCoordinates(testControl, driver, True)

    mouse.move(xy[0], xy[1])

    print("mouse location screen: " + str(autoit.mouse_get_pos()))
    print("mouse position Translated: " + str(Behave.TranslateMousetoDriver(driver, autoit.mouse_get_pos())))

    time.sleep(10)
    """

    for i in range(10):
        try:
            loginButton = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button')
            break
        except:
            Behave.NatWaitLoad()
    
    eMailBox = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input")
    passWordBox = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input')

    Behave.CurvedMouse(eMailBox, driver, True)
    Behave.Pause()
    autoit.mouse_click(clicks=2, speed=5)
    Behave.Pause(True)
    Behave.HumanWrite("JackJack54gary@gmail.com")
    Behave.Pause(True)

    autoit.send("{TAB}")

    Behave.Pause(True)
    Behave.Pause()

    Behave.HumanWrite("KDXzHfWZ82")
    Behave.Pause()
    Behave.Pause(True)

    autoit.send("{ENTER}")

    Behave.Pause(True)
    Behave.Pause(True)

    time.sleep(25)