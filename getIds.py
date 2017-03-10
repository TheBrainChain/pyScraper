
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



	# Pull spreadsheet data from Google Drive (incorporate parse args replace q="name = 'SX_RunLog'+ with just initials
    DriveResults = DriveService.files().list(q="name = 'SX_RunLog'", pageSize=50, fields="nextPageToken, files(id, name)").execute()
    items = DriveResults.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print("Item:")
            print("Name: " + item['name'])
            print("ID: " + item['id'])


	# Set up variables to be used to post to Google Sheets and scrape the applog
    spreadsheetId = [item['id']]
    subsheet = ['Summary','Pre-MBSR EEG', 'Pre-BMSR BCI', 'BCI 1','BCI 2','BCI 3','BCI 4','BCI 5','BCI 6','Post-BCI EEG']
    BCIsubSheet = [subsheet[2:8]]
#    for sheets in range(0,7):
        dataFilename.append([subsheet[sheets]+'!C9',subsheet[sheets]+'!C12',subsheet[sheets]+'!C15',subsheet[sheets]+'!C19',subsheet[sheets]+'!C22',subsheet[sheets]+'!C25'])  #For BCI 1 label
        hitRange = subsheet[sheets]+'!F9:F27'
        invalidRange = subsheet[sheets]+'!G9:G27'
        prmLoc = [subsheet[sheets]+'!D11',subsheet[sheets]+'D!14', subsheet[sheets]+'D!17',subsheet[sheets]+ 'D!21', subsheet[sheets]+'D!24', subsheet[sheets]+'D!27']
    
    tasks = ["LR1","UD1","2D1","LR2","UD2","2D2"]
    endOfLine = "S001.applog"


	#Pull data from Google Sheet
    filename = SpreadsheetService.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId[0], ranges=dataFilename).execute()
    filenameParams = filename.get('valueRanges')

    for vals in range(0,5):														#edit s oit can take ranges from all the sheets, not just 'BCI 1...
        fileNameValues.append(filenameParams[vals].get('values'))
    subjectInits = fileNameValues[1][0][0][0:4]
    dateOfExp = fileNameValues[1][0][0][7:16]
    if subjectInits[2] == "_":
        subjectInits = fileNameValues[1][0][0][0:3]
        dateOfExp = fileNameValues[1][0][0][6:15]

    #Read data from applog
    for taskNumber in range(0,6):
        fileToRead = "Z:\EEGDATA\Scraper\SX"+"/"+subjectInits+tasks[taskNumber]+dateOfExp+endOfLine[1:4]+"/"+subjectInits+tasks[taskNumber]+dateOfExp+endOfLine   #modify directory based on what computer 																																										this is on
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
    #for valzz in range(0,17):
        #hitValues.append(hits[valzz])
        #invalidValues.append(invalid[valzz])				Set up so that we skip one spot in between 8 and 9 (2D1 and LR2)


    hitValues = [[hits[0]],[hits[1]],[hits[2]],[hits[3]],[hits[4]],[hits[5]],[hits[6]],[hits[7]], [hits[8]],[],\
        [hits[9]],[hits[10]],[hits[11]],[hits[12]],[hits[13]],[hits[14]],[hits[15]],[hits[16]],[hits[17]]]
    invalidValues = [[invalid[0]],[invalid[1]],[invalid[2]],[invalid[3]],[invalid[4]],[invalid[5]],[invalid[6]],[invalid[7]],[invalid[8]],[],\
        [invalid[9]],[invalid[10]],[invalid[11]],[invalid[12]],[invalid[13]],[invalid[14]],[invalid[15]],[invalid[16]],[invalid[17]]]

    data = [
    	{
    		'range': hitRange,
    		'values': hitValues
    	},
    	{
    	    'range': invalidRange,
    	    'values': invalidValues
    	}
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
