from model import hf_chat
from config import model_name
def chart_maker(query: str):
    prompt = f"""
        You are an expert analyst specializing in MSME (Micro, Small, and Medium Enterprises) 
        business insights. Your task is to perform a detailed analysis of the entire provided
        transcript based on the user's query related to MSME issues such as GST rates, 
        government subsidy schemes, loan schemes, market trends, and business performance metrics.
        Instructions:
        1. Read the User Query carefully to understand the specific MSME-related analysis required
        (e.g., GST rate comparison, scheme benefits overview, sales growth analysis).
        2. Review the entire transcript context, which includes detailed MSME business data, government policies,
        financial schemes, and regulatory information.
        3. Perform the requested analysis with a focus on MSME business relevance.
        4. Return the results strictly in the simple text format shown in the example.
        Create an appropriate 'Title', 'x_label', and 'y_label' that are MSME business-centric. Do NOT add any conversational text.
        EXAMPLE:
        Chart Type: bar
        Title: GST Rate Comparison Across MSME Sectors
        x_label: MSME Sectors
        y_label: GST Rate (%)
        Data: 'Manufacturing'=18, 'Services'=12, 'Trading'=5
        User Query: '{query}'
        """

    response_text = hf_chat.chat(model_name, prompt)
    try:
        chart_details = {"type": "chart"}
        chart_type_match = re.search(r"Chart Type:\s*(\w+)", response_text, re.IGNORECASE)
        chart_details["chart_type"] = chart_type_match.group(1).lower() if chart_type_match else "bar"
        title_match = re.search(r"Title:\s*(.+)", response_text, re.IGNORECASE)
        chart_details["title"] = title_match.group(1).strip() if title_match else "Holistic Analysis Chart"
        xlabel_match = re.search(r"x_label:\s*(.+)", response_text, re.IGNORECASE)
        chart_details["x_label"] = xlabel_match.group(1).strip() if xlabel_match else ""
        ylabel_match = re.search(r"y_label:\s*(.+)", response_text, re.IGNORECASE)
        chart_details["y_label"] = ylabel_match.group(1).strip() if ylabel_match else ""
        data_pairs = re.findall(r"['\"]?([\w\s&]+)['\"]?\s*[:=]\s*(\d+)", response_text)
        if not data_pairs:
            raise ValueError("No valid data pairs found in the AI's holistic analysis response.")
        chart_details["data"] = {key.strip(): int(value) for key, value in data_pairs}
        return chart_details 
    except Exception as e:
        print(f"Holistic Chart Parsing Error: {e}\nLLM Response was:\n{response_text}")
        return {"type": "chart", "error": "The AI failed to perform the complex analysis."}


def display_chart(response):
    # (This function is unchanged)
    if "error" not in response:
        data = response.get("data")
        is_empty = False
        if data is None: is_empty = True
        elif isinstance(data, pd.Series): is_empty = data.empty
        elif isinstance(data, dict): is_empty = not data
        if is_empty:
            st.warning("The AI could not find any data to plot for this query.")
            return
        chart_type = response.get("chart_type")
        fig, ax = plt.subplots()
        if chart_type == "bar":
            df = pd.DataFrame.from_dict(data, orient='index', columns=['value'])
            df.plot(kind='bar', ax=ax, legend=False); plt.xticks(rotation=45, ha="right")
        elif chart_type == "pie":
            ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90); ax.axis('equal')
        elif chart_type == "line":
            data.plot(kind='line', ax=ax, legend=False)
            plt.axhline(0, color='grey', linewidth=0.8)
        ax.set_title(response.get("title", "Chart"))
        ax.set_xlabel(response.get("x_label", ""))
        ax.set_ylabel(response.get("y_label", ""))
        plt.tight_layout(); st.pyplot(fig)
    else:
        st.error(response.get("error"))