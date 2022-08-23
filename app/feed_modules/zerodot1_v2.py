from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'zerodot1 browser coinminers'
        self.type = 'blacklisted'
        self.feed_output_type = 'list'
        self.feed_url = 'https://gitlab.com/ZeroDot1/CoinBlockerLists/raw/master/list_browser.txt?inline=false'
        self.run_cycle = 3600 * 24 *7


