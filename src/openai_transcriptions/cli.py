import click
from PyPDF2 import PdfReader

def process_page(pdf_path, page_number):
    """Process a single page of a PDF file."""
    click.echo(f"Processing page {page_number} of {pdf_path}")

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
