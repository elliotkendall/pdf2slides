# pdf2slides

Converts PDFs of presentations into Google Slides documents using
ImageMagick and the Google Slides/Drive REST APIs

## How it works

Using ImageMagick (and specifically the Python pgmagick module), each page
of the PDF gets converted into an image.  That image then gets uploaded to
Google Drive, added to a Slides presentation as a new slide, then deleted
from Google Drive.  You're left with a Slides presentation containing one
slide per page of the source document, each with a full-page image of the
original page.

## Local Installation

Make sure you have the necessary Python modules.  You can fetch them all
with pip:

`pip install -r requirements.txt`

Or install them with APT if you're running Debian and friends:

`sudo apt-get install python-pgmagick python-oauth2client python-googleapi`

## Google Setup

Visit this link and click the "Enable the Drive API" button.  As the page
instructs, download the resulting file and save it as credentials.json in
the same directory as this python code.

https://developers.google.com/drive/api/v3/quickstart/python

The first time you run the program, it will open a web browser to prompt you
to authorize it to use Drive and Slides as your Google Account.

## Usage

Simply run the pdf2slides with the name of a PDF file. For example:

`./pdf2slides example.pdf`

or

`python pdf2slides example.pdf`
