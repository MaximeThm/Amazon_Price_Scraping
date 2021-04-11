from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import datetime

options = Options()
options.headless = True

driver_path = '/Users/maximethomas/PycharmProjects/chromedriver'

title = []
description = []
price = []


driver = webdriver.Chrome(options=options, executable_path=driver_path)


def accept_cookies():
    try:
        button1 = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/button/div')
        button1.click()
    except Exception:
        pass


def get_data(url):
    driver.get(url)
    time.sleep(5)
    accept_cookies()
    i = 1
    while True:
        try:
            title_selector = str('//*[@id="main_container"]/div/div/section/div[2]/div[2]/a[') + str(i) + str(
                ']/div/div[2]/div[2]/h2')
            desc_selector = str('//*[@id="main_container"]/div/div/section/div[2]/div[2]/a[') + str(i) + str(
                ']/div/div[2]/div[2]/div[1]/span')
            price_selector = str('//*[@id="main_container"]/div/div/section/div[2]/div[2]/a[') + str(i) + str(
                ']/div/div[2]/div[2]/div[2]/span')

            title_1 = driver.find_element_by_xpath(title_selector)
            sub_title = driver.find_element_by_xpath(desc_selector)
            price_1 = driver.find_element_by_xpath(price_selector)

            title.append(title_1.text)
            description.append(sub_title.text)
            price.append(price_1.text)

            i += 1
        except Exception:
            break


Iphone_11_Pro = 'https://www.backmarket.fr/smartphones-reconditionnes.html#brand=0%20%20Apple&model=007%20iPhone%2011%20Pro&states_list=0%20Comme%20neuf&states_list=1%20Très%20bon%20état'

product_list = [Iphone_11_Pro]

for items in product_list:
    get_data(items)

df = pd.DataFrame(columns=['Date', 'Modèle', 'Description', 'Price'])
df['Modèle'] = title
df['Description'] = description
df['Price'] = price
df['Date'] = datetime.date.today()
print(df)
driver.quit()
