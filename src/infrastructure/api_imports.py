from infrastructure.apis.News.GNews.gnews_api import GNewsClient
from infrastructure.apis.coinlore_api import CoinloreAPI
from infrastructure.apis.finance.alpha_vantage.alpha_vantage_api import AlphaVantageClient
from infrastructure.apis.google_console_api.google_console_api import GoogleServicesClient
from infrastructure.apis.here_api import HereAPI
from infrastructure.apis.social_media.pinterest.pinterest_client import PinterestClient
from infrastructure.apis.social_media.reddit.reddit_client import RedditClient
from infrastructure.apis.social_media.twitter.twitter_client import TwitterClient
from infrastructure.apis.binance_api import BinanceAPI
from infrastructure.apis.cdc_api import CDCAPI
from infrastructure.apis.crunchbase_api import CrunchbaseAPI
from infrastructure.apis.ecb_exchange_rates_api import ECBExchangeRatesAPI
from infrastructure.apis.free_forex_api import FreeForexAPI
from infrastructure.apis.guardian_media_api import GuardianNewsAPI
from infrastructure.apis.health_care_api import HealthCareAPI
from infrastructure.apis.human_api import HumanAPI
from infrastructure.apis.open_fda_api import OpenFDAAPI
from infrastructure.apis.crypto_compare_api import CryptoCompareAPI
from .apis.trello_api import TrelloAPI
from .apis.hacker_news import HackerNewsAPI
from infrastructure.apis.quickbook_api.quickbook_api import QuickBooksAPI
from infrastructure.apis.slack_api.slack_service import SlackService
from .apis.hubspot_api import HubSpotAPI
from .apis.news_api import NewsAPIInitializer
from .apis.github_api.github_api import  GitHubAPIIntializer
from .apis.statista_api import StatistaAPI
from .apis.hunter_api import HunterAPI


def get_flat_api_instance_tree() -> dict:
    """
    Generate and return a flat tree structure where API names map directly to their class instances.
    """
    try:
        tree = {
            "alpha_vantage_api": AlphaVantageClient(),
            "crypto_compare_api": CryptoCompareAPI(),
            "binance_api": BinanceAPI(),
            "coinlore_api": CoinloreAPI(),
            "free_forex_api": FreeForexAPI(),
            "ecb_exchange_rates_api": ECBExchangeRatesAPI(),
            "quickbook_api": SlackService(),
            "slack_api": SlackService(),
            "news_api": NewsAPIInitializer(),
            "gnews_api": GNewsClient(),
            "guardian_media_api": GuardianNewsAPI(),
            "hacker_news_api": HackerNewsAPI(),
            "twitter_api": TwitterClient(),
            "pinterest_api": PinterestClient(),
            "reddit_api": RedditClient(),
            "hubspot_api": HubSpotAPI(),
            "trello_api": TrelloAPI(),
            "crunchbase_api": SlackService(),
            "statista_api": SlackService(),
            "github_search_api_call": GitHubAPIIntializer(),
            "google_services_api": GoogleServicesClient(),
            "health_care_api": HealthCareAPI(),
            "cdc_api": CDCAPI(),
            "human_api": SlackService(),
            "open_fda_api": OpenFDAAPI(),
            "here_api": HereAPI(),
        }

        return tree
    except Exception as e:
        print(f"Error inside get_flat_api_instance_tree: {e}")
        raise
