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
    for i in range(10):
        optionsUserAgent = login_check.SetProxy_SetUserAgent()
        driver = uc.Chrome(options=optionsUserAgent[0])
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # ------------- STEALTH DRIVER ------------- #
        stealth(driver, fix_hairline=True, hardware_concurrency=12, run_on_insecure_origins=False, platform="Win32", webgl_vendor="WebKit", renderer="WebKit WebGL", languages=["tr-TR" , "tr", "en-US", "en"])
        #driver.get("https://gologin.com/check-browser")
        #driver.get("https://bot.incolumitas.com/")
        #driver.get("https://bot.sannysoft.com/")
        #driver.get("https://amiunique.org")
        #driver.get("https://benimtestim.com")
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        login_check.wait()
        ipControl = driver.find_element(By.NAME, 'ip')
        print(ipControl.get_attribute('value'))
        driver.quit()