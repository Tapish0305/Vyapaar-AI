import os
from smolagents.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
from typing import List

# --- Tavily Client Setup ---
# Load environment variables from .env file
load_dotenv()

# Initialize the Tavily Client
try:
    api_key = os.environ["TAVILY_API_KEY"]
    tavily_client = TavilyClient(api_key=api_key)
    print("Tavily Client initialized successfully.")
except KeyError:
    print("Tavily API key not found. Please set TAVILY_API_KEY in your .env file.")
    tavily_client = None

# --- End of Setup ---


# Define the specific websites to search using the 'site:' operator
MSME_WEBSITE = "site:msme.gov.in"
MUDRA_WEBSITE = "site:mudra.org.in"
SBI_WEBSITE = "site:sbi.co.in"
RBI_WEBSITE = "site:rbi.org.in"

# Combine all trusted sites into one string
# We use the 'OR' operator to tell the search engine to look in any of these sites
TRUSTED_SITES = f"{MSME_WEBSITE} OR {MUDRA_WEBSITE} OR {SBI_WEBSITE} OR {RBI_WEBSITE}"

@tool
def loan_info_tool(query: str) -> str:
    """
    Searches and summarizes information related to MSME loans,
    Pradhan Mantri Mudra Yojana, or business financing schemes in India
    from specific, trusted government and banking websites.

    Args:
        query (str): The search query for loan information 
                     (e.g., "Mudra loan eligibility", "MSME schemes").

    Returns:
        str: A synthesized, clean answer based on context from the trusted sites,
             or a message if no results are found.
    """
    if not tavily_client:
        return "Error: Tavily client is not initialized. Check API key."

    # Create one single, powerful query
    # This tells Tavily: "Answer the user's query, but ONLY use
    # information found on these specific websites."
    combined_query = f"{query} {TRUSTED_SITES}"
    
    print(f"--- Calling Tavily with query: {combined_query} ---")

    try:
        # Use get_search_context, which is designed for AI agents.
        # It finds the best info and returns a clean, summarized string.
        response = tavily_client.get_search_context(
            query=combined_query,
            search_depth="basic",
            max_tokens=2500 # Give it space to find good info
        )
        
        if not response or response.strip() == "":
             return "No specific results found from the designated websites. Please try a different query."
             
        return response
    
    except Exception as e:
        print(f"Error during Tavily search: {e}")
        return f"Error: Failed to perform search due to: {e}"

# --- Test Harness ---
# You can run this file directly (python your_file_name.py) to test the tool
if __name__ == "__main__":
    print("--- Testing loan_info_tool ---")
    
    test_query_1 = "Mudra loan eligibility for women"
    print(f"\nTest Query 1: '{test_query_1}'")
    print(loan_info_tool(test_query_1))
    
    print("\n" + "="*30 + "\n")
    
    test_query_2 = "What is the CGTMSE scheme?"
    print(f"Test Query 2: '{test_query_2}'")
    print(loan_info_tool(test_query_2))