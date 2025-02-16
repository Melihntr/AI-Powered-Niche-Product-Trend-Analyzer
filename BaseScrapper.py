import requests
from bs4 import BeautifulSoup
import time


class BaseScraper:
    def __init__(self, headers=None):
        self.headers = headers if headers else {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def fetch_page(self, url):
        """Fetches the HTML content of a webpage."""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None


class EtsyScraper(BaseScraper):
    """
    Scrapes product data from Etsy.
    """

    def __init__(self):
        super().__init__()
        self.base_url = "https://www.etsy.com/search?q="

    def scrape_products(self, query, max_results=10):
        """Scrapes Etsy for product listings based on a search query."""
        url = self.base_url + query.replace(" ", "+")
        html = self.fetch_page(url)
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        products = []
        for item in soup.select(".v2-listing-card")[:max_results]:
            title = item.select_one(".text-body").get_text(strip=True) if item.select_one(".text-body") else "Unknown"
            price = item.select_one(".currency-value").get_text(strip=True) if item.select_one(
                ".currency-value") else "Unknown"
            link = item.select_one("a")["href"] if item.select_one("a") else "#"
            products.append({"title": title, "price": price, "link": link})

        return products


class RedditScraper(BaseScraper):
    def __init__(self, client_id, client_secret, user_agent):
        super().__init__()
        self.auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        self.headers.update({"User-Agent": user_agent})
        self.token = self.get_token()
        self.headers.update({"Authorization": f"bearer {self.token}"})
        self.base_url = "https://oauth.reddit.com/r/"

    def get_token(self):
        """Fetches an OAuth token for Reddit API access."""
        data = {"grant_type": "client_credentials"}
        auth_response = requests.post("https://www.reddit.com/api/v1/access_token", auth=self.auth, data=data,
                                      headers=self.headers)
        if auth_response.status_code != 200:
            print("Failed to get access token for Reddit.")
            return ""
        return auth_response.json().get("access_token", "")

    def scrape_posts(self, subreddit, limit=10):
        """Scrapes top discussions from a given subreddit."""
        url = f"{self.base_url}{subreddit}/hot?limit={limit}"
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print("Failed to fetch Reddit posts, status code:", response.status_code)
            return []

        try:
            posts = response.json().get("data", {}).get("children", [])
        except ValueError as e:
            print(f"Error parsing Reddit response: {e}")
            return []

        return [{"title": post["data"]["title"], "score": post["data"]["score"]} for post in posts]