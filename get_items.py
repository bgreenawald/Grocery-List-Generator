#!/usr/bin/python
# -*- coding: utf-8 -*-"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


def get_items():
    """
    Wrapper function for the get items methods.

    Returns:
        (bool): Whether the execution of the program was successful.
        (string): Additional message on program execution.
        (list): List of items to add.

    """

    # Attemp to connect to sheets
    try:
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials\
            .from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)
    except:
        message = "Error in authorizing with Google Sheets"
        return False, message, []

    # Get the base items.
    base_success, base_message, base_items = get_base_items(client)

    # Get additional items
    add_success, add_message, add_items = get_additional_items(client)

    return base_success and add_success, \
        base_message + " " + add_message, \
        base_items + add_items


def get_base_items(client):
    """
    Call Sheets API to get list of items we need for meal prep.

    Args:
        client (gspread.client.Client): Gkeep API client.
    Returns:
        (list): List of grocery items to add.
    """
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    try:
        sheet = client.open("Food Tracker").worksheet("Main")
    except gspread.SpreadsheetNotFound:
        message = "Could not find the spreadsheet specified."
        return False, message, []
    except gspread.WorksheetNotFound:
        message = "Could not find the worksheet specified."
        return False, message, []

    # Extract and print all of the values
    records = sheet.get_all_records()

    # Convert to pandas Dataframe
    df = pd.DataFrame(records)

    # Filter based on need
    try:
        df_need = df[df['Need?'] == 1]

        # Get a list of items we need
        need = list(df_need["Item"])
    except KeyError:
        message = "Columns with names 'Need?' and 'Items' required."
        return False, message, []

    return True, "", need


def get_additional_items(client):
    """
    Get the items from additional recipes.

    Args:
        client (gspread.client.Client): Gkeep API client.
    """
    try:
        sheet = client.open("Food Tracker").worksheet("Other")
    except gspread.SpreadsheetNotFound:
        message = "Could not find the spreadsheet specified."
        return False, message, []
    except gspread.WorksheetNotFound:
        message = "Could not find the worksheet specified."
        return False, message, []

    # Extract and print all of the values
    records = sheet.get_all_records()

    # Convert to pandas Dataframe
    df = pd.DataFrame(records)

    try:
        # Filter based on need
        df_need = df[df['Need?'] == 1]

        # Get the list of all items with a unit
        ret = []

        # Iterate over all rows
        for _, row in df_need.iterrows():
            if row["Unit"]:
                s = "{item} ({quantity} {unit})".\
                            format(item=row["Item"], quantity=row["Total"],
                                   unit=row["Unit"])
            else:
                s = row["Item"]

            ret.append(s)
    except KeyError:
        message = "Column names 'Need?', 'Unit', 'Item', and 'Total' required."
        return False, message, []

    return True, '', ret


if __name__ == "__main__":
    print(get_items())
