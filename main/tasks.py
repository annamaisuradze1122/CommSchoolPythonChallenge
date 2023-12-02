import requests


LOCAL_HOST = "http://127.0.0.1:8000/"       # localhost api for product creation


def create_product_task(link):
    requests.post(
        url=f'{LOCAL_HOST}/api/create_ind_product/',
        json={"url": link}
    )
