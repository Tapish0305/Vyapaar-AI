from smolagents import tool
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Union
import json  # Added this import

# Defined the URL that will be used by the function
url = 'https://cleartax.in/s/gst-rates'

@tool
def scrape_gst_rates_tool(query: str) -> List[Dict[str, Union[str, List]]]:
    """
    Searches the fixed Cleartax GST rates page (https://cleartax.in/s/gst-rates)
    for paragraphs or tables matching a specific product or category query.
    Use this to find the GST rate for a specific item (e.g., 'shoes', 'milk', 'laptops').

    Args:
        query (str): The specific product or category to search for (e.g., 'shoes', 'milk', 'laptops').

    Returns:
        List[Dict[str, Union[str, List]]]: A list of dictionaries. Each dictionary 
        represents a matching paragraph or table. Returns a list with a single 
        error or info dictionary if no query is given, the page fails to load, 
        or no matches are found.
    """
    
    if not query:
        return [{"error": "A search query must be provided."}]

    try:
        # (Fixed) Changed GST_DATA_URL to the defined 'url'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return [{"error": f"Failed to fetch GST data: {e}"}]

    soup = BeautifulSoup(response.text, "html.parser")
    # Robustly find all 'p' and 'table' tags even if <body> is missing
    content_elements = (soup.body or soup).find_all(['p', 'table'])

    if not content_elements:
        return [{"info": "No paragraphs or tables found on the GST page."}]

    # --- 1. Scrape ALL data first ---
    scraped_data = []
    for element in content_elements:
        if element.name == 'p':
            text = element.get_text(strip=True)
            if text:
                scraped_data.append({
                    "type": "paragraph",
                    "content": text
                })

        elif element.name == 'table':
            table_data = []
            headers_tags = element.find_all('th')
            header_row = element.find('tr') # Fallback for tables with <td> headers
            headers = []
            body_rows = []

            if headers_tags:
                # Standard case: Table has <th> tags
                headers = [h.get_text(strip=True) for h in headers_tags]
                body_rows = element.find('tbody').find_all('tr') if element.find('tbody') else element.find_all('tr')[1:]
            elif header_row:
                # Fallback: No <th>, use first <tr> as header
                headers = [cell.get_text(strip=True) for cell in header_row.find_all('td')]
                body_rows = element.find_all('tr')[1:]

            # Process table rows
            for row in body_rows:
                cols = row.find_all('td')
                if len(cols) == len(headers) and any(col.get_text(strip=True) for col in cols):
                    row_data = {headers[i]: col.get_text(strip=True) for i, col in enumerate(cols)}
                    table_data.append(row_data)

            if table_data:
                scraped_data.append({
                    "type": "table",
                    "content": table_data # content is a List[Dict]
                })

    # --- 2. Filter the scraped data based on the query ---
    filtered_data = []
    lower_query = query.lower()

    for item in scraped_data:
        if item["type"] == "paragraph":
            # If the query is in the paragraph text
            if lower_query in item["content"].lower():
                filtered_data.append(item)
        
        elif item["type"] == "table":
            # If query is in the table (check by converting table to string)
            # (Fixed) 'json' is now imported
            table_as_string = json.dumps(item["content"]).lower()
            if lower_query in table_as_string:
                filtered_data.append(item)

    if not filtered_data:
        return [{"info": f"No paragraphs or tables found matching your query: '{query}'"}]

    return filtered_data
