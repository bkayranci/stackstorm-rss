import feedparser
from st2common.runners.base_action import Action


class RssGetFeedAction(Action):
    def run(self, feed_url):
        feeds = feedparser.parse(feed_url)
        return dict(feeds)