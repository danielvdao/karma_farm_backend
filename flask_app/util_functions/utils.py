import re

def get_link_id(link):
    match = re.search(r'\/([A-Za-z0-9]*)$', link)
    return str(match.group(1))
