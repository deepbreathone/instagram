import json
import random
from instapy import InstaPy
from instapy import smart_run

with open("credentials.json", "r") as f:
    credentials = json.loads(f.read())

insta_username = credentials["username"]
insta_password = credentials["password"]

comments = [
    ":heart_eyes:",
    ":smiley:",
    ":thumbsup:",
]

with open("hashtags.txt") as f:
    hashtags = [h.strip() for h in f.read().split(",")]

session = InstaPy(
    username=insta_username,
    password=insta_password,
    headless_browser=True,
    disable_image_load=True,
    multi_logs=True,
)

# while True:
with smart_run(session):
    session.set_quota_supervisor(
        enabled=True,
        sleep_after=["likes", "comments_d", "follows", "unfollows", "server_calls_h"],
        sleepyhead=True,
        stochastic_flow=True,
        notify_me=True,
        peak_likes_daily=111,
        peak_comments_hourly=3,
        peak_comments_daily=21,
        peak_follows_daily=222,
        peak_unfollows_hourly=35,
        peak_unfollows_daily=222,
        peak_server_calls_hourly=500,
        # peak_server_calls_daily=3000,
    )

    session.set_relationship_bounds(
        enabled=True,
        potency_ratio=None,
        # potency_ratio=-1.5,
        delimit_by_numbers=True,
        # max_followers=10000,
        # max_following=None,
        # min_followers=25,
        # min_following=25,
    )

    session.set_skip_users(
        skip_private=True, skip_no_profile_pic=True, skip_business=True,
    )
    # general settings
    random.shuffle(hashtags)
    my_hashtags = hashtags[:9]
    session.set_simulation(enabled=True)
    session.set_do_like(enabled=True, percentage=69)
    # session.set_delimit_liking(enabled=True, max_likes=1005, min_likes=20)
    session.set_comments(comments, media="Photo")
    session.set_do_comment(enabled=True, percentage=17)

    session.set_do_follow(enabled=True, percentage=34, times=1)
    session.set_user_interact(amount=3, randomize=True, percentage=27, media="Photo")
    session.set_delimit_commenting(enabled=True, max_comments=10000, min_comments=0)

    # activity
    session.like_by_tags(my_hashtags, amount=7, interact=True, randomize=True)
    session.follow_user_followers(
        ["wordsfrom.soul_", "wordselite0", " h.e.l.e.n.m.a.r.i.e"],
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
        ["penning.poetry", "thequotesoriginals", "poetsandpoemz"],
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
