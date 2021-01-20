import requests
import time
from config import keys
from config import itemCats
from config import descriptList
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
                print "Found the URL: " + newURL

                nextPage(newURL, itemDesc)
                print "_______________________________"
    else:
        print("Error")

def nextPage(urlStr, itemSpecs):
    resp2 = requests.get(urlStr)

    if resp2.status_code == 200:
         print("Looking for specific item...")

         parser = BeautifulSoup(resp2.text, 'html.parser')

         itemList = parser.find("ul", id="container")

         #gets all tags that are product names
         found = 0
         for i in itemList.find_all("div", "product-name"):
            #gets all item names in item list
            for item in itemSpecs:
                if item in i.contents[0].text:
                    found = 1
                    itemTag = i.contents[0]
                    #looks at the style of the product
                    colorTag = i.next_sibling.contents[0]
                    if itemSpecs.get(item)[0] == colorTag.text:
                        nextURL = "https://www.supremenewyork.com" + itemTag['href']
                        print nextURL
                        browser.get(nextURL)
                        resp2 = requests.get(nextURL)
                        parser = BeautifulSoup(resp2.text, 'html.parser')
                        #trys to get the correct size
                        try:
                            sizeList = parser.find("select", id="s")
                            sizeCount = 0
                            options = sizeList.find_all("option")
                            for size in options:
                                sizeCount += 1
                                if itemSpecs.get(item)[1] == size.text:
                                    pathName = '//*[@id="s"]/option[' + str(sizeCount) + ']'
                                    #if (len(options) == 1):
                                        #pathName = '//*[@id="s"]/option'
                                    #print("PATH NAME: ", pathName)
                                    #browser.find_element_by_xpath(pathName).click()

                        except:
                            print("This item doesn't have sizes")
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
    browser.find_element_by_xpath('//*[@id="order_tel"]').send_keys(keys['tel'])
    browser.find_element_by_xpath('//*[@id="bo"]').send_keys(keys['address'])
    browser.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(keys['zip'])
    #city auto added by supremem website
    #browser.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(keys['city'])
    browser.find_element_by_xpath('//*[@id="cart-address"]/fieldset/div[7]/div/ins').click()
    browser.find_element_by_xpath('//*[@id="rnsnckrn"]').send_keys(keys['credNumber'])
    #card expiration date month (to change just change the number after "option" to desired month)
    browser.find_element_by_xpath('//*[@id="credit_card_month"]/option[6]').click()
    #card expiration date year (to change just change the number after
    #option with option 8 being the year 2027)
    browser.find_element_by_xpath('//*[@id="credit_card_year"]/option[8]').click()
    browser.find_element_by_xpath('//*[@id="orcer"]').send_keys(keys['cvv'])
    #clcik the terms and agreement box
    browser.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p/label/div/ins').click()




start = time.time()
browser = webdriver.Safari()
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
