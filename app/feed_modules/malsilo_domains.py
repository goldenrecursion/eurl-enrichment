from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'malsio'
        self.type = 'blacklisted'
        self.feed_output_type = 'custom'
        self.feed_url = 'https://malsilo.gitlab.io/feeds/dumps/domain_list.txt'

    def _parse_output_custom(self) -> bool:
        # Have to build a custom parser because the data does not come in 
        # a csv standard and there is more than just the url on the line.
        # TODO: add a flag that automatically regex's every line parsed
        # and make it optional. self.row_regex = '$.*?,.*?,(.*?),'
        response = self._make_web_request()
        
        for line in response.text.split('\n'):
            if line.startswith('#') or line.strip() == '':
                continue 

            try:
                formatted_line = line.split(',')[2].strip()
            except IndexError:
                print(f"[!] Unable to parse '{self.name}'. Value: {line}")
                return False
            else:
                self._queue(formatted_line)
        
        return True

