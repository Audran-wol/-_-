#Install the required python libraries
import csv
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

# Add browser-executable path
# s = Service(r"C:\Users\Tiedang\Desktop\Development\chromedriver_win32\chromedriver.exe")
#
# driver = webdriver.Chrome(service=s)
url = "https://www.handelsregister.de/rp_web/welcome.xhtml"
driver.get(url)

time.sleep(10)

#Create some sleep variables
wait = WebDriverWait(driver, 10)
wait5 = WebDriverWait(driver, 5)

#Locate the Register anouncements section and click
register_announcement = driver.find_element_by_xpath('//*[@id="naviForm:rpNavMainMenuID"]/ul/li[4]')
register_announcement.click()

time.sleep(5)

#Locate the kategorie field and select "Submission of New documents"
kategorie = driver.find_element_by_id('formId:kategorie_label')
kategorie.click()
#Select selection of new documents
submission_of_new_documents = driver.find_element_by_xpath('//*[@id="formId:kategorie_3"]')
submission_of_new_documents.click()
time.sleep(5)

#Filter the form of selected arguments
filter_button = driver.find_element_by_xpath('//*[@id="formId:rrbSuche"]/span')
filter_button.click()

time.sleep(6)

#Parse the result with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract the required data
# find div  containing the data
data_div = soup.find('div', {'id': 'formId:datalistId_content', 'class': 'ui-datalise-content'})

# Find the dl within the div
data_list = soup.find('dl', {'id': 'formId:datalistId_list'})

# Find all dt elements within the dl
items = data_list.find_all('dt', {'class': 'ui-datalist-item'})

data = []

#Iterate over each item
for i, item in enumerate(items):
    # Construct the id for data span and the anchor tag
    date_id = f"formId:datalistId:{i}:datatumId"
    anchor_id = f"formId:datalistId:{i}:j_idt132:0:j_idt133"

    # Find the date span and the anchor tag
    date_span = item.find('span', {'id': re.compile(date_id)})
    anchor_tag = item.find('a', {'id': re.compile(anchor_id)})

    # Extract the date and the information
    date = date_span.text.strip()
    info = anchor_tag.text.strip()

    #Split the info to extract the company name and registration date
    info_parts = info.split('<br>')
    company_name = info_parts[1].strip()
    company_registration_date = info_parts[0].strip()

    # Append the data to the list
    data.append({
        'date': date,
        'company_name': company_name,
        'company_registration_date': company_registration_date
    })

# Write the data to csv file in JSON format
with open('data.csv', 'w', newline='') as csvfile:
    fieldnames = ['date', 'company_name', 'company_registration_date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in data:
        writer.writerow(row)


print("Data saved to data.csv")




