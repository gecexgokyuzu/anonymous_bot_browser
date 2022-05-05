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
    driver = uc.Chrome(options=login_check.SetProxy_SetUserAgent())
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # ------------- STEALTH DRIVER ------------- #
    stealth(driver, fix_hairline=False, hardware_concurrency=4, run_on_insecure_origins=False)
    driver.get("https://bot.incolumitas.com/")
    time.sleep(250)
    login_check.wait()
    login_check.wait()

    scroll_target = driver.find_element(By.ID, "newDetectionTests")
    driver.execute_script('arguments[0].scrollIntoView(true);', scroll_target)
    login_check.wait()

    driver.find_element(By.NAME, "userName").clear()
    driver.find_element(By.NAME, "userName").send_keys("bot")
    login_check.wait()

    driver.find_element(By.NAME, "eMail").clear()
    driver.find_element(By.NAME, "eMail").send_keys("bot@bottington.com")
    login_check.wait()
    login_check.wait()

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