import re
import requests
from bs4 import BeautifulSoup
import time
import wget
import os


def use_regex(input_text):
    pattern = re.findall(r"https://api\.modpacks\.ch/public/modpack/[0-9]+/[0-9]+/server/windows", input_text)
    return pattern


path = r"ADD_YOUR_DOWNLOAD_PATH"
index = 1
matches = []
not_downloaded = []

for i in range(130):
    time.sleep(0.6)
    url = f'https://www.feed-the-beast.com/modpacks/{index}'
    print(url)

    html_text = requests.get(url)
    print(html_text.status_code)
    if html_text.status_code == 404:
        index += 1
        pass

    else:
        soup = BeautifulSoup(html_text.content, 'html.parser')

        title = [title for title in soup.find_all('title')][0]
        link = [link.get('href') for link in soup.find_all('a')]
        for i in link:
            if use_regex(i):
                matches.append(i)
                print(i)
                try:
                    version = [version for version in soup.find_all("div", {"class": "Stat_value__qUmap"})][2]
                    title = title.get_text().replace(':', '')

                    if not os.path.exists(fr"{path}\{title}"):
                        os.mkdir(fr"{path}\{title}")

                    time.sleep(0.2)

                    if not os.path.exists(fr"{path}\{title}\{version.get_text()}"):
                        os.mkdir(fr"{path}\{title}\{version.get_text()}")

                    time.sleep(0.2)
                    file_id = [file_id for file_id in soup.find_all("div", {"class": "Badge_value__wvYgo"})][0].get_text()
                    download_path = fr"{path}\{title}\{version.get_text()}\serverinstall_{index}_{file_id}.exe"
                    if not os.path.isfile(path):
                        wget.download(i, download_path)
                except ValueError or FileExistsError:
                    not_downloaded.append(i)
                    pass
        index += 1

print(f"Downloaded: {matches}")
print(f"Not Downloaded: {not_downloaded}")




