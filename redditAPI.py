import praw as praw

reddit = praw.Reddit(client_id="RkREULvtiNB51w",
                     client_secret="sLhrKO4NU7GEexK9DPbOOgUumDIVyw",
                     password="yXm@~LK,v8",
                     user_agent="jkleinau",
                     username="clubmano")

print(reddit.user.me())
i = 1
for submission in reddit.subreddit("ProgrammerHumor").hot(limit=25):
    print(i + ". " + submission.name)
    i += 1