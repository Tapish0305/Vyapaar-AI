import matplotlib.pyplot as plt
import streamlit as st
def display_chart(response):
    """Utility function to display a chart from a tool's JSON output."""
    if "error" in response:
        st.error(response.get("error"))
        return

    data = response.get("data")
    if data is None or (isinstance(data, (pd.Series, dict)) and not data):
        st.warning("The AI could not find any data to plot for this query.")
        return

    chart_type = response.get("chart_type")
    fig, ax = plt.subplots()

    try:
        if chart_type == "bar":
            df = pd.DataFrame.from_dict(data, orient='index', columns=['value'])
            df.plot(kind='bar', ax=ax, legend=False)
            plt.xticks(rotation=45, ha="right")
        elif chart_type == "pie":
            ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
        elif chart_type == "line":
            pd.Series(data).plot(kind='line', ax=ax, legend=False)
            plt.axhline(0, color='grey', linewidth=0.8)

        ax.set_title(response.get("title", "Chart"))
        ax.set_xlabel(response.get("x_label", ""))
        ax.set_ylabel(response.get("y_label", ""))
        plt.tight_layout()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Failed to plot chart: {e}")
        st.json(data) # Show the raw data for debugging
    finally:
        plt.close(fig)
