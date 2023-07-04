## python examples/pic.py NicKoehler
## Post images with title and optional body using the command line

import argparse
import os

from pythorhead import Lemmy

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "community",
    action="store",
    help="the community name to post to",
)
arg_parser.add_argument(
    "title",
    action="store",
    help="the title of the post",
)
arg_parser.add_argument(
    "image",
    action="store",
    help="the image to upload",
)
arg_parser.add_argument(
    "-b",
    "--body",
    action="store",
    required=False,
    help="the body of the post",
)
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
args = arg_parser.parse_args()


lemmy_domain = args.lemmy_domain
if not lemmy_domain:
    lemmy_domain = os.getenv("LEMMY_DOMAIN", "lemmy.dbzer0.com")
if not lemmy_domain:
    raise Exception("You need to provide a lemmy domain via env var or arg")

lemmy_username = args.lemmy_username
if not lemmy_username:
    lemmy_username = os.getenv("LEMMY_USERNAME")
if not lemmy_username:
    raise Exception("You need to provide a lemmy username via env var or arg")

lemmy_password = args.lemmy_password
if not lemmy_password:
    lemmy_password = os.getenv("LEMMY_PASSWORD")
if not lemmy_password:
    raise Exception("You need to provide a lemmy password via env var or arg")

lemmy = Lemmy(f"https://{lemmy_domain}")
if not lemmy.log_in(lemmy_username, lemmy_password):
    print("Failed to log in")
    exit(1)

community_id = lemmy.discover_community(args.community)

if not community_id:
    print(f"Community {args.community} not found")
    exit(1)

try:
    image = lemmy.image.upload(args.image)
except IOError as e:
    print(e)
    exit(1)

if image is not None:
    post = lemmy.post(
        community_id,
        args.title,
        url=image[0]["image_url"],
        body=args.body,
    )
    if post:
        print(f"Successfully posted ({post['post_view']['post']['ap_id']})")
    else:
        print("Failed to post")
        exit(1)
else:
    print("Failed to upload image")
    exit(1)
