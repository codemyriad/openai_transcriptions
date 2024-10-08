from setuptools import setup, find_packages

setup(
    name="openai_transcriptions",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "click",
        "PyPDF2",
        "pdf2image",
        "pytesseract",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A project for OpenAI transcriptions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/openai_transcriptions",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'process-pdf=openai_transcriptions.cli:process_pdf',
        ],
    },
)
