#! python3

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests, os, bs4

url = 'https://killsixbilliondemons.com/'
os.makedirs('killsixbilliondemons', exist_ok=True)

failed_pages = []


while not url.endswith('kill-six-billion-demons-chapter-1'):

    print('Downloading page %s...' % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
 # Find the URL of the comic image.
    comicElem = soup.select('#comic img')
    if comicElem == []:
        print('Could not find comic image.')
    else:
        comicUrl =  comicElem[0].get('src')
        # Download the image.
        print('Downloading image %s...' % (comicUrl))
        res = requests.get(comicUrl)
        res.raise_for_status()


        try:

            imageFile = open(os.path.join('killsixbilliondemons', os.path.basename(comicUrl)), 'wb')
            for chunk in res.iter_content(100000):
                imageFile.write(chunk)
            imageFile.close()
        except OSError:
            print("failed to download image.")
            failed_pages += comicUrl



    # Get the Prev button's url.
    try:

        prevLink = soup.select('a[class="navi comic-nav-previous navi-prev"]')[0]
        url =  prevLink.get('href')
    except IndexError:
        break





print('Done.')
if failed_pages:
    print("There were some un-downloaded pages. URLS listed here:")
    for page in failed_pages:
        print(page)