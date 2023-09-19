# Create an empty set to store unique entries
unique_entries = set()

# Create an empty set to store duplicate entries
duplicate_entries = set()

print("startin'")

# Open the file for reading
with open("people_list.txt", "r") as file:
    # Read each line from the file
    for line in file:
        # Remove leading and trailing whitespace and convert to lowercase for case-insensitive comparison
        entry = line.strip().lower()

        # Check if the entry is already in the set of unique entries
        if entry in unique_entries:
            duplicate_entries.add(entry)
        else:
            # Add the entry to the set if it's not a duplicate
            unique_entries.add(entry)

# Print the duplicate entries
for entry in duplicate_entries:
    print(f"{entry}")
