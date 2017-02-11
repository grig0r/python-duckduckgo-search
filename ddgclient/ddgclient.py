from urllib.parse import parse_qs, urlsplit
from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://duckduckgo.com/html'

def get_param_from_url(url, param):
     querystring = urlsplit(url).query
     value_list = parse_qs(querystring).get(param)
     if value_list is None:
         return None
     else:
         return value_list[0]

class ResultPage(object):

    def __init__(self, q, start=0):
        self.q = q
        self.start = start
        self.soup = self.get_soup()
        self.results = [Result(result_tag) for result_tag in self.soup.find_all('div', class_='result')]

    def get_soup(self):
        payload = {
            'q' : self.q,
            's' : self.start,
            'o' : 'json',
            'api' : '/d.js',
            'dc' : '-1'
            }
        response = requests.get(BASE_URL, params=payload)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def is_nav_tag(self, tag):
        if tag.name == 'div' \
                and 'class' in tag.attrs.keys() \
                and 'nav-link' in tag.attrs.get('class'):
            return True
        else:
            return False

    def is_next_tag(self, tag):
        if self.is_nav_tag(tag) and tag.find('input', type='submit').attrs.get('value') == 'Next':
            return True
        else:
            return False

    def is_previous_tag(self, tag):
        if self.is_nav_tag(tag) and tag.find('input', type='submit').attrs.get('value') == 'Previous':
            return True
        else:
            return False

    @staticmethod
    def _get_s(nav_tag):
        return nav_tag.find('input', attrs={'name' : 's'}).attrs.get('value')

    def get_next_page(self):
        next_tag = self.soup.find(self.is_next_tag)
        if not next_tag:
            raise StopIteration
        return self.__class__(q=self.q, start=self._get_s(next_tag))

    def get_previous_page(self):
        previous_tag = self.soup.find(self.is_previous_tag)
        if not previous_tag:
            raise StopIteration
        return self.__class__(q=self.q, start=self._get_s(previous_tag))

class Result(object):

    def __init__(self, result_tag):
        self.result_tag = result_tag
        self.url = self._fetch_url()
        self.title = self._fetch_title()

    def __repr__(self):
        return '<Result: {} ({})>'.format(self.title, self.url)

    def _fetch_url(self):
        a_tag = self.result_tag.find('a', class_='result__a')
        href = a_tag.attrs.get('href')
        url = get_param_from_url(href, 'uddg')
        return url

    def _fetch_title(self):
        a_tag = self.result_tag.find('a', class_='result__a')
        title = a_tag.get_text()
        return title

class Search(object):

    def __init__(self, q):
        self.q = q
        self.pages = [ResultPage(q)]

    def fetch_next_page(self):
        self.pages.append(self.pages[-1].get_next_page())

    def page_generator(self):
        """yields result list from each page"""
        for p in self.pages:
            yield p.results
        while True:
            self.fetch_next_page()
            yield self.pages[-1].results

    def results(self, stop=30):
        out = []
        page_iterator = self.page_generator()
        while len(out) < stop:
            try:
                page = next(page_iterator)
            except StopIteration:
                return out
            out.extend(page)
        return out[:stop]
