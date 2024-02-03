import dotenv
from engine.web_scraping import WebScraping


ENV = dotenv.find_dotenv('.env')
if ENV:
    dotenv.load_dotenv(ENV)


# URL of the news website
NEWS_URL= "https://apnews.com/"

def main():
    WebScraping(url=NEWS_URL)


if __name__ == "__main__":
    main()
