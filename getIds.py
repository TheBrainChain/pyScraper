<<<<<<< HEAD

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import argparse
flags = argparse.ArgumentParser()
flags.add_argument("a")
test = flags.parse_args()

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
    spreadsheetCreds = Storage(os.path.join(os.path.join(home_dir, '.credentials'),
                                       'client_secret.json')).get()

    credentials = Storage(os.path.join(os.path.join(home_dir, '.credentials'),
                                    'drive-python-quickstart.json')).get()

    http = spreadsheetCreds.authorize(httplib2.Http())
    SpreadsheetService = discovery.build('sheets', 'v4', http=http,discoveryServiceUrl=('https://sheets.googleapis.com/$discovery/rest?'
                                              'version=v4'))

    http = credentials.authorize(httplib2.Http())
    DriveService = discovery.build('drive', 'v3', http=http)

    DriveResults = DriveService.files().list(q="name = '" + test.a + "_RunLog'", pageSize=50, fields="nextPageToken, files(id, name)").execute()


    items = DriveResults.get('files', [])
    if not items:
        print('No files found.')
    else:
        for item in items:
#            print("Item:")
            print("Name: " + item['name'])
    #        print("ID: " + item['id'])
    spreadsheetId = [item['id']]
    subsheet = ['Summary','Pre-MBSR EEG', 'Pre-BMSR BCI', 'BCI 1','BCI 2','BCI 3','BCI 4','BCI 5','BCI 6','Post-BCI EEG']

    for sheets in range(3,8):
        dataFilename.extend([subsheet[sheets]+'!C9',subsheet[sheets]+'!C12',subsheet[sheets]+'!C15',subsheet[sheets]+'!C19',subsheet[sheets]+'!C22',subsheet[sheets]+'!C25'])  #For BCI 1 label
        hitRange.append(subsheet[sheets]+'!F9:F27')
        invalidRange.append(subsheet[sheets]+'!G9:G27')

    tasks = ["LR1","UD1","2D1","LR2","UD2","2D2"]
    endOfLine = "S001.applog"

    filename = SpreadsheetService.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId[0], ranges=dataFilename).execute()
    filenameParams = filename.get('valueRanges')
    for vals in range(0,30):
        fileNameValues.extend(filenameParams[vals].get('values'))
    subjectInits = fileNameValues[0][0][0:2]
    if fileNameValues[0][0][2] != "_":
        subjectInits = fileNameValues[0][0][0:3]

    for i in range(0,5):
        if fileNameValues[0][0][2] != "_":
            dateOfExp.append(fileNameValues[i*6][0][8:17])
        else:
            dateOfExp.append(fileNameValues[i*6][0][7:16])

    #Read data from applog
        for taskNumber in range(0,6):
            fileToRead = "Z:/EEGDATA/MBSR_BCI_incomplete/Cohort 7/"+subjectInits+"/"+subjectInits+"_"+tasks[taskNumber]+"_"+dateOfExp[i]+endOfLine[1:4]+"/"+subjectInits+"_"+tasks[taskNumber]+"_"+dateOfExp[i]+endOfLine   #modify directory based on what computer this is on
            with open(fileToRead,'r') as f:
                for line in f:
                    for word in line.split():
                        if word == "finished:":
                            for x in range(1,4):
                                if line.split()[1] == '{}'.format(x):
                                    hits.append(line.split()[5])
                                    invalid.append(line.split()[7])
            f.close()

    #Read data from EEG Data (Matlab stuff)
    time = "Z:/EEGDATA/MBSR_BCI_incomplete/Cohort 7/"+subjectInits+"/"+subjectInits+"/"+subjectInits+"_"+dateOfExp[i]+"_time_textoutput.txt"
    with open(time,'r') as f:
        for line in f:
            for word in line.split():
                if word == "Avg":
                    for x in range(1,4):
                        if line.split()[1] == '{}'.format(x):
                            timeOutput.append(line.split()[3])
                print(word)
    f.close()
    print(timeOutput)




    #Get values to write to spreadsheet
    for i in range(0,72):
        hitValues.append([hits[i]])
        invalidValues.append([invalid[i]])
    hitValues.insert(9,[])
    hitValues.insert(28,[])
    hitValues.insert(47,[])
    hitValues.insert(66,[])
    invalidValues.insert(9,[])
    invalidValues.insert(28,[])
    invalidValues.insert(47,[])
    invalidValues.insert(66,[])

    data = [
    	{'range': hitRange[0],'values': hitValues[0:19]},
    	{'range': invalidRange[0],'values': invalidValues[0:19]},
    	{'range': hitRange[1],'values': hitValues[19:38]},
        {'range': invalidRange[1],'values': invalidValues[19:38]},
    	{'range': hitRange[2],'values': hitValues[38:57]},
        {'range': invalidRange[2],'values': invalidValues[38:57]},
        {'range': hitRange[3],'values': hitValues[57:76]},
        {'range': invalidRange[3],'values': invalidValues[57:76]}
                ]
    body = 	{
    	    'valueInputOption': "USER_ENTERED",
    	    'data': data
    	}

    #Write data to spreadsheet
