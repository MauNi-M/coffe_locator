from pprint import pp

import requests
from bs4 import BeautifulSoup
import html5lib


def get_coffee_facts():
    coffee_facts_url = "https://www.goodhousekeeping.com/health/diet-nutrition/a30303/facts-about-coffee/"
    response = requests.get(coffee_facts_url)
    soup = BeautifulSoup(response.text, "html5lib")
    # first fact header
    first_fact = soup.select("div.article-body-content > h2")[0]
    print(f"first header: {first_fact}, type: {type(first_fact)}")
    facts = [first_fact]
    for sibling in first_fact.next_siblings:
        if sibling.name == "p" or sibling.name == "h2":
            facts.append(sibling)
        else:
            continue
    facts_dict = {}

    for index in range(len(facts)):
        current_tag = facts[index]
        if current_tag.name == "h2":
            facts_dict[index] = {}
            facts_dict[index]["header"] = [tx for tx in current_tag.stripped_strings][0]
            next_tag = facts[index+1]
            facts_dict[index]["content"] = " ".join([tx for tx in next_tag.stripped_strings])
        else:
            continue
    pp(facts_dict)
    return facts_dict
