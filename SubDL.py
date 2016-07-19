# Created by Jonathan Wang
# Download subtitles from ONLY yifysubtitles.com
import mechanize
from BeautifulSoup import BeautifulSoup
import sys
br = mechanize.Browser()

# get movie name and open - not case sensitive
print 'Enter movie name'
movie_name = raw_input()
movie_query = movie_name.replace(" ", "+")
url_search = 'http://www.yifysubtitles.com/search?q=' + movie_query
br.open(url_search)

# get results of search query, remove first element b/c we dont want it
movie_titles = []
for l in br.links():
	if '[IMG]' in l.text:
		movie_titles.append(l)
movie_titles.pop(0)
		
# output list and let user choose which movie
if len(movie_titles) == 0:
    print 'No movies found for 2 possible reasons: \n1. Make sure you spelled the movie title correctly.\n2. Subtitle is not available on YIFY'
    sys.exit()
print '\nList of movies\n--------------'
number = 1
for t in movie_titles:
    print str(number) + " --- " + t.text.split('[IMG]', 1)[0]
    number += 1
print '\nPick movie number\n-----------------'
movie_number = raw_input()

# user selects movie and we search for chinese subs only
url_movie = 'http://www.yifysubtitles.com' + movie_titles[int(movie_number)-1].url
br.open(url_movie)

# go through table row, find chinese, get table data, find download, finally download!
soup = BeautifulSoup(br.response().read())
table = soup.find('tbody')
for tr in table.findChildren('tr'):
	if 'Chinese' in tr.text: 
		for td in tr:
			if 'download' in td.text:
				new_url = (td.find('a')['href'])[11:]
				url_dl = 'http://www.yifysubtitles.com/subtitle/' + new_url + '.zip'
				print '\nDownloading ' + url_dl
				br.retrieve(url_dl, new_url + '.zip')
