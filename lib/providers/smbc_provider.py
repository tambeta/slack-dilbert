import re
import json

from lib.provider import Provider
from lib.resource import Resource

class SMBCProvider(Provider):
    COMIC_PAGE_URL = "https://www.smbc-comics.com/"
    
    def fetch_latest_resource(self):
        return self._scrape_comic(self._fetch_soup(self.COMIC_PAGE_URL))

    def _scrape_comic(self, soup):
        metadata_tag = soup.find("script", type="application/ld+json")
        metadata = json.loads(metadata_tag.string)
        
        url = metadata["image"]
        _id = re.split(r"[/.]", url)[-2]
        title = re.split(r"[-–—]", metadata["name"])[1].strip()
        alt_text = soup.find("img", src=url)["title"]
        
        return Resource(id=_id, url=url, title=title, alt_text=alt_text)
