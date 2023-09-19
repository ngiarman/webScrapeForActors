
from selenium import webdriver
import random
import os
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import sys
import time
import re
import subprocess

userAgents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
]

# Set a random user agent from the list
user_agent = random.choice(userAgents)

#Get the site from the other class

site = sys.argv[1]

# Test scraper
#site = (" ")

# Check if the required command-line arguments are provided
if len(sys.argv) != 4:
    print("Usage: python your_script.py <site> <person_name> <line_number>")
    sys.exit(1)

# Get the variables from main
dsite = sys.argv[1]
person_name = sys.argv[2]
line_number = sys.argv[3]

# Set up ChromeOptions to open a new tab
chrome_options = Options()
chrome_options.add_argument("--new-tab")

# Set up the webdriver with a longer timeout
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(6)

# Function to navigate to the site with retry and increasing wait times
def navigate_with_retry(site_url):
    max_wait_time = 60
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            # Open the provided site in a new tab
            driver.get(site_url)

            # Check if the webpage is loaded every 2 seconds
            current_wait_time = 0
            while current_wait_time < max_wait_time:
                if EC.presence_of_element_located((By.TAG_NAME, 'body'))(driver):
                    print("Webpage loaded.")
                    return True  # Page loaded successfully
                else:
                    print("Webpage not fully loaded. Waiting for 2 more seconds...")
                    time.sleep(2)
                    current_wait_time += 2

            # If the page is still not loaded after the current wait time, increase wait time and retry
            max_wait_time *= 2  # Double the wait time
            retries += 1
            print(f"Retry #{retries}: Page not loaded after {current_wait_time} seconds. Retrying in {max_wait_time} seconds...")
            time.sleep(max_wait_time)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False  # Error occurred, do not retry

    print("Exceeded maximum retries. Could not load the page.")
    return False

# Main script logic
print("startin'")

try:
    # Get the page source after it has loaded using the navigate_with_retry function
    if not navigate_with_retry(site):
        driver.quit()  # Close the webdriver if retries are exhausted
        sys.exit("Script terminated due to repeated failures to load the page.")

    # Check if the site is down on wayback machine

except Exception as e:
    print(f"An error occurred: {str(e)}")

#

# Check if the page is an archive page and the site wasn't archived
if "The Wayback Machine has not archived that URL." in driver.page_source:
    print("Webpage is not archived. Switching to the regular site.")
    # Extract the regular link from the archive URL
    regular_site = re.search(r'web/(\d{14})/(https?://\S+)', site)
    if regular_site:
        regular_site = regular_site.group(2)
        print(f"Navigating to the regular site: {regular_site}")
        driver.get(regular_site)
    else:
        sys.exit("Regular site not found in the archive URL.")
else:
    print("Webpage is archived.")

#

print("startin'")

try:

    # Get the page source after it has loaded
    page_source = driver.page_source

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(page_source, "html.parser")

#

#

    # Read filter words from a text file
    filter_words = set()
    filter_file = "filter_words.txt"  # Replace with the path to your text file
    if os.path.exists(filter_file):
        with open(filter_file, "r") as file:
            for line in file:
                filter_words.add(line.strip().lower())  # Convert to lowercase for case-insensitive matching

#

#

    # name section

    # Find the element with both classes "post-title" and "entry-title"
    name_element = soup.find("h1", class_="post-title entry-title")

    # Initialize the "full_name" variable
    full_name = ""

    # Check if the element exists
    if name_element:
        # Get the content under the <h1> element
        full_name = name_element.get_text()

    # Print the extracted "full_name"
    print(f"Full Name: {full_name}")

#

#

#

