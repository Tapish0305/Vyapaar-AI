from smolagents.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from typing import List

# Initialize the search tool
# DuckDuckGoSearchRun is a simple tool that doesn't require an API key.
search_tool = DuckDuckGoSearchRun()

# Define the specific websites to search using the 'site:' operator
MSME_WEBSITE = "site:msme.gov.in"
MUDRA_WEBSITE = "site:mudra.org.in"
SBI_WEBSITE = "site:sbi.co.in"
RBI_WEBSITE = "site:rbi.org.in"

@tool
def loan_info_tool(query: str) -> str: # <-- Added the '-> str' return type
    """
    Searches and summarizes information related to MSME loans,
    Pradhan Mantri Mudra Yojana, or business financing schemes in India
    from specific, trusted government and banking websites.

    Args:
        query (str): The search query for loan information 
                     (e.g., "Mudra loan eligibility", "MSME schemes").

    Returns:
        str: A combined string of search results from all sites,
             or a message if no results are found.
    """
    results = []
    
    # Create site-specific queries
    msme_query = f"{query} {MSME_WEBSITE}"
    mudra_query = f"{query} {MUDRA_WEBSITE}"
    sbi_query = f"{query} {SBI_WEBSITE}"
    rbi_query = f"{query} {RBI_WEBSITE}"

    # --- Search relevant government and banking websites ---
    # We run these in separate try/except blocks in case one site fails
    try:
        results.append(f"--- Results from {MSME_WEBSITE} ---\n{search_tool.run(msme_query)}")
    except Exception as e:
        print(f"Error searching {MSME_WEBSITE}: {e}")
        
    try:
        results.append(f"--- Results from {MUDRA_WEBSITE} ---\n{search_tool.run(mudra_query)}")
    except Exception as e:
        print(f"Error searching {MUDRA_WEBSITE}: {e}")

    try:
        results.append(f"--- Results from {SBI_WEBSITE} ---\n{search_tool.run(sbi_query)}")
    except Exception as e:
        print(f"Error searching {SBI_WEBSITE}: {e}")
        
    try:
        results.append(f"--- Results from {RBI_WEBSITE} ---\n{search_tool.run(rbi_query)}")
    except Exception as e:
        print(f"Error searching {RBI_WEBSITE}: {e}")

    # Combine results and return
    # Filter out any potential empty strings before joining
    filtered_results = [r for r in results if r and "No specific results" not in r]
    
    if not filtered_results:
        return "No specific results found from the designated websites. Please try a different query."
    
    combined_results = "\n\n".join(filtered_results)
    return combined_results
