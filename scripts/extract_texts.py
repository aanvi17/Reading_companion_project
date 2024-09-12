# import os
# import json
# from pptx import Presentation

# def extract_text_from_pptx(file_path):
#     prs = Presentation(file_path)
#     text_runs = []
#     for slide in prs.slides:
#         for shape in slide.shapes:
#             if hasattr(shape, "text"):
#                 text_runs.append(shape.text)
#     return text_runs

# def extract_texts_from_directory(directory):
#     all_texts = []
#     skipped_files = []
#     files = os.listdir(directory)
#     print(f"Total files found in directory: {len(files)}")
    
#     for filename in files:
#         file_path = os.path.join(directory, filename)
#         if not os.access(file_path, os.R_OK):
#             print(f"File not readable: {filename}")
#             skipped_files.append(filename)
#             continue
        
#         print(f"Found file: {filename}")
#         if filename.endswith(".pptx"):
#             try:
#                 print(f"Processing file: {filename}")
#                 text = extract_text_from_pptx(file_path)
#                 if text:  # Check if any text was extracted
#                     all_texts.append({"filename": filename, "text": " ".join(text)})
#                     print(f"Successfully processed file: {filename}")
#                 else:
#                     print(f"No text found in file: {filename}")
#                     skipped_files.append(filename)
#             except Exception as e:
#                 print(f"Error processing file {filename}: {e}")
#                 skipped_files.append(filename)
#     return all_texts, skipped_files

# if __name__ == "__main__":
#     directory_path = 'D:/Pihu/Ppt_summarizer/data'  # Replace with your PPT directory
#     texts, skipped_files = extract_texts_from_directory(directory_path)
#     with open('data/extracted_texts.json', 'w') as f:
#         json.dump(texts, f, indent=4)

#     print(f"Skipped files: {skipped_files}")
#     print(f"Total files processed: {len(texts)}")
#     print(f"Total files skipped: {len(skipped_files)}")


from pptx import Presentation
import os
import json
import comtypes.client

def extract_text_from_pptx(file_path):
    prs = Presentation(file_path)
    text_runs = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text_runs.append(shape.text)
    return text_runs

def extract_text_from_ppt(file_path):
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1
    presentation = powerpoint.Presentations.Open(file_path)
    text_runs = []
    for slide in presentation.Slides:
        for shape in slide.Shapes:
            if shape.HasTextFrame:
                text_runs.append(shape.TextFrame.TextRange.Text)
    presentation.Close()
    powerpoint.Quit()
    return text_runs

def extract_texts_from_directory(directory):
    all_texts = []
    skipped_files = []
    files = os.listdir(directory)
    print(f"Total files found in directory: {len(files)}")
    
    for filename in files:
        file_path = os.path.join(directory, filename)
        if filename.endswith(".pptx"):
            print(f"Found PPTX file: {filename}")
            if not os.access(file_path, os.R_OK):
                print(f"File not readable: {filename}")
                skipped_files.append(filename)
                continue
            try:
                print(f"Processing PPTX file: {filename}")
                text = extract_text_from_pptx(file_path)
                if text:  # Check if any text was extracted
                    all_texts.append({"filename": filename, "text": " ".join(text)})
                    print(f"Successfully processed file: {filename}")
                else:
                    print(f"No text found in file: {filename}")
                    skipped_files.append(filename)
            except Exception as e:
                print(f"Error processing PPTX file {filename}: {e}")
                skipped_files.append(filename)
        elif filename.endswith(".ppt"):
            print(f"Found PPT file: {filename}")
            if not os.access(file_path, os.R_OK):
                print(f"File not readable: {filename}")
                skipped_files.append(filename)
                continue
            try:
                print(f"Processing PPT file: {filename}")
                text = extract_text_from_ppt(file_path)
                if text:  # Check if any text was extracted
                    all_texts.append({"filename": filename, "text": " ".join(text)})
                    print(f"Successfully processed file: {filename}")
                else:
                    print(f"No text found in file: {filename}")
                    skipped_files.append(filename)
            except Exception as e:
                print(f"Error processing PPT file {filename}: {e}")
                skipped_files.append(filename)
        else:
            print(f"Skipping non-PPT/PPTX file: {filename}")
    return all_texts, skipped_files

if __name__ == "__main__":
    directory_path = 'D:/Pihu/Ppt_summarizer/data'  # Replace with your PPT directory
    texts, skipped_files = extract_texts_from_directory(directory_path)
    with open('data/extracted_texts.json', 'w') as f:
        json.dump(texts, f, indent=4)

    print(f"Skipped files: {skipped_files}")
    print(f"Total files processed: {len(texts)}")
    print(f"Total files skipped: {len(skipped_files)}")
