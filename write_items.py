import sys

import gkeepapi

import get_items

def write_items():
    """
    Write the needed items to keep.

    """
    # Get the list of needed items.
    items = get_items.get_base_items() + \
                get_items.get_additional_items()

    # Sort based on the name of the item
    items.sort()

    # Connect to the keep API
    keep = gkeepapi.Keep()
    success = keep.login("bgreenawald@gmail.com", ***REMOVED***)

    if not success:
        print("Connection failed, exiting program.")
        sys.exit()

    # Get all the notes
    notes = keep.all()

    # Get the grocery note
    grocery_note = [note for note in notes if note.title == "Grocery List"][0]

    # Add each item
    for item in items:
        grocery_note.add(item, False)

    # Sync with keep
    keep.sync()

if __name__=="__main__":
    write_items()