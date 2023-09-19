import subprocess
from selenium import webdriver
import random
import pymongo
from selenium.webdriver.chrome.options import Options

# set up the Chrome driver with a random user agent
options = Options()

userAgents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
]

# Set a random user agent from the list
user_agent = random.choice(userAgents)

# Define MongoDB connection
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["ethnicitydb"]
collection = db["actorsMini"]

# The people list file is a text file with rows of names. The script will read the names sequentially, match
# a name to the name in mongodb, and find the link.
# Define the path here
people_list_file_path = "d/PycharmProjects/actorsSite/people_list.txt"

print("Startin' webdriver")

# Initialize a Selenium WebDriver
try:
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
except Exception as e:
    print(f"Error initializing WebDriver: {str(e)}")
    exit(1)

print("Making a log")

# Open a log file for progress updates
log_file_path = "scrape_log.txt"
log_file = open(log_file_path, "w")

print("Startin' a loop...")

# Iterate through the list of people in the plain text file
with open(people_list_file_path, "r") as plain_text_file:
    for line_number, line in enumerate(plain_text_file, 1):  # Enumerate with starting line number 1
        print("Step 1")
        person_name = line.strip()

        # Query MongoDB to find the person's document and retrieve person_link
        person_document = collection.find_one({"name": person_name})
        if person_document:
            person_link = person_document.get("ethnicityLink", "")
            log_file.write(f"Found {person_name} in MongoDB\n")
            log_file.write(f"sending page for {person_name}\n")
            log_file.write(f"{person_link}\n")

            # Call the scraper script and pass person_link, person_name, and line_number as arguments
            try:
                subprocess.call(["python", "scrape.py", person_link, person_name, str(line_number)])
            except Exception as e:
                log_file.write(f"Error calling 'scrape.py': {str(e)}\n")
        else:
            log_file.write(f"Could not find {person_name} in MongoDB\n")

# Close the log file
log_file.close()

# Close the Selenium WebDriver
driver.quit()

# Show progress
print("Scraping completed. Check 'scrape_log.txt' for details.")

