import json

f = open('sample.json')

data = json.load(f)

# # json format
  # {
  #   "data": [
  #     {...}, ..., {...}
  #   ]
  # }


subreddits = ["coronavirus", "news", "politics", "ideological", "local", "science", "technology", "health", "business"]
urls = ["http://empirenews.net/", "http://firebrandleft.com/", "https://www.huzlers.com/", "http://thelastlineofdefense.org/", "http://linkbeef.com/", "http://politicops.com/", "http://newsmutiny.com/", "http://www.react365.com/", "http://www.rilenews.com/", "http://stuppid.com/", "http://www.thenewsnerd.com/", "http://worldnewsdailyreport.com/", "http://www.newshounds.us/", "http://www.infowars.com/", "http://www.naturalnews.com/", "http://prntly.com/", "https://www.redflagnews.com/", "http://www.activistpost.com/", "http://beforeitsnews.com/", "http://civictribune.com/", "http://dailybuzzlive.com/", "http://thedcgazette.com/", "http://www.disclose.tv/", "http://gummypost.com/", "https://libertywritersnews.com/", "http://en.mediamass.net/", "http://www.newsexaminer.com/", "https://newsbreakshere.com/", "http://the-daily.buzz/", "http://now8news.com/", "http://realnewsrightnow.com/", "http://worldtruth.tv/", "http://bigamericannews.com/", "http://christwire.org/", "http://www.clickhole.com/", "http://creambmp.com/", "http://www.dcclothesline.com/", "http://www.derfmagazine.com/", "http://duhprogressive.com/", "http://www.enduringvision.com/", "http://www.newsbiscuit.com/", "http://www.politicalears.com/", "http://www.private-eye.co.uk/", "http://witscience.org/", "http://theuspatriot.com/", "http://www.breitbart.com/", "http://usapoliticszone.com/", "http://times.com.mx/", "https://therealstrategy.com/", "https://nodisinfo.com/", "https://veteranstoday.com/", "https://www.rt.com/", "https://sputniknews.com/", "http://www.lifezette.com/",]

fdata = []
for i in data["data"]:
  # filter subreddits
  # TODO: filter urls
  if "subreddit" in i and i["subreddit"].lower() in subreddits: # and "url" in i and (regex domain of) i["url"] in urls
    print("subreddit: {}, url: {}".format(i["subreddit"], i["url"]))
    # TODO: get specific objects
    # author, created_utc, awarders, domain, full_link, gildings, id, is_crosspostable, is_original_content, is_reddit_media_domain, is_self, is_video, locked, num_comments, num_crossposts, over_18, permalink, pinned, removed_by_category, retrieved_on, score, selftext, stickied, subreddit, subreddit_id, subreddit_subscribers, subreddit_type, suggested_sort, thumbnail, title, total_awards_received, upvote_ratio, url, post_hint, preview, banned_by, edited, html_decode
    fdata.append(i)

# create new json file with filtered data
with open('filtered.json', 'w') as outfile:
  json.dump(fdata, outfile)
