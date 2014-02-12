# Opensubtitles command line downloader
# Copyright (C) 2014  Tomas Meszaros <exo at tty dot sk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from bs4 import BeautifulSoup
from urllib import urlretrieve
from urllib2 import urlopen
from os import getcwd
from sys import exit

OPEN_SUBTITLES_URL = 'http://www.opensubtitles.org'

def main():
    movie = raw_input("Search for movie title: ")

    if movie == '':
        print "Not found, see ya!"
        exit(0)

    url = construct_url(movie)
    titles_source = get_html_source(url)
    titles_handler = BeautifulSoup(titles_source)
    titles = get_title_href_zip(titles_handler)

    for i in range(len(titles)):
        print "[%d] %s" % (i, titles[i][0])

    movie_index = input("Pick movie number in brackets: ")

    subtitles_source = get_html_source(titles[movie_index][1])
    subtitles_handler = BeautifulSoup(subtitles_source)
    subtitles = get_sub_name_href_zip(subtitles_handler)

    for i in range(len(subtitles)):
        print "[%d] %s" % (i, subtitles[i][0])

    subtitles_index = input("Pick subtitles number in brackets you want to download: ")
    subtitles_url = subtitles[subtitles_index][1]
    download_path = raw_input("Give me path where to save it: ")
    if download_path == '':
        download_path = "%s/%s.zip" % (getcwd(), subtitles[subtitles_index][0])
    download(subtitles_url, download_path)

def download(url, path):
    urlretrieve(url, path)

def get_html_source(url):
    return urlopen(url).read()

def construct_url(movie):
    return "http://www.opensubtitles.org/en/search2/sublanguageid-all/moviename-%s" % movie.replace(' ', '+')

def get_title_href_zip(source_handler):
    # filter entries from handler starting with name* and save them to list
    names = source_handler.findAll("tr", id=lambda x: x and x.startswith('name'))
    # filter names list so we end up only with titles and href to them
    entries = map(lambda x: x.find("a", title=lambda y: y), names)
    titles = map(lambda x: x.text.split("\n")[0], entries)
    hrefs = map(lambda x: OPEN_SUBTITLES_URL + x.get("href"), entries)
    return zip(titles, hrefs)

def get_sub_name_href_zip(source_handler):
    names = source_handler.findAll('td', id=lambda x: x and x.startswith('main'))
    sub_names = map(lambda x: x.text.split('Download')[0], names)
    hrefs = map(lambda x: OPEN_SUBTITLES_URL + "/en/subtitleserve/sub/" + x.get('id')[4:], names)
    return zip(sub_names, hrefs)

if __name__ == '__main__':
    main()
