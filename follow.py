import json
import random
from instapy import InstaPy
from instapy import smart_run

with open("credentials.json", "r") as f:
    credentials = json.loads(f.read())

insta_username = credentials["username"]
insta_password = credentials["password"]
session = InstaPy(
    username=insta_username, password=insta_password, headless_browser=True
)

# 7–13 follows per hour or 100–150 follows per day,
# 300–400 likes per day (of followed accounts),
# 2–5comments per hour
# or 20–30 comments per day,
# up to 10 DMs per hour under strict considerations
with smart_run(session):
    session.set_relationship_bounds(
        enabled=True,
        delimit_by_numbers=True,
        max_followers=4590,
        min_followers=45,
        min_following=77,
    )

    # activities
    session.follow_user_followers(
        ["wordsfrom.soul_", "wordselite0"],
        amount=111,
        randomize=False,
        interact=False,
        sleep_delay=601,
    )

    session.unfollow_users(
        amount=111,
        instapy_followed_enabled=True,
        instapy_followed_param="nonfollowers",
        style="FIFO",
        unfollow_after=12 * 60 * 60,
        sleep_delay=601,
    )
    
    session.follow_user_followers(
        ["penning.poetry", "thequotesoriginals"],
        amount=111,
        randomize=False,
        interact=False,
        sleep_delay=601,
    )

    session.unfollow_users(
        amount=111,
        instapy_followed_enabled=True,
        instapy_followed_param="nonfollowers",
        style="FIFO",
        unfollow_after=12 * 60 * 60,
        sleep_delay=601,
    )

    """ Clean all followed user - Unfollow all users followed by InstaPy...
    """
    session.unfollow_users(
        amount=222,
        instapy_followed_enabled=True,
        instapy_followed_param="ALL",
        style="FIFO",
        unfollow_after=24 * 60 * 60,
        sleep_delay=601,
    )
