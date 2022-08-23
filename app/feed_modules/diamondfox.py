import re 

from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'diamond fox github'
        self.type = 'blacklisted'
        self.feed_output_type = 'custom'
        self.feed_url = 'https://raw.githubusercontent.com/pan-unit42/iocs/master/diamondfox/diamondfox_panels.txt'
    
    def _parse_output_custom(self) -> bool:
        # Having to build a custom parser. It does conform to csv standards but I 
        # also need to replace hxxp with http so that it passes future validation.
        # TODO: It would be great if there was a regex for a row. 
        # self.regex = 'hxxp|http'
        response = self._make_web_request()

        for line in response.text.split('\n'):
            try:
                formatted_line = line.split(',')[0].strip()
            except IndexError:
                print(f"[!] Unable to parse '{self.name}'. Value: {line}")
                return False
            else:
                formatted_line = re.sub('hxxp', 'http', formatted_line)
                self._queue(formatted_line)
        
        return True

