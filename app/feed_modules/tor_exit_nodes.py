from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'tor exit nodes'
        self.type = 'blacklisted'
        self.feed_output_type = 'list'
        self.feed_url = 'https://www.dan.me.uk/torlist/?exit'
        self.run_cycle = 3600 * 24 *7

