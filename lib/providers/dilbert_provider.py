import re

import bs4

from lib.provider import Provider
from lib.user_agent import UserAgent
from lib.resource import Resource

class DilbertProvider(Provider):
    COMIC_PAGE_URL = "https://dilbert.com"
    
    def fetch_latest_resource(self):
        return self._scrape_comic(self._fetch_comic_page())

    def _fetch_comic_page(self):

        """ Fetch the daily comic URL and return the raw HTML string. """
        
        ua = UserAgent()
        response = ua.get(self.COMIC_PAGE_URL)

        if not response.ok:
          response.raise_for_status()

        return response.text

    def _scrape_comic(self, html):

        """ Scrape and return the comic image URL given a HTML string. """
        
        soup = bs4.BeautifulSoup(html, "html.parser")    
        anchor = soup.find("a", class_="img-comic-link")
        img = soup.find("img", class_="img-comic")
        
        if not anchor:
            raise LookupError("Could not look up the comic anchor tag")
        elif not img:
            raise LookupError("Could not look up the comic image tag")
        
        _id = re.search(r"/([\d-]+)$", anchor["href"])[1]
        title = re.sub(r"\s*-[^-]*$", "", img["alt"])
        
        return Resource(id=_id, url=img["src"], title=title, alt_text=title)
