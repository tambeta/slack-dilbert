from lib.provider import Provider
from lib.resource import Resource

class XKCDProvider(Provider):
    COMIC_PAGE_URL = "https://xkcd.com/"
    
    fullname = "XKCD"
    
    def fetch_latest_resource(self):
        return self._scrape_comic(self._fetch_soup(self.COMIC_PAGE_URL))

    def _scrape_comic(self, soup):
        page_url = soup.select("meta[property=\"og:url\"]")[0]["content"]
        _id = page_url.rstrip("/").split("/")[-1]
        img = soup.select("div#comic > img")[0]

        return Resource(
            provider=self,
            id=_id,
            url=img["src"],
            title=img["alt"],
            alt_text=img["title"]
        )
