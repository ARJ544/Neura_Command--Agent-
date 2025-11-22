"""
Research tools using Tavily API tavily_client.extract and tavily_client.search
Provided tools:
- internet_search: Perform an online web search using the Tavily Search API.
- web_scraper: Extract/Scrape detailed content directly from any specific webpages using Tavily's extractor.

"""

from dotenv import load_dotenv
import os
from langchain_core.tools import tool
from tavily import TavilyClient
from typing import Literal

load_dotenv()

def ask_and_save():
    name = input("Enter your name: ")
    gemini_key = input("Enter your Gemini API: ")
    tavily_key = input("Enter your Tavily API: ")

    with open(env_path, "w") as f:
        f.write(f"NAME={name}\n")
        f.write(f"GOOGLE_API_KEY={gemini_key}\n")
        f.write(f"TAVILY_API_KEY={tavily_key}\n")

    return name, gemini_key, tavily_key
def open_read_check_env(env_path):
    with open(env_path, 'r') as f:
        values = f.readlines()

        if values == [] or len(values) < 3:
            name, gemini_key, tavily_key = ask_and_save()
            values = [f"NAME={name}\n", f"GOOGLE_API_KEY={gemini_key}\n", f"TAVILY_API_KEY={tavily_key}\n"]

        name = values[0].strip().split("=")[1]
        gemini_key = values[1].strip().split("=")[1]
        tavily_key = values[2].strip().split("=")[1]

    return name, gemini_key, tavily_key

if "TAVILY_API_KEY" not in os.environ:
    env_path = ".env"

    if os.path.exists(env_path):
        name, gemini_key, tavily_key = open_read_check_env(env_path)
        print(f".env exists!!! name={name}, gemini_key={gemini_key}, tavily_key={tavily_key}")

    else:
        name, gemini_key, tavily_key = ask_and_save()
        print(f"New .env file created successfully! With name = {name}, gemini_key = {gemini_key}, tavily_key = {tavily_key}")
else:
    gemini_key = os.getenv("GOOGLE_API_KEY")
    tavily_key = os.getenv("TAVILY_API_KEY")
    name = os.environ.get("NAME")
    print(f"Tavily_Api_Key found!!! name = {name} gemini_key = {gemini_key} tavily_key = {tavily_key}")

if not tavily_key or not gemini_key or not name:
    name, gemini_key, tavily_key = open_read_check_env(env_path)
    print(f".env exists!!! Variables wasn't Found!!!\n Created name={name}, gemini_key={gemini_key}, tavily_key={tavily_key}")

tavily_client = TavilyClient(api_key=tavily_key)

@tool
def internet_search(
    query: str,
    max_results: int = 4,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """
    Perform an online web search using the Tavily Search API.

    USE THIS TOOL WHEN:
    - You need **current, public information, any info** from the internet.
    - You want **summaries of web pages**.
    - You are answering questions about:
        • general knowledge or trending topics
        • recent news or current events, sports, weather
        • financial information, markets, companies, or economic data
    - The user asks you to "search", "look up", "find online", or "check on the internet" or "go" or related keywords.

    DO NOT USE THIS TOOL WHEN:
    - The information is already provided in the conversation.
    - The answer is something you can generate from reasoning alone.

    Args:
    - query (str): The text query you want to search for.
    - max_results (int): Number of results to retrieve (default 4).
    - topic (str): Search domain — "general", "news", or "finance".
      Use:
        • "general" for broad informational searches.
        • "news" for recent events or breaking updates.
        • "finance" for markets, stocks, economics, or company profiles.
    - include_raw_content (bool): If True, includes raw webpage text in results.

    RETURNS:
    - A structured list of search results with titles, URLs, summaries,
      and optionally raw text.
    """
    return tavily_client.search(
        query,
        max_results=max_results if max_results is not None else 4,
        include_raw_content=include_raw_content,
        topic=topic,
    )

@tool
def web_scraper(urls: list[str]):
    """
    Extract/Scrape detailed content directly from any specific webpages using Tavily's extractor.
    This tool can also scrape social media websites (LinkedIn, Instagram, Facebook, Twitter).
    USE THIS TOOL WHEN:
    - You already have one or more **URLs/Links** and need to read their content.
    - You want to access **full page text**, **HTML-derived content**, or **structured sections**.
    - The task requires:
        • reading an article directly
        • extracting facts, tables, lists, or deep page information
        • verifying claims from a specific link
        • doing analysis on a known webpage
    - The user provides URLs/link or you have a link/url and asks to "scrape", "extract", "read", or "get content from" or "go and tell from" or "get more info about" or related keywords.

    DO NOT USE THIS TOOL WHEN:
    - You do not know about which link/url — use internet_search instead.
    - The information is already provided in the conversation.

    Args:
    - urls (list[str]): One or more URLs to scrape.

    RETURNS:
    - Detailed extracted content from each provided URL.
    """
    if isinstance(urls, str):
        urls = [urls]

    return tavily_client.extract(
        urls,
        extract_depth="advanced",
        format="markdown"
    )