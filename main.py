import os
import shutil
import fitz  # PyMuPDF
import cv2
import pytesseract
import openai
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

# Fetch the API key from the environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client with the fetched API key
client = openai.OpenAI(api_key=openai_api_key)

# Check if the PDF is a searchable PDF (contains searchable text)
def is_searchable_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        has_searchable_text = False

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # Extract text using PyMuPDF's text extraction
            text = page.get_text()
            if text.strip():
                has_searchable_text = True
                break

            # If no text is found, use OCR on the page image
            pix = page.get_pixmap()
            img_data = pix.tobytes("png")
            img_np = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)

            # Perform OCR to check for text presence
            ocr_text = pytesseract.image_to_string(gray)
            if ocr_text.strip():
                has_searchable_text = True
                break

        doc.close()
        return has_searchable_text

    except Exception as e:
        print(f"Error checking PDF: {e}")
        return False

# Step 1: Extract images from PDF
def extract_images_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        images = []
        for page_num in range(len(doc)):  # Iterate over all pages
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img_data = pix.tobytes("png")
            images.append(img_data)
        doc.close()
        return images
    except Exception as e:
        print(f"Error extracting images: {e}")
        return []

# Step 2: OCR using OpenCV and Pytesseract
def ocr_images(images):
    text = ""
    try:
        for img_data in images:
            img_np = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
            text += pytesseract.image_to_string(gray) + "\n"  # Ensure separation between pages
        return text
    except Exception as e:
        print(f"Error during OCR: {e}")
        return ""

# Step 3: Correct text using OpenAI
def correct_text(text):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"Correct the following text:\n\n{text}"}
            ],
            max_tokens=2048
        )
        corrected_text = response.choices[0].message.content.strip()
        return corrected_text
    except Exception as e:
        print(f"Error during text correction: {e}")
        return text

# Step 4: Generate a new PDF with corrected text
def generate_pdf(text, output_path):
    try:
        c = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        text_object = c.beginText(40, height - 40)
        text_object.setFont("Helvetica", 12)
        lines = simpleSplit(text, "Helvetica", 12, width - 80)
        for line in lines:
            text_object.textLine(line)
        c.drawText(text_object)
        c.save()
    except Exception as e:
        print(f"Error generating PDF: {e}")

# Main function
def main(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_pdf_path = os.path.join(input_folder, filename)
            output_pdf_path = os.path.join(output_folder, filename)

            # If not searchable, treat as raster PDF and process accordingly
            print(f"{filename} is being processed as a raster PDF.")

            # Extract images from the PDF
            images = extract_images_from_pdf(input_pdf_path)
            if not images:
                print(f"No images extracted from {filename}.")
                continue

            # Extract text from images
            raw_text = ocr_images(images)
            if not raw_text:
                print(f"No text extracted from images in {filename}.")
                continue

            # Correct the text using OpenAI
            corrected_text = correct_text(raw_text)

            # Generate a new PDF with corrected text
            generate_pdf(corrected_text, output_pdf_path)
            print(f"Processed and saved {filename} to {output_pdf_path}")

# Example usage
input_folder = "input"  # Replace with the path to the folder containing the PDFs
output_folder = "output"  # Replace with the path to the folder for output PDFs
main(input_folder, output_folder)
