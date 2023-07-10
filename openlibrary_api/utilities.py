import requests

BASE_URL = "https://openlibrary.org/search.json"


def retrieve_books(filters):
    params = create_query_parameters(filters)
    response = requests.get(f"{BASE_URL}", params=params)
    if response.status_code == requests.codes.ok:
        return response.json()["docs"]
    else:
        raise Exception(f"There was a problem retrieving data: {response.content}")


def create_query_parameters(filters):
    query_dict = {}
    if filters.keyword:
        query_dict["q"] = filters.keyword
    if filters.author:
        query_dict["author"] = filters.author
    if filters.title:
        query_dict["title"] = filters.title
    if filters.publisher:
        query_dict["publisher"] = filters.publisher
    if filters.category:
        query_dict["subject"] = filters.category
    return query_dict