#

    # Spelled out ethnicity section

    # Find all <strong> tags
    strong_tags = soup.find_all("strong")

    # Initialize a dictionary to store the extracted text with names
    extracted_text = {}
    seen_parts = set()  # To track seen parts and remove duplicates

    # Loop through the strong tags, assign each string a name, and extract their text
    for i, strong_tag in enumerate(strong_tags, start=1):
        text = strong_tag.get_text()
        name = f"String {i}"

        # Split the text based on line breaks
        text_lines = text.split('\n')

        # Define the bad keywords to search for
        keywords = ["some", "distant", "remote", "potential", "potentially", "possible", "possibly",
                    "small", "along with", "as well as", "smaller"]

        # Process each line
        processed_lines = []
        for line in text_lines:
            print(f"Line Content: {line}")

            # Iterate through bad keywords and remove text to the right of them
            for keyword in keywords:
                # find the keyword (case insensitive)
                pattern = re.compile(f"{re.escape(keyword)}.*", re.IGNORECASE)
                match = pattern.search(line)
                if match:
                    print(f"Found keyword '{keyword}' in line: {line}")
                    matched_text = match.group(0)
                    print(f"Matched text: {matched_text}")
                    line = pattern.sub('', line)
                    print(f"Processed line: {line}")

            # Append the processed line to the list
            processed_lines.append(line)

        # Join the processed lines back together
        processed_text = '\n'.join(processed_lines)

        # Split each line based on special characters using only filtered text
        text_parts = []
        for line in processed_text.split('\n'):
            parts = re.split(r'[-–!@#$%_/^&*(),/|\.?"{}[\]<>;:.,]', line)
            text_parts.extend(parts)

        #

        # Split each line based on "and" and "or"
        and_or_parts = []
        for line in text_lines:
            and_or_parts.extend(re.split(r'\band\b|\bor\b', line, flags=re.IGNORECASE))

        # Filter and add each part as a separate string
        for j, part in enumerate(text_parts, start=1):
            # Filter unwanted characters and words
            filtered_part = re.sub(r'[0-9!@#$%^&/|\*()[],.?":{}|<>]', '', part)
            filtered_part = re.sub(r'[^a-zA-Z0-9\s]', '', part)
            for word in filter_words:
                filtered_part = re.sub(rf'\b{re.escape(word)}\b', '', filtered_part, flags=re.IGNORECASE)
            filtered_part = filtered_part.strip()  # Remove leading/trailing whitespace
            if filtered_part:  # Only add non-empty parts

                # Check for duplicate parts and skip if already seen
                if filtered_part not in seen_parts:
                    seen_parts.add(filtered_part)

                    # Convert the filtered_part to lowercase
                    filtered_part = filtered_part.lower()
                    extracted_text[f"{name} - Part {j}"] = filtered_part

        # Print both the names and contents of each string in the dictionary
        for name, text in extracted_text.items():
            print(f"Name: {name}")
            print(f"Content: {text}\n")

    #

    # Tags section

    #

    # Find the paragraph "<p class="post-tags">"
    post_tags_paragraph = soup.find("p", class_="post-tags")

    # Check if the paragraph exists
    if post_tags_paragraph:
        # Find all anchor (<a>) tags with a "rel" attribute of "tag" below the paragraph
        tag_anchors = post_tags_paragraph.find_all_next("a", attrs={"rel": "tag"})

        # Initialize a dictionary to store the extracted tag content
        tag_content = {}

        # Loop through the anchor tags and extract their content
        for i, tag_anchor in enumerate(tag_anchors, start=1):
            tag_text = tag_anchor.get_text()
            name = f"String 2"

            # Replace hyphens with spaces and strip leading/trailing whitespace
            formatted_tag_text = tag_text.replace('-', ' ').strip()

            # Convert the formatted_tag_text to lowercase
            formatted_tag_text = formatted_tag_text.lower()

            # Check if the tag content matches the pattern "b####" (b followed by four numbers)
            if not formatted_tag_text.startswith('b') or not formatted_tag_text[1:].isdigit() or len(
                    formatted_tag_text) != 5:
                # Add the formatted tag content to the dictionary only if it doesn't match the pattern
                tag_content[f"{name} - Part {i}"] = formatted_tag_text

        # Print the names and contents of the extracted tag content
        for name, text in tag_content.items():
            print(f"Name: {name}")
            print(f"Content: {text}\n")

except Exception as e:
    print(f"Extracting text didn't work properly: {str(e)}")


#

#

#image and URL section

# Find the main image with the data-srcset attribute
main_image = soup.find("img", attrs={"data-srcset": True})

# Initialize the "image_url" variable
image_url = ""

# Check if the image element exists and has the data-srcset attribute
if main_image and "data-srcset" in main_image.attrs:
    # Get the value of the data-srcset attribute
    image_srcset = main_image["data-srcset"]

    # Split the srcset by commas and select the first URL
    image_url = image_srcset.split(",")[0].split(" ")[0]

# Print the extracted image URL
print(f"Main Image URL: {image_url}")

# Print the current URL
#driver.get(url)
current_url = site
print(f"Current URL: {current_url}")

#

#

# Pass to MongoPut

# Create a list of arguments to pass to the mongoPut
args = [
    "python",  # Command to run Python
    "mongoPut.py",  # The name of the external script
    "--full-name", person_name,
    "--web-page-url", site,
    "--main-image-url", image_url,
#    "--line_number", line_number,
]

# Serialize the dictionaries and pass them as JSON strings
import json
extracted_text_json = json.dumps(extracted_text)
tag_content_json = json.dumps(tag_content)

# Pass the JSON strings as arguments
args.extend(["--extracted-text", extracted_text_json])
args.extend(["--tag-content", tag_content_json])

# Run the external script with the provided arguments
try:
    subprocess.run(args, check=True)
    print("Data sent to mongoPut.py successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error while running mongoPut.py: {e}")
except Exception as e:
    print(f"Error: {str(e)}")

print("Goin' to the next person")

# Close the tab at the end
driver.close()

# Switch back to the original tab
#driver.switch_to.window(driver.window_handles[0])

# Close the webdriver
driver.quit()

