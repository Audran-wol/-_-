#Install the required python libraries
import csv


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager


# Function to scrapedetails from the company page
def scrape_company_details(driver):
    # Wait for the details section to be present
    wait.until(EC.presence_of_element_located((By.ID, 'rrbPanel_content')))

    details_section = driver.find_element_by_id('rrbPanel_content')
    soup = BeautifulSoup(details_section.get_attribute('innerHTML'), 'html.parser')

    # Extracting date from the details dsection
    date = soup.find('label', {'id': 'j_idt111'}).text.strip()
    court_info = soup.find('label', {'id': 'j_idt114'}).text.strip()
    company_name = soup.find('label', {'id': 'j_idt121'}).text.strip()
    company_type = soup.find('label', {'id': 'j_idt123'}).text.strip()
    location = soup.find('label', {'id': 'j_idt125'}).text.strip()

    return date, court_info, company_name, company_type, location

driver = webdriver.Chrome(ChromeDriverManager().install())

url = "https://www.handelsregister.de/rp_web/welcome.xhtml"
driver.get(url)

time.sleep(15)

#Create some sleep variables
wait = WebDriverWait(driver, 10)
wait30 = WebDriverWait(driver, 30)

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


#Create a csv file to store the data
csv_file = open('company_data.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Date', 'Court Info', 'Company Name', 'Company Type', 'Location'])

#Extract data from each company in the list
company_list = driver.find_elements_by_xpath('//a[@class="ui-commandlink ui-widget"]')
company_count = len(company_list)

for index in range(company_count):
    # Click on the company link to go to eh details page
    company_list = driver.find_elements_by_xpath('//a[@class="ui-commandlink ui-widget"]')
    company = company_list[index]

    # Use JavaScript to click on the company link
    driver.execute_script("arguments[0].click();", company)

    # Wait for the overlay to disappear
    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.ID, 'j_idt168_modal'))
        )
    except Exception as e:
        print(f"Overlay not found or not disappearing: {e}")

    # Scrape details from the details page
    date, court_info, company_name, company_type, location = scrape_company_details(driver)

    # Write data to CSV
    csv_writer.writerow([date, court_info, company_name, company_type, location])

    # Go back to the list of companies
    driver.back()

    # Wait for the list of companies to be present again
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//a[@class="ui-commandlink ui-widget"]'))
    )
    time.sleep(2)  # Add a short sleep to allow the page to stabilize

# Close the csv file
csv_file.close()

#Close the webdiver
driver.quit()






