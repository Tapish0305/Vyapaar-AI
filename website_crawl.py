from langchain_community.document_loaders import RecursiveUrlLoader
from bs4 import BeautifulSoup

def crawl_urls(
    root_url: str,
    max_depth: int = 2,
    prevent_outside: bool = True,
    use_async: bool = True,
    output_format: str = "Text"
):
    extractor = (lambda x: x) if output_format == "HTML" else (lambda x: BeautifulSoup(x, "lxml").get_text())
    loader = RecursiveUrlLoader(
        url=root_url,
        max_depth=max_depth,
        prevent_outside=prevent_outside,
        use_async=use_async,
        extractor=extractor,
    )
    docs = loader.load()
    return [doc.page_content for doc in docs]