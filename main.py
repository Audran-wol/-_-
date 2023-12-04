#Install the required python libraries
import csv

from selenium.common.exceptions import  NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())


url = "https://www.unternehmensregister.de/ureg/search1.3.html;jsessionid=EADD84A092E46554E8E2217098252036.web01-1?submitaction=language&language=en"
driver.get(url)
time.sleep(10)

#Select the button menu
menu = driver.find_element_by_class_name("menu__toggle")
menu.click()

# Find and click the menu item "Register disclosures"
register_disclosures_option = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//ul[@id='item1']//li/a[text()='Register disclosures']"))
)
register_disclosures_option.click()
time.sleep(6)


# Select the registration form
select = Select(driver.find_element_by_id("searchRegisterForm:publicationsPublicationType"))
select.select_by_visible_text("Submission of new documents")

# Enter the form date
from_date = driver.find_element_by_id("searchRegisterForm:publicationsStartDate")
from_date.clear()
from_date.send_keys("01/01/2023")
time.sleep(5)

# Enter the unitl date
until_date = driver.find_element_by_id("searchRegisterForm:publicationsEndDate")
until_date.clear()
until_date.send_keys("12/02/2023")

#Click on the search Button
search_button = driver.find_element_by_name("searchRegisterForm:j_idt257")
search_button.click()
time.sleep(15)

#Increase the number of publications per page to 100
hits_per_page_select = Select(driver.find_element_by_id("hppForm:hitsperpage"))
hits_per_page_select.select_by_visible_text("100")
time.sleep(10)

#Create a csv file to store the data
with open("company_data.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Company Name", "Location", "Date"])

# Loop through the pages
    while True:
        company_results = driver.find_elements_by_class_name("company_result")

        #Loop through the company results
        for company_result in company_results:
            try:
                company_name = company_result.find_element_by_tag_name("span").text
                p_element = company_result.find_element_by_tag_name("p")
                p_text = p_element.text.split("\n")
                location = p_element.text.split("\n")[0]
                date = p_text[-1]
                date = date.replace("Last update: ", "").strip()

                #Write the data to the csv file
                writer.writerow([company_name, location, date])
            except NoSuchElementException as e:
                print(f"Error: {e}. Some elemenst not found in the the current 'company_result' div")

        try:
            # Wait for the next page button to become visible and clickable
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "next")))
            next_page = driver.find_element_by_class_name("next")
        except NoSuchElementException:
            # Break out of the loop if the next page button is not found
            break
        else:
            next_page.click()
            time.sleep(10)

driver.quit()





