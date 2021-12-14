#Libraries
import smtplib
import time
import os

import requests
from bs4 import BeautifulSoup
from playsound import playsound
#--------------------------------------------------------------------------------------------------------------------------------------------------
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

def Price():                                                                
    while True:
        page = requests.get(url, headers = header)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            price = soup.find(id = "priceblock_ourprice").get_text()
            print(f"Price - {price}")
            return price[1:].strip()
        except AttributeError:
            pass
        try:
            price = soup.find(id = "priceblock_dealprice").get_text()
            print(f"Price - {price}")
            return price[1:].strip()
        except AttributeError:
            pass
        try: 
            price = soup.find(id = "buyNewSection").get_text()
            print(f"Price - {price}")
            return price[1:].strip()
        except AttributeError:
            pass
        try:
            price = soup.find(id = "priceblock_saleprice").get_text()
            print(f"Price - {price}")
            return price[1:].strip()
        except AttributeError:
            pass
        finally:
            continue

def Send_Mail(email,password,remail): #Function for sending a mail to the user 
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login(email,password)
    
    body = f"Price Fell Down\n\nCheck -{url}"
    
    server.sendmail(email,remail,body)


url = input("Enter Your URL: ")
while True:
    try:
        page = requests.get(url, headers = header)
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find(id = "productTitle").get_text().strip() #Parsing for the id "productTitle" which contains the Title/Name of the product
    except:
        continue
    
    print("\n"+title+"\n")
    check = input("Is the this the Item You're Looking for? (Y/N)- ")
    if check.lower() == 'y':
        item_price = Price()
        break
    else:
        print("Try Again\n")

item_price = item_price.replace(',','')
print(item_price)
actual_price = float(item_price)
price_threshold = float(input("Enter Your Min Price: "))
print(f"Price Threshold - {price_threshold}")
run_time = int(input("How Often Would You Like to Check?(seconds) - "))
email = input("Enter Your Mail ID: ")
password = input("Enter your google app password: ")
remail = input("Enter the receivers Email: ")
music_path = input("Enter a Path to Your Music: ")
while True:
    if price_threshold >= actual_price:
        Send_Mail(email,password,remail)
        print("EMAIL SENT")
        playsound(music_path)
        break
    else:
        print("Running...\n")
        time.sleep(run_time)



if __name__ == '__main__':
    pass


