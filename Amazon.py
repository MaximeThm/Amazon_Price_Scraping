from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date

user_mail = ''
mdp_mail = ''
chromedriver_path = ''

options = Options()
options.headless = True

URL = ""


def check_amazon(URL):
    driver = webdriver.Chrome(chromedriver_path, options=options)
    driver.get(URL)

    try:
        element = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, "/html/body/div[2]/span/form/div[2]/span[1]/span/input"))
            )
    finally:
        element.click()

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    price = str(soup.find(id='price_inside_buybox').get_text())
    price = ''.join(price.split())
    converted_price = float(price[0:4])
    driver.close()

    if converted_price < 1500:
        send_email()


def send_email():
    server = smtplib.SMTP('SMTP.office365.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(user_mail, mdp_mail)

    msg = MIMEMultipart()
    msg['From'] = user_mail
    msg['To'] = user_mail
    msg['Subject'] = "Price felt down !"

    message = """
    Check the Amazon link : 
    
    URL    
    
    """
    """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       Price felt down ! Check the Amazon link :<br>
       """ +str(URL) """
    </p>
  </body>
</html>
"""

    msg.attach(MIMEText(message, 'html'))
    server.send_message(msg)
    server.quit()


check_amazon()
