import os
import requests


def scrape_linkedin_profile(linkedin_profile_url: str):
    """scrape information from LinkedIn profiles,
    Manually scrape LinkedIn profile information using the LinkedIn API"""
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": f"Bearer {os.environ.get('PROXYCURL_API_KEY')}"}
    params = {"url": linkedin_profile_url}
    response = requests.get(api_endpoint, params=params, headers=header_dic)
    return clean_data(response)


def scrape_linkedin_profile_test():
    """scrape information from LinkedIn profiles,
    Manually scrape LinkedIn profile information using the LinkedIn API
    This function uses a gist url so that we don't waste our API calls"""
    response = requests.get(
        "https://gist.githubusercontent.com/HermanCodes/cddeee919e9dfce464c2ba942a326e09/raw"
        "/c5079d00200ef890053ae33bb40cc96a74b781cc/harry-smith.json"
    )
    return clean_data(response)


def clean_data(linkedin_data):
    """clean the data from the LinkedIn profile"""
    data = linkedin_data.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None, "None")
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data
