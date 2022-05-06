import time
import autoit
import os.path
import random
import undetected_chromedriver as uc
import ua_generator
from random import uniform
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.wait import WebDriverWait
from chrome_proxy_extension import ProxyExtension
from selenium_stealth import stealth

# get usernames and passwords in this list. format="username|password"

userName_passWord = []

with open(os.path.dirname(__file__) + "/../facebook_accounts.txt", "r") as file:
    userName_passWord = file.readlines()

userNames = []
passWords = []
accountCount = 0
onlineAccounts = []
##-------------------------------------------------------------------------------------------##

# Setting up proxy:

with open(os.path.dirname(__file__) + "/../IPRoyal_TR_rotating.txt", "r") as proxyCredentials:
    proxyRaw = proxyCredentials.read()
    proxyCredentials.close()

splitter = proxyRaw.split(":")

proxyIp = splitter[0]
proxyPort = splitter[1]
proxyUser = splitter[2]
proxyPass = splitter[3]

proxy = (proxyIp, int(proxyPort), proxyUser, proxyPass)  # proxy with auth
proxy_extension = ProxyExtension(*proxy)


def SetProxy_SetUserAgent():
    options = uc.ChromeOptions()
    #options.add_argument(f"--load-extension={proxy_extension.directory}")
    #options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    #options.add_argument('--single-process')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    #options.add_experimental_option('useAutomationExtension', False)
    #options.add_experimental_option("excludeSwitches", ["enable-automation"])
    useragent = ua_generator.generate(device='desktop', browser='chrome', platform='windows')
    print(useragent)
    options.add_argument(f"--user-agent={useragent}")
    options.set_capability('unhandledPromptBehavior', 'dismiss')
    options.set_capability('pageLoadStrategy', 'none')
    options.add_argument("--disable-infobars")
    return options

##-------------------------------------------------------------------------------------------##

# split the string into username and password


for line in userName_passWord:
    splitter = line.split('|')
    userNames.append(splitter[0].strip())
    passWords.append(splitter[1].strip())

# log keeping function


def run_log(userName, passWord, isActive, accountCount):
    if isActive == True:
        print("OK --" + userName + '|' + passWord)
        onlineAccounts.append(userName + '|' + passWord)
        accountCount += 1
    else:
        print("FAIL --" + userName + '|' + passWord)
        accountCount += 1

# random time.sleep function


def wait():
    time.sleep(round(uniform(0.5, 2), 2))

##-------------------------------------------------------------------------------------------##

# Main App:


if __name__ == "__main__":
    for line in userNames:
        driver = uc.Chrome(options=SetProxy_SetUserAgent())
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # ------------- STEALTH DRIVER ------------- #
        stealth(driver, languages=["en-US", "en"], vendor="Google Inc.", platform="Win64", webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine", fix_hairline=False, hardware_concurrency=4, run_on_insecure_origins=False)
        driver.get("https://bot.incolumitas.com/")
        time.sleep(250)
        try:
            time.sleep(3, 14)

            email_input = driver.find_element(By.ID, "email")
            email_input.click()
            autoit.send(userNames[accountCount])

            wait()

            password_input = driver.find_element(By.ID, "pass")
            password_input.click()

            wait()

            autoit.send(passWords[accountCount])
            login_btn = driver.find_element(By.NAME, "login")

            wait()

            login_btn.click()
            logincheck = WebDriverWait(driver, 5).until(
                expect.element_to_be_clickable((By.XPATH, "//div[@aria-label='Hesap']")))
            # (Hesap means account in turkish, get the xpath again if you are using another lang option)

            wait()

            driver.quit()
            run_log(line, passWords[accountCount], True, accountCount)

        except Exception as e:
            try:
                logincheck = WebDriverWait(driver, 5).until(
                    expect.element_to_be_clickable((By.XPATH, "//div[@aria-label='Hesap']")))

                driver.quit()

                run_log(line, passWords[accountCount], True, accountCount)

            except Exception as e:
                driver.quit()
                run_log(line, passWords[accountCount], False, accountCount)