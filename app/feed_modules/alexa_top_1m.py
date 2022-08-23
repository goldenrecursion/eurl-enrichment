from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.csv_headers = False
        self.csv_parsed_field_offset = 1
        self.name = 'alexa top 1 million'
        self.type = 'whitelisted'
        self.feed_output_type = 'csv'
        self.feed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
        self.unzip = True        
        self.run_cycle = 0


