
import os
import sys
import argparse
from pythorhead import Lemmy


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "version",
    action="store",
    help="The version being released",
)
args = arg_parser.parse_args()

bot_password = os.getenv("LEMMY_BOT_PASSWORD")
if not bot_password:
    print("Bot password not set")
    sys.exit(1)
lemmy = Lemmy("https://lemmy.dbzer0.com")
lemmy.log_in("div0", bot_password)
community_id = lemmy.discover_community("pythorhead")
lemmy.post.create(
    community_id, 
    f"New Pythörhead release {args.version}",
    url=f"https://github.com/db0/pythorhead/releases/tag/{args.version}",
)
