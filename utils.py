import re 

def get_link_id(link):
    match = re.search(r'comments\/(.+)\/(.+)\/', link)
    return str(match.group(1))
  
