# import json
# import csv
# import os

# # Load extracted texts
# with open('data/extracted_texts.json', 'r') as f:
#     texts = json.load(f)

# # Dictionary to hold summaries with filenames as keys
# summaries_dict = {}

# # Load summaries from CSV file
# with open('data/summaries.csv', 'r') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         summaries_dict[row['filename']] = row['summary']

# # List to hold the final data
# data = []

# # Directory containing PPT files
# ppt_directory = 'D:/Pihu/Ppt_summarizer/data'  # Replace with your PPT directory

# # Track processed PPTs
# processed_files = []

# # Combine texts and summaries
# for i, filename in enumerate(os.listdir(ppt_directory)):
#     if filename.endswith(".pptx"):
#         if i < len(texts):
#             text = texts[i]  # Assuming texts are in the same order as PPTs
#             summary = summaries_dict.get(filename, "Summary not found")  # Default to "Summary not found"
#             data.append({"text": text, "summary": summary})
#             processed_files.append(filename)
#         else:
#             print(f"No extracted text left for file: {filename}")

# # Print summary of processing
# print(f"Processed files: {processed_files}")
# print(f"Total files processed: {len(processed_files)}")
# print(f"Total texts available: {len(texts)}")
# print(f"Total summaries available: {len(summaries_dict)}")

# # Save to a single JSON file
# with open('data/train_data.json', 'w') as f:
#     json.dump(data, f, indent=4)

# create_summaries_csv.py

import json
import csv

# Load extracted texts
with open('data/extracted_texts.json', 'r') as f:
    texts = json.load(f)

# Dictionary to hold summaries with filenames as keys
summaries_dict = {}

# Load summaries from CSV file
with open('data/summaries.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        summaries_dict[row['filename']] = row['summary']

# List to hold the final data
data = []

# Track processed PPTs
processed_files = []

# Combine texts and summaries
for entry in texts:
    filename = entry["filename"]
    text = entry["text"]
    summary = summaries_dict.get(filename, "Summary not found")  # Default to "Summary not found"
    data.append({"text": text, "summary": summary})
    processed_files.append(filename)

# Print summary of processing
print(f"Processed files: {processed_files}")
print(f"Total files processed: {len(processed_files)}")
print(f"Total texts available: {len(texts)}")
print(f"Total summaries available: {len(summaries_dict)}")

# Save to a single JSON file
with open('data/train_data.json', 'w') as f:
    json.dump(data, f, indent=4)
