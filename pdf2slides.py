#!/usr/bin/env python3
from pgmagick import Image, ImageList
from wand.image import Image
from GoogleAPIs import GoogleDrive, GoogleSlides
import sys, os

# If modifying these scopes, delete the file token.json
SCOPES = [
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/drive",
]

if not os.path.isfile("token.json"):
    drive = GoogleDrive("token.json", "credentials.json", SCOPES)
    slides = GoogleSlides("token.json", "credentials.json", SCOPES)
    sys.exit()

if len(sys.argv) < 2:
    print("Syntax: " + sys.argv[0] + " <pdf file>")
    sys.exit()

pages = Image(filename=sys.argv[1], resolution=300)
print("Read PDF file")

drive = GoogleDrive("token.json", "credentials.json", SCOPES)
slides = GoogleSlides("token.json", "credentials.json", SCOPES)
print("Initialized APIs")

# Create the presentation
presentation = slides.createPresentation(sys.argv[1])
pid = presentation["presentationId"]
print("Created presentation " + pid)

# Remove the blank first slide
slides.clearSlides(presentation)
print("Removed blank slide")

# Populate the slides
i = 0
for page in pages.sequence:
    print("Processing page " + str(i))

    # Write the image out
    with Image(page) as image:
        image.format = "png"
        image.save(filename="temp.png")

    # Create the slide
    slideid = slides.createSlide(pid)
    print("Added slide " + slideid)

    # Upload the image
    fid = drive.uploadFile("temp.png", "image/png")
    print("Uploaded image as " + fid)

    # Remove it locally
    os.remove("temp.png")
    print("Deleted local image file")

    # Make it public
    drive.makePublic(fid)
    print("Shared image file")

    # Get the public URL
    url = drive.getWebContentLink(fid)
    print("Public URL is " + url)

    # Add the image
    slides.addImageToSlide(pid, slideid, url)
    print("Added image to slide")

    # Remove the image from Google Drive
    drive.deleteFile(fid)
    print("Deleted file " + fid + " from Google Drive")

    i = i + 1
