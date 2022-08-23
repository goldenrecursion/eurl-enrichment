from core import FeedBase

class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'openphish'
        self.type = 'blacklisted'
        self.feed_output_type = 'list'
        self.feed_url = 'https://openphish.com/feed.txt'       
        self.run_cycle = 3600

