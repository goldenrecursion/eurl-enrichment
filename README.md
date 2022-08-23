# eURL Enrichment Tool
This is a basic python application that processess different public enrichment lists and sends them to
the eURL service.

## Contributing to the Feed_Modules
We have built the application to dynamically read from `app/feed_modules`. To create a new
module, add a new python file (ensure it ends in `.py`) and instanciate the `FeedBase` class
from `/app/core.py` and name your new class `Feed`. 

Your `Feed` class will require the following values to be assigned and not `None`: 

 - `name`. This is any string that you want to identify the source of the feed. Does not have to be unique.
 - `type`. This is a string and only two values are accepted: `blacklisted`, `whitelisted`.
 - `run_cycle`. This is how often to run the feed. This field takes in an integer that represents seconds. Default is `86400` which is 1 day. If this is a one time feed read then use `0`. 
 - `feed_output_type`. this is the type of list we will be reading in. Currently, supports: 
   - `csv`. This will read in a web page that returns a CSV file. There are a couple of flags that you will need to pass into this.
     - `csv_delimiter`. This is the string delimiter used to split fields in the CSV file. Default is `,`.
     - `csv_headers`. This is a boolean value that will tell the parser that you have header if set to `True`. 
     - `csv_parsed_field_name`. This is required if `csv_headers` is `True`. You will specify a string that 
     represents the column header.
     - `csv_parsed_field_offset`. This is required if `csv_headers` is `False`. This is an integer to control the field offset starting at 0. Default is `0` which would be the first column.
   - `custom`. This will give you power to do whatever you want for the parser. It needs to return boolean and 
   use `_queue()` to add new entries.
   - `dict`. This will read in a web page that returns JSON output. If you specify this type then you 
   will also need to specify `json_keys`
     - `json_keys`. This is a list (ordered) for recursing through the dictionary for the right key. Example, 
     if your json is { 'site': { 'foo': {'urls': ['site1.com', 'site2.com']}}} then you would specify `[ 'site', 
     'foo', 'urls' ]`.
   - `list`. This will read in a web page where each line of the page is a url.
   - `misp`. This will parse a site according to the MISP standard format.
 - `feed_url`. This is URL for pulling data. 

A few other flags that you can pass into your `Feed` include:

 - `flush_limit`. This tells the service how often to flush the queue and ship data to eURL. Default is `1000`. Keep in mind that `1000` is the max limit supported by eURL.
 - `unzip`. This tell the parsers that the web request is zipped and will need to be unzipped first. Default is `False`. 

 An Example would be:

    from core import FeedBase
    
    
    class Feed(FeedBase):
    
        def __init__(self) -> None:
            super().__init__()
            self.name = 'mysite'
            self.type = 'blacklisted' 
            self.feed_output_type = 'list'
            self.feed_url = 'https://mysite.com/list.txt'
