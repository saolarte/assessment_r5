import requests

BASE_URL = "https://www.googleapis.com/books"
    

def retrieve_books(filters):
    query_parameters = build_query(filters)
    response = requests.get(f"{BASE_URL}/v1/volumes", params={ "q":query_parameters })
    if response.status_code == requests.codes.ok:
        
        return response.json().get("items", [])
    else:
        raise Exception(f"There was a problem retrieving data: {response.content}")


def get_book(id):
    response = requests.get(f"{BASE_URL}/v1/volumes/{id}")
    if response.status_code == requests.codes.ok:
        return response.json()
    else:
        raise Exception(f"There was a problem retrieving data: {response.content}")


def build_query(filters):
    query_string = []
    if filters.keyword:
        query_string.append(filters.keyword)
    if filters.author:
        query_string.append(f"inauthor:{filters.author}")
    if filters.title:
        query_string.append(f"intitle:{filters.title}")
    if filters.publisher:
        query_string.append(f"inpublisher:{filters.publisher}")
    if filters.category:
        query_string.append(f"subject:{filters.category}")
    return "+".join(query_string)
