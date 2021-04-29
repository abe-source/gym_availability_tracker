#!/usr/bin/env python3
from selenium import webdriver
from datetime import datetime
import pytz
import sqlite3
# uncomment this to run on ubuntu server
#from pyvirtualdisplay import Display

# define variables for easier alterations later
driver_location = "/Users/arminasbek/Downloads/chromedriver"
web_page = 'https://lemongym.lt'
x_path = '/html/body/div[5]/div/div/div/div/div[2]/div/div[4]/h2'
database_file = "db/lemongym.db"
# uncomment the below to run on ubuntu server
#display = Display(visible=0, size=(800, 600))

# initiate database connection
conn = sqlite3.connect(database_file)
cursor = conn.cursor()

# define Vilnius time zone
vilnius_time_zone = pytz.timezone('Europe/Vilnius')
vilnius_time = datetime.now(vilnius_time_zone)

# uncomment the below to run on ubuntu server
#display.start()

# initiate web driver and define options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(driver_location, options=options)

# load the website
driver.get(web_page)

# find element by xpath and assign element text to variable
availability_element = driver.find_element_by_xpath(x_path).text

# strip percentage sign, convert string to integer and assign to variable
availability_percentage = int(availability_element.rstrip("%"))

# uncomment the below for debugging
#print(availability_percentage) # availability percentage
#print(vilnius_time.strftime("%d-%m-%y")) # date
#print(vilnius_time.strftime("%H:%M:%S")) # time

# insert scraped inf with date and time to database
insert_to_db = f"INSERT INTO lemongym (availability_percentage, vilnius_date, vilnius_time) VALUES ('{availability_percentage}','{vilnius_time.strftime('%d-%m-%y')}','{vilnius_time.strftime('%H:%M:%S')}')"
cursor.execute(insert_to_db)
conn.commit()

driver.quit()

# uncomment this to run on ubuntu server
#display.stop()
