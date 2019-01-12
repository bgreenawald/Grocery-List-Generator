import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)


def get_base_items():
    """
    Call Sheets API to get list of items we need for meal prep.

    Returns:
        (list): List of grocery items to add.
    """
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("Food Tracker").worksheet("Main")

    # Extract and print all of the values
    records = sheet.get_all_records()

    # Convert to pandas Dataframe
    df = pd.DataFrame(records)

    # Filter based on need
    df_need = df[df['Need?'] == 1]

    # Get a list of items we need
    need = list(df_need["Item"])

    return need


def get_additional_items():
    """
    Get the items from additional recipes.

    """
    sheet = client.open("Food Tracker").worksheet("Other")

    # Extract and print all of the values
    records = sheet.get_all_records()

    # Convert to pandas Dataframe
    df = pd.DataFrame(records)

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

    return ret


if __name__=="__main__":
    get_additional_items()