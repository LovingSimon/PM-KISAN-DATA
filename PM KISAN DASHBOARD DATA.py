#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import re
import winsound
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions
import random


webd_with_location = "C:\\Users\\HP\\Desktop\\chromedriver.exe" #webdriver
frame_dataset= 'C:\\Users\\HP\\Documents\\frame_final.xlsx' #available in the github repository
save_location= 'C:\\Users\\HP\\Desktop\\PMK New\\sample_' #where you want to save


chrome_options = webdriver.ChromeOptions()   
driver = webdriver.Chrome(webd_with_location, options=chrome_options)
url = 'https://pmkisan.gov.in/'
driver.get(url)
driver.maximize_window()
sleep(5)
click = driver.find_element_by_xpath('//*[@id="Button1"]').click()
sleep(5)
num_states = len(driver.find_elements_by_xpath('//*[@id="DdlState"]/option'))
print(num_states)
frame_num = pd.read_excel(frame_dataset)
frame_num = pd.DataFrame(frame_num)
runner = 0
for i in range(1, num_states):
    state = '//*[@id="DdlState"]/option[' + str(i+1) +']'
    c1 = driver.find_element_by_xpath(state).click()
    st_name = driver.find_element_by_xpath(state).text
    sleep(1)
    num_districts = len(driver.find_elements_by_xpath('//*[@id="DdlDistrict"]/option'))
    print(num_districts)
    for j in range(1, num_districts):
        data = pd.DataFrame(columns=['state', 'district', 'sub_district', 'village', 'fname', 'fathername', 'num_intalls', 
                            'reg_date', 'inst1', 'inst2', 'inst3', 'inst4', 'inst5', 'inst6', 'inst7', 'inst8'
                            , 'inst9'])
        district = '//*[@id="DdlDistrict"]/option[' + str(j+1) + ']'
        c2 = driver.find_element_by_xpath(district).click()
        dis_name = driver.find_element_by_xpath(district).text
        dis_name2 = frame_num.iloc[runner,1]
        print(dis_name)
        print(dis_name2)
        sleep(1)
        num_sdis = len(driver.find_elements_by_xpath('//*[@id="DdlSubDistrict"]/option'))
        print(num_sdis)
        people_sample = frame_num.iloc[runner,3]
        runner = runner+1
        print(people_sample)
        if(people_sample<=3):
            print(dis_name + 'did not do')
            continue
        if(num_sdis<2):
            sample_sdis = num_sdis
        elif(num_sdis%2==1):
            sample_sdis = (num_sdis+1)/2
        else:
            sample_sdis = num_sdis/2
        ppl_per_sdis = int(people_sample/sample_sdis)
        for k in range(1, int(sample_sdis+1)):
            random1 = random.randint(1,num_sdis)
            print(random1)
            sub_dist = '//*[@id="DdlSubDistrict"]/option[' + str(random1+1) + ']'
            try:
                c3 = driver.find_element_by_xpath(sub_dist).click()
            except:
                continue
            sdis_name = driver.find_element_by_xpath(sub_dist).text
            sleep(1)
            num_vill = len(driver.find_elements_by_xpath('//*[@id="DdlVillage"]/option'))
            sample_vill = int(ppl_per_sdis/3)
            if(num_vill<sample_vill):
                sample_vill = num_vill
            for l in range(1, int(sample_vill+1)):
                random2 = random.randint(1,num_vill)
                print(random2)
                village = '//*[@id="DdlVillage"]/option[' + str(random2+1) + ']'
                try:
                    c4 = driver.find_element_by_xpath(village).click()
                    vill_name = driver.find_element_by_xpath(village).text
                except:
                    sample_vill = sample_vill+1
                    if(sample_vill>num_vill/2):
                        sample_vill=1
                    continue
                vill_name2 = re.split(' -', vill_name)
                vill_name_file = vill_name2[0]
                sleep(1)
                sleep(3)
                click2 = driver.find_element_by_xpath('//*[@id="btnShow"]').click()
                sleep(30)
                try:
                    click3 = driver.find_element_by_xpath('//*[@id="visiblepan"]/ul/li[2]/a').click()
                except:
                    print(vill_name_file + ' is not opening')
                    sample_vill = sample_vill+1
                    if(sample_vill>num_vill/2):
                        sample_vill=1
                    continue
                print(l)
                for m in range(1,2):
                    if(m==1):
                        #click4 = driver.find_element_by_xpath('//*[@id="rdBenReceive"]').click()
                        num_rows = len(driver.find_elements_by_xpath('//*[@id="gvBenefeciaryStatus"]/tbody/tr'))
                        print(num_rows)
                        if(num_rows<=3):
                            rand_rows = num_rows
                        else:
                            rand_rows = 4
                        for n in range(1, rand_rows):
                            random3 = random.randint(2,num_rows+1)
                            print(random3)
                            print(n)
                            f_totinst = '//*[@id="gvBenefeciaryStatus"]/tbody/tr['+  str(random3) + ']/td[5]'
                            try:
                                f_totinst2 = driver.find_element_by_xpath(f_totinst).text
                            except:
                                continue
                            f_moredeets = '/html/body/form/div[4]/div[3]/div/div[2]/div[3]/div/div/div/table/tbody/tr['+  str(n) + ']/td[7]/a'
                            sleep(2)
                            try:
                                f_click = driver.find_element_by_xpath(f_moredeets).click()
                            except:
                                print(vill_name + 'not going' + str(n))
                                rand_rows = rand_rows+1
                                if(rand_rows>num_rows):
                                    rand_rows=1
                                continue
                            p = driver.current_window_handle
                            chwd = driver.window_handles
                            for w in chwd:
                                if(w!=p):
                                    driver.switch_to.window(w)
                            farmer_name = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_txtFarmerName"]').text
                            farmer_father_name =driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_txtFatherName"]').text
                            reg_date = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_txtRegDate"]').text
                            inst1 = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_tr8"]/td[2]').text
                            inst2 = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_tr8"]/td[3]').text
                            inst3 = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_tr8"]/td[4]').text
                            inst4 = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_tr8"]/td[5]').text
                            inst5 = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_tr8"]/td[6]').text
                            inst6 = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_tr19"]/td[2]').text
                            inst7 = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_tr19"]/td[3]').text
                            inst8 = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_tr19"]/td[4]').text
                            inst9 = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_tr19"]/td[5]').text
                            data.loc[len(data)] = [st_name, dis_name, sdis_name, vill_name, farmer_name, farmer_father_name, f_totinst2,
                                                  reg_date, inst1, inst2, inst3, inst4, inst5, inst6, inst7, inst8, inst9]
                            closeclick = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_btnback"]').click()
                            driver.switch_to.window(p)       
                    
            filename = save_location+ st_name+'_'+dis_name+'_'+sdis_name + '.csv'
            data.to_csv(filename)
            print(filename)
                    
                


# In[12]:


filename = 'C:\\Users\\HP\\Downloads\\PM KISAN\\sample'+ st_name+'_'+dis_name+'_'+sdis_name + 'temp.csv'
data.to_csv(filename)


# In[ ]:





# In[50]:


data


# In[10]:


print(st_name)


# In[11]:


print(i)


# In[6]:


data


# In[ ]:




