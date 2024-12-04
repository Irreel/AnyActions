from anyactions import ActionHub

hub = ActionHub()

# tools = hub.tools(["get_current_time", "get_current_date"])
tools = hub.tools(["serpapi_google_search"])