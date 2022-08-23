from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'cybercrime tracker'
        self.type = 'blacklisted'
        self.feed_output_type = 'list'
        self.feed_url = 'https://cybercrime-tracker.net/all.php'

