from __future__ import print_function
import httplib2
import os

import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secretSheets.json'
APPLICATION_NAME = 'PY'
KEY ='AIzaSyAG46d7Drgmz88Ek7DU8cWsgnwZvRxPWAk'
hits = []
invalid = []
fileNameValues = []
filenameParams = {}

def logScraper(a):
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'client_secret.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store,)
        print('Storing credentials to ' + credential_path)

    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    
    spreadsheetId = [a]									#Input all the Ids in the folder, and sift through until you find....initials?
    dataFilename = ['BCI 1!C9','BCI 1!C12','BCI 1!C15','BCI 1!C19','BCI 1!C22','BCI 1!C25']
    hitRange = 'BCI 1!F9:F27'
    invalidRange = 'BCI 1!G9:G27'
    tasks = ["LR1","UD1","2D1","LR2","UD2","2D2"]
    endOfLine = "S001.applog"



    #Read data from spreadsheet
    filename = service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheetId[0], ranges=dataFilename).execute()
    filenameParams = filename.get('valueRanges')
    for vals in range(0,5):
        fileNameValues.append(filenameParams[vals].get('values'))
    subjectInits = fileNameValues[1][0][0][0:4] 
    dateOfExp = fileNameValues[1][0][0][7:16]
    if subjectInits[2] == "_":
        subjectInits = fileNameValues[1][0][0][0:3]
        dateOfExp = fileNameValues[1][0][0][6:15]

    #Read data from applog
    for taskNumber in range(0,6):
        fileToRead = ".."+"/"+subjectInits+tasks[taskNumber]+dateOfExp+endOfLine[1:4]+"/"+subjectInits+tasks[taskNumber]+dateOfExp+endOfLine   #modify directory based on what computer this is on
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
    result = service.spreadsheets().values().batchUpdate(
	        spreadsheetId=spreadsheetId[0], body=body).execute()

if __name__ == '__main__':
    a = str(sys.argv[1])
    logScraper(a)



