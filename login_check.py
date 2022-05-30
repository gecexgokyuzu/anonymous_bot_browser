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
from selenium_stealth import stealth
import humanBehaviour.Behave as Behave

# get usernames and passwords in this list. format="username|password"

userName_passWord = []

with open(os.path.dirname(__file__) + "/../facebook_accounts.txt", "r") as file:
    userName_passWord = file.readlines()

userNames = []
passWords = []
onlineAccounts = []
##-------------------------------------------------------------------------------------------##

# Setting up proxy:

proxyWL = "geo.iproyal.com:12323"
"""
with open(os.path.dirname(__file__) + "/../IPRoyal_TR_rotating.txt", "r") as proxyCredentials:
    proxyRaw = proxyCredentials.read()
    proxyCredentials.close()

splitter = proxyRaw.split(":")

proxyIp = splitter[0]
proxyPort = splitter[1]
proxyUser = splitter[2]
proxyPass = splitter[3]
"""
# webrtc disabler path

webrtcDisabler_Path = os.path.dirname(__file__) + "/../WebRTC-Leak-Prevent-Toggle"

# proxy with auth
"""
proxy = (proxyIp, int(proxyPort), proxyUser, proxyPass)
proxy_extension = ProxyExtension(*proxy)

# setting up proxy and user agent
"""
def SetProxy_SetUserAgent(username=""):
    
    # user path, options instance

    options = uc.ChromeOptions()
    userPATH = os.path.dirname(__file__) + "/../User Data/" + username
    
    # check to see if data dir has already been created for the current user
    if username != "":
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
    options.add_argument(f"--load-extension={webrtcDisabler_Path}")
    #,{proxy_extension.directory}
    #options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-remote-fonts')
    options.add_argument("--disable-plugins-discovery")
    options.set_capability('unhandledPromptBehavior', 'dismiss')
    options.set_capability('pageLoadStrategy', 'none')
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-webgl")
    options.add_argument("--disable-3d-apis")
    #options.add_argument('--disable-web-security')
    options.add_argument('--proxy-server=%s' %proxyWL)
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


def run_log(userName, passWord, isActive, userAgent):
    if isActive == True:
        print("OK --" + userName + '|' + passWord)
        onlineAccounts.append(userName + '|' + passWord)
        with open(os.path.dirname(__file__) + "/../User Data/" + user + "/useragent.txt", "x") as userAgentFile:
            userAgentFile.write(userAgent)
            userAgentFile.close()
    else:
        print("FAIL --" + userName + '|' + passWord)
        shutil.rmtree(os.path.dirname(__file__) + "/../User Data/" + user)

##-------------------------------------------------------------------------------------------##

# Main App:


if __name__ == "__main__":
    for user, passWord in zip(userNames, passWords):
        proxyUseragent = SetProxy_SetUserAgent(user)
        driver = uc.Chrome(options=proxyUseragent[0])
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # ------------- STEALTH DRIVER ------------- #
        stealth(driver, fix_hairline=True, hardware_concurrency=12, run_on_insecure_origins=False, platform="Win32", webgl_vendor="WebKit", renderer="WebKit WebGL", languages=["tr-TR" , "tr", "en-US", "en"])
        try:
            driver.get("https://www.facebook.com/")
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
            Behave.HumanWrite(user)
            Behave.Pause(True)

            autoit.send("{TAB}")

            Behave.Pause(True)
            Behave.Pause()

            Behave.HumanWrite(passWord)
            Behave.Pause()
            Behave.Pause(True)

            autoit.send("{ENTER}")

            Behave.Pause(True)
            Behave.Pause(True)

            time.sleep(1.337)
            time.sleep(1.337)
            time.sleep(1.337)

            time.sleep(30)
            logincheck = WebDriverWait(driver, 5).until(
                expect.element_to_be_clickable((By.XPATH, "//div[@aria-label='Hesap']")))
            # (Hesap means account in turkish, get the xpath again if you are using another lang option)

            driver.quit()
            run_log(user, passWord, True, proxyUseragent[1])

        except Exception as e:
            print(e)
            try:
                logincheck = WebDriverWait(driver, 5).until(
                    expect.element_to_be_clickable((By.XPATH, "//div[@aria-label='Hesap']")))

                driver.quit()

                run_log(line, passWord, True, proxyUseragent[1])

            except Exception as e:
                driver.quit()
                
                run_log(line, passWord, False, proxyUseragent[1])
    