import os
import json
import requests
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()
api_key = os.getenv("PROXYCURL_API_KEY")
proxycurl_endpoint = os.getenv("PROXYCURL_API_ENDPOINT")

def is_linkedin_profile(url):
    return url.startswith("https://www.linkedin.com/in/")

def get_profile_url(name):

    lookup_tool = TavilySearchResults(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True,
        include_images=True,
        include_domains=["https://www.linkedin.com/in/"],  # Include only LinkedIn domain
        exclude_domains=["linkedin.com/company", "linkedin.com/feed"],  # Exclude company and feed pages
    )

    results = lookup_tool.run(f"{name} LinkedIn Profile")

    if not results:
        return "No results found."

    # Process the results to find a LinkedIn profile URL
    for result in results:
        url = result.get('url')  # Extract the URL from the result dictionary
        if url and is_linkedin_profile(url):
            return url
        
    return "No valid LinkedIn profile URL found."

def preprocess_profile(profile_data):
    return {k: v for k, v in profile_data.items() if v and k != 'similarly_named_profiles'}

def fetch_linkedin_profile(linkedin_url):
    headers = {'Authorization': 'Bearer ' + api_key}
    params = {'url': linkedin_url}

    response = requests.get(
        proxycurl_endpoint, 
        headers=headers, 
        params=params,
        timeout=60
    )

    if response.status_code == 200:
        # Fetch and clean the profile data before returning
        profile_data = response.json()
        cleaned_profile_data = {k: v for k, v in profile_data.items() if v and (k != 'people_also_viewed' or k != 'similarly_named_profiles')}
        return cleaned_profile_data
    else:
        print(f"Failed to fetch LinkedIn profile data: {response.status_code}")
        return None
    
def search_local_profiles(name, json_files):
    for file_path in json_files:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for profile in data.values():
                if name.lower() == profile.get("full_name", "").lower():
                    # Preprocess the profile data to remove unwanted fields and empty values
                    return preprocess_profile(profile)
    return None
