"""_summary_
This is a temporary database mockup just for demo

db is formatted as 
db = {
    "PROVIDER_NAME":
    {
        "ACTION_NAME"
    }
}

"""

import pydantic

db_index = ["GOOGLE_SEARCH", "WIKIPEDIA_SEARCH"]

tool_name_to_index = {
    # tool_name is how LLM called these tools in their response
    "google_search": "GOOGLE_SEARCH",
    "wikipedia_search": "WIKIPEDIA_SEARCH"
}


db = {
    "GOOGLE":
        {
            "SEARCH":
            {
                "author": "AAPI",
                "provider": "serpapi",
                "description": "Search in google",
                "request": "GET",
                "entrypoint": "https://serpapi.com/search",
                "input_schema": {
                    "q": "Parameter defines the query you want to search.", # Add more field like type, description, etc
                },
                "required": ["q"],
                "output_schema": { #TODO: this output schema is generated from serapi official document
                    "type": "object",
                    "properties": {
                        "search_metadata": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "status": {"type": "string"},
                                "json_endpoint": {"type": "string"},
                                "created_at": {"type": "string"},
                                "processed_at": {"type": "string"},
                                "google_url": {"type": "string"},
                                "raw_html_file": {"type": "string"},
                                "total_time_taken": {"type": "number"}
                            }
                        },
                        "search_parameters": {
                            "type": "object",
                            "properties": {
                                "engine": {"type": "string"},
                                "q": {"type": "string"},
                                "google_domain": {"type": "string"},
                                "hl": {"type": "string"},
                                "gl": {"type": "string"},
                                "device": {"type": "string"}
                            }
                        },
                        "search_information": {
                            "type": "object",
                            "properties": {
                                "organic_results_state": {"type": "string"},
                                "query_displayed": {"type": "string"},
                                "total_results": {"type": "integer"},
                                "time_taken_displayed": {"type": "number"}
                            }
                        },
                        "organic_results": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "position": {"type": "integer"},
                                    "title": {"type": "string"},
                                    "link": {"type": "string"},
                                    "displayed_link": {"type": "string"},
                                    "snippet": {"type": "string"},
                                    "snippet_highlighted_words": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    },
                                    "sitelinks": {
                                        "type": "object",
                                        "properties": {
                                            "inline": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "title": {"type": "string"},
                                                        "link": {"type": "string"}
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    "cached_page_link": {"type": "string"},
                                    "related_pages_link": {"type": "string"}
                                }
                            }
                        },
                        "related_searches": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "query": {"type": "string"},
                                    "link": {"type": "string"}
                                }
                            }
                        },
                        "pagination": {
                            "type": "object",
                            "properties": {
                                "current": {"type": "integer"},
                                "next": {"type": "string"},
                                "other_pages": {
                                    "type": "object",
                                    "additionalProperties": {"type": "string"}
                                }
                            }
                        },
                        "serpapi_pagination": {
                            "type": "object",
                            "properties": {
                                "current": {"type": "integer"},
                                "next_link": {"type": "string"},
                                "next": {"type": "string"}
                            }
                        }
                    }
                },
                "api_key_flg": 1, # 1 means its calling only needs an API key, 0 means its calling can work without API. The other numbers are reserved for other authentication methods in the future
                "ai_tool_desc": { # The format below is inspired by Claude official practice
                    "name": "google_search",
                    "description": "Performs a Google search for the given query",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "q": {
                                "type": "string",
                                "description": "The search query to be used for the Google search"
                            }
                        },
                        "required": ["q"]
                    }
                }
            },           
        },
    "WIKIPEDIA":
        {
            "SEARCH":
            {
                "author": "AAPI",
                "provider": "wikipedia",
                "description": "Search in wikipedia",
                "request": "GET",
                "entrypoint": "https://en.wikipedia.org/w/api.php",
                "input_schema": {
                    "srsearch": "query string",
                    "srlimit": "maximum number of results to return"
                },
                "required": ["srsearch"],
                "config_params": {
                    "action": "query",
                    "format": "json",
                    "list": "search",
                }, # Config_params are some parameters not specified by user input but still required for wikipedia API calling
                "output_schema": { # what api response looks like
                        "batchcomplete": {"type": "string"},
                        "continue": {
                            "type": "object",
                            "properties": {
                                "sroffset": {"type": "integer"},
                                "continue": {"type": "string"}
                            }
                        },
                        "query": {
                            "type": "object",
                            "properties": {
                                "searchinfo": {
                                    "type": "object",
                                    "properties": {
                                        "totalhits": {"type": "integer"}
                                    }
                                },
                                "search": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "ns": {"type": "integer"},
                                            "title": {"type": "string"},
                                            "pageid": {"type": "integer"},
                                            "size": {"type": "integer"},
                                            "wordcount": {"type": "integer"},
                                            "snippet": {"type": "string"},
                                            "timestamp": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }

                },
                "api_key_flg": 0, # 0 means its calling can work without API
                "ai_tool_desc": {
                    "name": "wikipedia_search",
                    "description": "Searches Wikipedia for the given query and returns a list of relevant articles",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "srsearch": {
                                "type": "string",
                                "description": "The search query to be used for the Wikipedia search"
                            },
                            "srlimit": {
                                "type": "integer",
                                "description": "The maximum number of results to return (optional)",
                                "default": 10
                            }
                        },
                        "required": ["srsearch"]
                    }
                },            
            },
        },
}
