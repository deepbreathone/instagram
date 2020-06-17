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
        ["andreasoosart", "amystoneart"],
        amount=100,
        randomize=False,
        interact=False,
        sleep_delay=601,
    )

    """ First step of Unfollow action - Unfollow not follower users...
    """
    session.unfollow_users(
        amount=100,
        instapy_followed_enabled=True,
        instapy_followed_param="nonfollowers",
        style="FIFO",
        unfollow_after=12 * 60 * 60,
        sleep_delay=601,
    )

    """ Second step of Massive Follow...
    """

    session.follow_user_followers(
        ["jeanniedouglasart", "betty.krause.art", "claire_desjardins_art"],
        amount=100,
        randomize=False,
        interact=False,
        sleep_delay=601,
    )

    """ Second step of Unfollow action - Unfollow not follower users...
    """
    session.unfollow_users(
        amount=100,
        instapy_followed_enabled=True,
        instapy_followed_param="nonfollowers",
        style="FIFO",
        unfollow_after=12 * 60 * 60,
        sleep_delay=601,
    )

    """ Clean all followed user - Unfollow all users followed by InstaPy...
    """
    session.unfollow_users(
        amount=200,
        instapy_followed_enabled=True,
        instapy_followed_param="ALL",
        style="FIFO",
        unfollow_after=24 * 60 * 60,
        sleep_delay=601,
    )
