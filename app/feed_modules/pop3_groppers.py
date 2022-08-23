from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'pop3 groppers'
        self.type = 'blacklisted'
        self.feed_output_type = 'list'
        self.feed_url = 'https://home.nuug.no/~peter/pop3gropers.txt'

