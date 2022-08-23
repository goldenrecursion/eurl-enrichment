from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'mirai security'
        self.type = 'blacklisted'
        self.feed_output_type = 'list'
        self.feed_url = 'https://mirai.security.gives/data/ip_list.txt'

