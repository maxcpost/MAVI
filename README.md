MAVI
# PDF Text Extractor

## Overview
This project provides a script for extracting text content from PDF files using multiple methods, including direct text extraction and Optical Character Recognition (OCR). It processes PDF files from an input folder and saves the extracted text as TXT files in an output folder. ✅📂💾

## Features 
- Extracts text from PDFs using PyMuPDF
- Uses OCR (Tesseract) for image-based PDFs
- Handles scanned and text-based PDFs with a hybrid approach
- Saves extracted text as `.txt` files
- Processes multiple PDFs in batch mode
- Logs progress and errors for debugging

## Dependencies 
Ensure you have the following dependencies installed before running the script:

```bash
pip install pymupdf opencv-python pytesseract numpy openai
```

### Required Libraries 📚
| Library      | Purpose                           |
|-------------|----------------------------------|
| `fitz` (PyMuPDF)  | Extracts text from PDFs       |
| `cv2` (OpenCV)    | Processes images for OCR    |
| `pytesseract`     | Performs OCR on images      |
| `openai`          | Not currently in use        |
| `numpy`          | Handles numerical operations |

## Main Functions ⚙️

### `extract_text_from_pdf(pdf_path)`
Extracts text directly from PDFs using PyMuPDF.
- Works best for PDFs with selectable text.

### `extract_images_from_pdf(pdf_path)`
Extracts images from PDF pages and converts them to PNG format.
- Useful for scanned documents.

### `ocr_images(images)`
Performs OCR on extracted images.
- Converts images to grayscale for better accuracy.
- Uses `pytesseract` for text recognition.

### `mixed_extract_from_pdf(pdf_path)`
A hybrid approach that first attempts direct text extraction and falls back to OCR if needed.
- Ensures both text-based and scanned PDFs are processed correctly.

### `generate_txt(text, output_path)`
Creates and saves the extracted text as a `.txt` file.

### `main(input_folder, output_folder)`
Orchestrates the entire workflow:
- Processes all PDFs in the input folder.
- Extracts text using the best available method.
- Saves output to the specified folder.
- Logs progress and errors.

## Usage

### Running the Script 
```bash
python mavi.py /path/to/input_folder /path/to/output_folder
```

### Workflow 🔄
1. The script scans the input folder for PDF files.
2. Each PDF is processed using the `mixed_extract_from_pdf()` method.
3. Extracted text is saved as a `.txt` file in the output folder.
4. Errors and progress are logged for reference.

## Use Cases 📂
This tool is useful for:
- **Batch converting PDFs to text** for documentation processing.
- **Extracting text from scanned PDFs** to make them searchable.
- **Automating document conversion** workflows.

## Troubleshooting ⚠️
- **OCR accuracy is low?** Ensure Tesseract OCR is installed correctly and try different preprocessing steps.
- **Text extraction fails?** Some PDFs may be encrypted or image-heavy; try OCR mode.
- **Missing dependencies?** Run `pip install -r requirements.txt` to ensure all packages are installed.

## Future Enhancements
- Add support for different OCR languages.
- Implement parallel processing for faster batch conversion.
- Improve text formatting for better readability.

## License
This project is released under the MIT License. 

---
For questions or contributions, feel free to submit an issue or pull request! 💬🔗📩
