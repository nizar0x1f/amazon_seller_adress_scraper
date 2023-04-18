from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re, csv


DRIVER_PATH = './chromedriver.exe'



def intialize_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
    return driver


def get_adress(driver, url):
    driver.get(url)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[text()='Detailed Seller Information']/../.."))
        )
        
        seller_info_box = driver.find_element(By.XPATH, "//h3[text()='Detailed Seller Information']/../..")
        raw_text = seller_info_box.text
        business_address = raw_text.split('Business Address:')[1]
        business_address = business_address.replace('\n', ' ')
        business_name = raw_text.split('Business Name:')[1].split('Business Address:')[0]
        business_name = business_name.replace('Business Name: ', '')
        business_name = business_name.replace('\n', ' ')
        print('business name: ', business_name)
        print('business address: ', business_address)
        return driver, business_name, business_address      


    except:
        driver.quit()



def utility():
    # read sellers urls fron text file
    with open('sellers.txt', 'r') as f:
        urls = f.readlines()
    # initialize driver
    driver = intialize_driver()
    # open csv file
    with open('sellers.csv', 'w', newline='') as csvfile:
        fieldnames = ['business_name', 'business_address']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for url in urls:
            driver, business_name, business_address = get_adress(driver, url)
            writer.writerow({'business_name': business_name, 'business_address': business_address})
    driver.quit()

if __name__ == '__main__':
    utility()
    