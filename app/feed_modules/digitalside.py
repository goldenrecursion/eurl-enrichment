from core import FeedBase 


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'digitalside'
        self.type = 'blacklisted'
        self.feed_output_type = 'misp'
        self.feed_url = 'https://osint.digitalside.it/Threat-Intel/digitalside-misp-feed/'       
        self.run_cycle = 3600

