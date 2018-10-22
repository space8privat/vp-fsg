#!/usr/bin/env python3

"""
Pull the Vertretungsplan from the Web and compare it to
the last stored version.
"""

import os
import getpass
import hashlib
import datetime
import sys
import pathlib

import convert
import utils
import pull_plan
import vp_bot


user = getpass.getuser()

__version__ = '0.1'
__authors__ = ('Léon Becker <lb@space8.me>', 'Frank Becker <fb@alien8.de>')

def compare(latest_file=None):
    """ Creates a hash of the latest Vertretungsplan and a hash 
    of the newest Vertretungsplan (from the web)
    """

    # Pulls newest created file
    old_page = open(latest_file).read().encode("utf-8")

    # Pulls current page from the web and replaces '\r\n' with '\n'
    current_page = pull_plan.get_page()
    current_page = current_page.text.replace("\r\n", "\n").encode("utf-8")

    # Creates hash of current page and old page to compare if something changed
    old_hash = hashlib.sha256(old_page).hexdigest()
    new_hash = hashlib.sha256(current_page).hexdigest()
    print("Created hash: ", "\nold_hash= ", old_hash, "\nnew_hash= ", new_hash)

    # Checks if something changed between old_page and current_page
    if new_hash == old_hash:
        print("--> No new Vertretungsplan version found.")
        convert.main()
        return False
    else:
        print("--> New Vertretungsplan version found!")
        pull_plan.main()
        convert.main()
        vp_bot.main()
        return True


def check_requirements():
    creds_path = os.path.expanduser('~/.config/vertretungsplan/creds.ini')
    config_path = os.path.expanduser('~/.config/vertretungsplan/config.ini')
    telegram_path = os.path.expanduser('~/.config/vertretungsplan/telegram.ini')

    if not os.path.isfile(creds_path):
        sys.stderr.write("E: Could not find creds.ini in \'~/.config/vertretungsplan/creds.ini\'.\n")
        sys.exit(1)

    if not os.path.isfile(config_path):
        sys.stderr.write("E: Could not find config.ini in \'~/.config/vertretungsplan/config.ini\'.\n")
        sys.exit(1)
    if not os.path.isfile(config_path):
        sys.stderr.write("E: Could not find config.ini in \'~/.config/vertretungsplan/telegram.ini\'.\n")
        sys.exit(1)

    backup_path = utils.get_raw_html_file_path()
    pathlib.Path(os.path.dirname(backup_path)).mkdir(parents=True, exist_ok=True)

    cache_file_path = utils.get_cache_file_path()
    pathlib.Path(os.path.dirname(cache_file_path)).mkdir(parents=True, exist_ok=True)

def main():
    date = datetime.datetime.now()
    print("--- Session started: ", date, " ---") # example: --- Session started: 2018-10-21 11:00:01.875420  ---
    
    check_requirements()
    latest_file = utils.get_latest_file()
    compare(latest_file)

    date = datetime.datetime.now()
    print("--- Session ended: ", date, " ---\n") # example: --- Session ended: 2018-10-21 11:00:01.875420 ---


if __name__ == "__main__":
    main()