import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def scrape_gst_rates(url: str)  -> List[Dict[str, Union[str, List]]]:
    """
    Scrapes all paragraphs and tables from a given URL and returns them
    in a structured list, all within a single function.

    Args:
        url (str): The URL of the page to scrape.

    Returns:
        A list where each item is a dictionary representing a piece of
        content (either a paragraph or a table).
        Returns an empty list if the page cannot be fetched or contains no content.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors (like 404, 500)
    except requests.exceptions.RequestException as e:
        # If the request fails, return an informative error.
        print(f"Error fetching URL {url}: {e}")
        return [{"error": f"Failed to fetch URL: {e}"}]

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all paragraph and table tags in the order they appear.
    content_elements = soup.body.find_all(['p', 'table'])

    if not content_elements:
        return []

    scraped_data = []
    for element in content_elements:
        if element.name == 'p':
            # --- Handle Paragraph Content ---
            text = element.get_text(strip=True)
            if text:  # Only add non-empty paragraphs.
                scraped_data.append({
                    "type": "paragraph",
                    "content": text
                })
        
        elif element.name == 'table':
            # --- Handle Table Content (Inlined Logic) ---
            table_data = []
            headers_tags = element.find_all('th')
            header_row = element.find('tr')
            
            headers = []
            body_rows = []

            if headers_tags:
                headers = [h.get_text(strip=True) for h in headers_tags]
                # If <th> exists, data rows are in <tbody> or are all <tr> after the first one.
                body_rows = element.find('tbody').find_all('tr') if element.find('tbody') else element.find_all('tr')[1:]
            elif header_row:
                # If no <th>, use the first row's <td>s as headers.
                headers = [cell.get_text(strip=True) for cell in header_row.find_all('td')]
                body_rows = element.find_all('tr')[1:] # All other rows are data.
            
            # Process the data rows into a list of dictionaries.
            for row in body_rows:
                cols = row.find_all('td')
                if len(cols) == len(headers): # Ensure row aligns with header.
                    row_data = {headers[i]: col.get_text(strip=True) for i, col in enumerate(cols)}
                    table_data.append(row_data)

            if table_data: # Only add non-empty tables.
                scraped_data.append({
                    "type": "table",
                    "content": table_data
                })
                
    return scraped_data
