import csv
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Step 1: Read Data from CSV
csv_file_path = "company_data.csv"

companies = []  # List to store company details
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    header = next(csv_reader)  # Skip the header
    for row in csv_reader:
        date, court_info, company_name, company_type, location = row
        companies.append({"name": company_name, "location": location})

# Step 2: Navigate to Gelbe Seiten and Search for Companies
driver = webdriver.Chrome(ChromeDriverManager().install())
gelbe_seiten_url = "https://www.gelbeseiten.de/"
driver.get(gelbe_seiten_url)
time.sleep(5)

# Loop through the companies list
for company in companies:
    # Find and interact with the "What" input
    what_input = driver.find_element(By.ID, "what_search")
    what_input.clear()
    what_input.send_keys(company["name"])

    # Find and interact with the "Where" input
    where_input = driver.find_element(By.ID, "where_search")
    where_input.clear()
    where_input.send_keys(company["location"])

    # Find and click the "Find" button
    find_button = driver.find_element(By.CSS_SELECTOR, 'button.search_go')

    # Use WebDriverWait to wait until the button is clickable
    wait = WebDriverWait(driver, 10)
    find_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.search_go')))
    find_button.click()

    # Add a sleep time to wait for the search results to load
    time.sleep(5)

    #Check if there  are search results
    no_results= driver.find_elements(By.CLASS_NAME, 'mod-Treffer--keineTreffer')
    if no_results:
        print(f"No results found for {company['name']} in {company['location']}")
        continue  # Move on to the next company

    # Click on the first result by clicking on the link
    try:
        first_result_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article.mod-Treffer a'))
        )
        first_result_link.click()

        # Add a sleep time to wait for the detailed page to load
        time.sleep(5)
    except Exception as e:
        print(f"Error clicking on result for {company['name']} in {company['location']}: {e}")
        continue  # Move on to the next company

    # Add a sleep time to wait for the detailed page to load
    time.sleep(5)

    #TODO: Extract information from the detailed page
    # Extract information from the detailed page
    # ...

    # Extract information only if the elements are present
    try:

        # Email
        email_link = driver.find_element(By.ID, 'email_versenden')
        email = email_link.get_attribute('data-link').split(":")[1].split("?")[0]

        # Website
        website_link = driver.find_element(By.CSS_SELECTOR,
                                           'a[data-wipe-realview="detailseite_aktionsleiste_webadresse"]')
        website = website_link.get_attribute('href')
    except Exception as e:
        print(f"Failed to extract information for {company['name']} in {company['location']}. Error: {e}")
        continue

    # Save the information to a new Csv file
    output_csv_file = "company_details.csv"
    with open(output_csv_file, mode='a', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['company_name', 'location', 'website', 'email']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Check if the csv file is empty, if so, write the header
        if csvfile.tell() == 0:
            writer.writeheader()

        # Write the company details to the csv file
        writer.writerow({
            'company_name': company['name'],
            'location': company["location"],
            'website': website,
            'email': email
        })

    # Go back to the search resukts page for the next iteration
    driver.back()


# Close the browser window
driver.quit()
