
ums_ID = ''                 # Your UMS ID           Make sure they are correct
ums_Password = ''           # Your UMS PASSWORD     Make sure they are correct

path_to_chromeDriver = r''  # put the path to chrome driver. example r'C:\Users\My USER\my directory\my folder\chromedriver.exe'
pivot_pages = 1             # How many number of display sheets you want to capture, defualt = 1 sheet 


###     -------------
###     -------------
###    ---IMPORTANT---
###     -------------
###     -------------
# IF not a DEVELOPER, do not change anything below


# In[ ]:


# IF not a DEVELOPER, do not change anything below



from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
import pandas as pd
import time
import numpy as np
from bs4 import BeautifulSoup

import warnings
warnings.filterwarnings('ignore')


# In[ ]:


browser = webdriver.Chrome(path_to_chromeDriver)


# In[ ]:


baseURL = 'https://ums.lpu.in/Placements/'
browser.get(baseURL)


# In[ ]:


usr_name = browser.find_element_by_id('txtUserName')
usr_name.send_keys(ums_ID)


# In[ ]:


usr_pass = browser.find_element_by_id('txtPassword')
usr_pass.send_keys(ums_Password)


# In[ ]:


# Clicking Submit ID/Pass button
browser.find_element_by_xpath('//*[@id="Button1"]').click()
# Drive Registration Button
browser.find_element_by_xpath('//*[@id="ctl00_RadMenu1"]/ul/li[3]/a/span').click()


# In[ ]:


company = []
ctc = []
streams = []
Date = []
myStream = ""


# In[ ]:


# Get salary package details, returns None if can't fetch
def getSalary(count):
    cnt = ''
    ctc = np.NaN
    if count < 10:
        cnt = '0' + str(count)
    else:
        cnt = str(count)
        
    try:
        browser.find_element_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_gdvPlacement_ctl{cnt}_hypJobProfile"]').click()
        browser.switch_to.window(browser.window_handles[1])
        ctc = browser.find_element_by_xpath('//*[@id="tblEmailData"]/table[1]/tbody/tr[6]/td/table/tbody/tr[2]/td[4]').text
    except:
        pass
    finally:
        if browser.title != 'Placement Drive Registration':
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
        else:
            browser.switch_to.window(browser.window_handles[0])
    
    return ctc



# Get the company details 
def getDetails(Drives):
    global company, ctc, streams, Date, myStream
#     print(Drives[3].findAll('td')[1])
    count = 2
    for i in range(1, len(Drives)-2):
        data = Drives[i].findAll('td')
#         print(i)
        if len(myStream) == 0:                 #checks for specific stream only, depricated
            Date.append(data[2].text.strip())
            company.append(data[3].text.strip())
            streams.append(data[4].text.strip())
            ctc.append(getSalary(count))
            count += 1
            
        else:
            if myStream in data[4].text.strip():
                streams.append(data[4].text.strip())
                Date.append(data[2].text.strip())
                company.append(data[3].text.strip())
                ctc.append(getSalary(count))
                
            count += 1


# Main Script

def main():
    
    for pivotPage in range(1, pivot_pages+1):
        pgStart = 3
        pgEnd = 12

        if pivotPage == 1:            # For 1st page, we have only 11 blocks
            pgStart = 2
            pgEnd = 11
            
        while(pgStart <= pgEnd):
            
            html = browser.page_source
            soup=BeautifulSoup(html,'html.parser')

            table = soup.find("table",{'class': 'aspGridView'})
            tableRow = table.findAll('tr')
            try:
                getDetails(tableRow)
            except:
                pass

            if pivotPage == 1:         #Clicks every next page till the pivot end
                browser.find_element_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_gdvPlacement"]/tbody/tr[52]/td/table/tbody/tr/td[{pgStart}]/a').click()
            else:
                browser.find_element_by_xpath(f'//*[@id="ctl00_ContentPlaceHolder1_gdvPlacement"]/tbody/tr[52]/td/table/tbody/tr/td[{pgStart}]/a').click()

            pgStart+=1
 


if __name__ == "__main__":
    main()

browser.quit()

allDrives = pd.DataFrame(list(zip(Date, company, streams, ctc)), columns=['Date', 'Company', 'stream', 'ctc'])

allDrives.to_csv('drives.csv')





