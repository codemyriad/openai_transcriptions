import click

@click.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--page', type=int, default=None, help='Page number to process (optional)')
def process_pdf(pdf_path, page):
    """Process a PDF file and optionally specify a page number."""
    click.echo(f"Processing PDF: {pdf_path}")
    if page:
        click.echo(f"Processing page: {page}")
    else:
        click.echo("Processing all pages")
    # Add your PDF processing logic here
