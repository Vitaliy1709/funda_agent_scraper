import requests
import re
from bs4 import BeautifulSoup

from load_django import *
from parser_app.models import *


# Define headers
headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "authorization": "Basic ZWE3M2M2OWU5ZjQyOmE2ODhkNjMyLWY5NTUtNGI1ZC04ZTM1LWYyN2ZkOGQxOWMzNw==",
    "content-type": "application/json",
    "origin": "https://www.funda.nl",
    "referer": "https://www.funda.nl/",
    "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "x-search-client": "ReactiveSearch Vue",
    "x-timestamp": "1731310662554"
}

# Define the payload
payload = {
    "settings": {
        "recordAnalytics": False,
        "enableQueryRules": True,
        "emptyQuery": True,
        "suggestionAnalytics": True
    },
    "query": [
        {
            "id": "SearchResult",
            "type": "search",
            "dataField": ["name"],
            "execute": True,
            "react": {
                "and": "SearchResult__internal"
            },
            "size": 10,
            "from": 0,
            "defaultQuery": {
                "id": "get-agents-by-area-sorted-by-relevance-score",
                "params": {
                    "geo_identifier": "biddinghuizen",
                    "max_number_of_transactions_in_area": 1,
                    "tenant": 1,
                    "transaction_type": 1,
                    "weight_characteristics": 1,
                    "weight_focus_in_area": 1,
                    "weight_market_share": 1,
                    "weight_profile_completeness_score": 0.2
                }
            }
        }
    ]
}

BASE_URL = "https://www.funda.nl/makelaar/"

def safe_get_text(element, *selectors, default=""):
    for selector in selectors:
        if element:
            element = element.find(*selector)
        else:
            break
    return element.get_text().strip() if element else default

all_info = []

# Make the POST request
response_post = requests.post("https://agent-search-arc.funda.io/agents/_reactivesearch", headers=headers, json=payload)

if response_post.status_code == 200:
    response_data = response_post.json()

    urls = []

    # Extract agency URLs
    for hit in response_data.get("SearchResult", {}).get("hits", {}).get("hits", []):
        agency_id = hit["_id"]
        hit_id = re.search(r'_(\d+)', agency_id) if agency_id else None
        if hit_id:
            number = hit_id.group(1)
            urls.append(f"{BASE_URL}{number}")

    # Parsing each agency page
    for url in urls:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        info = {}

        # Contact Info
        info["agent_name"] = safe_get_text(soup, ("h1",))
        info["agency_phone"] = safe_get_text(soup,
                                             ("a", {
                                                 "class": "text-secondary-70 hover:text-secondary-70-darken-1 inline-flex items-center gap-2 gtm-makelaar-contact-call-phone md:hidden"}),
                                             ("span", {"class": "hidden md:block"}))

        email_elem = soup.find("a", class_="text-secondary-70 hover:text-secondary-70-darken-1 inline-flex items-center gap-2 gtm-makelaar-contact-message")
        info["agency_email"] = email_elem.get("href") if email_elem else None

        image_elem = soup.find("img", class_="size-full object-cover")
        info["image"] = image_elem.get("srcset") if image_elem else None

        logo_elem = soup.find("img", class_="size-full rounded object-cover")
        info["image_logo"] = logo_elem.get("srcset") if logo_elem else None

        website_elem = soup.find("a", class_="flex items-center gap-2 text-secondary-70 hover:text-secondary-70-darken-1")
        info["website_url"] = f'https://www.funda.nl{website_elem.get("href")}' if website_elem else None

        # Address
        nuxt_data_script = soup.find("script", id="__NUXT_DATA__")
        if nuxt_data_script:
            email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
            emails = re.findall(email_pattern, nuxt_data_script.string)
            info["agency_email_address"] = emails[0] if emails else None

        # Other details
        info["agency_address"] = safe_get_text(soup, ("address", {"class": "not-italic"}))
        info["agency_description"] = safe_get_text(soup, ("div", {"id": "description"}), ("span", {"class": "break-words"}))
        info["agency_association"] = safe_get_text(soup, ("div", {"class": "mt-4 flex lg:mt-6 lg:gap-6"}), ("p",))
        info["agency_customer_reviews"] = safe_get_text(soup, ("div", {"id": "highlightedReview"}), ("p", {"class": "text-xl font-medium lg:text-[28px] lg:leading-9"}))

        # Reviews and ratings
        info["rating"] = safe_get_text(soup, ("h2", {"class": "text-xl font-semibold lg:text-[28px] lg:leading-9"}))
        info["rating_points"] = safe_get_text(soup, ("p", {"class": "text-2xl font-semibold lg:text-4xl"}))
        info["number_of_reviews"] = safe_get_text(soup, ("p", {"class": "text-neutral-50"}))
        info["colleagues"] = safe_get_text(soup, ("div", {"class": "flex gap-[10px] lg:items-center"}))

        # Characteristics
        certificates_tag = soup.select("div.flex abbr.cursor-help")
        info["certificates"] = [abbr.get_text().strip() for abbr in certificates_tag]
        languages_tag = soup.select_one("p:contains('Talen') + p")
        info["languages"] = [lang.strip() for lang in languages_tag.get_text().split(",")] if languages_tag else None
        info["association"] = safe_get_text(soup, ("div", {"id": "affiliation"}), ("p",))
        info["customer_reviews"] = safe_get_text(soup, ("p", {"class": "text-xl font-medium lg:text-[28px] lg:leading-9"}))

        # Employees
        info["total_employees"] = safe_get_text(soup, ("span", {"class": "text-xl font-semibold"}))

        # Social media links
        social_media = soup.find_all("a", class_="text-secondary-70 hover:text-secondary-70-darken-1 inline-flex items-center gap-2 w-full lg:py-2.5")
        info["link_facebook"] = social_media[0].get("href") if len(social_media) > 0 else None
        info["link_instagram"] = social_media[1].get("href") if len(social_media) > 1 else None
        info["link_linkedin"] = social_media[2].get("href") if len(social_media) > 2 else None

        all_info.append(info)

        agent, created = RealEstateAgent.objects.update_or_create(
            agency_id=number,
            defaults=info
        )
        if created:
            print(f"Created new agent: {agent.agent_name}")
        else:
            print(f"Updated agent: {agent.agent_name}")
