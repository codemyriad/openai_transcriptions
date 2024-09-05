import click
import os
import multiprocessing
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
from PIL import Image

def get_output_directory(pdf_path):
    """Get the output directory for intermediate results."""
    pdf_dir = os.path.dirname(pdf_path)
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    return os.path.join(pdf_dir, pdf_name)

def get_tiff_path(output_dir, page_number):
    """Get the path for the TIFF file."""
    return os.path.join(output_dir, f"page{page_number}.tiff")

def get_text_path(output_dir, page_number):
    """Get the path for the OCR text file."""
    return os.path.join(output_dir, f"page{page_number}-ocr.txt")

def get_chatgpt_text_path(output_dir, page_number):
    """Get the path for the ChatGPT transcription."""
    return os.path.join(output_dir, f"page{page_number}-chatgpt-transcription.txt")

def get_default_cores():
    """Calculate the default number of cores to use."""
    total_cores = multiprocessing.cpu_count()
    return max(1, total_cores - 2)  # Ensure at least 1 core is used

import requests
import json
import base64
import os
import io
from openai_transcriptions.config import PROMPT

def submit_to_chatgpt(image_path, ocr_text, destination_path):
    """Submit the image and the OCR text to ChatGPT using our PROMPT."""
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    with Image.open(image_path) as img:
        width, height = img.size
        click.echo(f"Image size: {width}x{height} pixels")
        click.echo(f"OCRed text length: {len(ocr_text)} characters")

        # Convert image to PNG
        png_buffer = io.BytesIO()
        img.save(png_buffer, format="PNG")
        png_buffer.seek(0)
        encoded_image = base64.b64encode(png_buffer.getvalue()).decode('utf-8')

    click.echo("Uploading the file and getting transcription from ChatGPT")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Prepare the messages
    messages = [
        {
            "role": "system",
            "content": "Sei un esperto nel trascrivere articoli di giornale riconoscendo il testo e migliorando trascrizioni OCR."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"{PROMPT}\n\n{ocr_text}\n\n"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                }
            ]
        }
    ]

    # Prepare the payload
    payload = {
        "model": "gpt-4o",
        "messages": messages,
    }

    # Make the API call
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        transcription = result['choices'][0]['message']['content']

        # Save the transcription to the destination file
        with open(destination_path, 'w', encoding='utf-8') as f:
            f.write(transcription)

        click.echo(f"Transcription saved to {destination_path}")
    else:
        click.echo(f"Error: Unable to get transcription. Status code: {response.status_code}")
        click.echo(f"Response: {response.text}")

def process_page(pdf_path, page_number, lang='ita', num_cores=None):
    """Process a single page of a PDF file."""
    click.echo(f"Processing page {page_number} of {pdf_path}")

    output_dir = get_output_directory(pdf_path)
    os.makedirs(output_dir, exist_ok=True)

    tiff_path = get_tiff_path(output_dir, page_number)
    ocr_text_path = get_text_path(output_dir, page_number)

    # Check if TIFF file already exists
    if not os.path.exists(tiff_path):
        # Convert the specific page to an image with a height of 3000 pixels
        images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number, size=(None, 3000))

        if images:
            # Save the image as a TIFF file
            images[0].save(tiff_path, format="TIFF")
            click.echo(f"Created TIFF file: {tiff_path}")
        else:
            click.echo(f"Failed to convert page {page_number} to image")
            return
    else:
        click.echo(f"TIFF file already exists: {tiff_path}")

    # Check if OCR text file already exists
    if not os.path.exists(ocr_text_path):
        # Perform OCR on the TIFF file
        try:
            click.echo(f"Performing OCR on the page using language: {lang}")
            config = f'--oem 3 --psm 6 -l {lang}'
            if num_cores:
                config += f' -c tessedit_thread_count={num_cores}'
            text = pytesseract.image_to_string(tiff_path, config=config)
            with open(ocr_text_path, 'w', encoding='utf-8') as f:
                f.write(text)
            click.echo(f"OCR completed. Text saved to: {ocr_text_path}")
        except pytesseract.TesseractError as e:
            click.echo(f"Error performing OCR on page {page_number}: {str(e)}")
            return
    else:
        click.echo(f"OCR text file already exists: {ocr_text_path}")
        with open(ocr_text_path, 'r', encoding='utf-8') as f:
            text = f.read()

    click.echo("Analyzing image and text:")
    destination_path = get_chatgpt_text_path(output_dir, page_number)
    submit_to_chatgpt(tiff_path, text, destination_path)
    click.echo("Done! Time to submit the text to ChatGPT together with the original image and our prompt")

@click.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--page', type=int, default=None, help='Page number to process (optional)')
@click.option('--lang', type=str, default='ita', help='Language for OCR (default: Italian)')
@click.option('--cores', type=int, default=None, help='Number of cores to use for OCR (default: total cores - 2)')
def process_pdf(pdf_path, page, lang, cores):
    """Process a PDF file and optionally specify a page number."""
    click.echo(f"Processing PDF: {pdf_path}")

    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)

    if cores is None:
        cores = get_default_cores()
    click.echo(f"Using {cores} cores for OCR")

    if page:
        if 1 <= page <= num_pages:
            process_page(pdf_path, page, lang, cores)
        else:
            click.echo(f"Error: Page {page} is out of range. The PDF has {num_pages} pages.")
    else:
        click.echo(f"Processing all {num_pages} pages")
        for page_num in range(1, num_pages + 1):
            process_page(pdf_path, page_num, lang, cores)
