from selenium import webdriver
import sys,os
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

#choose the correct chrome driver for your chrome version
chromedriver = r"chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
browser.maximize_window()
browser.implicitly_wait(10)
#opening the browser and details will be scrapped automatically
browser.get("https://uniswap.exchange/add-liquidity")
browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div[4]/div/div[2]/input').send_keys('1')
#pandas data frame
df = pd.DataFrame({'token','Exchange-rate','Pool-size'})




for token in range(2,200):
    try:
        t=str(token)
        browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div[6]/div/div[2]/button/span').click()
        browser.find_element_by_xpath('/html/body/reach-portal/div[3]/div/div/div/div/div[3]/div['+t+']').click()
        time.sleep(1.5)
        exchange_rate=browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div[7]/div[2]/div[1]/span[2]').text
        print(exchange_rate)
        lst=exchange_rate.split(' ')
        token_name=lst[-1]
        print(token_name)
        current_pool_size=browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div[7]/div[2]/div[2]/span[2]').text
        print('pool-size'+current_pool_size)
        i=token-2
        df.loc[i]={token_name,exchange_rate,current_pool_size}
    except nosuchelementexception:
       pass
print(df)
    







