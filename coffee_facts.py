from pprint import pprint

import requests
from bs4 import BeautifulSoup
import html5lib


def get_coffee_facts():
    coffee_facts_url = "https://www.coffeeinformer.com/fun-facts-about-coffee/"
    response = requests.get(coffee_facts_url)
    soup = BeautifulSoup(response.text, "html5lib")
    first_fact = soup.select("body > div.site-container > div.site-inner > div > div > main > article > div > h2:nth-child(4)")[0]
    print(first_fact)
    print(type(first_fact))
    facts = []
    facts.append(first_fact)
    for sibling in first_fact.next_siblings:
        if sibling.name == "p" or sibling.name == "h2":
            print(sibling)
            facts.append(sibling)
        else:
            continue
    del facts[-1:-2]
    facts_dict = {}

    for index in range(len(facts)):
        if facts[index].name == "h2":
            print(facts[index].findAll(text=True)[0])
            facts_dict[index] = {}
            facts_dict[index]["header"] = facts[index].findAll(text=True)[0]
            print(facts_dict)
            new_index = index + 1
            try:
                while facts[new_index].name != "h2":
                    facts_dict[index]["content"] = facts[new_index].findAll(text=True)[0]
                    new_index += 1
            except IndexError:
                print(index)
                print(new_index)
                continue
        else:
            continue

    return facts_dict

pprint(get_coffee_facts())



