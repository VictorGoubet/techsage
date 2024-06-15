import json
import os
from typing import Optional
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from crewai_tools import tool
from duckduckgo_search import DDGS
from lxml import etree


@tool("Scraping tool")
def scrap_website_tool(website_url: str) -> str:
    """Scrap the content of a website

    :param str website_url: The url of the website to scrap
    :return str: The HTML dom of the scraped website
    """
    try:
        page = requests.get(
            website_url,
            timeout=15,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/96.0.4664.110 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng\
,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Accept-Encoding": "gzip, deflate, br",
            },
            cookies={},
        )
        parsed = BeautifulSoup(page.content, "html.parser")
        text = parsed.get_text()
        text = "\n".join([i for i in text.split("\n") if i.strip() != ""])
        text = " ".join([i for i in text.split(" ") if i.strip() != ""])
        return text
    except requests.RequestException as e:
        return f"Error scraping website: {e}"


@tool("An alternative to google searching tool")
def duckduckgo_search_tool(search_value: str) -> str:
    """Perform a duckduckgo search with the given search_value.

    :param str search_value: The value to use as input for the search
    :return Optional[str]: The google HTML results
    """
    res = "\n".join(DDGS().text(search_value, max_results=5))
    return res


@tool("Google Searching tool")
def google_search_tool(search_value: str) -> Optional[str]:
    """Perform a google search with the given search_value

    :param str search_value: The value to use as input for the search
    :return Optional[str]: The google HTML results, None if something failed
    """
    url = "https://www.google.com/search?" + urlencode(
        {"q": search_value, "hl": "en", "start": 0, "num": 10, "sourceid": "chrome", "ie": "UTF-8"}
    )
    if os.environ.get("GOOGLE_SEARCH_API_KEY", "") not in ["NA", ""]:
        res = api_google_search(url)
    else:
        res = local_google_search(url)
    return res


def local_google_search(url: str) -> str:
    """Perform a local google search

    :param str url: The google url to search
    :return str: The google results or the encountered error
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        dom = requests.get(url, headers=headers, cookies={"CONSENT": "YES+"}).text
        res = extract_results(dom)
        return res
    except Exception as e:
        return f"Error performing Google search: {e}"


def extract_results(dom: str) -> str:
    """Extract the results from the google search

    :param str dom: The dom of the google search
    :return str: The google results
    """
    xml_tree = etree.HTML(dom, parser=None)
    blocks = xml_tree.xpath(
        "//div[@id='search']//div[(contains(@class, 'g ') or @class='g') and descendant::a[@href != ''] "
        "and not(descendant::div[contains(@class, 'g ') or @class='g']) "
        "and not(descendant::span[text()='See results about'])]"
    )
    res = "\n".join(["".join(block.itertext()) for block in blocks])
    return res


def api_google_search(url: str) -> str:
    """Perform a google search using a google search api

    :param str url: The google url to search
    :return str: The google results or the encountered error
    """
    try:
        # Delpha API
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": os.environ["GOOGLE_SEARCH_API_KEY"],
        }
        api_url = "https://delpha-recommender.delpha.io/global/v1/google-search"
        resp = requests.request(
            "POST",
            api_url,
            headers=headers,
            data=json.dumps({"url": url}),
        ).json()
        return "\n".join(resp["results"]["searches_text"])
    except Exception as e:
        return f"Error performing Google search: {e}"
