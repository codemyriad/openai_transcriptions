import click

def process_page(pdf_path, page_number):
    """Process a single page of a PDF file."""
    click.echo(f"Processing page {page_number} of {pdf_path}")

@click.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--page', type=int, default=None, help='Page number to process (optional)')
def process_pdf(pdf_path, page):
    """Process a PDF file and optionally specify a page number."""
    click.echo(f"Processing PDF: {pdf_path}")
    if page:
        process_page(pdf_path, page)
    else:
        click.echo("Processing all pages")
        # Assuming we have a way to get the total number of pages
        # For now, let's just process pages 1 to 5 as an example
        for page_num in range(1, 6):
            process_page(pdf_path, page_num)
