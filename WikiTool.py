import wikipediaapi

class WikiTool:
    def __init__(self):
        user_agent = "ReAct-Agent/1.0 (For research purposes; contact: your-email@example.com)"
        self.wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='en')
    
    def search(self, query):
        """
        Search for a query in Wikipedia and return the summary of the first result.
        """
        page = self.wiki_wiki.page(query)
        if page.exists():
            return page.summary
        else:
            return f"No results found for '{query}'."
    
    def lookup(self, page):
        """
        Look up a specific page in Wikipedia and return its summary.
        """
        wiki_page = self.wiki_wiki.page(page)
        if wiki_page.exists():
            return wiki_page.summary
        else:
            return f"No results found for '{page}'."
