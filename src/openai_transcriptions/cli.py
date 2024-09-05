import click
import tempfile
import os
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

def process_page(pdf_path, page_number):
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
                text = pytesseract.image_to_string(tiff_path)
                click.echo(f"OCR Result for page {page_number}:")
                click.echo(text)
            except pytesseract.TesseractError as e:
                click.echo(f"Error performing OCR on page {page_number}: {str(e)}")
        else:
            click.echo(f"Failed to convert page {page_number} to image")

@click.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--page', type=int, default=None, help='Page number to process (optional)')
def process_pdf(pdf_path, page):
    """Process a PDF file and optionally specify a page number."""
    click.echo(f"Processing PDF: {pdf_path}")
    
    reader = PdfReader(pdf_path)
    num_pages = len(reader.pages)
    
    if page:
        if 1 <= page <= num_pages:
            process_page(pdf_path, page)
        else:
            click.echo(f"Error: Page {page} is out of range. The PDF has {num_pages} pages.")
    else:
        click.echo(f"Processing all {num_pages} pages")
        for page_num in range(1, num_pages + 1):
            process_page(pdf_path, page_num)
