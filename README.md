# pdf2slides

Converts PDFs of presentations into Google Slides documents using ImageMagick
and the Google Slides/Drive REST APIs.

## How it works

Using ImageMagick (and specifically the Python wand module), each page of the
PDF gets converted into an image. That image then gets uploaded to Google
Drive, added to a Slides presentation as a new slide, then deleted from Google
Drive. You're left with a Slides presentation containing one slide per page of
the source document, each with a full-page image of the original page.

## Installation

Make sure you have Python 3 and ImageMagick installed. On macOS, using
Homebrew:

```bash
brew install python3 imagemagick
```

Or Linux:

```bash
sudo apt-get install python3 imagemagick
```

Then create a virtual environment:

```bash
python3 -m venv venv
```

And activate it:

```bash
source venv/bin/activate
```

Install the necessary Python modules with pip:

```bash
pip3 install -r requirements.txt
```

Or install them with APT if you're running Debian and friends:

```bash
sudo apt-get install python-wand python-oauth2client python-googleapi
```

## Set up Google API

Make sure this script is allowed to interact with your Google account. Visit
this link and click the "Enable the Drive API" button. As the page instructs,
download the resulting file and save it as `credentials.json` in the same
directory as this python code.

https://developers.google.com/drive/api/v3/quickstart/python

Fill in any name, and select "desktop app".

The first time you'll have to authenticate the Google API. Do this by running
`pdfslides.py` without any arguments:

```bash
./pdf2slides.py
```

This will open a web browser to prompt you to authorize it to use Drive and
Slides as your Google Account. You can close the browser after the "The
authentication flow has completed" message.

Finally, you'll have to separately enable the Slides API once. You can find
your project ID in the `credentials.json` file after `project_id`:

https://console.developers.google.com/apis/library/slides.googleapis.com?project=YOUR-PROJECT-ID

Alternatively you can run the script (`./pdf2slides.py example.pdf`) and grab
the URL from the error message.

## Usage

Run `pdf2slides.py` with the name of a PDF file. For example:

```bash
./pdf2slides.py example.pdf
```

or

```bash
python3 pdf2slides.py example.pdf
```