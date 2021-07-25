import re

from lib.provider import Provider
from lib.resource import Resource

class DilbertProvider(Provider):
    COMIC_PAGE_URL = "https://dilbert.com"
    
    fullname = "Dilbert"
    
    def fetch_latest_resource(self):
        return self._scrape_comic(self._fetch_soup(self.COMIC_PAGE_URL))

    def _scrape_comic(self, soup):
        anchor = soup.find("a", class_="img-comic-link")
        img = soup.find("img", class_="img-comic")
        
        if not anchor:
            raise LookupError("Could not look up the comic anchor tag")
        elif not img:
            raise LookupError("Could not look up the comic image tag")
        
        _id = re.search(r"/([\d-]+)$", anchor["href"])[1]
        title = re.sub(r"\s*-[^-]*$", "", img["alt"])
        
        return Resource(provider=self, id=_id, url=img["src"], title=title, alt_text=title)
