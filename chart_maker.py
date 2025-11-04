from model import hf_chat
from config import model_name
import re
import json
from smolagents import tool

def chart_maker(query: str, retrieved_docs: str) -> dict:
    """
    Generates a structured chart configuration based on a user query and retrieved MSME documents.
    """

    prompt = f""" 
    You are an expert analyst specializing in MSME (Micro, Small, and Medium Enterprises) insights.
    Based on the provided context, perform the requested analysis and respond ONLY in the following format:

    Chart Type: <bar/line/pie>
    Title: <meaningful title>
    x_label: <x-axis label>
    y_label: <y-axis label>
    Data: 'Label1'=Value1, 'Label2'=Value2, ...

    User Query: '{query}'
    Context: '{retrieved_docs}'
    """

    response_text = hf_chat(model_name, prompt)

    try:
        chart_details = {"type": "chart"}

        # --- Extract details using regex ---
        chart_type_match = re.search(r"Chart Type:\s*(\w+)", response_text, re.IGNORECASE)
        chart_details["chart_type"] = chart_type_match.group(1).lower() if chart_type_match else "bar"

        title_match = re.search(r"Title:\s*(.+)", response_text, re.IGNORECASE)
        chart_details["title"] = title_match.group(1).strip() if title_match else "MSME Chart"

        xlabel_match = re.search(r"x_label:\s*(.+)", response_text, re.IGNORECASE)
        chart_details["x_label"] = xlabel_match.group(1).strip() if xlabel_match else ""

        ylabel_match = re.search(r"y_label:\s*(.+)", response_text, re.IGNORECASE)
        chart_details["y_label"] = ylabel_match.group(1).strip() if ylabel_match else ""

        # --- Match key=value data pairs ---
        data_pairs = re.findall(r"['\"]?([\w\s&]+)['\"]?\s*[:=]\s*(\d+)", response_text)
        if data_pairs:
            chart_details["data"] = {key.strip(): int(value) for key, value in data_pairs}
            return chart_details

        # --- If no simple pairs found, maybe JSON data was returned ---
        possible_json = re.search(r"\{[\s\S]*\}", response_text)
        if possible_json:
            try:
                parsed_json = json.loads(possible_json.group(0))
                if isinstance(parsed_json, dict):
                    parsed_json["type"] = "chart"
                    return parsed_json
            except Exception:
                pass

        # --- If still no valid data, raise error ---
        raise ValueError("No valid chart data structure found in AI response.")

    except Exception as e:
        print(f"[chart_maker] Parsing Error: {e}\nRaw response:\n{response_text}")
        # ✅ Return only clean minimal error dict
        return {
            "type": "error",
            "error": f"Chart creation failed. Model response was:\n{response_text[:800]}..."
        }
