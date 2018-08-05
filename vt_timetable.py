# Package modified from pyvt. Original source code by Kevin Cianfarini
import re
import requests
from html import unescape
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
from html.parser import HTMLParser

class MyPrereqHTMLParser(HTMLParser):
    
    prereqs_begins = False
    is_recording = False
    saved_stream = list()

    def __init__(self):
        HTMLParser.__init__(self)
        self.prereqs_begins = False
        self.is_recording = False
        self.saved_stream = list()

    def handle_starttag(self, tag, attrs):
        if tag.lower() == '<td>' and self.is_recording:
            self.is_recording = False
        if tag.lower() == 'a' and self.prereqs_begins:
            self.is_recording = True

    def handle_data(self, data):
        if "Prerequisites:" in data:
            self.prereqs_begins = True
        if "Corequisites:" in data:
            self.prereqs_begins = False
        if self.is_recording and "grade of" not in data:
            self.saved_stream.append(data)

    def get_stream(self):
        return self.saved_stream


"""
class MyCreditHTMLParser(HTMLParser):

    credits_begins = False
    num_steps = 0
    is_recording = False
    credits = 0
    has_recorded = True

    def __init__(self):
        HTMLParser.__init(self)
        self.credits_begins = False
        self.is_recording = True
        self.num_steps = 0
        self.is_recording = False
        self.credits = 0
        self.has_recorded = True

    def handle_starttag(self, tag, attrs):
        if has_recorded:
            pass
        else:

    def handle_data(self, data):

    def get_credits(self):
        return self.credits
"""

