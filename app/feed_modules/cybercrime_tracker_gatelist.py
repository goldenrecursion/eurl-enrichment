from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'cybercrime-tracker gate'
        self.type = 'blacklisted'
        self.feed_output_type = 'custom'
        self.feed_url = 'https://cybercrime-tracker.net/ccamgate.php'

    def _parse_output_custom(self) -> bool:
        response = self._make_web_request()
        
        for line in response.text.split('\n'):
            try:
                formatted_line = line.split('|')[0].strip()
            except IndexError:
                print(f"[!] Unable to parse '{self.name}'. Value: {line}")
                return False
            else:
                self._queue(formatted_line)
        
        return True
        
