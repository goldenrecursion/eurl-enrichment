from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'malsio'
        self.type = 'blacklisted'
        self.feed_output_type = 'list'
        self.feed_url = 'https://malsilo.gitlab.io/feeds/dumps/url_list.txt'

