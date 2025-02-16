# main.py

# Import necessary classes
from BaseScrapper import EtsyScraper, RedditScraper
from DataStorage import DataStorage
from Analyzer import Analyzer

# Define the Main class before using it
class Main:
    def __init__(self, etsy_scraper, reddit_scraper, data_storage, analyzer):
        self.etsy_scraper = etsy_scraper
        self.reddit_scraper = reddit_scraper
        self.data_storage = data_storage
        self.analyzer = analyzer

    def run(self):
        # Scrape data
        etsy_data = self.etsy_scraper.scrape_products("eco-friendly gadgets")
        reddit_data = self.reddit_scraper.scrape_posts(subreddit="EcoFriendly", limit=10)

        # Combine and save data
        combined_data = etsy_data + reddit_data
        self.data_storage.save(combined_data)

        # Analyze trends
        self.analyzer.data = combined_data
        trends = self.analyzer.analyze_trends()

        # Print trends
        print("Top Trends:")
        for word, count in trends:
            print(f"{word}: {count}")

if __name__ == "__main__":
    # Initialize the components
    etsy_scraper = EtsyScraper()
    reddit_scraper = RedditScraper(client_id="NEG8mReyFjJpnVPXMGnD4w", client_secret="hNAYUe78clzQGVlB69ihOsZYOaOMIA", user_agent="python:my_scraper:v1.0 (by /u/Previous_Car7508)")
    data_storage = DataStorage()
    analyzer = Analyzer(data=[])

    # Initialize the Main class
    main = Main(etsy_scraper, reddit_scraper, data_storage, analyzer)

    # Run the program
    main.run()
