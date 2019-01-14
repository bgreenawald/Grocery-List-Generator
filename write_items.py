#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

import gkeepapi

import creds


def write_items(items):
    """
    Write the needed items to keep.

    Args:
        items (list): List of items from the Google sheet.
    Returns:
        (bool): Success of the program
        (str): Status of the program execution
    """
    # Connect to the keep API
    keep = gkeepapi.Keep()
    success = keep.login(creds.KEEP_USERNAME, creds.KEEP_PASSWORD)

    if not success:
        message = "Connection failed, exiting program."
        return False, message

    # Get all the notes
    notes = keep.all()

    # Local function to ensure title matches and note is not trashed
    def validate_note(note):
        # Remove alpha numeric
        pattern = re.compile('[^a-zA-Z]+')
        return not note.trashed and \
            pattern.sub('', note.title).lower() == "grocerylist"

    # Get the grocery note
    grocery_note = [note for note in notes if validate_note(note)]

    # Validate the output
    if not grocery_note:
        # If there is no note with name 'Grocery List', create it
        grocery_note = keep.createList('Grocery List')
    elif len(grocery_note) > 1:
        error = "More than one note has the name 'grocery list' (spacing" + \
                "and capitalization do not matter. Please make sure only" + \
                "one such note exists."
        return False, error
    else:
        # Otherwise, there should only be one note in the list, extract it.
        grocery_note = grocery_note[0]

    # Get the list of items in the grocery note
    items_in_list = set([x.text for x in grocery_note.items])

    # Make sure we are not adding duplicat elements.
    items = set(items)
    items = items.difference(items_in_list)

    # Sort based on the name of the item
    items = list(items)
    items.sort()

    # Add each item
    for item in items:
        grocery_note.add(item, False)

    # Sync with keep
    keep.sync()

    return True, "Program execution succesful."


if __name__ == "__main__":
    write_items(['2', '5'])
