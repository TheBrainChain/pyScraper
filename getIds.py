from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import argparse
flags = argparse.ArgumentParser()
flags.add_argument("Subject")
flags.add_argument("Task")
flags.add_argument("ParamName")
Params = flags.parse_args()

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES2 = 'https://www.googleapis.com/auth/drive.metadata.readonly'
SCOPES1 = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

hits = []
invalid = []

timeOutput = []

fileNameValues = []
filenameParams = {}
dataFilename = []
hitRange = []
hitValues=[]
invalidRange = []
invalidValues = []
dateOfExp = []

def main():

    home_dir = os.path.expanduser('~')
    spreadsheetCreds = Storage(os.path.join(os.path.join(home_dir, '.credentials'), 'client_secret.json')).get()

    credentials = Storage(os.path.join(os.path.join(home_dir, '.credentials'), 'drive-python-quickstart.json')).get()

    http = spreadsheetCreds.authorize(httplib2.Http())
    SpreadsheetService = discovery.build('sheets', 'v4', http=http,discoveryServiceUrl=('https://sheets.googleapis.com/$discovery/rest?' 'version=v4'))

    http = credentials.authorize(httplib2.Http())
    DriveService = discovery.build('drive', 'v3', http=http)

    DriveResults = DriveService.files().list(q="name = '" + Params.Subject + "_RunLog'", pageSize=50, fields="nextPageToken, files(id, name)").execute()

    items = DriveResults.get('files', [])
    if not items:
        print('No files found.')
    else:
        for item in items:
            print("Name: " + item['name'])
    spreadsheetId = [item['id']]
    subsheet = ['Summary','Pre-MBSR EEG', 'Pre-BMSR BCI', 'BCI 1','BCI 2','BCI 3','BCI 4','BCI 5','BCI 6','BCI 7','BCI 8','BCI 9','BCI 10','Post-BCI EEG']

    for sheets in range(3,13):
        dataFilename.extend([subsheet[sheets]+'!C9',subsheet[sheets]+'!C12',subsheet[sheets]+'!C15',subsheet[sheets]+'!C19',subsheet[sheets]+'!C22',subsheet[sheets]+'!C25'])  #For BCI 1 label
        hitRange.append(subsheet[sheets]+'!F9:F27')
        invalidRange.append(subsheet[sheets]+'!G9:G27')

    tasks = ["LR1","UD1","2D1","LR2","UD2","2D2"]
    endOfLine = "S001.applog"

    filename = SpreadsheetService.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId[0], ranges=dataFilename).execute()
    filenameParams = filename.get('valueRanges')
    for vals in range(0,60):
        fileNameValues.extend(filenameParams[vals].get('values'))
    subjectInits = fileNameValues[0][0][0:2]
    if fileNameValues[0][0][2] != "_":
        subjectInits = fileNameValues[0][0][0:3]

    print(fileNameValues[0][0])

    for i in range(0,10):
        if fileNameValues[0][0][2] != "_":
            dateOfExp.append(fileNameValues[i*6][0][8:17])
        else:
            dateOfExp.append(fileNameValues[i*6][0][7:16])
    #Read data from applog
        for taskNumber in range(0,6):
            fileToRead = "Z:/EEGDATA/MBSR_BCI_incomplete/"+subjectInits+"/"+subjectInits+"_"+tasks[taskNumber]+"_"+dateOfExp[i]+endOfLine[1:4]+"/"+subjectInits+"_"+tasks[taskNumber]+"_"+dateOfExp[i]+endOfLine   #modify directory based on what computer this is on
            with open(fileToRead,'r') as f:
                for line in f:
                    for word in line.split():
                        if word == "finished:":
                            for x in range(1,4):
                                if line.split()[1] == '{}'.format(x):
                                    hits.append(line.split()[5])
                                    invalid.append(line.split()[7])
            f.close()

    #Get values to write to spreadsheet
    for i in range(0,180):
        hitValues.append([hits[i]])
        invalidValues.append([invalid[i]])
    hitValues.insert(9,[])
    hitValues.insert(28,[])
    hitValues.insert(47,[])
    hitValues.insert(66,[])
    hitValues.insert(85,[])
    hitValues.insert(104,[])
    hitValues.insert(123,[])
    hitValues.insert(142,[])
    hitValues.insert(161,[])
    hitValues.insert(180,[])
    invalidValues.insert(9,[])
    invalidValues.insert(28,[])
    invalidValues.insert(47,[])
    invalidValues.insert(66,[])
    invalidValues.insert(85,[])
    invalidValues.insert(104,[])
    invalidValues.insert(123,[])
    invalidValues.insert(142,[])
    invalidValues.insert(161,[])
    invalidValues.insert(180,[])
    print(hitRange[0])
    if Params.ParamName == fileNameValues[0][0]:
        data = [
        {'range': 'BCI 1!F9:F11','values': hitValues[0:3]},
        {'range': 'BCI 1!G9:G11','values': invalidValues[0:3]}
        ]
    elif Params.ParamName == fileNameValues[1][0]:
        data = [
        {'range': 'BCI 1!F12:F14','values': hitValues[3:6]},
        {'range': 'BCI 1!G12:G14','values': invalidValues[3:6]}
        ]
    elif Params.ParamName == fileNameValues[2][0]:
        data = [
        {'range': 'BCI 1!F15:F17','values': hitValues[6:9]},
        {'range': 'BCI 1!G15:G17','values': invalidValues[6:9]}
        ]

    data1 = [
    	{'range': hitRange[0],'values': hitValues[0:19]},
    	{'range': invalidRange[0],'values': invalidValues[0:19]},
    	{'range': hitRange[1],'values': hitValues[19:38]},
        {'range': invalidRange[1],'values': invalidValues[19:38]},
    	{'range': hitRange[2],'values': hitValues[38:57]},
        {'range': invalidRange[2],'values': invalidValues[38:57]},
        {'range': hitRange[3],'values': hitValues[57:76]},
        {'range': invalidRange[3],'values': invalidValues[57:76]},
        {'range': hitRange[4],'values': hitValues[76:95]},
        {'range': invalidRange[4],'values': invalidValues[76:95]},
        {'range': hitRange[5],'values': hitValues[95:114]},
        {'range': invalidRange[5],'values': invalidValues[95:114]},
        {'range': hitRange[6],'values': hitValues[114:133]},
        {'range': invalidRange[6],'values': invalidValues[114:133]},
        {'range': hitRange[7],'values': hitValues[133:152]},
        {'range': invalidRange[7],'values': invalidValues[133:152]},
        {'range': hitRange[8],'values': hitValues[152:171]},
        {'range': invalidRange[8],'values': invalidValues[152:171]},
        {'range': hitRange[9],'values': hitValues[171:190]},
        {'range': invalidRange[9],'values': invalidValues[171:190]}]

    body = 	{
    	    'valueInputOption': "USER_ENTERED",
    	    'data': data
    	}

    #Write data to spreadsheet
    SheetResults = SpreadsheetService.spreadsheets().values().batchUpdate(
	        spreadsheetId=spreadsheetId[0], body=body).execute()

if __name__ == '__main__':
    main()
