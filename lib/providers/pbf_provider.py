import re
import json

from lib.provider import Provider
from lib.resource import Resource

class PBFProvider(Provider):
    COMIC_PAGE_URL = "https://pbfcomics.com/"
    
    fullname = "Perry Bible Fellowship"
    
    def fetch_latest_resource(self):
        return self._scrape_comic(self._fetch_soup(self.COMIC_PAGE_URL))

    def _scrape_comic(self, soup):
        _id = soup.find("article")["id"].split("-")[1]
        url = soup.select("div#comic > img")[0]["data-src"]
        title = soup.find("h1").string
        
        return Resource(provider=self, id=_id, url=url, title=title, alt_text=title)
        
