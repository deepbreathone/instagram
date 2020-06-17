import json
import random
from instapy import InstaPy
from instapy import smart_run

with open("credentials.json", "r") as f:
    credentials = json.loads(f.read())

insta_username = credentials["username"]
insta_password = credentials["password"]

comments = [
    "Awesome work @{}",
    "Getting inspired by you @{}",
    "Looks great",
    "Love it!",
    "Nice work",
    "Super cool  @{}",
    "Loving it!",
    "Wonderful",
    "Amazing",
    ":heart_eyes:",
    "This is awesome!! :heart_eyes:",
    ":smiley:",
    "Great work :smiley:",
    ":thumbsup:",
    "Looks awesome @{}",
    "Really Cool",
]

hashtags = [
    "#acrylicpainting",
    "#acrylic",
    "#acrylicart",
    "#art",
    "#arts",
    "#arte",
    "#artoftheday",
    "#artistic",
    "#artsy",
    "#artistsoninstagram",
    "#artoninsta",
    "#instaart",
    "#myart",
    "#artwork",
    "#artist",
    "#abstractart",
    "#color",
    "#colour",
    "#colorful",
    "#paintings",
    "#painting",
]

session = InstaPy(
    username=insta_username,
    password=insta_password,
    headless_browser=False,
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
        peak_likes_daily=238,
        peak_comments_hourly=21,
        peak_comments_daily=182,
        peak_follows_hourly=48,
        peak_follows_daily=253,
        peak_unfollows_hourly=35,
        peak_unfollows_daily=253,
        peak_server_calls_hourly=3000,
        peak_server_calls_daily=4700,
    )

    session.set_relationship_bounds(
        enabled=True,
        potency_ratio=None,
        # potency_ratio=-1.5,
        delimit_by_numbers=True,
        max_followers=10000,
        max_following=None,
        min_followers=25,
        min_following=25,
    )

    session.set_skip_users(
        skip_private=True, skip_no_profile_pic=True, skip_business=True,
    )
    # general settings
    random.shuffle(hashtags)
    my_hashtags = hashtags[:10]
    session.set_simulation(enabled=True)
    session.set_do_like(enabled=True, percentage=69)
    # session.set_delimit_liking(enabled=True, max_likes=1005, min_likes=20)
    session.set_comments(comments, media="Photo")
    session.set_do_comment(enabled=True, percentage=17)

    session.set_do_follow(enabled=True, percentage=34, times=1)
    session.set_user_interact(amount=3, randomize=True, percentage=27, media="Photo")

    # activity
    session.like_by_tags(my_hashtags, amount=7, interact=True, randomize=True)

    """ First follow user followers leaves comments on these user's posts...
    """
    session.follow_user_followers(
        ["jeanniedouglasart", "betty.krause.art", "claire_desjardins_art"],
        amount=random.randint(75, 100),
        randomize=True,
        interact=True,
        sleep_delay=600,
    )

    """ Second follow user follows doesn't comment on users' posts...
    """
    session.follow_user_followers(
        ["andreasoosart", "amystoneart"],
        amount=random.randint(75, 100),
        randomize=False,
        interact=False,
        sleep_delay=600,
    )

    session.unfollow_users(
        amount=random.randint(75, 100),
        instapy_followed_enabled=True,
        instapy_followed_param="nonfollowers",
        style="FIFO",
        unfollow_after=12 * 60 * 60,
        sleep_delay=501,
    )
    session.unfollow_users(
        amount=random.randint(75, 125),
        instapy_followed_enabled=True,
        instapy_followed_param="ALL",
        style="FIFO",
        unfollow_after=24 * 60 * 60,
        sleep_delay=501,
    )
