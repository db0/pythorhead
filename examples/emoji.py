
## python examples/emoji.py db0

import os
import argparse
import json
from pythorhead import Lemmy


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('username', action="store")
arg_parser.add_argument('-d', '--lemmy_domain', action='store', required=False, type=str, help="the domain in which to look for this user")
arg_parser.add_argument('-u', '--lemmy_username', action='store', required=False, type=str, help="Which user to authenticate as")
arg_parser.add_argument('-p', '--lemmy_password', action='store', required=False, type=str, help="Which password to authenticate with")
args = arg_parser.parse_args()



lemmy_domain = args.lemmy_domain
if not lemmy_domain:
    lemmy_domain = os.getenv('LEMMY_DOMAIN', "lemmy.dbzer0.com")
if not lemmy_domain:
    raise Exception("You need to provide a lemmy domain via env var or arg")

lemmy_username = args.lemmy_username
if not lemmy_username:
    lemmy_username = os.getenv("LEMMY_USERNAME")

lemmy_password = args.lemmy_password
if not lemmy_password:
    lemmy_password = os.getenv("LEMMY_PASSWORD")

lemmy = Lemmy(f"https://{lemmy_domain}", raise_exceptions=True)
if lemmy_username and lemmy_password:
    login = lemmy.log_in(lemmy_username, lemmy_password)
emoji = lemmy.emoji.get()
if emoji:
    print(json.dumps(emoji, indent=4))
else:
    print("Retrieval of emoji information failed")