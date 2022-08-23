from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'ci-badguys'
        self.type = 'blacklisted'
        self.feed_output_type = 'list'
        self.feed_url = 'https://cinsscore.com/list/ci-badguys.txt'

