# OpenAI Transcriptions

OpenAI Transcriptions is a Python-based tool that processes PDF files, performs OCR (Optical Character Recognition) on each page, and then uses OpenAI's GPT-4 Vision model to analyze and transcribe the content, focusing on articles while excluding advertisements, headers, and other non-article content.

## Features

- Convert PDF pages to high-resolution TIFF images
- Perform OCR on the images to extract text
- Submit both the image and OCR text to OpenAI's GPT-4 Vision model
- Generate accurate transcriptions of articles, excluding ads and other non-article content
- Support for multi-page PDFs
- Option to process specific pages or entire documents
- Customizable language settings for OCR

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/openai_transcriptions.git
   cd openai_transcriptions
   ```

2. Install the package:
   ```
   pip install -e .
   ```

3. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

Use the `process-pdf` command to process a PDF file:

```
process-pdf path/to/your/file.pdf
```

Options:
- `--page`: Process a specific page (optional)
- `--lang`: Set the language for OCR (default: Italian)
- `--cores`: Specify the number of CPU cores to use for OCR

Example:
```
process-pdf path/to/your/file.pdf --page 1 --lang eng --cores 4
```

## Output

The tool will create a directory with the same name as the input PDF file, containing:
- TIFF images of each processed page
- OCR text files for each page
- ChatGPT transcriptions for each page

## Requirements

- Python 3.6+
- Tesseract OCR
- OpenAI API key

## License

This project is licensed under the GNU General Public License v3 (GPLv3). This means you are free to use, modify, and distribute this software, but any derivative work must also be distributed under the same license. For more details, see the [LICENSE.txt](LICENSE.txt) file in the project repository or visit [https://www.gnu.org/licenses/gpl-3.0.en.html](https://www.gnu.org/licenses/gpl-3.0.en.html).
