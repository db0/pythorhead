
## python examples/user.py db0

import os
import argparse
import json
from pythorhead import Lemmy

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-d', '--lemmy_domain', action='store', required=False, type=str, help="the domain in which to look for this user")
arg_parser.add_argument('-c', '--lemmy_community', action='store', required=False, type=str, help="the community which to discover")
args = arg_parser.parse_args()

lemmy_domain = args.lemmy_domain
if not lemmy_domain:
    lemmy_domain = os.getenv('LEMMY_DOMAIN', "lemmy.dbzer0.com")
if not lemmy_domain:
    raise Exception("You need to provide a lemmy domain via env var or arg")
lemmy_community = args.lemmy_community
if not lemmy_community:
    lemmy_community = os.getenv('LEMMY_COMMUNITY', "div0@lemmy.dbzer0.com")

lemmy = Lemmy(f"https://{lemmy_domain}")
community_id = lemmy.discover_community(lemmy_community)
if community_id:
    print(f"Community '{lemmy_community} has id {community_id}")
else:
    print(f"Community '{lemmy_community} could not be found")
