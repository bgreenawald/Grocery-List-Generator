#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Runner program. """

import json

from get_items import get_items
from write_items import write_items


def lambda_handler(event, context):
    """
    Runner function.

    Returns:
        (dict): Message about the function execution.

    """
    # Try to read in the items
    success, msg, items = get_items()
    if not success:
        return {
            'statusCode': 200,
            'body': json.dumps(msg)
        }

    # Pass the items along to the write function
    _, msg = write_items(items)

    return {
        'statusCode': 200,
        'body': json.dumps(msg)
    }
