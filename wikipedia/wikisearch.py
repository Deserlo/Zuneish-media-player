import wikipediaapi
import asyncio

titles = ["1979 in music", "1979 in film", "1979 in united states"]


def print_sections(sections, level=0):
    for s in sections:
        print("%s: %s - %s" % ("*" * (level + 1), s.title, s.text))
        print_sections(s.sections, level + 1)


def wiki_page_search():
    for title in titles:
        print(title)
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(title)
        print("Page - Exists: %s" % page_py.exists())
        # Page - Exists: True
        if page_py.exists() == True:
            print("Page - Title: %s" % page_py.title)
            # Page - Title: Python (programming language)
            print("Page - Summary: %s" % page_py.summary)
            # Page - Summary: Python is a widely used high-level programming language for
            print_sections(page_py.sections)


'''
page_missing = wiki_wiki.page('NonExistingPageWithStrangeName')
print("Page - Exists: %s" % page_missing.exists())
# Page - Exists: False
'''
