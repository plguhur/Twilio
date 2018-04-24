import json
import time
import gspread
from twilio.rest  import Client
import os
from utils import configuration, get_credentials, receive_msgs

#Message your attendees from a spreadsheet
config = configuration('client_secret.json')
workbook = get_workbook(config['gspread'])
twilio = get_twilio(config['twilio'])



for num in range(2, 100):

    guest_number = workbook.acell('E' +str(num)).value
    guest_name = workbook.acell('A'+str(num)).value
    status   = workbook.acell('F'+str(num)).value

    if not  guest_number:
        print(guest_name + ' telephone number empty not messaging')
        

    elif len(status) == 0:

    else:
        print('Sent a message to %s, %d'.format(guest_name, guest_number))
        twilio.messages.create(
            to="+" + guest_number,
            from_=config['twilio']['phone_number']
            body= "\u2B50\u1F381\u2B50\u1F381\u2B50\u1F381\u2B50\u1F381\n\n   \
            Venez jouer les groupies et casser les fauteuils à l'occasion des 60 ans de Pascal Piroux ! \u2709" +
            "\n\nLe samedi 1er septembre 2018 de *midi précise* à minuit.\n\n \
            Manoir Carrefour de l'Obélisque, 77174 Villeneuve le Comte. \n\n  \
            Attention, anniversaire surprise ! Rien ne doit s'ébruiter !\n\n  \
            Renseignements :  Valérie 06 77 64 83 30, Nathalie 06 23 15 13 74.\
            \n\nRépondre OUI si vous serez de la partie ou NON si malheureusement, vous ne pourrez vous joindre à nous.\n\n" u"\u2B50" + u"\u1F381" + u"\u2B50" + u"\u1F381" + u"\u2B50" + u"\u1F381" + u"\u2B50" + u"\u1F381",
        )
        workbook.update_acell('E'+str(num), int(workbook.acell('E' +str(num)).value) + 1) #increment the message count row

        print("sleeping for 2 seconds to avoid filtering")
        time.sleep(2)


print('Messages are sent.')
