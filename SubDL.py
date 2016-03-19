# Created by Jonathan Wang
# Download subtitles from ONLY yifysubtitles.com
import mechanize
import sys
br = mechanize.Browser()

# get movie name and open - not case sensitive
print 'Enter movie name'
movie_name = raw_input()
movie_query = movie_name.replace(" ", "+")
url_search = 'http://www.yifysubtitles.com/search?q=' + movie_query
br.open(url_search)

# get results of search query, extract only titles and url
movie_titles = [link for link in br.links() if movie_name.lower() in link.text.lower()]

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
movie_subs = []
for s in br.links():
    if "Chinese" in s.text:
        movie_subs.append(s)
    # break out of loop once it finds upload subtitles
    # if I didn't add this in it would result in attribute error
    if "upload subtitles" in s.text:
        break
if len(movie_subs) == 0:
    print 'No subtitles found in Chinese.'
    sys.exit()
print '\nFound ' + str(len(movie_subs)) + ' subtitles in Chinese\n'

# download subtitles to same directory as script
for d in movie_subs:
    new_url = d.url.split('/subtitles/', 1)[1]
    url_dl = 'http://www.yifysubtitles.com/subtitle/' + new_url + '.zip'
    print 'Downloading ' + url_dl
    br.retrieve(url_dl, new_url + '.zip')
