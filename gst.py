import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_gst_rates(url: str) -> List[Dict[str, str]]:
    """
    Scrape GST rates from a table on the given URL.
    Args:
        url (str): URL of the page containing GST rate table.
    Returns:
        List[Dict[str, str]]: List of GST rate records with category, items, and rate.
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="ck-table-resized")
    if not table:
        print("No table with class ck-table-resized found.")
        return []
    rows = table.find_all("tr")
    data = []
    for row in rows[1:]:  # skip header row
        cols = row.find_all(["td", "th"])
        if len(cols) >= 3:
            category = cols[0].get_text(strip=True)
            items = cols[1].get_text(strip=True)
            from_percent = cols[2].get_text(strip=True)
            data.append({
                "category": category,
                "items": items,
                "from_percent": from_percent
            })
    return data
