import time
import autoit
import os.path
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.wait import WebDriverWait
from chrome_proxy_extension import ProxyExtension
from user_agent import generate_user_agent

#get usernames and passwords in this list. format="username|password"

userName_passWord = []

with open(os.path.dirname(__file__) + "/../facebook_accounts.txt", "r") as file:
    userName_passWord = file.readlines()

userNames = [] 
passWords = []
accountCount = 0
onlineAccounts = []
execPath = (os.path.dirname(__file__) + "/../chromedriver.exe")

##-------------------------------------------------------------------------------------------##

#Setting up proxy:

with open (os.path.dirname(__file__) + "/../IPRoyal_TR_rotating.txt", "r") as proxyCredentials:
    proxyRaw = proxyCredentials.read()
    proxyCredentials.close()

splitter = proxyRaw.split(":")

proxyIp = splitter[0]
proxyPort = splitter[1]
proxyUser = splitter[2]
proxyPass = splitter[3]

proxy = (proxyIp, int(proxyPort), proxyUser, proxyPass) #proxy with auth
proxy_extension = ProxyExtension(*proxy)

def SetProxy_SetUserAgent():
    options = uc.ChromeOptions()
    options.add_argument(f"--load-extension={proxy_extension.directory}")
    agent = generate_user_agent(os="win", navigator="chrome")
    options.add_argument(f"--user-agent={agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    return options

##-------------------------------------------------------------------------------------------##

#split the string into username and password

for line in userName_passWord:
    splitter = line.split('|')
    userNames.append(splitter[0].strip())
    passWords.append(splitter[1].strip())

# log keeping function

def run_log(userName, passWord, isActive):
    if isActive == True:
        print("OK --" + userName + '|' + passWord)
        onlineAccounts.append(userName + '|' + passWord)
        accountCount = accountCount + 1
    else:
        print("FAIL --" + userName + '|' + passWord)
        accountCount = accountCount + 1

# random time.sleep function

def wait():
    time.sleep(round(random.random.uniform(0.5, 2), 2))

##-------------------------------------------------------------------------------------------##

#Main App:

if __name__ == "__main__":
    for line in userNames:
        driver = uc.Chrome(options=SetProxy_SetUserAgent(), browser_executable_path=execPath)
        driver.get("https://www.facebook.com")
        try:
            time.sleep(3,14)

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
                #(Hesap means account in turkish, get the xpath again if you are using another lang option)

            wait()

            driver.quit()
            run_log(line, passWords[accountCount], True)

        except Exception as e:
            try:
                logincheck = WebDriverWait(driver, 5).until(
                    expect.element_to_be_clickable((By.XPATH, "//div[@aria-label='Hesap']")))
                
                driver.quit()

                run_log(line, passWords[accountCount], True)

            except Exception as e:
                driver.quit()
                run_log(line, passWords[accountCount], False)