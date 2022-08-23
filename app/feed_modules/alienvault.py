from core import FeedBase


class Feed(FeedBase):

    def __init__(self) -> None:
        super().__init__()
        self.name = 'alienvault'
        self.type = 'blacklisted'
        self.feed_output_type = 'custom'
        self.feed_url = 'https://reputation.alienvault.com/reputation.generic'       
        self.run_cycle = 3600

    def _parse_output_custom(self) -> bool:
        # Having to build a custom parser because the data doesn't comform.
        # TODO: it would be great to have a regex to support this.
        # self.regex = '$(.*?)#'
        response = self._make_web_request()
        
        for line in response.text.split('\n'):
            if line.startswith('#') or line.strip() == '':
                continue
            
            try:
                formatted_line = line.split('#')[0].strip()
            except IndexError:
                print(f"[!] Unable to parse '{self.name}'. Value: {line}")
                return False
            else:
                self._queue(formatted_line)
        
        return True
        
