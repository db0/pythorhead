## python examples/ban_user.py db0

import argparse
import json
import os
from datetime import datetime, timedelta
from pythorhead import Lemmy

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("username", action="store")
arg_parser.add_argument(
    "-d",
    "--lemmy_domain",
    action="store",
    required=False,
    type=str,
    help="the domain in which to look for this user",
)
arg_parser.add_argument(
    "-u",
    "--lemmy_username",
    action="store",
    required=False,
    type=str,
    help="Which user to authenticate as",
)
arg_parser.add_argument(
    "-p",
    "--lemmy_password",
    action="store",
    required=False,
    type=str,
    help="Which password to authenticate with",
)
arg_parser.add_argument(
    "--reason",
    action="store",
    default=None,
    required=False,
    type=str,
    help="Optional reason to use for ban",
)
arg_parser.add_argument(
    "--days",
    action="store",
    default=None,
    required=False,
    type=int,
    help="Amount of days to ban for",
)
args = arg_parser.parse_args()


lemmy_domain = args.lemmy_domain
if not lemmy_domain:
    lemmy_domain = os.getenv("LEMMY_DOMAIN", "lemmy.dbzer0.com")
if not lemmy_domain:
    raise Exception("You need to provide a lemmy domain via env var or arg")

lemmy_username = args.lemmy_username
if not lemmy_username:
    lemmy_username = os.getenv("LEMMY_USERNAME")

lemmy_password = args.lemmy_password
if not lemmy_password:
    lemmy_password = os.getenv("LEMMY_PASSWORD")

lemmy = Lemmy(f"https://{lemmy_domain}", raise_exceptions=True, request_timeout=2)
if lemmy_username and lemmy_password:
    login = lemmy.log_in(lemmy_username, lemmy_password)
user = lemmy.user.get(username=args.username)
if not user:
    print("no matching username found")
    import sys
    sys.exit(1)
expires = None
if args.days:
    expires = datetime.utcnow() + timedelta(days=args.days)
ban = lemmy.user.ban(
    person_id = user["person_view"]["person"]["id"],
    reason = args.reason,
    expires = expires,
    remove_data = False,
)
if ban is not None:
    print(json.dumps(f"Banned: {ban['banned']}", indent=4))
