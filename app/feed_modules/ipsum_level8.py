from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'ipsum no false positives'
        self.type = 'blacklisted'
        self.feed_output_type = 'list'
        self.feed_url = 'https://raw.githubusercontent.com/stamparm/ipsum/master/levels/8.txt'
        self.run_cycle = 3600 * 24 *7

