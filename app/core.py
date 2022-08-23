import csv
import json
import os
import random
import shutil
import string
import tempfile
import time
import zipfile 

import requests
import validators 

from io import StringIO
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from db import  db, add_db_entry, feedlist_entry_exist, add_feedlist, FeedRunTime


class FeedBase:

    def __init__(self) -> None:
        '''
            private and does not need to be modified manually
        '''
        self._urls = [] # Stores urls for future processing
        self.download_dir = tempfile.gettempdir() # Used to write zip files if needed
        self.runtime = None # Used by the database to determine running environment

        '''
            public and able to be modified
        '''
        self.feed_output_type = None
        self.feed_url = None
        self.name = None
        self.type = None

        # csv specific settings
        self.csv_delimiter = ','
        self.csv_headers = True
        self.csv_parsed_field_name = None
        self.csv_parsed_field_offset = 0

        # dict specific settings
        self.json_keys = [ 'data' ]
        
        # misc settings
        self.flush_limit = 1000 # Tells how many urls to batch before shipping to eURL
        self.run_cycle = 86400 # Tells the database how often to allow this parser to run
        self.unzip = False # Tells the parsers that it will need to unzip contents from feed_url first
    
    def _choose_parser(self, data: any, is_file: bool=False):
        if self.feed_output_type == 'csv':
            return self._parse_output_csv(data, is_file)
        
        if is_file:
            data = open(data, 'r').read()

        if self.feed_output_type == 'list':
            return self._parse_output_list(data.text.lower())

        if self.feed_output_type == 'json':
            return self._parse_output_json(data.json())
        
        return False

    def _cleanup_files(self, filepath: str) -> None:
        os.remove(filepath)

    def _download_file(self) -> str:
        local_filename = ''.join(random.choices(string.ascii_lowercase, k=15))
        local_filepath = os.path.join(self.download_dir, local_filename)

        with requests.get(self.feed_url, stream=True) as r:
            with open(local_filepath, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        return local_filepath

    def _end_scheduled_job(self) -> bool:
        self.runtime.last_runtime = int(time.time())
        return add_db_entry(self.runtime)

    def _extract_zip(self, local_file: str) -> None:
        with zipfile.ZipFile(local_file) as zf:
            zf.extractall(self.download_dir)
            extracted_files = [os.path.join(self.download_dir, f) for f in zf.namelist()]
        
        self._cleanup_files(local_file)
        return extracted_files

    def _flush_queue(self) -> None:
        if len(self._urls) == 0:
            return 
        
        enrichment = EnrichmentList()
        enrichment.type = self.type
        enrichment.source = self.name

        self.runtime.processed += len(self._urls)

        while len(self._urls) > 0:
            if not submit_data(enrichment.get_structured_data(self._urls[0:999])):
                print(f"\t[!] Submit data module failed, please troubleshoot for {enrichment.source}")
            self._urls = self._urls[1000:]
        
        self.runtime = add_db_entry(self.runtime)
        
    def _make_web_request(self, url=None) -> requests.Response:
        if not url:
            url = self.feed_url

        response = requests.get(url)
        if response.status_code != 200:
            print(f"[!] Failed to connect to {self.name}. Received status code '{response.status_code}")
            return False
        else:
            return response

    def _parse_output_csv(self, data: any, is_file: bool=False) -> None:
        def __parser(csv_file_as_string: StringIO) -> None:
            if self.csv_headers and self.csv_parsed_field_name:
                reader = csv.DictReader(csv_file_as_string, delimiter=self.csv_delimiter)
                for row in reader:
                    print(row)
                    self._queue(row.get(self.csv_parsed_field_name))
            else:
                reader = csv.reader(csv_file_as_string, delimiter=self.csv_delimiter)
                for row in reader:
                    self._queue(row[self.csv_parsed_field_offset])
            self._flush_queue()

        if is_file:
            with open(data, newline='') as f:
                __parser(f)

            self._cleanup_files(data)
        else:
            if isinstance(data, str):
                __parser(StringIO(data))
            else:
                __parser(StringIO(data.text))

        return True

    def _parse_output_custom(self) -> bool:
        # You will need to overload this with custom stuff
        return False
        
    def _parse_output_json(self, data: dict) -> None:
        for value in self.json_keys:
            data = data[value]

        self._urls = data

    def _parse_output_list(self, data:str) -> None:
        self._urls = [d.strip().rstrip('/') for d in data.split('\n') if d != '' and not d.startswith('#')]

    def _parse_output_misp(self) -> bool:
        # Starting off by grabbing all the repos
        response = self._make_web_request()
        if not response:
            return False

        soup = BeautifulSoup(response.text, 'html.parser')

        feed_urls = []

        for node in soup.find_all('a'):
            if node.get('href').endswith('json') and not node.get('href').startswith('manifest'):
                feed_urls.append(node.get('href'))
        
        # Iterating through each list to grab domains
        for uri in feed_urls:
            print(f"\tDownloading from: {uri}")
            if feedlist_entry_exist(self.name, uri):
                continue # Prevents us from processing again

            # Processing list
            response = self._make_web_request(f"{self.feed_url}{uri}")
            if not response:
                return False

            try:
                data = response.json()
            except:
                print(f"\t[!] Data format has changed for {self.name}/{uri}... skipping")
                continue

            if not data.get('Event'):
                continue

            # Their new schema
            if data['Event'].get('Attribute'):
                for value in data['Event']['Attribute']:
                    if validators.url(value.get('value')):
                        self._queue(value['value'])

            # Their old schema
            if data['Event'].get('Object'):
                for object in data['Event']['Object']:
                    if object.get('Attribute'):
                        for value in object['Attribute']:
                            if validators.url(value.get('value')):
                                self._queue(value['value'])
            
            if not add_feedlist(self.name, uri):
                print(f"\t[!] Failed to add {self.name}/{uri} to the database")
                return False

        self._flush_queue()
        return True

    def _queue(self, data: str) -> None:
        if not data:
            return
        elif len(self._urls) > self.flush_limit:
            self._flush_queue()
        else:
            self._urls.append(data.lower())

    def _start_scheduled_job(self) -> bool:
        self.runtime = db.query(FeedRunTime).filter_by(source=self.name).first()

        if self.runtime:
            if self.runtime.last_runtime:
              if self.run_cycle == 0:
                print('\t[*] Runtime is a fixed, one time run. Will not run again.')
                return False
              elif int(time.time()) < self.run_cycle + self.runtime.last_runtime:
                print('\t[*] Runtime dictates that this flow should not run yet.')
                return False
        else:
            self.runtime = FeedRunTime(source=self.name)

        self.runtime.last_starttime = int(time.time())
        self.runtime.processed = 0
        self.runtime = add_db_entry(self.runtime)

        return True

    def _validate(self) -> bool:
        if not self.name:
            print('\t[!] Missing name in class, erroring out.')
        elif not self.type:
            print('\t[!] No enrichment type defined, options [blacklisted|whitelisted], erroring out.')
        elif not self.feed_output_type:
            print('\t[!] No feed_output_type defined, options [text|json|custom], erroring out.')
        elif not self.feed_url:
            print('\t[!] No feed_url defined, erroring out.')
        else:
            return True
        
        return False

    def get_enriched_urls(self) -> bool:        
        if not self._validate():
            return False

        if not self._start_scheduled_job():
            return False

        if self.feed_output_type == 'custom':
            if not self._parse_output_custom():
                return False
        elif self.feed_output_type == 'misp':
            if not self._parse_output_misp():
                return False
        else:
            
            if self.unzip:
                filepath = self._download_file()
                for extracted_file in self._extract_zip(filepath):
                    self._choose_parser(extracted_file, True)
            else:
                response = requests.get(url=self.feed_url)
                if response.status_code != 200:
                    print(f"\t[!] Failed to connect, status code: {response.status_code}")
                    return False
                
                self._choose_parser(response)
        
        self._flush_queue()
        return self._end_scheduled_job()


class EnrichmentList:

    def __init__(self) -> None:
        self.type = None
        self.source = None
    
    def output_object(self) -> dict:
        return {
            'enrichment_type': self.type,
            'enrichment_source': self.source,
            'domains': [],
            'urls': []
        }
    
    def get_structured_data(self, data: any) -> dict:
        output_data = self.output_object()

        for element in data:
            formatted_element = element.lower()
            
            if formatted_element.startswith('hxxp'):
                formatted_element = f"http{formatted_element[4:]}"
            if not formatted_element.startswith('http'):
                formatted_element = f"http://{formatted_element}"
            
            output_data['domains'].append(urlparse(formatted_element).netloc)
            output_data['urls'].append(formatted_element)
        
        output_data['domains'] = list(set(output_data['domains']))
        output_data['urls'] = list(set(output_data['urls']))

        return output_data


def submit_data(data: EnrichmentList.output_object) -> bool:
    
    def __web_request(source: str, names: list, status: str, note: str, endpoint: str) -> bool:
        print(f"\t\tShipping off new web request. Starting domain: {names[0]}")
        eurl_base_url = os.environ['EURL_BASE_URL'] if os.environ.get('EURL_BASE_URL') else 'http://localhost:8000'
        header = { 'Content-Type': 'application/json' }
        
        data = {    
            'names': [name for name in names],
            'note': note,
            'status': status,
            'source': source
        }

        if endpoint == 'domains':
            eurl_uri = '/api/v1/domain/add'
        elif endpoint == 'urls':
            return True
        else:
            print(f"\t[!] Invalid endpoint. '{endpoint}' was supplied")
            return False
        
        response = requests.post(url=f"{eurl_base_url}{eurl_uri}", headers=header, data=json.dumps(data))
        if response.status_code == 200:
            return True

        print(f"\t[!] Unable to conduct transaction. Recieved status code: {response.status_code}")
        print(response.text)
        return False

    source = data.get('enrichment_source')
    status = data.get('enrichment_type')
    note = f"Detected in '{source}' enrichment list"

    for name_type in ['domains', 'urls']:
        names = data.get(name_type)
        if not __web_request(source, names, status, note, name_type):
            print(f"\t[!] Ending transaction for {source}")
            return False

    return True

