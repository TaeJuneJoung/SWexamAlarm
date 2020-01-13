from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup as bs
import os, json, time

def lambda_handler(event, context):
    # TODO implement
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = os.getcwd() + "/bin/headless-chromium"

    driver = webdriver.Chrome(chrome_options=chrome_options)
    
    url = 'https://swexpertacademy.com/main/sst/common/userTestList.do?'
    driver.get(url)

    SW_ID = os.getenv('SW_ID')
    SW_PW = os.getenv('SW_PW')

    slack_url = os.getenv('SLACK_URL')
    headers = {'Content-type': 'application/json'}

    driver.find_element_by_id('id').send_keys(json_data.get('SW_ID'))
    driver.find_element_by_id('pwd').send_keys(json_data.get('SW_PW'))
    driver.find_element_by_xpath('/html/body/div[4]/form/div/div/div[2]/div/div/fieldset/div/div[4]/button').click()
    driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/div[2]/div[2]/div/a').click()

    time.sleep(1.5)

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

    ANSWER = ""

    if isHave:
        ANSWER = "A형 시험 나왔어!"
    else:
        ANSWER = "공부하세요!"

    
    data = {'text': ANSWER}
    requests.post(slack_url, data=json.dumps(data), headers=headers)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
