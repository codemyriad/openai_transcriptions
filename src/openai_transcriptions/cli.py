import click
import tempfile
import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

def process_page(pdf_path, page_number, lang='ita'):
    """Process a single page of a PDF file."""
    click.echo(f"Processing page {page_number} of {pdf_path}")

    # Create a temporary directory to store the TIFF file
    with tempfile.TemporaryDirectory() as temp_dir:
        # Convert the specific page to an image with a height of 3000 pixels
        images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number, size=(None, 3000))

        if images:
            # Save the image as a TIFF file
            tiff_path = os.path.join(temp_dir, f"page_{page_number}.tiff")
            images[0].save(tiff_path, format="TIFF")
            click.echo(f"Created temporary TIFF file: {tiff_path}")

            # Perform OCR on the TIFF file
            try:
                click.echo(f"Performing OCR on the page using language: {lang}")
                text = pytesseract.image_to_string(tiff_path, lang=lang)
                click.echo("OCR completed. Text extracted:")
                click.echo(text)
                click.echo("Done! Time to submit the text to ChatGPT together with the original image and our prompt")
            except pytesseract.TesseractError as e:
                click.echo(f"Error performing OCR on page {page_number}: {str(e)}")
        else:
            click.echo(f"Failed to convert page {page_number} to image")

@click.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--page', type=int, default=None, help='Page number to process (optional)')
@click.option('--lang', type=str, default='ita', help='Language for OCR (default: Italian)')
def process_pdf(pdf_path, page, lang):
    """Process a PDF file and optionally specify a page number."""
    click.echo(f"Processing PDF: {pdf_path}")

    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)

    if page:
        if 1 <= page <= num_pages:
            process_page(pdf_path, page, lang)
        else:
            click.echo(f"Error: Page {page} is out of range. The PDF has {num_pages} pages.")
    else:
        click.echo(f"Processing all {num_pages} pages")
        for page_num in range(1, num_pages + 1):
            process_page(pdf_path, page_num, lang)
