import json
import time
import gspread
import os
import argparse

from oauth2client import client
from oauth2client import tools
from oauth2client.service_account import ServiceAccountCredentials

from flask import Flask,render_template, url_for, request, redirect, make_response

from twilio.rest  import Client
from twilio.twiml.messaging_response import MessagingResponse


def configuration(config_file='client_secret.json'):
    config = json.load(open(config_file))
    config['config_file'] = config_file

    for key, value in config:
        if os.environ[value.upper()]:
            config[key] = value.lower()

    return config


def get_credentials(config):
    """Gets valid google user credentials.

    Returns:
        Credentials, the obtained credential.
    """
    gspread.authorize(credentials)

    # use creds to create a client to interact with the Google Drive API

    creds = ServiceAccountCredentials.from_json_keyfile_name(
                config['credential_files'], config['scope'])

    return creds


def get_workbook(config):
    creds = get_credentials(config)
    client = gspread.authorize(creds)
    wks = client.open(config['workbook'])
    wk = wks.get_worksheet(0)
    return wk


def get_twilio(config):
    client = Client(config['account_sid'], config['auth_token'])
    return client


def error_msgs(resp):
    resp = MessagingResponse()
    resp.message("Votre reponse n'a pas comprise par notre robot")


def receive_msgs(request, workbook):
    from_number = request.values.get('From', None)
    from_body = request.values.get('Body', None)
    clean_number = from_number.strip("+")


    guest_confirmation_cell = workbook.find(str(clean_number).strip())
    guest_row = guest_confirmation_cell.row

    try:
        Nguests = int(from_body)
    except ValueError:
        resp = error_msgs()
    finally:
        resp = MessagingResponse()

        if Nguests == 0:
            workbook.update_acell("F" + str(guest_row), 'NON')
            resp.message("Navré de l'entendre ! A bientot !")

        else:
            workbook.update_acell("F" + str(guest_row), 'OUI')
            workbook.update_acell("D" + str(guest_row), Nguests)
            resp.message(u"\u2665" + " Merci d'avoir confirmé !" + u"\u2665")


    # elif "numbers" in from_body.lower(): #return statistics (total guests, food choices list)
    #     resp.message("R.S.V.P update:\n\nTotal Accepted: " + guest_confirmed +
    #      "\n\nTotal declined: " + guest_unconfirmed + "\n\nTotal no response: " +
    #     guest_no_response + "\n\nTotal acceptance rate: " + guest_acceptance)

    return str(resp)
