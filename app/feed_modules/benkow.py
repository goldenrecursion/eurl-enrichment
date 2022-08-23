from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.csv_delimiter = ';'
        self.csv_parsed_field_name = 'url'
        self.name = 'benkow'
        self.type = 'blacklisted'
        self.feed_output_type = 'csv'
        self.feed_url = 'https://benkow.cc/export.php'

