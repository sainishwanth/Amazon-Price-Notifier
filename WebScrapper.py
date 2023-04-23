#In-Built Libs
import smtplib 
import time
import os

#Third Party Libs
import requests
from bs4 import BeautifulSoup
from playsound import playsound
#--------------------------------------------------------------------------------------------------------------------------------------------------
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'} #User-Agent

def Price():
    while True:
        page = requests.get(url, headers = header)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            price = soup.find("span", id = "priceblock_ourprice").get_text()
            return price_slice(price)
        except AttributeError:
            pass
        try:
            price = soup.find("span", class_ = "a-offscreen").get_text()
            return price_slice(price)
        except AttributeError:
            pass
        try:
            price = soup.find("span", class_ = "a-size-medium a-color-price priceBlockBuyingPriceString").get_text()
            return price_slice(price)
        except AttributeError:
            pass
        try:
            price = soup.find(id = "priceblock_ourprice").get_text()
            return price_slice(price)
        except AttributeError:
            pass
        try:
            price = soup.find(id = "priceblock_dealprice").get_text()
            return price_slice(price)
        except AttributeError:
            pass
        try:
            price = soup.find(id = "buyNewSection").get_text()
            return price_slice(price)
        except AttributeError:
            pass
        try:
            price = soup.find(id = "priceblock_saleprice").get_text()
            return price_slice(price)
        except AttributeError:
            pass

def price_slice(price):
    print(f"Price - {price}")
    return price[1:].strip()


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
while True:
    check = int(input("1.Email\n2.Music Alert: "))
    if check == 1:
        email = input("Enter Your Mail ID: ")
        password = input("Enter your google app password: ")
        remail = input("Enter the receivers Email: ")
        break
    elif check == 2:
        music_path = input("Enter a Path to Your Music: ")
        break
    else:
        print("Wrong Input!\n")
if check == 1:
    while True:
        item_price = Price()
        item_price = item_price.replace(',','')
        actual_price = float(item_price)
        if price_threshold >= actual_price:
            Send_Mail(email,password,remail)
            print("EMAIL SENT")
            break
        else:
            print("Running...\n")
            time.sleep(run_time)
else:
    while True:
        item_price = Price()
        item_price = item_price.replace(',','')
        actual_price = float(item_price)
        if price_threshold >= actual_price:
            playsound(music_path)
            print("The Price has Dropped!\n")
            break
        else:
            print("Running...\n")
            time.sleep(run_time)
    playsound(music_path)

if __name__ == '__main__':
    pass


