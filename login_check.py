import time
import autoit
import os.path
import undetected_chromedriver as uc
import ua_generator
from os import rmdir
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

# proxy with auth

proxy = (proxyIp, int(proxyPort), proxyUser, proxyPass)
proxy_extension = ProxyExtension(*proxy)

# setting up proxy and user agent

def SetProxy_SetUserAgent(username=""):
    options = uc.ChromeOptions()
    options.add_argument(f"--load-extension={proxy_extension.directory}")
    #options.add_argument('--no-sandbox')
    #options.add_experimental_option('useAutomationExtension', False)
    #options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #options.add_argument('--single-process')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-remote-fonts')
    options.add_argument("--disable-plugins-discovery")
    useragent = ua_generator.generate(device='desktop', browser='chrome', platform='windows')
    options.add_argument(f"--user-agent={useragent}")
    print(useragent)
    options.set_capability('unhandledPromptBehavior', 'dismiss')
    options.set_capability('pageLoadStrategy', 'none')
    options.add_argument("--disable-infobars")
    if username != "":
        options.add_argument("--user-data-dir=" + os.path.dirname(__file__) + "/../User Data/" + username)
        options.add_argument("--profile-directory=Profile 1")
    return options, useragent

##-------------------------------------------------------------------------------------------##

# split the string into username and password


for line in userName_passWord:
    splitter = line.split('|')
    userNames.append(splitter[0].strip())
    passWords.append(splitter[1].strip())

# log keeping function


def run_log(userName, passWord, isActive, accountCount, userAgent):
    if isActive == True:
        print("OK --" + userName + '|' + passWord)
        onlineAccounts.append(userName + '|' + passWord)
        accountCount += 1
        with open(os.path.dirname(__file__) + "/../User Data/" + line + "/useragent.txt") as userAgentFile:
            userAgentFile.write(userAgent)
            userAgentFile.close()
    else:
        print("FAIL --" + userName + '|' + passWord)
        accountCount += 1
        rmdir(os.path.dirname(__file__) + "/../User Data/" + line)

# random time.sleep function


def wait():
    time.sleep(round(uniform(0.5, 2), 2))

##-------------------------------------------------------------------------------------------##

# Main App:


if __name__ == "__main__":
    for line in userNames:
        proxyUseragent = SetProxy_SetUserAgent(line)
        driver = uc.Chrome(options=proxyUseragent[0])
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # ------------- STEALTH DRIVER ------------- #
        stealth(driver, fix_hairline=False, hardware_concurrency=4, run_on_insecure_origins=False, platform="Win32", webgl_vendor="Google Inc. (Intel)")
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
            run_log(line, passWords[accountCount], True, accountCount, proxyUseragent[1])

        except Exception as e:
            try:
                logincheck = WebDriverWait(driver, 5).until(
                    expect.element_to_be_clickable((By.XPATH, "//div[@aria-label='Hesap']")))

                driver.quit()

                run_log(line, passWords[accountCount], True, accountCount, proxyUseragent[1])

            except Exception as e:
                driver.quit()
                
                run_log(line, passWords[accountCount], False, accountCount, proxyUseragent[1])
    