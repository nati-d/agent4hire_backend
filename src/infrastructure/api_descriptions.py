from infrastructure.embedding_service import EmbeddingService

api_data = [
    {
        "name": "Health Care API",
        "description": "Provides access to a wide range of healthcare information, including news, clinical trials, and drug information.",
        "domain": "Healthcare"
    },
    {
        "name": "CDC API",
        "description": "Offers data and tools related to public health and safety, including infectious disease trends, immunization information, and environmental health data.",
        "domain": "Healthcare"
    },
    {
        "name": "Human API",
        "description": "Provides personalized health insights and recommendations based on biometric data.",
        "domain": "Healthcare"
    },
    {
        "name": "Open FDA API",
        "description": "Offers access to a variety of FDA data, including drug labels, adverse event reports, and medical device recalls.",
        "domain": "Healthcare"
    },
    {
        "name": "Here API",
        "description": "Provides mapping, routing, and location-based services.",
        "domain": "Location and Mapping"
    },
    {
        "name": "GitHub API",
        "description": "Provides programmatic access to GitHub's features, allowing you to automate tasks, integrate with other tools, and build custom applications.",
        "domain": "Development Tools"
    },
    {
        "name": "Google Cloud Platform (GCP) API",
        "description": "Offers access to a wide range of Google Cloud services, including compute, storage, database, and machine learning.",
        "domain": "Development Tools"
    },
    {
        "name": "Trello API",
        "description": "Provides programmatic access to Trello's features, allowing you to automate tasks, integrate with other tools, and build custom applications.",
        "domain": "Project Management"
    },
    {
        "name": "Crunchbase API",
        "description": "Offers access to a vast database of companies, organizations, people, and funding information.",
        "domain": "Business Intelligence"
    },
    {
        "name": "Statista API",
        "description": "Provides access to a wide range of market research data, including statistics, forecasts, and consumer insights.",
        "domain": "Statistics, Business Intelligence"
    },
    {
        "name": "Slack API",
        "description": "Allows integration with Slack for team messaging, collaboration, and automated workflows within channels and direct messages.",
        "domain": "Communication"
    },
    {
        "name": "Twitter API",
        "description": "Provides access to Twitter's data and functionality, allowing you to read and write tweets, analyze trends, and build custom applications.",
        "domain": "Social Media"
    },
    {
        "name": "Pinterest API",
        "description": "Provides access to Pinterest's data and functionality, allowing you to search and save pins, analyze user behavior, and build custom applications.",
        "domain": "Social Media"
    },
    {
        "name": "Reddit API",
        "description": "Provides access to Reddit's data and functionality, allowing you to read and write posts, analyze community trends, and build custom applications.",
        "domain": "Social Media"
    },
    {
        "name": "HubSpot API",
        "description": "Provides access to HubSpot's CRM and marketing automation features, allowing you to manage contacts, track deals, and automate marketing campaigns.",
        "domain": "Social"
    },
    {
        "name": "News API",
        "description": "Provides access to a vast database of news articles from various sources.",
        "domain": "News"
    },
    {
        "name": "GNews API",
        "description": "Offers access to a wide range of news articles, including top headlines, search results, and country-specific news.",
        "domain": "News"
    },
    {
        "name": "Guardian Media API",
        "description": "Provides access to news articles, blogs, and multimedia content from The Guardian.",
        "domain": "News"
    },
    {
        "name": "Hacker News API",
        "description": "Provides access to Hacker News's data, including stories, comments, and user information.",
        "domain": "News"
    },
    {
        "name": "Free Forex API",
        "description": "Provides real-time and historical foreign exchange rates for various currency pairs.",
        "domain": "Finance, Forex"
    },
    {
        "name": "ECB Exchange Rates API",
        "description": "Provides historical and current exchange rates for currencies against the Euro, published by the European Central Bank.",
        "domain": "Finance, Forex"
    },
    {
        "name": "QuickBooks API",
        "description": "Provides programmatic access to QuickBooks's features, allowing you to automate tasks, integrate with other tools, and build custom applications.",
        "domain": "Accounting, Finance Management"
    },
    {
        "name": "Alpha Vantage API",
        "description": "Provides real-time and historical cryptocurrency data, including prices, market capitalization, and trading volume.",
        "domain": "Finance, Crypto"
    },
    {
        "name": "Crypto Compare API",
        "description": "Provides real-time and historical cryptocurrency data, including prices, market capitalization, and trading volume, as well as cryptocurrency exchange data and news.",
        "domain": "Finance, Crypto"
    },
    {
        "name": "Binance API",
        "description": "Provides programmatic access to Binance's exchange platform, allowing you to trade cryptocurrencies, manage your portfolio, and access market data.",
        "domain": "Finance, Crypto"
    },
    {
        "name": "Coinlore API",
        "description": "Provides real-time and historical cryptocurrency data, including prices, market capitalization, and trading volume.",
        "domain": "Finance, Crypto"
    }
]

def setup_embeddings():
    embedding_service = EmbeddingService()
    embedding_service.add_entities(api_data, "api")
    
if __name__ == "__main__":
    setup_embeddings()