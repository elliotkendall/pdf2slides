from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client import file, client, tools

class GoogleSlides:
  def __init__(self, tokenfile, credsfile, scopes):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
      flow = client.flow_from_clientsecrets('credentials.json', scopes)
      creds = tools.run_flow(flow, store)
    self.api = build('slides', 'v1', http=creds.authorize(Http()))

  def createPresentation(self, title):
    presentation = self.api.presentations().create(body={"title": title}).execute()
    if not 'presentationId' in presentation:
      raise Exception('Failed to create presentation')
    return presentation

  def clearSlides(self, presentation):
    for slide in presentation['slides']:
      self.api.presentations().batchUpdate(
       body={'requests': {'deleteObject': {'objectId': slide['objectId']}}},
       presentationId=presentation['presentationId']).execute()

  def createSlide(self, pid):
    slide = self.api.presentations().batchUpdate(
      body={"requests":{"createSlide": {}}},
      presentationId=pid).execute()
    try:
      slideid = slide['replies'][0]['createSlide']['objectId']
    except KeyError:
      raise Exception('Failed to create slide')
    return slideid

  def addImageToSlide(self, pid, slideid, url):
    body = {"requests": [{'createImage': {'url': url, 'elementProperties': {'pageObjectId': slideid}}}]}
    self.api.presentations().batchUpdate(
      body=body,
      presentationId=pid).execute()

class GoogleDrive:
  def __init__(self, tokenfile, credsfile, scopes):
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
      flow = client.flow_from_clientsecrets('credentials.json', scopes)
      creds = tools.run_flow(flow, store)
    self.api = build('drive', 'v3', http=creds.authorize(Http()))

  def uploadFile(self, filename, type):
    media = MediaFileUpload(filename, mimetype=type)
    upload = self.api.files().create(body={'name': filename}, media_body=media).execute()
    return upload.get('id')

  def makePublic(self, fid):
    self.api.permissions().create(fileId=fid, body={'role': 'reader', 'type': 'anyone'}).execute()

  def getWebContentLink(self, fid):
    # You have to ask for the webContentLink field by name or it isn't
    # returned
    info = self.api.files().get(fileId=fid, fields='webContentLink').execute()
    return info['webContentLink']

  def deleteFile(self, fid):
    self.api.files().delete(fileId=fid).execute()
  