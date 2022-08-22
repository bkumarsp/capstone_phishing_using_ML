## Backend process for data collection

#import section
from selenium import webdriver as wd
import selenium
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

##import ends


def test(param="Test"):
    print("Got input: ", param)


#Main Data collection method
# Common attributes
url_whatsmyname = "https://whatsmyname.app/"

# browser = wd.Chrome(executable_path="D:\\Python_projects_2022\\SeleniumDrivers\\chrome104\\chromedriver.exe")


#wait for some time for page to load
timeoutPeriod = 15
sleepDuration = 25

def scrapeWebpage(victimId="@ElonMusk", urls=url_whatsmyname, timeout=timeoutPeriod, sleepTime=sleepDuration):
    
    options = wd.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("incognito")
    options.add_argument("--disable-logging")
    options.add_argument("--log-level=3")
   
    browser = wd.Chrome(ChromeDriverManager().install(), options=options)
    browser.get(urls) # connect to required url

    # Check internet connectivity
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/div[1]/div/div/div[1]/div[1]/img")))
    except TimeoutException:
        print("Timed out to load page")
        browser.quit()
        return "failure"

    
    # create page elements
    searchUsername = browser.find_element(By.XPATH, "//*[@id='targetUsername']")
    searchBtn = browser.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div/div[2]/div[1]/div/div/button')

    # fill and use page contents
    username = victimId

    searchUsername.send_keys(username)
    searchBtn.click()
    sleep(sleepTime) #increase sleep time to reduce failure

    #After the request is processed, collect the data in dictionary format
    userData = {} # "{ Category : {site: link, site2: link2} }

    #fetch rows and columns length
    row_size = 1 + len(browser.find_elements(By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/table/tbody/tr"))
    column_size = 1 + len(browser.find_elements(By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/table/tbody/tr/td"))

    #manual row_size
    row_size = min(row_size, 10) #only for testing purpose

    for row in range(2, row_size+1):

        try:
        #site, category, link
            site = browser.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/table/tbody/tr["+str(row)+"]/td[1]").text
            category = browser.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/table/tbody/tr["+str(row)+"]/td[2]").text
            link = browser.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div/table/tbody/tr["+str(row)+"]/td[3]/a").text
            
            if category not in userData:
                userData[category] = {site: [link]}
            else:
                if site not in userData[category]:
                    userData[category][site] = [link]
                else:
                    userData[category][site].append(link) #additional links for same site
        except selenium.common.exceptions.NoSuchElementException:
            print("Missing data for row: ", row)
		    
    print(userData)
    			
			
    #Download data as a csv file
    downloadCSVBtn = browser.find_element(By.XPATH, '//*[@id="collectiontable_wrapper"]/div[1]/button[3]')
    downloadCSVBtn.click()
    print(str(downloadCSVBtn.tag_name))

    sleep(sleepTime*10)


    # browser.close()
    # browser.quit()
    return "success"