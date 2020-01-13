from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
import time, json, os

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 10)
url = 'https://swexpertacademy.com/main/sst/common/userTestList.do?'
driver.get(url)

with open('./secret_data/user.json') as f:
    json_data = json.load(f)

driver.find_element_by_id('id').send_keys(json_data.get('SW_ID'))
driver.find_element_by_id('pwd').send_keys(json_data.get('SW_PW'))
driver.find_element_by_xpath('/html/body/div[4]/form/div/div/div[2]/div/div/fieldset/div/div[4]/button').click()
driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/div[2]/div[2]/div/a').click()

time.sleep(1.5) #여유롭게 설정

html = driver.page_source
soup = bs(html, 'html.parser')
selector = '.support_wrap_table'
data = soup.select(selector)
res = []
for i in data:
    for j in i.text.split('\n'):
        if j.strip():
            res.append(j)

isHave = False

test_data = []
temp_str = ""
for i in range(1, len(res)):
    temp_str += res[i] + " "
    if i%5 == 0:
        test_data.append(temp_str)
        temp_str = ""
    if i%5 == 1 and res[i] == 'A형':
        isHave = True

if isHave:
    #소식을 보내줘!
    print("A형 시험 나왔어!")
    