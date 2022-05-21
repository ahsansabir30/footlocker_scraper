import requests
import string
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
import pandas as pd

csv_file = open("men_shoes.csv", "w")
csv_writer = csv.writer(csv_file, dialect=csv.excel)
csv_writer.writerow(['shoes_id', 'name', 'colour', 'desc', 'features', 'price', 'original_price', 'size_list', 'images', 'alternatives'])

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/95.0.4638.69 Safari/537.36"}

url = "https://www.footlocker.co.uk/en/category/men/shoes.html"
r = requests.get(url, headers=header).text
shoes_body = BeautifulSoup(r, "html.parser")
shoes = shoes_body.find_all(class_="product-container col")

# amount of pages
pages = shoes_body.find_all(class_="col col-shrink Pagination-option Pagination-option--digit")[2]
pages = pages.text
print(pages)


def connection(connection_drivers):
    no_connection = True
    while no_connection:
        try:
            try:
                connection_drivers.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div[2]/button').click()
            except Exception as f:
                print("no cookie pop-up")
            time.sleep(2)
            # checking if the last element is loaded on the page - so need to scroll to the bottom of the page
            connection_drivers.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            connection_drivers.find_element(By.XPATH, '/html/body/div[1]/div[1]/footer/div[1]/div/div[3]/div[1]/a')
            time.sleep(5)
            # scroll back up
            connection_drivers.execute_script("window.scroll(0, 0);")
            print("Connected")
            return connection_drivers
        except Exception:
            no_connection = True
            print("No Connection")
            time.sleep(20)


def information(information_drivers):
    name = information_drivers.find_element(By.XPATH, '//*[@id="pageTitle"]/span/span[1]').text
    print(name)
    desc = information_drivers.find_element(By.XPATH, '//*[@id="pageTitle"]/span/span[2]').text
    print(desc)
    colour = information_drivers.find_element(By.XPATH, '//*[@id="ProductDetails"]/div[4]/p').text
    print(colour)
    text_container = driver.find_element(By.CLASS_NAME, 'ProductDetails-description')
    features = text_container.find_element(By.TAG_NAME, 'ul').text.replace("\n", ", ")
    print(features)
    try:
        price = information_drivers.find_element(By.CLASS_NAME, 'ProductPrice-final').text.strip(" ").strip(
            "£").strip(
            "VAT included")
        original_price = information_drivers.find_element(By.CLASS_NAME, 'ProductPrice-original').text.strip(
            " ").strip(
            "£").strip("VAT included")
    except Exception as e:
        price = information_drivers.find_element(By.CLASS_NAME, 'ProductPrice').text.strip("").strip("£").strip(
            "VAT included")
        original_price = "N/A"
    print(price)
    print(original_price)

    shoe_info = information_drivers.find_element(By.XPATH,
                                    '//*[@id="ProductDetails-tabs-details-panel"]').text.strip(
        "Product #:")
    shoes_id = []
    for numbers in shoe_info:
        digits = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        alphabet = list(string.ascii_lowercase)
        alphabet_upper = list(string.ascii_uppercase)
        if numbers in digits:
            shoes_id.append(numbers)
        elif numbers in alphabet or alphabet_upper:
            break
    shoes_id = ''.join(map(str, shoes_id))
    print(shoes_id)

    size_list = []
    for size in sizes_table:
        try:
            size_availability = information_drivers.find_element(By.XPATH,
                                                    f'//*[@id="ProductDetails_radio_size_{size}"]"]')
            aria_label = size_availability.get_attribute('aria-label')
            size_list.append(aria_label)
        except Exception as f:
            size_availability = information_drivers.find_element(By.XPATH,
                                                    f'//*[@id="ProductDetails_radio_size_{size.replace(".", "").replace("/", "").replace(" ", "")}"]')
            aria_label = size_availability.get_attribute('aria-label')
            size_list.append(aria_label)
    print(size_list)
    try:
        container = information_drivers.find_element(By.CLASS_NAME, "ProductGallery")
        shoe_links = container.find_elements(By.TAG_NAME, "img")
        image_links = []
        for picture in shoe_links:
            image_links.append(picture.get_attribute('src'))
        print(image_links)
    except Exception as f:
        pass
    time.sleep(5)
    if total_shoes == 2:
        other_alternatives = "False"
    else:
        other_alternatives = "True"
    print(alternatives)
    csv_writer.writerow(
        [shoes_id, name, colour, desc, features, price, original_price, size_list, image_links, other_alternatives])


