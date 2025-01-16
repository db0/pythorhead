
## Get the latest post by user and list its likes. Required admin access
## python examples/post_likes.py db0

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

lemmy = Lemmy(f"https://{lemmy_domain}")
if lemmy_username and lemmy_password:
    login = lemmy.log_in(lemmy_username, lemmy_password)
user = lemmy.get_user(username=args.username, return_user_object = True)    
if user:
    uposts = user.get_latest_posts()
    if not len(uposts):
        print("User hasn't made any posts")
    votes = []
    scores = []
    more_votes = []
    page = 1 
    # TODO: Make this into a built-in method once a post is a class
    while len(more_votes) >= 50 or page == 1:
        more_votes = lemmy.post.list_votes(uposts[0]["post"]["id"], page=page).get("post_likes", [])
        page += 1
        votes += more_votes
        for v in more_votes:
            scores.append(v["score"])
    #print(json.dumps(votes, indent=4))
    print(scores)
    print(f"{len(votes)} Total votes counted")
else:
    print("no matching username found")
