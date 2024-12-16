apis_schema= [
    {
    "type": "function",
    "function": {
        "name": "statista_api_call",
        "description": "Executes a single API call to Statista based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A descriptive string representing the specific request or action for the Statista API, including dataset ID, report type, date range, etc."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "github_search_api_call",
        "description": "Executes a search call on GitHub API based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the search criteria for GitHub API, such as keywords, repositories, or users."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "news_api",
        "description": "Fetches top headlines from the News API based on the provided search query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query string used to filter headlines from the News API."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "hunter_email_api",
        "description": "Searches for email addresses or finds specific email addresses using the Hunter API.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A query string to search for email addresses by domain or to find a specific email with a domain, first name, and last name."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "hubspot_api",
        "description": "Interacts with the HubSpot CRM API to perform operations based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the HubSpot CRM API, such as requests for contact or company information."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "quickbook_api",
        "description": "Interacts with the QuickBooks API to perform operations based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the QuickBooks API."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "slack_api",
        "description": "Interacts with the Slack API to perform operations based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the Slack API, including commands for messages or retrieving details."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "ecb_exchange_rates_api",
        "description": "Interacts with the ECB Exchange Rates API to perform operations based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the ECB Exchange Rates API."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "guardian_media_api",
        "description": "Interacts with the Guardian Media API to perform operations based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A query string representing terms, filters, or parameters to retrieve content from the Guardian Media API."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "binance_api",
        "description": "Interacts with the Binance API to perform operations based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the Binance API."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "cdc_api",
        "description": "Interacts with the CDC API to perform operations based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the CDC API."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "free_forex_api",
        "description": "Interacts with the Free Forex API to perform operations based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the Free Forex API."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "health_care_api",
        "description": "Interacts with the HealthCare.gov API to perform operations based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the HealthCare.gov API."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "human_api",
        "description": "Interacts with the Human API to perform operations based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the Human API."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "open_fda_api",
        "description": "Interacts with the OpenFDA API to perform operations based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the OpenFDA API."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "crunchbase_api",
        "description": "Interacts with the Crunchbase API to perform operations based on the provided query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the Crunchbase API."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "trello_api",
        "description": "Interacts with the Trello API to perform operations based on the provided query, allowing for board, list, and card management.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the Trello API, including commands for managing boards, lists, and cards."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "hackernews_api",
        "description": "Interacts with the Hacker News API to perform operations based on the provided query, allowing for fetching of stories, comments, jobs, or user profiles.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the Hacker News API, including commands for fetching stories, comments, jobs, or user profiles."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "crypto_compare_api",
        "description": "Interacts with the CryptoCompare API to perform operations based on the provided query, allowing for retrieval of cryptocurrency prices, historical data, and other supported operations.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "A string representing the query to execute against the CryptoCompare API, including commands for fetching prices, historical data, or other supported operations."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
}
]



endpoints_schema = {
    "crunchbase_api": [
        {
    "type": "function",
    "function": {
        "name": "search_locations",
        "description": "Search for locations in Crunchbase based on provided query parameters.",
        "parameters": {
            "type": "object",
            "properties": {
                "field_ids": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of field IDs to include in the search results."
                },
                "limit": {
                    "type": "integer",
                    "description": "The maximum number of results to return.",
                    "default": 100
                },
                "after_id": {
                    "type": ["string", "null"],
                    "description": "Cursor for pagination to retrieve results after a specific ID."
                },
                "before_id": {
                    "type": ["string", "null"],
                    "description": "Cursor for pagination to retrieve results before a specific ID."
                },
                "order": {
                    "type": ["array", "null"],
                    "items": {
                        "type": "object",
                        "properties": {
                            "field_id": {
                                "type": "string",
                                "description": "Field to order by."
                            },
                            "sort": {
                                "type": "string",
                                "enum": ["asc", "desc"],
                                "description": "Sort direction: ascending (asc) or descending (desc)."
                            }
                        },
                        "required": ["field_id", "sort"]
                    },
                    "description": "List of order conditions for sorting the results."
                },
                "query": {
                    "type": ["array", "null"],
                    "items": {
                        "type": "object",
                        "properties": {
                            "field_id": {
                                "type": "string",
                                "description": "Field ID to query on."
                            },
                            "operator_id": {
                                "type": "string",
                                "description": "Operator to use in the query."
                            },
                            "value": {
                                "type": "string",
                                "description": "Value to query for the given field."
                            }
                        },
                        "required": ["field_id", "operator_id", "value"]
                    },
                    "description": "List of query filters for narrowing search results."
                }
            },
            "required": ["field_ids"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "search_organizations",
        "description": "Search for organizations in Crunchbase based on location and name criteria.",
        "parameters": {
            "type": "object",
            "properties": {
                "location_type": {
                    "type": ["string", "null"],
                    "enum": ["city", "region", "country", "continent", "group"],
                    "description": "Type of location to search by."
                },
                "location_name": {
                    "type": ["string", "null"],
                    "description": "The name of the location to filter organizations by."
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
}
    ],
    
    "hubspot_api": [
    {
    "type": "function",
    "function": {
        "name": "get_contacts",
        "description": "Fetches all contacts from HubSpot CRM.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "create_contact",
        "description": "Creates a new contact in HubSpot CRM.",
        "parameters": {
            "type": "object",
            "properties": {
                "first_name": {
                    "type": "string",
                    "description": "The first name of the contact."
                },
                "last_name": {
                    "type": "string",
                    "description": "The last name of the contact."
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "description": "The email address of the contact."
                }
            },
            "required": ["first_name", "last_name", "email"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "update_contact",
        "description": "Updates an existing contact in HubSpot CRM by contact ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "contact_id": {
                    "type": "string",
                    "description": "The ID of the contact to update."
                },
                "updated_data": {
                    "type": "object",
                    "description": "A dictionary of the properties to update.",
                    "additionalProperties": {
                        "type": "string"
                    }
                }
            },
            "required": ["contact_id", "updated_data"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "delete_contact",
        "description": "Deletes a contact from HubSpot CRM by contact ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "contact_id": {
                    "type": "string",
                    "description": "The ID of the contact to delete."
                }
            },
            "required": ["contact_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_companies",
        "description": "Fetches all companies from HubSpot CRM.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "create_company",
        "description": "Creates a new company in HubSpot CRM.",
        "parameters": {
            "type": "object",
            "properties": {
                "company_name": {
                    "type": "string",
                    "description": "The name of the company."
                },
                "domain": {
                    "type": "string",
                    "description": "The domain of the company."
                }
            },
            "required": ["company_name", "domain"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "update_company",
        "description": "Updates an existing company in HubSpot CRM by company ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "company_id": {
                    "type": "string",
                    "description": "The ID of the company to update."
                },
                "updated_data": {
                    "type": "object",
                    "description": "A dictionary of the properties to update.",
                    "additionalProperties": {
                        "type": "string"
                    }
                }
            },
            "required": ["company_id", "updated_data"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "delete_company",
        "description": "Deletes a company from HubSpot CRM by company ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "company_id": {
                    "type": "string",
                    "description": "The ID of the company to delete."
                }
            },
            "required": ["company_id"],
            "additionalProperties": False
        }
    }
},
    ],
    
    "news_api": [
        {
    "type": "function",
    "function": {
        "name": "get_top_headlines",
        "description": "Fetches the top headlines from the News API based on specified parameters such as country, category, and keywords.",
        "parameters": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "description": "The country code (e.g., 'us') to filter the headlines."
                },
                "category": {
                    "type": "string",
                    "description": "The category of news (e.g., 'technology')."
                },
                "sources": {
                    "type": "string",
                    "description": "Comma-separated string of sources to filter the articles."
                },
                "q": {
                    "type": "string",
                    "description": "A keyword or phrase to search for in the articles."
                },
                "pageSize": {
                    "type": "integer",
                    "description": "The number of articles to return per page (default is 20).",
                    "default": 20
                },
                "page": {
                    "type": "integer",
                    "description": "The page number to retrieve (default is 1).",
                    "default": 1
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
}

    ],
    
    "statista_api_call": [
        {
    "type": "function",
    "function": {
        "name": "get_statistics",
        "description": "Retrieve statistics from the Statista API based on various query parameters.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "ID of a single statistic."
                },
                "query": {
                    "type": "string",
                    "description": "Search query to filter statistics."
                },
                "limit": {
                    "type": "integer",
                    "default": 20,
                    "description": "Maximum number of items to return."
                },
                "platform": {
                    "type": "string",
                    "enum": ["de", "en", "fr", "es"],
                    "description": "Platform to retrieve items from."
                },
                "date_from": {
                    "type": "string",
                    "format": "date",
                    "description": "Earliest publication date in YYYY-MM-DD format."
                },
                "date_to": {
                    "type": "string",
                    "format": "date",
                    "description": "Latest publication date in YYYY-MM-DD format."
                },
                "premium": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "1 for premium only, 0 for free only."
                },
                "industry": {
                    "type": "integer",
                    "description": "Industry ID to filter by."
                },
                "geolocation": {
                    "type": "integer",
                    "description": "Geolocation ID to filter by."
                },
                "sort": {
                    "type": "integer",
                    "enum": [0, 1, 2],
                    "description": "Sort by relevance (0), date (1), or popularity (2)."
                },
                "page": {
                    "type": "integer",
                    "default": 1,
                    "description": "Pagination page number."
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_statistics_by_id",
        "description": "Retrieve a specific statistic from the Statista API by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "stat_id": {
                    "type": "integer",
                    "description": "ID of the statistic to retrieve."
                }
            },
            "required": ["stat_id"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_infographics",
        "description": "Retrieve infographics from the Statista API based on query parameters.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "ID of a single infographic."
                },
                "query": {
                    "type": "string",
                    "description": "Search query to filter infographics."
                },
                "limit": {
                    "type": "integer",
                    "default": 20,
                    "description": "Maximum number of items to return."
                },
                "platform": {
                    "type": "string",
                    "enum": ["de", "en", "fr", "es"],
                    "description": "Platform to retrieve items from."
                },
                "date_from": {
                    "type": "string",
                    "format": "date",
                    "description": "Earliest publication date in YYYY-MM-DD format."
                },
                "date_to": {
                    "type": "string",
                    "format": "date",
                    "description": "Latest publication date in YYYY-MM-DD format."
                },
                "premium": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "1 for premium only, 0 for free only."
                },
                "industry": {
                    "type": "integer",
                    "description": "Industry ID to filter by."
                },
                "geolocation": {
                    "type": "integer",
                    "description": "Geolocation ID to filter by."
                },
                "sort": {
                    "type": "integer",
                    "enum": [0, 1, 2],
                    "description": "Sort by relevance (0), date (1), or popularity (2)."
                },
                "page": {
                    "type": "integer",
                    "default": 1,
                    "description": "Pagination page number."
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_infographic_by_id",
        "description": "Retrieve a specific infographic by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "ID of the infographic to retrieve."
                }
            },
            "required": ["id"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_studies",
        "description": "Retrieve studies from the Statista API based on query parameters.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "ID of a single study."
                },
                "query": {
                    "type": "string",
                    "description": "Search query to filter studies."
                },
                "limit": {
                    "type": "integer",
                    "default": 20,
                    "description": "Maximum number of items to return."
                },
                "platform": {
                    "type": "string",
                    "enum": ["de", "en", "fr", "es"],
                    "description": "Platform to retrieve items from."
                },
                "date_from": {
                    "type": "string",
                    "format": "date",
                    "description": "Earliest publication date in YYYY-MM-DD format."
                },
                "date_to": {
                    "type": "string",
                    "format": "date",
                    "description": "Latest publication date in YYYY-MM-DD format."
                },
                "premium": {
                    "type": "integer",
                    "enum": [0, 1],
                    "description": "1 for premium only, 0 for free only."
                },
                "industry": {
                    "type": "integer",
                    "description": "Industry ID to filter by."
                },
                "geolocation": {
                    "type": "integer",
                    "description": "Geolocation ID to filter by."
                },
                "sort": {
                    "type": "integer",
                    "enum": [0, 1, 2],
                    "description": "Sort by relevance (0), date (1), or popularity (2)."
                },
                "page": {
                    "type": "integer",
                    "default": 1,
                    "description": "Pagination page number."
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_study_by_id",
        "description": "Retrieve a specific study by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "ID of the study to retrieve."
                }
            },
            "required": ["id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_market_insights",
        "description": "Retrieve market insights from the Statista API based on query parameters.",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "ID of a single market insight."
                },
                "query": {
                    "type": "string",
                    "description": "Search query to filter market insights."
                },
                "limit": {
                    "type": "integer",
                    "default": 20,
                    "description": "Maximum number of items to return."
                },
                "platform": {
                    "type": "string",
                    "enum": ["de", "en", "fr", "es"],
                    "description": "Platform to retrieve items from."
                },
                "date_from": {
                    "type": "string",
                    "format": "date",
                    "description": "Earliest publication date in YYYY-MM-DD format."
                },
                "date_to": {
                    "type": "string",
                    "format": "date",
                    "description": "Latest publication date in YYYY-MM-DD format."
                },
                "geolocation": {
                    "type": "integer",
                    "description": "Geolocation ID to filter by."
                },
                "sort": {
                    "type": "integer",
                    "enum": [0, 1, 2],
                    "description": "Sort by relevance (0), date (1), or popularity (2)."
                },
                "page": {
                    "type": "integer",
                    "default": 1,
                    "description": "Pagination page number."
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
}
    ],
    
    "crypto_compare_api": [
        {
    "type": "function",
    "function": {
        "name": "get_price",
        "description": "Get the current price of a cryptocurrency in specific target currencies.",
        "parameters": {
            "type": "object",
            "properties": {
                "fsym": {
                    "type": "string",
                    "description": "The cryptocurrency symbol (e.g., BTC)."
                },
                "tsyms": {
                    "type": "string",
                    "description": "Comma-separated list of target currency symbols (e.g., USD, EUR)."
                }
            },
            "required": ["fsym", "tsyms"],
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_historical_data",
        "description": "Get historical price data for a cryptocurrency.",
        "parameters": {
            "type": "object",
            "properties": {
                "fsym": {
                    "type": "string",
                    "description": "The cryptocurrency symbol (e.g., BTC)."
                },
                "tsym": {
                    "type": "string",
                    "description": "The target currency symbol (e.g., USD)."
                },
                "endpoint": {
                    "type": "string",
                    "description": "The type of historical data (e.g., histominute, histohour, histoday)."
                },
                "limit": {
                    "type": "integer",
                    "description": "The number of data points to retrieve.",
                    "default": 30
                },
                "aggregate": {
                    "type": "integer",
                    "description": "The aggregation interval (e.g., minutes, hours, days).",
                    "default": 1
                }
            },
            "required": ["fsym", "tsym", "endpoint"],
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_minute_data",
        "description": "Get historical minute-level data for a cryptocurrency.",
        "parameters": {
            "type": "object",
            "properties": {
                "fsym": {
                    "type": "string",
                    "description": "The cryptocurrency symbol (e.g., BTC)."
                },
                "tsym": {
                    "type": "string",
                    "description": "The target currency symbol (e.g., USD)."
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of data points to retrieve.",
                    "default": 30
                },
                "aggregate": {
                    "type": "integer",
                    "description": "Aggregation interval in minutes.",
                    "default": 1
                }
            },
            "required": ["fsym", "tsym"],
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_hourly_data",
        "description": "Get historical hourly data for a cryptocurrency.",
        "parameters": {
            "type": "object",
            "properties": {
                "fsym": {
                    "type": "string",
                    "description": "The cryptocurrency symbol (e.g., BTC)."
                },
                "tsym": {
                    "type": "string",
                    "description": "The target currency symbol (e.g., USD)."
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of data points to retrieve.",
                    "default": 30
                },
                "aggregate": {
                    "type": "integer",
                    "description": "Aggregation interval in hours.",
                    "default": 1
                }
            },
            "required": ["fsym", "tsym"],
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_daily_data",
        "description": "Get historical daily data for a cryptocurrency.",
        "parameters": {
            "type": "object",
            "properties": {
                "fsym": {
                    "type": "string",
                    "description": "The cryptocurrency symbol (e.g., BTC)."
                },
                "tsym": {
                    "type": "string",
                    "description": "The target currency symbol (e.g., USD)."
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of data points to retrieve.",
                    "default": 30
                },
                "aggregate": {
                    "type": "integer",
                    "description": "Aggregation interval in days.",
                    "default": 1
                }
            },
            "required": ["fsym", "tsym"],
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_top_by_volume",
        "description": "Get top cryptocurrencies by total volume.",
        "parameters": {
            "type": "object",
            "properties": {
                "tsym": {
                    "type": "string",
                    "description": "The target currency symbol (e.g., USD)."
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of top coins to retrieve.",
                    "default": 10
                }
            },
            "required": ["tsym"],
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_coin_snapshot",
        "description": "Get a snapshot for a specific cryptocurrency.",
        "parameters": {
            "type": "object",
            "properties": {
                "fsym": {
                    "type": "string",
                    "description": "The cryptocurrency symbol (e.g., BTC)."
                },
                "tsym": {
                    "type": "string",
                    "description": "The target currency symbol (e.g., USD)."
                }
            },
            "required": ["fsym", "tsym"],
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_latest_social_stats",
        "description": "Get latest social statistics for a cryptocurrency.",
        "parameters": {
            "type": "object",
            "properties": {
                "coin_id": {
                    "type": "string",
                    "description": "The cryptocurrency ID."
                }
            },
            "required": ["coin_id"],
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_historical_day_social_stats",
        "description": "Get historical daily social statistics for a cryptocurrency.",
        "parameters": {
            "type": "object",
            "properties": {
                "coin_id": {
                    "type": "string",
                    "description": "The cryptocurrency ID."
                },
                "timestamp": {
                    "type": "integer",
                    "description": "The specific day's timestamp in Unix format."
                }
            },
            "required": ["coin_id", "timestamp"],
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_historical_hour_social_stats",
        "description": "Get historical hourly social statistics for a cryptocurrency.",
        "parameters": {
            "type": "object",
            "properties": {
                "coin_id": {
                    "type": "string",
                    "description": "The cryptocurrency ID."
                },
                "timestamp": {
                    "type": "integer",
                    "description": "The specific hour's timestamp in Unix format."
                }
            },
            "required": ["coin_id", "timestamp"],
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_coin_list",
        "description": "Retrieve the complete list of cryptocurrencies.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_news",
        "description": "Retrieve latest news articles on cryptocurrencies.",
        "parameters": {
            "type": "object",
            "properties": {
                "lang": {
                    "type": "string",
                    "description": "The language for the news articles.",
                    "default": "EN"
                }
            },
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_feeds",
        "description": "Retrieve cryptocurrency news feeds.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_categories",
        "description": "Retrieve cryptocurrency news categories.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_feeds_and_categories",
        "description": "Retrieve cryptocurrency news feeds and categories.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_asset_by_symbol",
        "description": "Retrieve the asset information by cryptocurrency symbol.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The cryptocurrency symbol (e.g., BTC)."
                }
            },
            "required": ["symbol"],
            "additionalProperties": False
        }
    }
}
    ],
"open_fda_api": [
    {
    "type": "function",
    "function": {
        "name": "get_drugs",
        "description": "Fetch drug information from the OpenFDA API.",
        "parameters": {
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "description": "Optional query parameters for the drug information request.",
                    "properties": {
                        "search": {
                            "type": "string",
                            "description": "Query to search specific drug information (e.g., active ingredient, brand name)."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of records to retrieve.",
                            "default": 10
                        },
                        "skip": {
                            "type": "integer",
                            "description": "Number of records to skip before retrieving results.",
                            "default": 0
                        }
                    },
                    "additionalProperties": True
                }
            },
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_devices",
        "description": "Fetch medical device information from the OpenFDA API.",
        "parameters": {
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "description": "Optional query parameters for the device information request.",
                    "properties": {
                        "search": {
                            "type": "string",
                            "description": "Query to search specific device information (e.g., device name, manufacturer name)."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of records to retrieve.",
                            "default": 10
                        },
                        "skip": {
                            "type": "integer",
                            "description": "Number of records to skip before retrieving results.",
                            "default": 0
                        }
                    },
                    "additionalProperties": True
                }
            },
            "additionalProperties": False
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_foods",
        "description": "Fetch food information from the OpenFDA API.",
        "parameters": {
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "description": "Optional query parameters for the food information request.",
                    "properties": {
                        "search": {
                            "type": "string",
                            "description": "Query to search specific food information (e.g., product description, company name)."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of records to retrieve.",
                            "default": 10
                        },
                        "skip": {
                            "type": "integer",
                            "description": "Number of records to skip before retrieving results.",
                            "default": 0
                        }
                    },
                    "additionalProperties": True
                }
            },
            "additionalProperties": False
        }
    }
}

],

"hunter_api": [
  {
    "type": "function",
    "function": {
        "name": "domain_search",
        "description": "Search for email addresses associated with the specified domain using Hunter.io.",
        "parameters": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "The domain to search for email addresses, e.g., 'example.com'."
                }
            },
            "required": ["domain"],
            "additionalProperties": False
        }
    }
},
  {
    "type": "function",
    "function": {
        "name": "email_finder",
        "description": "Find an email address given a domain and a person's first and last name using Hunter.io.",
        "parameters": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "description": "The domain to search for the email address, e.g., 'example.com'."
                },
                "first_name": {
                    "type": "string",
                    "description": "The first name of the person to find the email for."
                },
                "last_name": {
                    "type": "string",
                    "description": "The last name of the person to find the email for."
                }
            },
            "required": ["domain", "first_name", "last_name"],
            "additionalProperties": False
        }
    }
},
  

  
],
"guardian_media_api": [
    {
    "type": "function",
    "function": {
        "name": "get_sections",
        "description": "Retrieve the list of sections from the Guardian API. Call this to get sections based on an optional query term.",
        "parameters": {
            "type": "object",
            "properties": {
                "q": {
                    "type": "string",
                    "description": "Return sections based on the specified query term."
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "search_articles",
        "description": "Search for articles on the Guardian API. Use this to find articles by query, pagination, and sorting options.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query for finding articles."
                },
                "page": {
                    "type": "integer",
                    "description": "The page number to retrieve. Default is 1."
                },
                "page_size": {
                    "type": "integer",
                    "description": "The number of results per page. Default is 10."
                },
                "order_by": {
                    "type": "string",
                    "enum": ["newest", "oldest", "relevance"],
                    "description": "The order in which to sort results."
                },
                "use_date": {
                    "type": "string",
                    "enum": ["published", "newspaper-edition"],
                    "description": "The date type to filter results by."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_article",
        "description": "Retrieve a specific article by its ID from the Guardian API.",
        "parameters": {
            "type": "object",
            "properties": {
                "article_id": {
                    "type": "string",
                    "description": "The ID of the article to retrieve."
                }
            },
            "required": ["article_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_latest_headlines",
        "description": "Retrieve the latest headlines from the Guardian API, with optional filtering by section and pagination options.",
        "parameters": {
            "type": "object",
            "properties": {
                "section": {
                    "type": "string",
                    "description": "The section to filter results by. Optional."
                },
                "page": {
                    "type": "integer",
                    "description": "The page number to retrieve. Default is 1."
                },
                "page_size": {
                    "type": "integer",
                    "description": "The number of results per page. Default is 10."
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_tags",
        "description": "Retrieve a list of tags from the Guardian API based on a query.",
        "parameters": {
            "type": "object",
            "properties": {
                "q": {
                    "type": "string",
                    "description": "Request tags containing this free text."
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
    
],

"free_forex_api": [
    {
    "type": "function",
    "function": {
        "name": "get_exchange_rates",
        "description": "Fetches real-time exchange rates for specified currencies with respect to a source currency using the FreeForexAPI.",
        "parameters": {
            "type": "object",
            "properties": {
                "currencies": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "A currency pair code, like 'USDGBP' for USD to GBP conversion."
                    },
                    "description": "A list of currency pairs to fetch exchange rates for."
                },
                "source": {
                    "type": "string",
                    "description": "The source currency for the exchange rates, defaulting to 'USD'."
                }
            },
            "required": ["currencies"],
            "additionalProperties": False
        }
    }
},

],

"human_api": [
    {
    "type": "function",
    "function": {
        "name": "get_user_profile",
        "description": "Fetch the user's profile data from Human API. This includes basic user information.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_fitness_data",
        "description": "Fetch aggregated fitness data from various sources via Human API. This may include steps, activity, calories burned, etc.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_health_data",
        "description": "Fetch aggregated health data from Human API, including Electronic Health Records (EHR) data.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
],

"trello_api": [
    {
    "type": "function",
    "function": {
        "name": "get_boards",
        "description": "Fetch all boards for the authenticated Trello user.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_board",
        "description": "Fetch details of a specific board by ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "board_id": {
                    "type": "string",
                    "description": "The ID of the board to fetch."
                }
            },
            "required": ["board_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "update_board",
        "description": "Update the name of a specific board.",
        "parameters": {
            "type": "object",
            "properties": {
                "board_id": {
                    "type": "string",
                    "description": "The ID of the board to update."
                },
                "name": {
                    "type": "string",
                    "description": "The new name for the board."
                }
            },
            "required": ["board_id", "name"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "delete_board",
        "description": "Delete a specific board by ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "board_id": {
                    "type": "string",
                    "description": "The ID of the board to delete."
                }
            },
            "required": ["board_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "create_list",
        "description": "Create a new list in a specific board.",
        "parameters": {
            "type": "object",
            "properties": {
                "board_id": {
                    "type": "string",
                    "description": "The ID of the board where the list will be created."
                },
                "name": {
                    "type": "string",
                    "description": "The name of the new list."
                }
            },
            "required": ["board_id", "name"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_lists",
        "description": "Fetch all lists in a specific board.",
        "parameters": {
            "type": "object",
            "properties": {
                "board_id": {
                    "type": "string",
                    "description": "The ID of the board whose lists will be fetched."
                }
            },
            "required": ["board_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_list",
        "description": "Fetch details of a specific list by ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "list_id": {
                    "type": "string",
                    "description": "The ID of the list to fetch."
                }
            },
            "required": ["list_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "update_list",
        "description": "Update the name of a specific list by ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "list_id": {
                    "type": "string",
                    "description": "The ID of the list to update."
                },
                "name": {
                    "type": "string",
                    "description": "The new name for the list."
                }
            },
            "required": ["list_id", "name"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "delete_list",
        "description": "Delete a specific list by ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "list_id": {
                    "type": "string",
                    "description": "The ID of the list to delete."
                }
            },
            "required": ["list_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "create_card",
        "description": "Create a new card in a specific list.",
        "parameters": {
            "type": "object",
            "properties": {
                "list_id": {
                    "type": "string",
                    "description": "The ID of the list where the card will be created."
                },
                "name": {
                    "type": "string",
                    "description": "The name of the new card."
                },
                "desc": {
                    "type": "string",
                    "description": "The description of the card.",
                    "default": ""
                }
            },
            "required": ["list_id", "name"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_card",
        "description": "Fetch details of a specific card by ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "card_id": {
                    "type": "string",
                    "description": "The ID of the card to fetch."
                }
            },
            "required": ["card_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "update_card",
        "description": "Update the name of a specific card.",
        "parameters": {
            "type": "object",
            "properties": {
                "card_id": {
                    "type": "string",
                    "description": "The ID of the card to update."
                },
                "name": {
                    "type": "string",
                    "description": "The new name for the card."
                }
            },
            "required": ["card_id", "name"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "delete_card",
        "description": "Delete a specific card by ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "card_id": {
                    "type": "string",
                    "description": "The ID of the card to delete."
                }
            },
            "required": ["card_id"],
            "additionalProperties": False
        }
    }
},
    
],

"health_care_api": [
    {
    "type": "function",
    "function": {
        "name": "get_content_object",
        "description": "Fetch a single content object by post title.",
        "parameters": {
            "type": "object",
            "properties": {
                "post_title": {
                    "type": "string",
                    "description": "The title of the post (slug) to fetch."
                }
            },
            "required": ["post_title"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_content_collection",
        "description": "Fetch a collection of content objects by type.",
        "parameters": {
            "type": "object",
            "properties": {
                "content_type": {
                    "type": "string",
                    "description": "The type of content to fetch (e.g., 'articles', 'glossary')."
                }
            },
            "required": ["content_type"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_content_index",
        "description": "Fetch the content index.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    
],

"here_api": [
    {
    "type": "function",
    "function": {
        "name": "geocode_location",
        "description": "Geocodes a location name to get latitude and longitude.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location name to geocode."
                }
            },
            "required": ["location"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "reverse_geocode",
        "description": "Reverse geocodes latitude and longitude to get an address.",
        "parameters": {
            "type": "object",
            "properties": {
                "lat": {
                    "type": "number",
                    "description": "The latitude of the location."
                },
                "lng": {
                    "type": "number",
                    "description": "The longitude of the location."
                }
            },
            "required": ["lat", "lng"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "search_nearby",
        "description": "Searches for nearby places based on a query.",
        "parameters": {
            "type": "object",
            "properties": {
                "lat": {
                    "type": "number",
                    "description": "The latitude of the search area."
                },
                "lng": {
                    "type": "number",
                    "description": "The longitude of the search area."
                },
                "query": {
                    "type": "string",
                    "description": "The search query for nearby places."
                }
            },
            "required": ["lat", "lng", "query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_autosuggest",
        "description": "Provides autosuggestions for places based on partial input.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query for autosuggestions."
                },
                "lat": {
                    "type": "number",
                    "description": "The latitude for context-based suggestions.",
                    "nullable": True
                },
                "lng": {
                    "type": "number",
                    "description": "The longitude for context-based suggestions.",
                    "nullable": True
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_discover",
        "description": "Discovers places around a given location using a keyword or category.",
        "parameters": {
            "type": "object",
            "properties": {
                "lat": {
                    "type": "number",
                    "description": "The latitude of the discovery area."
                },
                "lng": {
                    "type": "number",
                    "description": "The longitude of the discovery area."
                },
                "query": {
                    "type": "string",
                    "description": "The discovery query, such as a keyword or category."
                }
            },
            "required": ["lat", "lng", "query"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_routes",
        "description": "Provides routes between two locations.",
        "parameters": {
            "type": "object",
            "properties": {
                "origin_lat": {
                    "type": "number",
                    "description": "The latitude of the origin location."
                },
                "origin_lng": {
                    "type": "number",
                    "description": "The longitude of the origin location."
                },
                "destination_lat": {
                    "type": "number",
                    "description": "The latitude of the destination location."
                },
                "destination_lng": {
                    "type": "number",
                    "description": "The longitude of the destination location."
                },
                "transport_mode": {
                    "type": "string",
                    "description": "The mode of transport (e.g., 'car', 'pedestrian').",
                    "default": "car"
                }
            },
            "required": ["origin_lat", "origin_lng", "destination_lat", "destination_lng"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Provides current weather information for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "lat": {
                    "type": "number",
                    "description": "The latitude of the location."
                },
                "lng": {
                    "type": "number",
                    "description": "The longitude of the location."
                }
            },
            "required": ["lat", "lng"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_traffic_flow",
        "description": "Provides real-time traffic flow information for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "lat": {
                    "type": "number",
                    "description": "The latitude of the location."
                },
                "lng": {
                    "type": "number",
                    "description": "The longitude of the location."
                }
            },
            "required": ["lat", "lng"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_traffic_incidents",
        "description": "Provides real-time traffic incidents within a bounding box.",
        "parameters": {
            "type": "object",
            "properties": {
                "bbox": {
                    "type": "string",
                    "description": "The bounding box for traffic incidents (north,south,east,west)."
                }
            },
            "required": ["bbox"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_position",
        "description": "Provides positioning services using device sensors like Wi-Fi, cell towers, and GPS.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    
],

"cdc_api": [
    {
    "type": "function",
    "function": {
        "name": "get_open_data",
        "description": "Fetch open data from the CDC Open Data API.",
        "parameters": {
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "description": "Additional query parameters for the CDC Open Data API.",
                    "properties": {},
                    "additionalProperties": True
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_phin_vads",
        "description": "Fetch standard vocabularies from the PHIN VADS API.",
        "parameters": {
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "description": "Additional query parameters for the PHIN VADS API.",
                    "properties": {},
                    "additionalProperties": True
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_wonder_data",
        "description": "Access data from the WONDER API using the specified database ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "database_id": {
                    "type": "string",
                    "description": "The ID of the database to query in the WONDER API."
                }
            },
            "required": ["database_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_content_syndication",
        "description": "Fetch content syndication data from the CDC Content Syndication API.",
        "parameters": {
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "description": "Additional query parameters for the CDC Content Syndication API.",
                    "properties": {},
                    "additionalProperties": True
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_tracking_network_data",
        "description": "Fetch data from the Environmental Public Health Tracking Network API.",
        "parameters": {
            "type": "object",
            "properties": {
                "params": {
                    "type": "object",
                    "description": "Additional query parameters for the Environmental Public Health Tracking Network API.",
                    "properties": {},
                    "additionalProperties": True
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
    
],

"hackernews_api": [
    {
    "type": "function",
    "function": {
        "name": "get_item",
        "description": "Fetch a specific item by ID (story, comment, poll, etc.) from Hacker News.",
        "parameters": {
            "type": "object",
            "properties": {
                "item_id": {
                    "type": "integer",
                    "description": "The ID of the item to fetch."
                }
            },
            "required": ["item_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_user",
        "description": "Fetch a specific user by ID from Hacker News.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user to fetch."
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_max_item",
        "description": "Fetch the current largest item ID from Hacker News.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_top_stories",
        "description": "Fetch the top 500 stories on Hacker News.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_new_stories",
        "description": "Fetch the newest 500 stories on Hacker News.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_best_stories",
        "description": "Fetch the best 500 stories on Hacker News.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_ask_stories",
        "description": "Fetch the latest 200 Ask HN stories.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_show_stories",
        "description": "Fetch the latest 200 Show HN stories.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_job_stories",
        "description": "Fetch the latest 200 job stories.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_updates",
        "description": "Fetch changed items and profiles on Hacker News.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
],

"coinlore_api": [
    {
    "type": "function",
    "function": {
        "name": "get_global_data",
        "description": "Fetch global cryptocurrency statistics from Coinlore.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_tickers",
        "description": "Fetch tick data for multiple cryptocurrencies from Coinlore.",
        "parameters": {
            "type": "object",
            "properties": {
                "start": {
                    "type": "integer",
                    "description": "The starting index for the ticker data.",
                    "default": 0
                },
                "limit": {
                    "type": "integer",
                    "description": "The maximum number of tickers to return.",
                    "default": 100
                }
            },
            "required": ["start", "limit"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_ticker",
        "description": "Fetch tick data for a specific cryptocurrency by its coin ID from Coinlore.",
        "parameters": {
            "type": "object",
            "properties": {
                "coin_id": {
                    "type": "integer",
                    "description": "The ID of the cryptocurrency to fetch."
                }
            },
            "required": ["coin_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_markets_for_coin",
        "description": "Fetch top exchanges and markets for a specific cryptocurrency from Coinlore.",
        "parameters": {
            "type": "object",
            "properties": {
                "coin_id": {
                    "type": "integer",
                    "description": "The ID of the cryptocurrency to fetch market data for."
                }
            },
            "required": ["coin_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_all_exchanges",
        "description": "Fetch all exchanges listed on the Coinlore platform.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_exchange",
        "description": "Fetch specific exchange data by its ID from Coinlore.",
        "parameters": {
            "type": "object",
            "properties": {
                "exchange_id": {
                    "type": "integer",
                    "description": "The ID of the exchange to fetch."
                }
            },
            "required": ["exchange_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_social_stats",
        "description": "Fetch social stats for a specific cryptocurrency by its coin ID from Coinlore.",
        "parameters": {
            "type": "object",
            "properties": {
                "coin_id": {
                    "type": "integer",
                    "description": "The ID of the cryptocurrency to fetch social stats for."
                }
            },
            "required": ["coin_id"],
            "additionalProperties": False
        }
    }
},
],

    "binance_api": [
        {
    "type": "function",
    "function": {
        "name": "get_ticker_price",
        "description": "Fetch the latest price for a specific symbol or all symbols from Binance.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": ["string", "null"],
                    "description": "The trading pair symbol (e.g., 'BTCUSDT'). If null, returns all symbols.",
                    "default": None # changed null to none for python... might come out wrong
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_order_book",
        "description": "Fetch the order book depth for a specific symbol from Binance.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The trading pair symbol (e.g., 'BTCUSDT')."
                }
            },
            "required": ["symbol"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_recent_trades",
        "description": "Fetch recent trades for a specific symbol from Binance.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The trading pair symbol (e.g., 'BTCUSDT')."
                }
            },
            "required": ["symbol"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_historical_trades",
        "description": "Fetch older trades for a specific symbol from Binance.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The trading pair symbol (e.g., 'BTCUSDT')."
                }
            },
            "required": ["symbol"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_candlestick_data",
        "description": "Fetch candlestick data for a specific symbol and interval from Binance.",
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The trading pair symbol (e.g., 'BTCUSDT')."
                },
                "interval": {
                    "type": "string",
                    "description": "The interval for candlesticks (e.g., '1h')."
                }
            },
            "required": ["symbol", "interval"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_exchange_info",
        "description": "Fetch current exchange trading rules and symbol information from Binance.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    ],
    
    "twitter_api": [
        {
  "type": "function",
  "function": {
    "name": "search_recent_tweets",
    "description": "Search recent tweets based on a query.",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "Search query for tweets."
        },
        "max_results": {
          "type": "integer",
          "description": "Number of results to return, default is 10.",
          "default": 10
        }
      },
      "required": ["query"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "get_user_by_username",
    "description": "Retrieve user details by Twitter username.",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "Twitter username."
        }
      },
      "required": ["username"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "get_tweet_liking_users",
    "description": "Retrieve users who liked a specific tweet.",
    "parameters": {
      "type": "object",
      "properties": {
        "tweet_id": {
          "type": "string",
          "description": "ID of the tweet."
        }
      },
      "required": ["tweet_id"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "get_trending_topics",
    "description": "Retrieve trending topics for a location.",
    "parameters": {
      "type": "object",
      "properties": {
        "woeid": {
          "type": "integer",
          "description": "Location identifier (WOEID) for trending topics, default is 1 for Worldwide.",
          "default": 1
        }
      },
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "post_tweet",
    "description": "Post a tweet with specified content.",
    "parameters": {
      "type": "object",
      "properties": {
        "text": {
          "type": "string",
          "description": "Content of the tweet."
        }
      },
      "required": ["text"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "upload_media",
    "description": "Upload media to Twitter for use in tweets.",
    "parameters": {
      "type": "object",
      "properties": {
        "file_path": {
          "type": "string",
          "description": "Path to the media file (e.g., image, video)."
        }
      },
      "required": ["file_path"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "add_media_metadata",
    "description": "Add metadata to uploaded media (e.g., alt text for accessibility).",
    "parameters": {
      "type": "object",
      "properties": {
        "media_id": {
          "type": "string",
          "description": "ID of the uploaded media."
        },
        "alt_text": {
          "type": "string",
          "description": "Alt text for the media."
        }
      },
      "required": ["media_id", "alt_text"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "create_list",
    "description": "Create a new Twitter list with optional description and privacy setting.",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "Name of the list."
        },
        "description": {
          "type": "string",
          "description": "Description of the list.",
          "default": ""
        },
        "mode": {
          "type": "string",
          "description": "List mode: 'public' or 'private'.",
          "default": "private",
          "enum": ["public", "private"]
        }
      },
      "required": ["name"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "add_member_to_list",
    "description": "Add a user to a Twitter list by list ID and user ID.",
    "parameters": {
      "type": "object",
      "properties": {
        "list_id": {
          "type": "string",
          "description": "ID of the Twitter list."
        },
        "user_id": {
          "type": "string",
          "description": "ID of the user to add."
        }
      },
      "required": ["list_id", "user_id"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "get_list_members",
    "description": "Retrieve members of a Twitter list by list ID.",
    "parameters": {
      "type": "object",
      "properties": {
        "list_id": {
          "type": "string",
          "description": "ID of the Twitter list."
        }
      },
      "required": ["list_id"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "remove_member_from_list",
    "description": "Remove a user from a Twitter list by list ID and user ID.",
    "parameters": {
      "type": "object",
      "properties": {
        "list_id": {
          "type": "string",
          "description": "ID of the Twitter list."
        },
        "user_id": {
          "type": "string",
          "description": "ID of the user to remove."
        }
      },
      "required": ["list_id", "user_id"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "show_list_details",
    "description": "Retrieve details of a Twitter list by list ID.",
    "parameters": {
      "type": "object",
      "properties": {
        "list_id": {
          "type": "string",
          "description": "ID of the Twitter list."
        }
      },
      "required": ["list_id"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "get_user_lists",
    "description": "Retrieve lists owned or subscribed by the authenticated user.",
    "parameters": {
      "type": "object",
      "properties": {},
      "additionalProperties": False
    }
  }
},

    ],
    
    "reddit_api": [
        {
    "type": "function",
    "function": {
        "name": "get_info",
        "description": "Fetch detailed information on specific posts or comments.",
        "parameters": {
            "type": "object",
            "properties": {
                "ids": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "List of fullnames (e.g., 't3_postid', 't1_commentid')."
                }
            },
            "required": ["ids"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "vote",
        "description": "Vote on a post or comment.",
        "parameters": {
            "type": "object",
            "properties": {
                "thing_id": {
                    "type": "string",
                    "description": "Fullname of the item to vote on (e.g., 't3_postid')."
                },
                "direction": {
                    "type": "integer",
                    "description": "1 for upvote, -1 for downvote, 0 to remove vote.",
                    "enum": [1, -1, 0]
                }
            },
            "required": ["thing_id", "direction"],
            "additionalProperties": False
        }
    }
},
        
        {
    "type": "function",
    "function": {
        "name": "submit_post",
        "description": "Submit a new post to a subreddit.",
        "parameters": {
            "type": "object",
            "properties": {
                "subreddit": {
                    "type": "string",
                    "description": "The subreddit to post to."
                },
                "title": {
                    "type": "string",
                    "description": "Title of the post."
                },
                "selftext": {
                    "type": "string",
                    "description": "Text content of the post.",
                    "default": ""
                }
            },
            "required": ["subreddit", "title"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "search_subreddits",
        "description": "Search for subreddits matching a query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_new_posts",
        "description": "Retrieve the latest posts from a subreddit.",
        "parameters": {
            "type": "object",
            "properties": {
                "subreddit": {
                    "type": "string",
                    "description": "Subreddit name."
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of posts to retrieve.",
                    "default": 5
                }
            },
            "required": ["subreddit"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_subreddit_info",
        "description": "Retrieve details about a specific subreddit.",
        "parameters": {
            "type": "object",
            "properties": {
                "subreddit": {
                    "type": "string",
                    "description": "Subreddit name."
                }
            },
            "required": ["subreddit"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "search_content",
        "description": "Search for content across Reddit or within a specific subreddit.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query."
                },
                "subreddit": {
                    "type": "string",
                    "description": "Subreddit to search within (optional)."
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of search results to return.",
                    "default": 10
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_user_overview",
        "description": "Retrieve an overview of a user's activity (posts and comments).",
        "parameters": {
            "type": "object",
            "properties": {
                "username": {
                    "type": "string",
                    "description": "Reddit username to fetch activity for."
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of activities to return.",
                    "default": 10
                }
            },
            "required": ["username"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "send_private_message",
        "description": "Send a private message to a Reddit user.",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {
                    "type": "string",
                    "description": "Username of the recipient."
                },
                "subject": {
                    "type": "string",
                    "description": "Subject of the message."
                },
                "message": {
                    "type": "string",
                    "description": "Body of the message."
                }
            },
            "required": ["recipient", "subject", "message"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_inbox_messages",
        "description": "Retrieve private messages from the inbox.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of messages to retrieve.",
                    "default": 10
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_sent_messages",
        "description": "Retrieve sent private messages.",
        "parameters": {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of sent messages to retrieve.",
                    "default": 10
                }
            },
            "required": [],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "create_collection",
        "description": "Create a new collection in a subreddit.",
        "parameters": {
            "type": "object",
            "properties": {
                "subreddit": {
                    "type": "string",
                    "description": "The subreddit to create the collection in."
                },
                "title": {
                    "type": "string",
                    "description": "Title of the collection."
                }
            },
            "required": ["subreddit", "title"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "delete_collection",
        "description": "Delete a collection from a subreddit.",
        "parameters": {
            "type": "object",
            "properties": {
                "subreddit": {
                    "type": "string",
                    "description": "The subreddit containing the collection."
                },
                "collection_id": {
                    "type": "string",
                    "description": "ID of the collection to delete."
                }
            },
            "required": ["subreddit", "collection_id"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "reorder_collection",
        "description": "Reorder posts within a collection.",
        "parameters": {
            "type": "object",
            "properties": {
                "subreddit": {
                    "type": "string",
                    "description": "The subreddit containing the collection."
                },
                "collection_id": {
                    "type": "string",
                    "description": "ID of the collection to reorder."
                },
                "link_ids": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Post ID."
                    },
                    "description": "List of post IDs in the desired order."
                }
            },
            "required": ["subreddit", "collection_id", "link_ids"],
            "additionalProperties": False
        }
    }
},
        {
    "type": "function",
    "function": {
        "name": "get_subreddit_emojis",
        "description": "Retrieve all custom emojis from a subreddit.",
        "parameters": {
            "type": "object",
            "properties": {
                "subreddit": {
                    "type": "string",
                    "description": "Subreddit name."
                }
            },
            "required": ["subreddit"],
            "additionalProperties": False
        }
    }
},


    ],
    
    "ecb_exchange_rates_api": [
        {
  "type": "function",
  "function": {
    "name": "get_supported_symbols",
    "description": "Retrieves a list of supported currency symbols from the API.",
    "parameters": {
      "type": "object",
      "properties": {},
      "required": [],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "get_latest_rates",
    "description": "Retrieves the latest exchange rates for a given base currency.",
    "parameters": {
      "type": "object",
      "properties": {
        "base_currency": {
          "type": "string",
          "description": "The base currency to retrieve rates for. Defaults to 'EUR'."
        },
        "symbols": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "A list of currency symbols to filter the results."
        }
      },
      "required": ["base_currency"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "get_historical_rates",
    "description": "Retrieves historical exchange rates for a specified date.",
    "parameters": {
      "type": "object",
      "properties": {
        "date": {
          "type": "string",
          "description": "The date for which to retrieve exchange rates (format: YYYY-MM-DD)."
        },
        "base_currency": {
          "type": "string",
          "description": "The base currency to retrieve rates for. Defaults to 'EUR'."
        },
        "symbols": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "A list of currency symbols to filter the results."
        }
      },
      "required": ["date", "base_currency"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "convert_currency",
    "description": "Converts a specified amount from one currency to another.",
    "parameters": {
      "type": "object",
      "properties": {
        "from_currency": {
          "type": "string",
          "description": "The currency to convert from."
        },
        "to_currency": {
          "type": "string",
          "description": "The currency to convert to."
        },
        "amount": {
          "type": "number",
          "description": "The amount to convert."
        },
        "date": {
          "type": "string",
          "description": "The date for historical conversion (format: YYYY-MM-DD). If None, uses the latest rates."
        }
      },
      "required": ["from_currency", "to_currency", "amount"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "get_time_series",
    "description": "Retrieves the exchange rates time series for a specified date range.",
    "parameters": {
      "type": "object",
      "properties": {
        "start_date": {
          "type": "string",
          "description": "The start date of the time series (format: YYYY-MM-DD)."
        },
        "end_date": {
          "type": "string",
          "description": "The end date of the time series (format: YYYY-MM-DD)."
        },
        "base_currency": {
          "type": "string",
          "description": "The base currency to retrieve rates for. Defaults to 'EUR'."
        },
        "symbols": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "A list of currency symbols to filter the results."
        }
      },
      "required": ["start_date", "end_date", "base_currency"],
      "additionalProperties": False
    }
  }
},
        {
  "type": "function",
  "function": {
    "name": "get_fluctuation",
    "description": "Retrieves the fluctuation of exchange rates for a specified date range.",
    "parameters": {
      "type": "object",
      "properties": {
        "start_date": {
          "type": "string",
          "description": "The start date of the fluctuation period (format: YYYY-MM-DD)."
        },
        "end_date": {
          "type": "string",
          "description": "The end date of the fluctuation period (format: YYYY-MM-DD)."
        },
        "base_currency": {
          "type": "string",
          "description": "The base currency to retrieve rates for. Defaults to 'EUR'."
        },
        "symbols": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "A list of currency symbols to filter the results."
        }
      },
      "required": ["start_date", "end_date", "base_currency"],
      "additionalProperties": False
    }
  }
},
    ],
    
"google_console_api": [
    {
    "type": "function",
    "function": {
        "name": "get_site_info",
        "description": "Fetches site information from Google Search Console.",
        "parameters": {
            "type": "object",
            "properties": {
                "site_url": {
                    "type": "string",
                    "description": "The URL of the site to retrieve information for."
                }
            },
            "required": ["site_url"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_search_analytics",
        "description": "Retrieves search analytics data for a site.",
        "parameters": {
            "type": "object",
            "properties": {
                "site_url": {
                    "type": "string",
                    "description": "The URL of the site to retrieve search analytics for."
                },
                "start_date": {
                    "type": "string",
                    "description": "The start date for the analytics data in YYYY-MM-DD format."
                },
                "end_date": {
                    "type": "string",
                    "description": "The end date for the analytics data in YYYY-MM-DD format."
                },
                "dimensions": {
                    "type": "array",
                    "description": "Dimensions to filter the data by, such as query.",
                    "items": { "type": "string" },
                    "default": ["query"]
                }
            },
            "required": ["site_url", "start_date", "end_date"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "list_sitemaps",
        "description": "Lists all sitemaps for a site.",
        "parameters": {
            "type": "object",
            "properties": {
                "site_url": {
                    "type": "string",
                    "description": "The URL of the site to list sitemaps for."
                }
            },
            "required": ["site_url"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "submit_sitemap",
        "description": "Submits a sitemap to Google Search Console.",
        "parameters": {
            "type": "object",
            "properties": {
                "site_url": {
                    "type": "string",
                    "description": "The URL of the site to submit the sitemap for."
                },
                "sitemap_url": {
                    "type": "string",
                    "description": "The URL of the sitemap to submit."
                }
            },
            "required": ["site_url", "sitemap_url"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "inspect_url",
        "description": "Inspects a URL using the URL Inspection API.",
        "parameters": {
            "type": "object",
            "properties": {
                "site_url": {
                    "type": "string",
                    "description": "The URL of the site containing the URL to inspect."
                },
                "url": {
                    "type": "string",
                    "description": "The URL to inspect."
                }
            },
            "required": ["site_url", "url"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "list_crawl_errors",
        "description": "Lists crawl errors for a site.",
        "parameters": {
            "type": "object",
            "properties": {
                "site_url": {
                    "type": "string",
                    "description": "The URL of the site to list crawl errors for."
                }
            },
            "required": ["site_url"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "get_mobile_usability",
        "description": "Fetches mobile usability data for a site.",
        "parameters": {
            "type": "object",
            "properties": {
                "site_url": {
                    "type": "string",
                    "description": "The URL of the site to fetch mobile usability data for."
                }
            },
            "required": ["site_url"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "transcribe_audio",
        "description": "Transcribes audio from a file using Google Speech-to-Text.",
        "parameters": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "string",
                    "description": "The audio file data to be transcribed, in binary format."
                },
                "language_code": {
                    "type": "string",
                    "description": "The language code for the transcription, e.g., 'en-US'.",
                    "default": "en-US"
                }
            },
            "required": ["file"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "transcribe_streaming",
        "description": "Performs streaming transcription of audio data.",
        "parameters": {
            "type": "object",
            "properties": {
                "audio_stream": {
                    "type": "string",
                    "description": "The audio stream data to be transcribed, in binary format."
                },
                "language_code": {
                    "type": "string",
                    "description": "The language code for the transcription, e.g., 'en-US'.",
                    "default": "en-US"
                }
            },
            "required": ["audio_stream"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "synthesize_text",
        "description": "Synthesizes speech from text using Google Text-to-Speech.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to be synthesized into speech."
                },
                "language_code": {
                    "type": "string",
                    "description": "The language code for the synthesized speech, e.g., 'en-US'.",
                    "default": "en-US"
                },
                "voice_type": {
                    "type": "string",
                    "description": "The voice type for synthesis, e.g., 'NEUTRAL', 'FEMALE', 'MALE'.",
                    "default": "NEUTRAL"
                },
                "audio_format": {
                    "type": "string",
                    "description": "The audio format for the synthesized output, e.g., 'MP3'.",
                    "default": "MP3"
                }
            },
            "required": ["text"],
            "additionalProperties": False
        }
    }
},
],

"pintrest_client_api": [
    {
    "type": "function",
    "function": {
        "name": "get_user_info",
        "description": "Retrieves information about the authenticated user.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_user_boards",
        "description": "Fetches the authenticated user's boards.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "create_pin",
        "description": "Creates a pin on a specific board.",
        "parameters": {
            "type": "object",
            "properties": {
                "board_id": {
                    "type": "string",
                    "description": "The ID of the board to create the pin on."
                },
                "note": {
                    "type": "string",
                    "description": "The description of the pin."
                },
                "link": {
                    "type": "string",
                    "description": "The URL link to associate with the pin.",
                    "nullable": True
                },
                "image_url": {
                    "type": "string",
                    "description": "The image URL for the pin.",
                    "nullable": True
                }
            },
            "required": ["board_id", "note"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_board_pins",
        "description": "Retrieves all pins from a specific board.",
        "parameters": {
            "type": "object",
            "properties": {
                "board_id": {
                    "type": "string",
                    "description": "The ID of the board to retrieve pins from."
                }
            },
            "required": ["board_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_analytics",
        "description": "Retrieves analytics for the user's pins.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "upload_media",
        "description": "Uploads a media file to Pinterest.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path of the media file to upload."
                }
            },
            "required": ["file_path"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "get_media_info",
        "description": "Retrieves information about an uploaded media file.",
        "parameters": {
            "type": "object",
            "properties": {
                "media_id": {
                    "type": "string",
                    "description": "The ID of the media file to retrieve information for."
                }
            },
            "required": ["media_id"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "get_user_following_boards",
        "description": "Retrieves the boards the authenticated user is following.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "get_user_following_users",
        "description": "Retrieves the users the authenticated user is following.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "follow_board",
        "description": "Follows a specific board.",
        "parameters": {
            "type": "object",
            "properties": {
                "board_id": {
                    "type": "string",
                    "description": "The ID of the board to follow."
                }
            },
            "required": ["board_id"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "unfollow_board",
        "description": "Unfollows a specific board.",
        "parameters": {
            "type": "object",
            "properties": {
                "board_id": {
                    "type": "string",
                    "description": "The ID of the board to unfollow."
                }
            },
            "required": ["board_id"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "follow_user",
        "description": "Follows a specific user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user to follow."
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "unfollow_user",
        "description": "Unfollows a specific user.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The ID of the user to unfollow."
                }
            },
            "required": ["user_id"],
            "additionalProperties": False
        }
    }
},
   {
    "type": "function",
    "function": {
        "name": "search_pins",
        "description": "Searches for pins based on a query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query string to search pins."
                }
            },
            "required": ["query"],
            "additionalProperties": False
        }
    }
},
],

"slack_api": [
  {
    "type": "function",
    "function": {
      "name": "notify_team",
      "description": "Notify the team by sending a message to the default Slack channel.",
      "parameters": {
        "type": "object",
        "properties": {
          "message": {
            "type": "string",
            "description": "The message text to send."
          }
        },
        "required": ["message"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "get_member_info",
      "description": "Get information about a Slack team member.",
      "parameters": {
        "type": "object",
        "properties": {
          "user_id": {
            "type": "string",
            "description": "The Slack user ID."
          }
        },
        "required": ["user_id"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "send_insight",
      "description": "Send real-time market insights to a specific user via DM.",
      "parameters": {
        "type": "object",
        "properties": {
          "insight_data": {
            "type": "string",
            "description": "The insight text to send."
          },
          "user_id": {
            "type": "string",
            "description": "The Slack user ID to send the message to."
          }
        },
        "required": ["insight_data", "user_id"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "generate_business_plan",
      "description": "Send a business plan generation message to a specific user via DM.",
      "parameters": {
        "type": "object",
        "properties": {
          "industry": {
            "type": "string",
            "description": "The industry for which to generate the plan."
          },
          "user_id": {
            "type": "string",
            "description": "The Slack user ID to send the message to."
          }
        },
        "required": ["industry", "user_id"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "list_conversations",
      "description": "List all conversations in the workspace.",
      "parameters": {
        "type": "object",
        "properties": {
          "types": {
            "type": "string",
            "description": "Comma-separated list of conversation types to include."
          },
          "limit": {
            "type": "integer",
            "description": "Maximum number of conversations to return."
          }
        },
        "required": [],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "get_conversation_history",
      "description": "Get message history for a specific channel.",
      "parameters": {
        "type": "object",
        "properties": {
          "channel_id": {
            "type": "string",
            "description": "The ID of the channel to retrieve history for."
          },
          "limit": {
            "type": "integer",
            "description": "Maximum number of messages to return."
          }
        },
        "required": ["channel_id"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "join_conversation",
      "description": "Have the bot join a specific channel.",
      "parameters": {
        "type": "object",
        "properties": {
          "channel_id": {
            "type": "string",
            "description": "The ID of the channel to join."
          }
        },
        "required": ["channel_id"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "create_conversation",
      "description": "Create a new channel in the workspace.",
      "parameters": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "The name of the new channel."
          },
          "is_private": {
            "type": "boolean",
            "description": "Whether the channel should be private."
          }
        },
        "required": ["name"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "add_reminder",
      "description": "Add a reminder for the authenticated user.",
      "parameters": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "description": "The reminder text."
          },
          "time": {
            "type": "string",
            "description": "When to send the reminder."
          }
        },
        "required": ["text", "time"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "list_reminders",
      "description": "List all reminders for the authenticated user.",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "complete_reminder",
      "description": "Complete a reminder by ID.",
      "parameters": {
        "type": "object",
        "properties": {
          "reminder_id": {
            "type": "string",
            "description": "The ID of the reminder to complete."
          }
        },
        "required": ["reminder_id"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "delete_reminder",
      "description": "Delete a reminder by ID.",
      "parameters": {
        "type": "object",
        "properties": {
          "reminder_id": {
            "type": "string",
            "description": "The ID of the reminder to delete."
          }
        },
        "required": ["reminder_id"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "upload_file",
      "description": "Upload a file to specified Slack channels through the external upload process.",
      "parameters": {
        "type": "object",
        "properties": {
          "file_path": {
            "type": "string",
            "description": "The path to the file to upload."
          },
          "channels": {
            "type": "string",
            "description": "Comma-separated list of channel IDs to upload the file to."
          },
          "title": {
            "type": "string",
            "description": "Optional title for the uploaded file."
          }
        },
        "required": ["file_path", "channels"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "list_files",
      "description": "List files in the workspace, optionally filtered by channel.",
      "parameters": {
        "type": "object",
        "properties": {
          "channel": {
            "type": "string",
            "description": "Optional channel ID to filter the files by."
          },
          "count": {
            "type": "integer",
            "description": "Maximum number of files to return."
          }
        },
        "required": [],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "delete_file",
      "description": "Delete a file by its ID.",
      "parameters": {
        "type": "object",
        "properties": {
          "file_id": {
            "type": "string",
            "description": "The ID of the file to delete."
          }
        },
        "required": ["file_id"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "get_team_info",
      "description": "Get workspace information.",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "get_team_profile",
      "description": "Get workspace profile fields.",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
      }
    }
  }
],  

"gnews_api": [
  {
    "type": "function",
    "function": {
      "name": "fetch_news_by_category",
      "description": "Fetch news articles by a specific category.",
      "parameters": {
        "type": "object",
        "properties": {
          "category": {
            "type": "string",
            "description": "The category of news to fetch."
          },
          "lang": {
            "type": "string",
            "description": "The language for the news articles (default is 'en')."
          }
        },
        "required": ["category"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_top_headlines",
      "description": "Fetch the top headlines in a specific language.",
      "parameters": {
        "type": "object",
        "properties": {
          "lang": {
            "type": "string",
            "description": "The language for the news articles (default is 'en')."
          }
        },
        "required": [],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_technology_news",
      "description": "Fetch news articles related to technology.",
      "parameters": {
        "type": "object",
        "properties": {
          "lang": {
            "type": "string",
            "description": "The language for the news articles (default is 'en')."
          }
        },
        "required": [],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_topic_news",
      "description": "Fetch news articles related to a specific topic.",
      "parameters": {
        "type": "object",
        "properties": {
          "topic": {
            "type": "string",
            "description": "The topic of news to fetch."
          },
          "lang": {
            "type": "string",
            "description": "The language for the news articles (default is 'en')."
          }
        },
        "required": ["topic"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "search_news",
      "description": "Search for news articles based on a query.",
      "parameters": {
        "type": "object",
        "properties": {
          "query": {
            "type": "string",
            "description": "The search query for news."
          },
          "lang": {
            "type": "string",
            "description": "The language for the news articles (default is 'en')."
          }
        },
        "required": ["query"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_news_by_country",
      "description": "Fetch news articles by a specific country.",
      "parameters": {
        "type": "object",
        "properties": {
          "country": {
            "type": "string",
            "description": "The country for which to fetch news."
          },
          "lang": {
            "type": "string",
            "description": "The language for the news articles (default is 'en')."
          }
        },
        "required": ["country"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_news_by_language",
      "description": "Fetch news articles by a specific language.",
      "parameters": {
        "type": "object",
        "properties": {
          "lang": {
            "type": "string",
            "description": "The language for the news articles."
          }
        },
        "required": ["lang"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_news_by_source",
      "description": "Fetch news articles from a specific source.",
      "parameters": {
        "type": "object",
        "properties": {
          "source": {
            "type": "string",
            "description": "The source from which to fetch news."
          },
          "lang": {
            "type": "string",
            "description": "The language for the news articles (default is 'en')."
          }
        },
        "required": ["source"],
        "additionalProperties": False
      }
    }
  }
],
"alpha_vantage_api":[
  {
    "type": "function",
    "function": {
      "name": "fetch_stock_daily",
      "description": "Fetch daily time series data for a specific stock symbol.",
      "parameters": {
        "type": "object",
        "properties": {
          "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch the daily data for."
          }
        },
        "required": ["symbol"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_forex_rate",
      "description": "Fetch the exchange rate between two currencies.",
      "parameters": {
        "type": "object",
        "properties": {
          "from_currency": {
            "type": "string",
            "description": "The currency to convert from."
          },
          "to_currency": {
            "type": "string",
            "description": "The currency to convert to."
          }
        },
        "required": ["from_currency", "to_currency"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_sma",
      "description": "Fetch the Simple Moving Average (SMA) for a stock symbol.",
      "parameters": {
        "type": "object",
        "properties": {
          "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch the SMA data for."
          },
          "interval": {
            "type": "string",
            "description": "The time interval for the SMA data (default is 'daily')."
          },
          "time_period": {
            "type": "integer",
            "description": "The time period (number of days) for the SMA (default is 10)."
          }
        },
        "required": ["symbol"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_crypto_exchange_rate",
      "description": "Fetch the exchange rate between two cryptocurrencies.",
      "parameters": {
        "type": "object",
        "properties": {
          "from_currency": {
            "type": "string",
            "description": "The cryptocurrency to convert from."
          },
          "to_currency": {
            "type": "string",
            "description": "The cryptocurrency to convert to."
          }
        },
        "required": ["from_currency", "to_currency"],
        "additionalProperties": False
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "fetch_intraday_stock",
      "description": "Fetch intraday time series data for a specific stock symbol.",
      "parameters": {
        "type": "object",
        "properties": {
          "symbol": {
            "type": "string",
            "description": "The stock symbol to fetch intraday data for."
          },
          "interval": {
            "type": "string",
            "description": "The time interval for the intraday data (default is '5min')."
          }
        },
        "required": ["symbol"],
        "additionalProperties": False
      }
    }
  }
],

"quickbook_api": [
    {
    "type": "function",
    "function": {
        "name": "get_accounts",
        "description": "Retrieve all accounts from QuickBooks.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "create_account",
        "description": "Create a new account with a specified name and type.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the account."
                },
                "account_type": {
                    "type": "string",
                    "description": "The type of the account, such as 'Expense'."
                }
            },
            "required": ["name", "account_type"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_transactions",
        "description": "Retrieve all transactions from QuickBooks.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "create_transaction",
        "description": "Create a new transaction with a specified type, amount, account ID, and category.",
        "parameters": {
            "type": "object",
            "properties": {
                "transaction_type": {
                    "type": "string",
                    "description": "The type of the transaction, e.g., 'journalentry'."
                },
                "amount": {
                    "type": "number",
                    "description": "The amount of the transaction."
                },
                "account_id": {
                    "type": "string",
                    "description": "The ID of the account for the transaction."
                },
                "category": {
                    "type": "string",
                    "description": "The category of the transaction."
                }
            },
            "required": ["transaction_type", "amount", "account_id", "category"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "delete_transaction",
        "description": "Delete an existing transaction by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "transaction_id": {
                    "type": "string",
                    "description": "The ID of the transaction to delete."
                }
            },
            "required": ["transaction_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "get_budgets",
        "description": "Retrieve all budgets from QuickBooks.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "delete_budget",
        "description": "Delete an existing budget by its ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "budget_id": {
                    "type": "string",
                    "description": "The ID of the budget to delete."
                }
            },
            "required": ["budget_id"],
            "additionalProperties": False
        }
    }
},
    {
    "type": "function",
    "function": {
        "name": "compare_budget_with_actual",
        "description": "Compare a budget with actual transactions within its time frame using the budget ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "budget_id": {
                    "type": "string",
                    "description": "The ID of the budget to compare."
                }
            },
            "required": ["budget_id"],
            "additionalProperties": False
        }
    }
},    
]
,"spotify_api": [
    {
        "type": "function",
        "function": {
            "name": "get_album",
            "description": "Get an album by its Spotify ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "album_id": {
                        "type": "string",
                        "description": "The Spotify ID of the album."
                    },
                    "market": {
                        "type": "string",
                        "description": "The market to get the album from. Default is 'US'."
                    }
                },
                "required": ["album_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_albums",
            "description": "Get multiple albums by their Spotify IDs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "album_ids": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "A Spotify album ID."
                        },
                        "description": "A list of Spotify IDs of the albums."
                    },
                    "market": {
                        "type": "string",
                        "description": "The market to get the albums from. Default is 'US'."
                    }
                },
                "required": ["album_ids"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_album_tracks",
            "description": "Get the tracks of an album by its Spotify ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "album_id": {
                        "type": "string",
                        "description": "The Spotify ID of the album."
                    },
                    "market": {
                        "type": "string",
                        "description": "The market to get the album from. Default is 'US'."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "The number of tracks to return. Default is 10."
                    },
                    "offset": {
                        "type": "integer",
                        "description": "The index of the first track to return. Default is 0."
                    }
                },
                "required": ["album_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_artist",
            "description": "Get an artist by their Spotify ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "artist_id": {
                        "type": "string",
                        "description": "The Spotify ID of the artist."
                    }
                },
                "required": ["artist_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_artists",
            "description": "Get multiple artists by their Spotify IDs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "artist_ids": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "A Spotify artist ID."
                        },
                        "description": "A list of Spotify IDs of the artists."
                    }
                },
                "required": ["artist_ids"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_artist_albums",
            "description": "Get the albums of an artist by their Spotify ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "artist_id": {
                        "type": "string",
                        "description": "The Spotify ID of the artist."
                    },
                    "include_groups": {
                        "type": "string",
                        "description": "A comma-separated list of album types. Default is 'single,appears_on'."
                    },
                    "market": {
                        "type": "string",
                        "description": "The market to get the albums from. Default is 'US'."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "The number of albums to return. Default is 10."
                    },
                    "offset": {
                        "type": "integer",
                        "description": "The index of the first album to return. Default is 0."
                    }
                },
                "required": ["artist_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_artist_top_tracks",
            "description": "Get the top tracks of an artist by their Spotify ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "artist_id": {
                        "type": "string",
                        "description": "The Spotify ID of the artist."
                    },
                    "market": {
                        "type": "string",
                        "description": "The market to get the top tracks from. Default is 'US'."
                    }
                },
                "required": ["artist_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_artist_related_artists",
            "description": "Get Spotify catalog information about artists similar to a given artist.",
            "parameters": {
                "type": "object",
                "properties": {
                    "artist_id": {
                        "type": "string",
                        "description": "The Spotify ID of the artist."
                    }
                },
                "required": ["artist_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_tracks",
            "description": "Get Spotify catalog information for multiple tracks by their Spotify IDs.",
            "parameters": {
                "type": "object",
                "properties": {
                    "track_ids": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "A Spotify track ID."
                        },
                        "description": "A list of Spotify IDs of the tracks."
                    },
                    "market": {
                        "type": "string",
                        "description": "The market to get the tracks from. Default is 'US'."
                    }
                },
                "required": ["track_ids"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_for_item",
            "description": "Search for Spotify catalog information about albums, artists, playlists, tracks, shows, episodes, or audiobooks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query string."
                    },
                    "type": {
                        "type": "string",
                        "description": "A comma-separated list of item types to search for (e.g., 'album,artist,track'). Default is 'album,artist,track'."
                    },
                    "market": {
                        "type": "string",
                        "description": "The market to search in. Default is 'US'."
                    },
                    "limit": {
                        "type": "integer",
                        "description": "The maximum number of items to return. Default is 10."
                    },
                    "offset": {
                        "type": "integer",
                        "description": "The index of the first item to return. Default is 0."
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    }
],
"openaire_api": [
    {
        "type": "function",
        "function": {
            "name": "search_research_products",
            "description": "Search in the content of research products.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "The search query."
                    },
                    "type": {
                        "type": "string",
                        "description": "The type of research product. Options are 'publication', 'dataset', 'software', or 'other'. Default is 'publication'."
                    },
                    "page": {
                        "type": "integer",
                        "description": "The page number to retrieve. Default is 1."
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "The number of items per page. Default is 3."
                    },
                    "sort_by": {
                        "type": "string",
                        "description": "The sorting criteria, such as 'popularity DESC'. Default is 'popularity DESC'."
                    }
                },
                "required": ["search"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_research_products_by_title",
            "description": "Search research products by their main title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the research product."
                    },
                    "type": {
                        "type": "string",
                        "description": "The type of research product. Options are 'publication', 'dataset', 'software', or 'other'. Default is 'publication'."
                    },
                    "page": {
                        "type": "integer",
                        "description": "The page number to retrieve. Default is 1."
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "The number of items per page. Default is 3."
                    },
                    "sort_by": {
                        "type": "string",
                        "description": "The sorting criteria, such as 'popularity DESC'. Default is 'popularity DESC'."
                    }
                },
                "required": ["title"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_research_products_by_openaire_id",
            "description": "Search for a research product by its OpenAIRE ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                        "description": "The OpenAIRE ID of the research product."
                    }
                },
                "required": ["id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_organization",
            "description": "Search for organizations by their content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "The search query for the organization."
                    },
                    "country_code": {
                        "type": "string",
                        "description": "The country code of the organization. Default is an empty string."
                    },
                    "page": {
                        "type": "integer",
                        "description": "The page number to retrieve. Default is 1."
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "The number of items per page. Default is 10."
                    }
                },
                "required": ["search"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_organization_by_legal_name",
            "description": "Search for organizations by their legal name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "legal_name": {
                        "type": "string",
                        "description": "The legal name of the organization."
                    },
                    "country_code": {
                        "type": "string",
                        "description": "The country code of the organization. Default is an empty string."
                    },
                    "page": {
                        "type": "integer",
                        "description": "The page number to retrieve. Default is 1."
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "The number of items per page. Default is 10."
                    }
                },
                "required": ["legal_name"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_project",
            "description": "Search for projects by their content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "The search query for the project."
                    },
                    "page": {
                        "type": "integer",
                        "description": "The page number to retrieve. Default is 1."
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "The number of items per page. Default is 10."
                    },
                    "sort_by": {
                        "type": "string",
                        "description": "The sorting criteria, such as 'relevance DESC'. Default is 'relevance DESC'."
                    }
                },
                "required": ["search"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_project_by_title",
            "description": "Search for projects by their title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title of the project."
                    },
                    "page": {
                        "type": "integer",
                        "description": "The page number to retrieve. Default is 1."
                    },
                    "page_size": {
                        "type": "integer",
                        "description": "The number of items per page. Default is 10."
                    },
                    "sort_by": {
                        "type": "string",
                        "description": "The sorting criteria, such as 'relevance DESC'. Default is 'relevance DESC'."
                    }
                },
                "required": ["title"],
                "additionalProperties": False
            }
        }
    }
],

"scholarly_api": [
    {
        "type": "function",
        "function": {
            "name": "search_author",
            "description": "Search for an author by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "author_name": {
                        "type": "string",
                        "description": "Name of the author to search for."
                    }
                },
                "required": ["author_name"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_publication",
            "description": "Search for a publication by title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "publication_title": {
                        "type": "string",
                        "description": "Title of the publication to search for."
                    }
                },
                "required": ["publication_title"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_author_id",
            "description": "Search for an author by their Google Scholar ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "author_id": {
                        "type": "string",
                        "description": "Google Scholar ID of the author."
                    }
                },
                "required": ["author_id"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_organization",
            "description": "Search for an organization by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "organization": {
                        "type": "string",
                        "description": "Name of the organization to search for."
                    }
                },
                "required": ["organization"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_author_by_organization",
            "description": "Search for authors affiliated with a specific organization.",
            "parameters": {
                "type": "object",
                "properties": {
                    "organization": {
                        "type": "string",
                        "description": "Name of the organization to search authors for."
                    }
                },
                "required": ["organization"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_keyword",
            "description": "Search for a keyword in Google Scholar.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "Keyword to search for in Google Scholar."
                    }
                },
                "required": ["keyword"],
                "additionalProperties": False
            }
        }
    }
]

}