for page in range(0, int(pages)):
    url = f"https://www.footlocker.co.uk/en/category/men/shoes.html?currentPage={page}"
    print(url)
    r = requests.get(url, headers=header).text
    shoes_body = BeautifulSoup(r, "html.parser")
    shoes = shoes_body.find_all(class_="product-container col")
    for shoe in shoes:
        link = "https://www.footlocker.co.uk" + shoe.find(class_="ProductCard-link ProductCard-content")["href"]
        r = requests.get(link, headers=header).text
        shoe_body = BeautifulSoup(r, "html.parser")
        # need to put an if statement - to distinguish between out of stock and not
        geoBlocked = webdriver.FirefoxOptions()
        geoBlocked.set_preference("geo.prompt.testing", True)
        geoBlocked.set_preference("geo.prompt.testing.allow", False)
        driver = webdriver.Firefox(options=geoBlocked)
        driver.maximize_window()
        driver.get(link)
        time.sleep(20)
        connection(driver)
        time.sleep(20)
        try:
            # checking if shoe is in stock or not
            heading = driver.find_element(By.XPATH, '//*[@id="oosroi-148"]/div/div[1]/h5').text
            if heading == "Sorry, We've Sold Out!":
                time.sleep(2)
                try:
                    name = driver.find_element(By.XPATH, '//*[@id="pageTitle"]/span/span[1]').text
                    colour = driver.find_element(By.XPATH, '//*[@id="pageTitle"]/span/span[3]').text
                    image = driver.find_element(By.XPATH, '//*[@id="oosroi-148"]/div/div[2]/div[1]/div/img')
                    image = image.get_attribute('src')
                    time.sleep(5)
                    shoes_id = desc = features = price = original_price = size_list = other_alternatives = None
                    csv_writer.writerow([shoes_id, name, colour, desc, features, price, original_price, size_list, image, other_alternatives])
                    driver.close()
                except Exception as f:
                    pass
        except Exception as f:
            # getting sizes for shoes
            sizes_table = []
            try:
                sizes = shoe_body.find("div", class_="ProductSize-group")
                for size in sizes:
                    value = size.input["value"]
                    sizes_table.append(value)
            except Exception as f:
                pass
            # number of shoes being displayed
            # if there is more than 4 shoes, we have to display a pop-up first
            try:
                # we have more than 4 shoes, which requires a pop-up to get other alternatives
                more_4 = driver.find_element(By.XPATH, '//*[@id="ProductDetails"]/div[2]/button')
                total_shoes = 2 + len(
                    shoe_body.find_all(class_="c-form-field c-form-field--radio SelectStyle col")) + int(
                    shoe_body.find("button", class_="Button ProductStyles-toggler").text)
                alternatives = "True"
                for indivdual in range(1, total_shoes):
                    driver.find_element(By.XPATH, '//*[@id="ProductDetails"]/div[2]/button').click()
                    time.sleep(5)
                    # clicking on the shoe I want
                    driver.find_element(By.XPATH,
                                        f'/html/body/div[1]/div[1]/main/div/div[2]/div/div/form/div[2]/fieldset/div[{indivdual}]').click()
                    time.sleep(2)
                    driver.execute_script("window.scrollTo(0, 700)")
                    # applying what I have clicked
                    driver.find_element(By.XPATH, '//*[@id="ProductDetails"]/div[2]/div[3]/button').click()
                    time.sleep(5)
                    information(driver)
                    time.sleep(10)
            except Exception as f:
                # we do not have more than 4 shoes, so does not require a pop-up to choose the other options
                try:
                    total_shoes = 2 + len(shoe_body.find_all(class_="c-form-field c-form-field--radio SelectStyle col"))
                    for indivdual in range(1, total_shoes):
                        # clicking on the shoe I want
                        driver.find_element(By.XPATH,
                                            f'/html/body/div[1]/div[1]/main/div/div[2]/div/div/form/div[2]/fieldset/div[{indivdual}]').click()
                        time.sleep(2)
                        information(driver)
                except Exception as f:
                    pass
        driver.close()


csv_file.close()
df = pd.read_csv("men_shoes.cvs", encoding='unicode_escape')
df.to_excel("men_shoes.xlsx", index=None, header=True)
