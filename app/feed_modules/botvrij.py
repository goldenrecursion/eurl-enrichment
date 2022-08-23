from core import FeedBase 


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'botvrij'
        self.type = 'blacklisted'
        self.feed_output_type = 'misp'
        self.feed_url = 'http://www.botvrij.eu/data/feed-osint/'       
        self.run_cycle = 3600

