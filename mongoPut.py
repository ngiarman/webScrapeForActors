import argparse
import json
import re
from pymongo import MongoClient

print("***************This is the start of mongoPut*********************")

def main(args=None):
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Receive and print data for MongoDB")

    # Define command-line arguments
    parser.add_argument("--full-name", help="Full name")
    parser.add_argument("--web-page-url", help="Web page URL")
    parser.add_argument("--main-image-url", help="Main image URL")
    parser.add_argument("--extracted-text", help="Extracted text (JSON)")
    parser.add_argument("--tag-content", help="Tag content (JSON)")

    # Parse command-line arguments
    args = parser.parse_args()

    # Clean name
    clean_name = args.full_name.lower()
    # Remove special characters
    clean_name = re.sub(r'[!@#$%^&*(/)[\],.?"`~;:{}|<>=_+-]', ' ', clean_name)
    # Remove extra tabs newline characters at the beginning and end of text:
    clean_name = re.sub(r'^\s+|\s+$', '', clean_name)
    # Remove leading and trailing whitespaces:
    clean_name = clean_name.strip()
    # Replace multiple consecutive spaces
    clean_name = re.sub(r'\s+', ' ', clean_name)
    # Remove empty spaces between occurrences of two or more single letters
    clean_name = re.sub(r'(?<=\b[a-zA-Z])\s+(?=[a-zA-Z]\b)', '', clean_name)

    # Print the received data
    print("Received Data:")
    print(f"Full Name: {args.full_name}")
    print(f"Cleaned Name: {clean_name}")
    print(f"Web Page URL: {args.web_page_url}")
    print(f"Main Image URL: {args.main_image_url}")

    if args.extracted_text:
        extracted_text = json.loads(args.extracted_text)
        print("\nExtracted Text:")
        for key, value in extracted_text.items():
            print(f"{key}: {value}")

    if args.tag_content:
        tag_content = json.loads(args.tag_content)
        print("\nTag Content:")
        for key, value in tag_content.items():
            print(f"{key}: {value}")

    # Connect to the MongoDB client
    client = MongoClient("mongodb://localhost:27017/")

    # Access the "ethnicitydb" database
    db = client.ethnicitydb

    # Find the document in the "actorsMini" collection with a matching "name" field
    actor_document = db.actorsMini.find_one({"name": args.full_name})

    # If the actor document exists, update it
    if actor_document:
        # Define the updated data
        update_data = {
            "cleanName": clean_name,  # Use the cleaned name variable
            "ethnicityImage": args.main_image_url  # Assuming you want to update the image URL as well
        }

        # Update the document
        db.actorsMini.update_one({"_id": actor_document["_id"]}, {"$set": update_data})

        # Parse and update the extracted text (if provided)
        if args.extracted_text:
            extracted_text = json.loads(args.extracted_text)
            ethnicity_list_1 = [{"ethnicity": value, "percentage": 9} for key, value in extracted_text.items()]
            db.actorsMini.update_one({"_id": actor_document["_id"]}, {"$set": {"ethnicityList1": ethnicity_list_1}})

        # Parse and update the tag content (if provided)
        if args.tag_content:
            tag_content = json.loads(args.tag_content)
            ethnicity_list_2 = [{"ethnicity": value, "percentage": 9} for key, value in tag_content.items()]
            db.actorsMini.update_one({"_id": actor_document["_id"]}, {"$set": {"ethnicityList2": ethnicity_list_2}})

        print(f"Updated actor document for {args.full_name}")

    else:
        print(f"No actor document found for {args.full_name}")

if __name__ == "__main__":
    main()

print("***************this is the end of mongoPut*********************")
