import shutil
import time
import autoit
import os.path
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

# proxy with auth and webrtc disabler path

proxy = (proxyIp, int(proxyPort), proxyUser, proxyPass)
proxy_extension = ProxyExtension(*proxy)
webrtcDisabler_Path = os.path.dirname(__file__) + "/../WebRTC-Leak-Prevent-Toggle"

# setting up proxy and user agent

def SetProxy_SetUserAgent(username=""):
    options = uc.ChromeOptions()
    userPATH = os.path.dirname(__file__) + "/../User Data/" + username
    
    # check to see if data dir has already been created for the current user

    if os.path.isdir(userPATH):
        with open (userPATH + "/useragent.txt", "r") as useragentTXT:
            useragent = useragentTXT.read()
            useragentTXT.close()
        options.add_argument(f"--user-agent={useragent}")
        print(useragent)
    else:
        useragent = ua_generator.generate(device='desktop', browser='chrome', platform='windows')
        options.add_argument(f"--user-agent={useragent}")
        print(useragent)
    
    options.add_argument(f"--load-extension={proxy_extension.directory}")
    options.add_argument(f"--load-extension={webrtcDisabler_Path}")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-remote-fonts')
    options.add_argument("--disable-plugins-discovery")
    options.set_capability('unhandledPromptBehavior', 'dismiss')
    options.set_capability('pageLoadStrategy', 'none')
    options.add_argument("--disable-infobars")
    if username != "":
        options.add_argument("--user-data-dir=" + userPATH)
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
        with open(os.path.dirname(__file__) + "/../User Data/" + line + "/useragent.txt", "x") as userAgentFile:
            userAgentFile.write(userAgent)
            userAgentFile.close()
    else:
        print("FAIL --" + userName + '|' + passWord)
        accountCount += 1
        shutil.rmtree(os.path.dirname(__file__) + "/../User Data/" + line)

# random time.sleep function

def wait():
    time.sleep(round(uniform(0.5, 1), 3))

##-------------------------------------------------------------------------------------------##

# Main App:


if __name__ == "__main__":
    for line in userNames:
        proxyUseragent = SetProxy_SetUserAgent(line)
        driver = uc.Chrome(options=proxyUseragent[0])
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # ------------- STEALTH DRIVER ------------- #
        stealth(driver, fix_hairline=True, hardware_concurrency=12, run_on_insecure_origins=False, platform="Win32", webgl_vendor="WebKit", renderer="WebKit WebGL", languages=["tr-TR" , "tr", "en-US", "en"])
        try:
            driver.get("https://www.facebook.com/")
            wait()
            wait()
            wait()
            wait()
            
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
    