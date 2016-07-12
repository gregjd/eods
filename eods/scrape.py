import bs4
import csv
import pandas as pd
import re
import urllib2



# 'Powered by the Socrata Open Data Platform'


class Place(object):

    def __init__(self, input_dict):

        self.loc = input_dict['Location']
        self.state = input_dict['State']
        self.pop = input_dict['Population (US Census, 2011)']
        self.ownership = input_dict['Ownership?']
        self.policy = input_dict['Open Data Policy?']
        self.link = input_dict['Link']
        self.type = input_dict['Type']

        self.datasets = pd.DataFrame()

        self._get_info()

    @property
    def shortlink(self):

        return self.link.lstrip('htps:/').rstrip('/')

    @property
    def name(self):

        return '{0} ({1})'.format(self.loc, self.shortlink)

    @property
    def _link_to_try(self):

        link = (self.link if self.link[-1] == '/' else self.link + '/')

        return link + 'browse?sortBy=most_accessed'

    def _get_info(self):

        try:
#            s = bs4.BeautifulSoup(urllib2.urlopen(self.link_to_try).read(),
#                                  'html.parser')
            s = self._get_soup(self._link_to_try)
        except urllib2.HTTPError:
#            self.soup = None
            pass
        else:
            # self.soup = s
            # self._read_page(s)
            # get first page results
#            rp = self._read_page(s)
#            print type(rp)
#            print len(rp)
#            print 'first run'
            for res in self._read_page(s):
#                print 'res'
                self._parse_result(res)
            end_page_num = self._get_end_num(s)
            if end_page_num:
                self._read_all_pages(2, end_page_num + 1)
            # if end page number: read all other pages
        finally:
            return

    def _read_all_pages(self, start, end):
        print(start, end)

        #for num in range(start, end):
        for num in range(start, 4):
#            print(num)
            url = self._link_to_try + '&utf8=%E2%9C%93&page=' + str(num)
#            print(url)
            for result in self._read_page(self._get_soup(url)):
                #print('before')
                self._parse_result(result)
                #print('after')

        return

    @staticmethod
    def _get_soup(url):

        return bs4.BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')

    @staticmethod
    def _read_page(page_soup):
#        print('reading page')
#        print(type(page_soup.find_all('div', {'class': 'browse2-result'})))
#        for i in page_soup.find_all('div', {'class': 'browse2-result'}):
#            print type(i)

        return page_soup.find_all('div', {'class': 'browse2-result'})

    def _parse_result(self, result):

#        print('parsing result')

        def _find(child_tag_type, class_):

            child_tag = result.find(child_tag_type,
                                    {'class': 'browse2-result-' + class_})

            return child_tag.text.strip().encode('utf-8')

#        print('pr2')

        result_dict = {
            'name': _find('a', 'name-link'),
#            'category': _find('a', 'category'),
            'type': _find('span', 'type-name'),
#            'topics': [t.test.strip() for t in
#                result.find_all('a', {'class': 'browse2-result-topic'})],
            'views': _integer(_find('div', 'view-count-value'))
            #'descrip': _find('div', 'description')
        }

        #print(result_dict)

#        print('pr3')
#        print(len(self.datasets))

        self.datasets = self.datasets.append(result_dict, ignore_index=True)
#        print(len(self.datasets))

#        print('pr4')

        return

#    @staticmethod
#    def _find(parent_tag, child_tag_type, class_):
#
#        return parent_tag.find(child_tag_type, {'class': class_})

    @staticmethod
    def _get_end_num(page_soup):

        print('looking for end num')

        link = page_soup.find('a', {'class': 'lastLink'}).get('href')
        end_num = re.search(r".+&page=(\d+)", link).group(1)

        return int(end_num)

#    def _get_results(self):
#
#        return self.soup.find_all('div', {'class': 'browse2-result'})

class Result(bs4.element.Tag):

    pass



def visit_all_sites():

    # for row in CSV, visit_site(row)

    return

def visit_site():

    return

def parse_all_pages(url):

    # for i in range(2,end): parse page-i
    # need to handle case where there's no last page link

    return

#def parse_first_page(page_soup):
#
#    return

#def get_results(page_soup):
#
#    return page_soup.find_all('div', {'class': 'browse2-result'})

#def get_soup(url):
#
#    try:
#        soup = bs4.BeautifulSoup(urllib2.urlopen(url).read(), 'html.parser')
#    except urllib2.HTTPError:
#        return None
#    else:
#        return soup


def _integer(number_string):

    return int(number_string.replace(',', ''))
