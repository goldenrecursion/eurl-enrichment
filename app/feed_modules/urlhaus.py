from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'urlhaus'
        self.type = 'blacklisted'
        self.feed_output_type = 'custom'
        self.feed_url = 'https://urlhaus.abuse.ch/downloads/csv/'
        self.unzip = True
        self.csv_headers = False
        self.csv_parsed_field_offset = 2

    def _parse_output_custom(self) -> bool:
        # Having to build a custom parser because this list comes over as a zip
        # After unzipping, we have to parse the csv data inside but the problem
        # is that the file does not conform to csv standards. The first 7 lines
        # are comments which break all csv parsers. 
        # TODO: Add logic in the core to be able to starting reading any datasource
        # at a predetermined line number. Maybe add a flag self.file_entry_point = 7
        stored_zip_location = self._download_file()
        for extracted_file in self._extract_zip(stored_zip_location):
            with open(extracted_file, 'r') as f:
                csv_data = ''.join([line for line in f.readlines()[8:]])
                return self._parse_output_csv(csv_data)