class Timetable:
    def __init__(self):
        
        self.url = 'https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest'
        self.sleep_time = 1
        self.base_request = {  # base required request data
            'BTN_PRESSED': 'FIND class sections',
            'CAMPUS': '0',  # blacksburg campus
            'SCHDTYPE': '%'
        }
        self.data_keys = ['crn', 'code', 'name', 'lecture_type', 'credits', 'capacity',
                          'instructor', 'days', 'start_time', 'end_time', 'location', 'exam_type']

    @property
    def _default_term_year(self):
        term_months = [1, 6, 7, 9]  # Spring, Summer I, Summer II, Fall
        current_year = datetime.today().year
        current_month = datetime.today().month
        term_month = max(key for key in term_months if key <= current_month)
        return '%d%s' % (current_year, str(term_month).zfill(2))

    def crn_lookup(self, crn_code, term_year=None, open_only=True):
        section = self.refined_lookup(crn_code=crn_code, term_year=term_year, open_only=open_only)
        return section[0] if section is not None else None

    def class_lookup(self, subject_code, class_number, term_year=None, open_only=True):
        return self.refined_lookup(subject_code=subject_code, class_number=class_number,
                                   term_year=term_year, open_only=open_only)

    def cle_lookup(self, cle_code, term_year=None, open_only=True):
        return self.refined_lookup(cle_code=cle_code, term_year=term_year, open_only=open_only)

    def subject_lookup(self, subject_code, term_year=None, open_only=True):
        return self.refined_lookup(subject_code=subject_code, term_year=term_year, open_only=open_only)

    def refined_lookup(self, crn_code=None, subject_code=None, class_number=None, cle_code=None,
                       term_year=None, open_only=True):
        request_data = self.base_request.copy()
        request_data['TERMYEAR'] = term_year if term_year is not None else self._default_term_year

        if crn_code is not None:
            if len(crn_code) < 3:
                raise ValueError('Invalid CRN: must be longer than 3 characters')
            request_data['crn'] = crn_code

        if subject_code is not None:
            request_data['subj_code'] = subject_code

        if class_number is not None:
            if len(class_number) != 4:
                raise ValueError('Invalid Subject Number: must be 4 characters')
            request_data['CRSE_NUMBER'] = class_number

        if subject_code is None and class_number is not None:
            raise ValueError('A subject code must be supplied with a class number')

        request_data['CORE_CODE'] = 'AR%' if cle_code is None else cle_code

        request_data['open_only'] = 'on' if open_only else ''

        req = self._make_request(request_data)
        # return req
        sections = self._parse_table(req)
        return None if sections is None or len(sections) == 0 else sections

    def unrefined_crn_lookup(self, crn_code, term_year):
        request_data = self.base_request.copy()
        request_data['crn'] = crn_code
        request_data['TERMYEAR'] = term_year
        request_data['CORE_CODE'] = 'AR%'
        request_data['open_only'] = ''
        
        # req is a BeautifulSoup object
        req = self._make_request(request_data)
        intermediate_link = self._dirty_parse_table(req)

        # focused_req is also a BeautifulSoup object
        focused_req = self._make_focused_request(intermediate_link)
        prerequisites = self._parse_focused_page(focused_req)
        # focused_table_formatted = self._parse_focused_page(focused_table_unformatted)
        
        # getting the credit hours for the requested class
        searched_timetable = [
            [
                [td.text.replace('\\n', '') for td in tr.find_all('td')]
                for tr in table.find_all('tr')
            ]
            for table in req.find_all('table')
        ]
        
        end = prerequisites.index("Corequisites:") if "Corequisites:" in prerequisites else -1
        prerequisites_2 = prerequisites[0:end]
        credits = searched_timetable[-2][-1][4].replace('\n', '')

        temp_refine = self.refined_lookup(crn_code = crn_code, term_year = term_year)
        
        human_name = None
        if temp_refine:
            target = temp_refine[0]
            human_name = target[2]

        values = {"credits": int(credits), "prerequisites": prerequisites_2, "human_name": human_name}
        return values

    def _make_focused_request(self, request_data):
        opener = urllib.request.FancyURLopener({})
        focused_file = opener.open(request_data)
        content = str(focused_file.read())
        focused_bs = BeautifulSoup(content, 'html.parser')
        return content

    def _parse_focused_page(self, html):
        # print(html)
        raw_html_text = html.replace('\\n', '')
        # print(raw_html_text)
        parser = MyPrereqHTMLParser()
        parser.feed(raw_html_text)
        prerequisites = parser.get_stream()
        parser.close()
        # prerequisites = [a for a in html.find_all('a', href=True)]
        return prerequisites

    # old parses
    def _parse_row(self, row):
        entries = [entry.text.replace('\n', '').replace('-', ' ').strip() for entry in row.find_all('td')]
        if len(entries) <= 1:
            return None
        # return Section(**dict(zip(self.data_keys, entries)))
        return entries

    def _parse_table(self, html):
        table = html.find('table', attrs={'class': 'dataentrytable'})
        if table is None:
            return None
        rows = [row for row in table.find_all('tr') if row.attrs == {}]
        sections = [self._parse_row(c) for c in rows if self._parse_row(c) is not None]
        return None if not sections else sections
        # return rows

    # obtains the link as highlighted with the CRN number on the very left of the table
    def _dirty_parse_table(self, html):
        table = html.find('table', attrs={'class': 'dataentrytable'})
        if table is None:
            print("No valid table found.")
            return None
        rows = [row for row in str(table.find_all('tr')).split('\n') 
                    if 'javascript:flexibleWindow' in str(row)]
        
        raw_link = rows[0]

        link_left_filter = 'javascript:flexibleWindow("'
        link_right_filter = 'history=N'
        intermediate_link = str(raw_link[raw_link.find(link_left_filter) + len(link_left_filter): raw_link.rfind(link_right_filter)])
        intermediate_link = unescape(intermediate_link)
        intermediate_link = "https://banweb.banner.vt.edu/ssb/prod/" + intermediate_link + "history=N"
        
        # sections = [self._dirty_parse_row(c) for c in rows if self._dirty_parse_row(c) is not None]
        return intermediate_link

    def _dirty_parse_row(self, row):
        entries = [entry.text.replace('\n', '').replace('-', ' ').strip() for entry in row.find_all('td')]
        if len(entries) <= 1:
            return None
        return entries

    # returns as html source file
    def _make_request(self, request_data):
        r = requests.post(self.url, data=request_data)
        if r.status_code != 200:
            self.sleep_time *= 2
            raise TimetableError('The VT Timetable is down or the request was bad. Status Code was: %d'
                                 % r.status_code, self.sleep_time)
        self.sleep_time = 1

        return BeautifulSoup(r.content, 'html.parser')


class TimetableError(Exception):

    def __init__(self, message, sleep_time):
        super(TimetableError, self).__init__(message)
        self.sleep_time = sleep_time


class Section:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    def tuple_str(tup):
        return str(tup).replace("'", "")

    def __str__(self):
        return '%s (%s) on %s at %s' % (getattr(self, 'name'), getattr(self, 'crn'),
                                        getattr(self, 'days'),
                                        Section.tuple_str((getattr(self, 'start_time'), getattr(self, 'end_time'))))

    def __eq__(self, other):
        if isinstance(other, Section):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return int(getattr(self, 'crn'))

