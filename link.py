from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import joblib
from sklearn.preprocessing import LabelEncoder
import time

def retrive_data(link):
    data = []
    
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
        
    driver = webdriver.Chrome(options=options)
        
    driver.get(link)
        
    #clear cookies banner
    try:#waits till pop up appears
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="sp_message_iframe_1086457"]'))
        WebDriverWait(driver, 10).until(element_present)
    except TimeoutException:
        print ("Timed out waiting for page to load")

    #gets cookie pop up
    frame = driver.find_element(By.XPATH, '//*[@id="sp_message_iframe_1086457"]')

    #switches focus to cookies pop up
    driver.switch_to.frame(frame)

    #finds button
    cookies = driver.find_element(By.XPATH,'//*[@id="notice"]/div[4]/button[3]')
    cookies.click()

    #goes back to main web page
    driver.switch_to.default_content()
        
    car_title = driver.find_element(By.CSS_SELECTOR,'#layout-desktop > aside > section.at__sc-6sdn0z-0.gAsuwJ > h1').text
    
    price = driver.find_element(By.CLASS_NAME, 'at__sc-6sdn0z-6.kEwOIS').text
    
    #web page has 2 seperate grids for data. each stored in seperate array as sometimes size of 1 varies        
    f = driver.find_elements(By.CLASS_NAME,'at__sc-efqqw2-6.gIURrd')
    s = driver.find_elements(By.CLASS_NAME,'at__sc-1n64n0d-7.at__sc-6lr8b9-4.fcDnGr.gJQNgz')
    
    makes = joblib.load('Encoders/make_classes.joblib').classes_
    
    make = ''
    model = ''
    
    for m in makes:
        if m in car_title:
            tmp = car_title.split(m,1)
            make = m
            model = tmp[1].strip()
            
    price = int(price.replace('£','').replace(',','').strip())
    
    #get reg and miles out of first list
    reg = 0
    miles = 0
    for i in range(0,len(f)):
        if 'reg)' in f[i].text:
            reg = int(f[i].text[:4])
        
        if 'miles' in f[i].text[-5:]:
            miles = int(f[i].text.split(' ')[0].replace(',',''))
    
    #second list is more consistent and allows for direct access        
    vec = s[1].text
    fuel = s[0].text
    es = float(s[2].text.replace('L',''))
    tt = s[3].text
    
    driver.find_element(By.XPATH, '//*[@id="layout-desktop"]/article/div[1]/button').click()
    #sleep to allow for animations after clicks
    time.sleep(1)
    
    driver.find_element(By.XPATH, '//*[@id="modal-root"]/div[2]/div/section/div[2]/div/div[7]/ul/li/h3/button').click()
    
    time.sleep(1)
    
    hp = driver.find_element(By.XPATH, '//*[@id="modal-root"]/div[2]/div/section/div[2]/div/div[7]/ul/li/div/section/ul/li[5]/span[2]/span').text
    
    hp = int(hp[:-4])
    
    #appending all in order to make array for program use
    data.append(make)
    data.append(model)
    data.append(price)
    data.append(reg)
    data.append(vec)
    data.append(miles)
    data.append(es)
    data.append(hp)
    data.append(tt)
    data.append(fuel)
    
    return data