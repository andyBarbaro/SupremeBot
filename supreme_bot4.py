import requests
from datetime import datetime
from config import keys
import time
from config import itemCats
from config import descriptList
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

def categories(catList, itemDesc):
    # the target we want to open
    url='https://www.supremenewyork.com/shop/all/'

    #open with GET method
    resp=requests.get(url)

    #http_respone 200 means OK status
    if resp.status_code==200:
        print("Successfully opened the web page")
        print("The Supreme categories are as follows: \n")

        # we need a parser,Python built-in HTML parser is enough .
        soup=BeautifulSoup(resp.text,'html.parser')

        # l is the list which contains all the text i.e news
        l=soup.find("ul", id="nav-categories")

        #now we want to print only the text part of the anchor.
        #find all the elements of a, i.e anchor
        for i in l.find_all("a"):
            if i.text in catList:
                newURL = "https://www.supremenewyork.com" + i['href']
                print ("Found the URL: " + newURL)

                nextPage(newURL, itemDesc)
                print ("_______________________________")
    else:
        print("Error")

def nextPage(urlStr, itemSpecs):
    resp2 = requests.get(urlStr)

    if resp2.status_code == 200:
         print("Looking for specific item...")

         parser = BeautifulSoup(resp2.text, 'html.parser')

         itemList = parser.find("ul", id="container")

         # gets all tags that are product names
         found = 0
         for i in itemList.find_all("div", "product-name"):
            # gets all item names in item list
            for item in itemSpecs:
                if item in i.contents[0].text:
                    found = 1
                    itemTag = i.contents[0]
                    #looks at the style of the product
                    colorTag = i.next_sibling.contents[0]
                    if itemSpecs.get(item)[0] == colorTag.text:
                        nextURL = "https://www.supremenewyork.com" + itemTag['href']
                        print (nextURL)
                        browser.get(nextURL)
                        resp2 = requests.get(nextURL)
                        parser = BeautifulSoup(resp2.text, 'html.parser')
                        if itemSpecs.get(item)[1] != None:
                            while (1):
                                try:
                                    sizeList = parser.find("select", id="s")
                                    sizeCount = 0
                                    options = sizeList.find_all("option")
                                    for size in options:
                                        sizeCount += 1
                                        if itemSpecs.get(item)[1] == size.text:
                                            pathName = '//*[@id="s"]/option[' + str(sizeCount) + ']'
                                            if (len(options) == 1):
                                                pathName = '//*[@id="s"]/option'
                                            browser.find_element_by_xpath(pathName).click()
                                    break
                                except:
                                    print("Sizes not available yet.")

                        print("Adding to cart")
                        browser.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').click()

         if not found:
            print("Website not updated yet. Trying again!")
            nextPage(urlStr, itemSpecs)

def infoFill(checkoutPage, details):
    while (1):
        try:
            nameLine = browser.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(keys['name'])
            break
        except:
            print("Trying to enter name.")
    browser.find_element_by_xpath('//*[@id="order_email"]').send_keys(keys['email'])
    #sends phone number piece by piece cause of sendkeys error
    browser.find_element_by_xpath('//*[@id="order_tel"]').send_keys(keys['tel'])
    browser.find_element_by_xpath('//*[@id="bo"]').send_keys(keys['address'])
    browser.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(keys['zip'])
    #city auto added by supremem website
    browser.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(keys['city'])
    browser.find_element_by_xpath('//*[@id="cart-address"]/fieldset/div[7]/div/ins').click()
    browser.find_element_by_xpath('//*[@id="rnsnckrn"]').send_keys(keys['credNumber'])
    #card expiration date month (to change just change the number after "option" to desired month)
    browser.find_element_by_xpath('//*[@id="credit_card_month"]/option[5]').click()
    #card expiration date year (to change just change the number after
    #option with option 8 being the year 2027)
    browser.find_element_by_xpath('//*[@id="credit_card_year"]/option[6]').click()
    browser.find_element_by_xpath('//*[@id="orcer"]').send_keys(keys['cvv'])
    #click the terms and agreement box
    browser.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p/label/div/ins').click()
    #click the checkout (comment out when testing)
    browser.find_element_by_xpath('//*[@id="pay"]/input').click()
    #attempt to click in buster icon
    browser.switch_to.default_content()
    WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"/html/body/div[3]/div[2]/iframe")))
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='rc-imageselect']/div[3]/div[2]/div[1]/div[1]/div[4]"))).click()
    """while (1):
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[7]/div[2]/div[1]/div[1]/div[4]"))).click()
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='working']")))
        print("extra captcha")"""


start = time.time()
chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_extension("/Users/Andy/Desktop/mpbjkejclgfgadiemmefgebjfooflfhl/1.1.0_0.crx")
browser = webdriver.Chrome('./chromedriver', options=chrome_options)
categories(itemCats, descriptList)
time.sleep(1)
while (1):
    try:
        browser.find_element_by_xpath('//*[@id="cart"]/a[2]').click()
        break
    except:
        print("Trying to go to checkout.")
infoFill(browser, keys)
print (time.time() - start)
