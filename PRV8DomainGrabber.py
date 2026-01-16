from requests import get
from bs4 import BeautifulSoup as bs
from concurrent.futures import ThreadPoolExecutor as Thread
from rich.console import Console
import subprocess
import requests
import time
import os

c = Console()

class GreenSite:

    def __init__(self) -> None:
        self.domains = []
        self.url = 'https://www.greensiteinfo.com/domains/{}./'
        self.filename = ''

    def grab(self, ext, anext: bool=True):
        try:
            parse = bs(get(self.url.format(ext)).text, 'html.parser')
            is_nextable = parse.find('div', {'class': 'card-body'}).select('a')[-1].text == 'Next Page »'
            nexturl = parse.find('div', {'class': 'card-body'}).select('a')[-1].get('href') if is_nextable else None
            page = 1
            for x in parse.find('div', {'class': 'card-body'}).select('a')[:10]:
                self.domains.append(x.text.strip())
                open(self.filename, 'a+').write(x.text.strip() + '\n')
            print('page %d - %d' % (page, self.domains.__len__()))
            while True:
                if not is_nextable:
                    break
                else:
                    page += 1
                    reparse = bs(get(nexturl).text, 'html.parser')
                    is_nextable = reparse.find('div', {'class': 'card-body'}).select('a')[-1].text == 'Next Page »'
                    nexturl = reparse.find('div', {'class': 'card-body'}).select('a')[-1].get('href') if is_nextable else None
                    for x in reparse.find('div', {'class': 'card-body'}).select('a')[:10]:
                        self.domains.append(x.text.strip())
                        open(self.filename, 'a+').write(x.text.strip() + '\n')
                    print('page %d - %d' % (page, self.domains.__len__()))
            self.domains = []
        except Exception as e:
            print(e)


    def main(self):

        ext = input('YOUR DOMAINS NAME: ')
        thread = int(input('Threads : '))
        self.filename = f"{ext.replace(' ', '_')}.txt" 
        
        with Thread(max_workers=thread) as t:
            t.submit(self.grab, ext).result()


def banner():
    print('''

\033[93m 

██████╗ ██████╗ ██╗   ██╗ █████╗ 
██╔══██╗██╔══██╗██║   ██║██╔══██╗
██████╔╝██████╔╝██║   ██║╚█████╔╝
██╔═══╝ ██╔══██╗╚██╗ ██╔╝██╔══██╗
██║     ██║  ██║ ╚████╔╝ ╚█████╔╝
╚═╝     ╚═╝  ╚═╝  ╚═══╝   ╚════╝      
           \033[34m[ \033  [Domain Grabber\033[0m \033[34m]\033[0m
    \033[1;92mAuthor \033[1;91m: \033[1;96m@P_R_V_8''')
    print('-' * 50)

banner()

if __name__ == '__main__':
    GreenSite().main()
print('Success.')
