from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'vxvault'
        self.type = 'blacklisted'
        self.feed_output_type = 'custom'
        self.feed_url = 'http://vxvault.net/URL_List.php'

    def _parse_output_custom(self) -> bool:
        response = self._make_web_request()
        
        for line in response.text:
            if line.startswith('http') or line.strip() == '':
                continue
            
            self._queue(line)
        
        return True
        
