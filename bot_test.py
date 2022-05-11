import time
import autoit
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium_stealth import stealth
import login_check

if __name__=="__main__":
    optionsUserAgent = login_check.SetProxy_SetUserAgent()
    driver = uc.Chrome(options=optionsUserAgent[0])
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # ------------- STEALTH DRIVER ------------- #
    stealth(driver, fix_hairline=True, hardware_concurrency=12, run_on_insecure_origins=False, platform="Win32", webgl_vendor="WebKit", renderer="WebKit WebGL", languages=["tr-TR" , "tr", "en-US", "en"])
    #driver.get("https://gologin.com/check-browser")
    driver.get("https://bot.incolumitas.com/")
    #driver.get("https://bot.sannysoft.com/")
    #driver.get("https://amiunique.org")
    time.sleep(250)
    driver.quit()
    login_check.wait()
    login_check.wait()
    """
    autoit.mouse_wheel("down", 6)
    login_check.wait()
    autoit.mouse_wheel("down", 6)
    login_check.wait()
    """
    selectedObj = driver.find_element(By.NAME, "userName").location_once_scrolled_into_view
    print(selectedObj)
    objXY = list(selectedObj.values())
    autoit.mouse_move(x=objXY[0], y=objXY[1], speed=15)
    login_check.wait()  
    autoit.send("bottington")
    login_check.wait()
    autoit.send("{TAB}")
    login_check.wait()
    autoit.send("botting")
    login_check.wait()
    autoit.send("@fucker.com")
    login_check.wait()

    #selectedObj = driver.find_element(By.NAME, "eMail")
    #selectedObj.click()

    Select(driver.find_element(By.NAME, "cookies")).select_by_visible_text("I want all the Cookies")
    login_check.wait()

    driver.find_element(By.NAME, "terms").click()
    login_check.wait()

    driver.find_element(By.ID, "bigCat").click()
    login_check.wait()

    driver.find_element(By.ID, "submit").click()
    login_check.wait()
    login_check.wait()
    login_check.wait()

    driver.switch_to.alert.accept()
    time.sleep(250)