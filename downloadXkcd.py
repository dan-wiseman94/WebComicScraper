#! python3

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests, os, bs4, threading

url = 'https://xkcd.com'
os.makedirs('xkcd', exist_ok=True)

def downloadXkcd(startComic, endComic):
    for urlNumber in range(startComic, endComic):
        # Download the page.
        print('Downloading page https://xkcd.com/%s...' % (urlNumber))
        res = requests.get('https://xkcd.com/%s' % (urlNumber))
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        comicElem = soup.select('#comic img')

        if comicElem == []:
            print('Could not find comic image.')
        else:
            comicUrl = comicElem[0].get('src') # Download the image.
            print('Downloading image %s...' % (comicUrl))
            res = requests.get('https:' + comicUrl)
            res.raise_for_status()

            # Save the image to ./xkcd.
            imageFile = open(os.path.join('xkcd', os.path.basename(comicUrl)),
                             'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()



downloadThreads = []             # a list of all the Thread objects
res = requests.get(url)

soup = bs4.BeautifulSoup(res.text, 'html.parser')

prevLink = soup.select('a[rel=prev]')[0]


for i in range(0, 2632, 100): #hard-coded range TODO: automate range
    start = i
    end = i + 99
    if start == 0:
        start = 1 # There is no comic 0, so set it to 1.
    downloadThread = threading.Thread(target=downloadXkcd, args=(start, end))
    downloadThreads.append(downloadThread)
    downloadThread.start()

for downloadThread in downloadThreads:
    downloadThread.join()
print('Done.')


print('Done.')