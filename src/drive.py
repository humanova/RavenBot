# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def UploadFile(path):

    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("creds.txt")
    if gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("creds.txt")

    drive = GoogleDrive(gauth)

    new_file = drive.CreateFile()
    new_file.SetContentFile(path)
    new_file.Upload()
