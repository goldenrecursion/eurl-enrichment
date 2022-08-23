from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'cybercure'
        self.type = 'blacklisted'
        self.feed_output_type = 'json'
        self.json_keys = [ 'data', 'ip' ]
        self.feed_url = 'https://api.cybercure.ai/feed/get_ips'       
        self.run_cycle = 3600

