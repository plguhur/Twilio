import json
import time
import gspread
from twilio.rest  import Client
import os
from utils import *

#Message your attendees from a spreadsheet
ACCOUNT_SID = os.environ['Twilio_account_per']
AUTH_TOKEN  = os.environ['Twilio_account_token_per']
WORKBOOK    = os.environ['Twilio_workbook']

json_key = json.load(open('client_secret.json'))#add file name for the json created for the spread sheet
scope = ['https://spreadsheets.google.com/feeds']

#credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
credentials = get_credentials(CLIENT_SECRET_FILE, SCOPES, APPLICATION_NAME)
gc = gspread.authorize(credentials)
wks = gc.open(WORKBOOK) #add your workbook name here
wks_attendees = wks.get_worksheet(0) #attendees worksheet

client = Client(ACCOUNT_SID, AUTH_TOKEN)


for num in range(2,60):  #to iterate between guests, amend this based on your total
    print("sleeping for 2 seconds")
    time.sleep(2) #adding a delay to avoid filtering

    guest_number = wks_attendees.acell('B' +str(num)).value
    guest_name = wks_attendees.acell('A'+str(num)).value
    accepted   = wks_attendees.acell('F'+str(num)).value

    if not  guest_number:
        print(guest_name + ' telephone number empty not messaging')
        wks_attendees.update_acell('E'+str(num), '0') #set number to 0

    elif len(accepted) == 0:
        print('Envoi d\'un message à ' + guest_name)
        client.messages.create(
            to="+" + guest_number,
            from_="33757915976",#+33757915976", #your twilio number here
            body=  u"\u2B50" + u"\u1F381" + u"\u2B50" + u"\u1F381" + u"\u2B50" + u"\u1F381" + u"\u2B50" + u"\u1F381" + "\n\n" + u"\u2709"
            +" Venez jouer les groupies et casser les fauteuils à l'occasion des 60 ans de Pascal Piroux ! "+  u"\u2709" +
            "\n\nLe samedi 1er septembre 2018 de *midi précise* à minuit.\n\n \
            Manoir Carrefour de l'Obélisque, 77174 Villeneuve le Comte. \n\n  \
            Attention, anniversaire surprise ! Rien ne doit s'ébruiter !\n\n  \
            Renseignements :  Valérie 06 77 64 83 30, Nathalie 06 23 15 13 74.\
            \n\nRépondre OUI si vous serez de la partie ou NON si malheureusement, vous ne pourrez vous joindre à nous.\n\n" u"\u2B50" + u"\u1F381" + u"\u2B50" + u"\u1F381" + u"\u2B50" + u"\u1F381" + u"\u2B50" + u"\u1F381",
        )
        wks_attendees.update_acell('E'+str(num), int(wks_attendees.acell('E' +str(num)).value) + 1) #increment the message count row
else:                  # else part of the loop
   print('finished')
