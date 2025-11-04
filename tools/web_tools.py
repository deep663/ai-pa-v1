import requests
import webbrowser
from bs4 import BeautifulSoup
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults
import pywhatkit


def check_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

duckduckgo_tool = DuckDuckGoSearchResults()

@tool("advanced_web_search", description="Perform a web search, fetch content from top results, and return combined text.")
def advanced_web_search(query: str, max_results: int = 3) -> str:
    """
    Perform an advanced web search using DuckDuckGo, fetch content from the top results,
    and return the combined text content.

    Args:
        query: The search query string.
        max_results: Number of top results to fetch content from (default: 3).
    """
    if not check_connection():
        return "No internet connection."

    try:
        # Get search results from DuckDuckGo
        search_results_str = duckduckgo_tool.run(query)
        if not search_results_str:
            return "No search results found."

        # Parse the search results to extract URLs
        # DuckDuckGoSearchResults returns a string like: "[snippet1](url1), [snippet2](url2), ..."
        urls = []
        for item in search_results_str.split(', '):
            if '(' in item and ')' in item:
                url = item[item.find('(') + 1:item.find(')')]
                urls.append(url)
        
        if not urls:
            return "Could not extract URLs from search results."

        combined_content = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        for i, url in enumerate(urls):
            if i >= max_results:
                break
            try:
                response = requests.get(url, headers=headers, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract text from common content tags
                page_text = []
                for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'li']):
                    page_text.append(tag.get_text(separator=' ', strip=True))
                
                if page_text:
                    combined_content.append(f"--- Content from {url} ---" + "\n".join(page_text[:10])) # Limit to first 10 paragraphs/headings
                else:
                    combined_content.append(f"--- No readable content from {url} ---")

            except requests.exceptions.RequestException as e:
                combined_content.append(f"--- Error fetching {url}: {e} ---")
            except Exception as e:
                combined_content.append(f"--- Error processing {url}: {e} ---")

        if not combined_content:
            return "No content could be fetched from the top search results."

        return "\n\n".join(combined_content)

    except Exception as e:
        return f"Error during advanced web search: {str(e)}"

@tool("find_jobs", description="Find job listings for a specific job title and location.")
def find_jobs(job_title: str, location: str) -> str:
    """
    Find job listings for a specific job title and location using Google Jobs.

    Args:
        job_title: The job title to search for.
        location: The location to search for jobs in.
    """
    if not check_connection():
        return "No internet connection."

    query = f"{job_title} jobs in {location}"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}&ibp=htl;jobs"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.text, 'html.parser')

        job_listings = []
        for job_elem in soup.find_all('div', class_='gws-plugins-horizon-jobs__li-ed'):
            title_elem = job_elem.find('div', class_='gws-plugins-horizon-jobs__tl')
            company_elem = job_elem.find('div', class_='gws-plugins-horizon-jobs__detail-row')
            location_elem = job_elem.find_all('div', class_='gws-plugins-horizon-jobs__detail-row')[1]

            if title_elem and company_elem and location_elem:
                title = title_elem.text.strip()
                company = company_elem.text.strip()
                location = location_elem.text.strip()
                job_listings.append({"title": title, "company": company, "location": location})

        if not job_listings:
            return "No job listings found."

        # Format the results
        formatted_results = ""
        for job in job_listings:
            formatted_results += f"Title: {job['title']}\nCompany: {job['company']}\nLocation: {job['location']}\n---\n"

        return formatted_results.strip()

    except requests.exceptions.RequestException as e:
        return f"Error fetching job listings: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


@tool("search_youtube_video", description="Searches for a YouTube video and opens it in the default web browser.")
def search_youtube_video(query: str) -> str:
    """
    Searches for a YouTube video and opens the first result in the default web browser.

    Args:
        query: The search query for the YouTube video.
    """
    try:
        # Construct a YouTube search URL
        search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"

        # Use DuckDuckGo to find the first YouTube video link
        search_results_str = duckduckgo_tool.run(f"site:youtube.com {query}")
        
        if not search_results_str:
            # Fallback to opening the search page if no direct link is found
            webbrowser.open(search_url)
            return f"I couldn't find a specific video, but I've opened the YouTube search results for '{query}' in your browser."

        # Extract the first URL
        urls = []
        for item in search_results_str.split(', '):
            if '(' in item and ')' in item:
                url = item[item.find('(') + 1:item.find(')')]
                if 'youtube.com/watch' in url:
                    urls.append(url)
        
        if urls:
            video_url = urls[0]
            webbrowser.open(video_url)
            return f"Playing the top YouTube result for '{query}' in your browser."
        else:
            # Fallback to opening the search page
            webbrowser.open(search_url)
            return f"I couldn't find a specific video, but I've opened the YouTube search results for '{query}' in your browser."

    except Exception as e:
        return f"An error occurred while trying to play the YouTube video: {e}"

@tool("open_youtube_video", description="Opens a given YouTube video URL in the default web browser.")
def open_youtube_video(video_url: str) -> str:
    """
    Opens a given YouTube video URL in the default web browser.

    Args:
        video_url: The full URL of the YouTube video to open.
    """
    try:
        if "youtube.com/watch" not in video_url and "youtu.be/" not in video_url:
            return "Invalid YouTube video URL provided. Please provide a full YouTube video URL."
        
        webbrowser.open(video_url)
        return f"Opened YouTube video: {video_url} in your browser."
    except Exception as e:
        return f"An error occurred while trying to open the YouTube video: {e}"

@tool("play_youtube_video", description="Plays a YouTube video directly.")
def play_youtube_video(video_title: str) -> str:
    """
    Plays a YouTube video directly.
    This will open the video in your default web browser.

    Args:
        video_title: The title of the video to play.
    """
    try:
        pywhatkit.playonyt(video_title)
        return f"Attempting to play '{video_title}' on YouTube using pywhatkit."
    except Exception as e:
        return f"An error occurred while trying to play the YouTube video with pywhatkit: {e}"