#    SheetResults = SpreadsheetService.spreadsheets().values().batchUpdate(
#	        spreadsheetId=spreadsheetId[0], body=body).execute()

if __name__ == '__main__':
    if test.a == "SX_RunLog":
        print("Nailed it")
    main()
=======

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import argparse
flags = argparse.ArgumentParser()
test = flags.parse_args()

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES2 = 'https://www.googleapis.com/auth/drive.metadata.readonly'
SCOPES1 = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

hits = []
invalid = []
fileNameValues = []
filenameParams = {}
dataFilename = []
hitRange = []
hitValues=[]
invalidRange = []
invalidValues = []
dateOfExp = []
def get_credentials(select):

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)

    if select ==1:

        credential_path = os.path.join(credential_dir,
                                   'client_secret.json')

        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES1)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store, flags)
            print('Storing credentials to ' + credential_path)
        return credentials

    if select == 2:
        credential_path = os.path.join(credential_dir,
                                    'drive-python-quickstart.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES2)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

def main():
    spreadsheetCreds = get_credentials(1)
    credentials = get_credentials(2)

    http = spreadsheetCreds.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    SpreadsheetService = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    http = credentials.authorize(httplib2.Http())
    DriveService = discovery.build('drive', 'v3', http=http)


    DriveResults = DriveService.files().list(q="name = 'SX_RunLog'", pageSize=50, fields="nextPageToken, files(id, name)").execute()
    items = DriveResults.get('files', [])
    if not items:
        print('No files found.')
    else:
        for item in items:
            print("Item:")
            print("Name: " + item['name'])
            print("ID: " + item['id'])
    spreadsheetId = [item['id']]
    subsheet = ['Summary','Pre-MBSR EEG', 'Pre-BMSR BCI', 'BCI 1','BCI 2','BCI 3','BCI 4','BCI 5','BCI 6','Post-BCI EEG']

    for sheets in range(3,8):
        dataFilename.extend([subsheet[sheets]+'!C9',subsheet[sheets]+'!C12',subsheet[sheets]+'!C15',subsheet[sheets]+'!C19',subsheet[sheets]+'!C22',subsheet[sheets]+'!C25'])  #For BCI 1 label
        hitRange.append(subsheet[sheets]+'!F9:F27')
        invalidRange.append(subsheet[sheets]+'!G9:G27')

    tasks = ["LR1","UD1","2D1","LR2","UD2","2D2"]
    endOfLine = "S001.applog"

    filename = SpreadsheetService.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId[0], ranges=dataFilename).execute()
    filenameParams = filename.get('valueRanges')
    for vals in range(0,30):
        fileNameValues.extend(filenameParams[vals].get('values'))


    subjectInits = fileNameValues[0][0][0:4]
    if subjectInits[2] == "_":
        subjectInits = fileNameValues[0][0][0:3]

    for i in range(0,5):
        if subjectInits[2] == "_":
            dateOfExp.append(fileNameValues[i*6][0][7:16])
        else:
            dateOfExp.append(fileNameValues[i*6][0][6:15])

    #Read data from applog
        for taskNumber in range(0,6):
            fileToRead = "C:/Users/BME_HeLab/Documents/GitHub/Scraper/datafiles"+"/"+subjectInits+tasks[taskNumber]+"_"+dateOfExp[i]+endOfLine[1:4]+"/"+subjectInits+tasks[taskNumber]+"_"+dateOfExp[i]+endOfLine   #modify directory based on what computer this is on
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
    for i in range(0,72):
        hitValues.append([hits[i]])
        invalidValues.append([invalid[i]])
    hitValues.insert(9,[])
    hitValues.insert(28,[])
    hitValues.insert(47,[])
    hitValues.insert(66,[])
    invalidValues.insert(9,[])
    invalidValues.insert(28,[])
    invalidValues.insert(47,[])
    invalidValues.insert(66,[])
    print(hitValues)

    data = [
    	{'range': hitRange[0],'values': hitValues[0:19]},
    	{'range': invalidRange[0],'values': invalidValues[0:19]},
    	{'range': hitRange[1],'values': hitValues[19:38]},
        {'range': invalidRange[1],'values': invalidValues[19:38]},
    	{'range': hitRange[2],'values': hitValues[38:57]},
        {'range': invalidRange[2],'values': invalidValues[38:57]},
        {'range': hitRange[3],'values': hitValues[57:76]},
        {'range': invalidRange[3],'values': invalidValues[57:76]}
                ]

    body = 	{
    	    'valueInputOption': "USER_ENTERED",
    	    'data': data
    	}

    #Write data to spreadsheet
    SheetResults = SpreadsheetService.spreadsheets().values().batchUpdate(
	        spreadsheetId=spreadsheetId[0], body=body).execute()

if __name__ == '__main__':
    main()
>>>>>>> origin/master
