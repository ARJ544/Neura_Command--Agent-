"""
Utility used to open URl or simple query Text in default browser.
Provided tools:
 - open_url_or_query: Opens any provided url or text in default Browser.
"""

from langchain_core.tools import tool
import webbrowser
import urllib.parse

@tool
def open_url_or_query(url_or_query: str):
    """
    Opens any provided url or text in default Browser.
    
    Args:
        url_or_query (str): A url link or simple text to search
    
    Returns:
        Success message or error msg
    
    """

    url_or_query = url_or_query.strip()
    
    try:
        if url_or_query.startswith(("http://", "https://", "www.")):
            if not url_or_query.startswith(("http://", "https://")):
                url_or_query = "https://" + url_or_query
                
            webbrowser.open_new_tab(url_or_query)
            return f"Opened Url in browser: {url_or_query}"
        else:
            
            query = urllib.parse.quote(url_or_query)
            webbrowser.open_new_tab(f"https://www.google.com/search?q={query}")
            return f"Opened Google search for: {url_or_query}" 
    except Exception as e:
        return f"An error occured: {e}"
