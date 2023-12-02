from rest_framework.response import Response
from pymongo import MongoClient, errors
import re
import requests
import random
import time


uri = "mongodb+srv://annamaisuradze0:w02KuWcDG5F3ToZ1@test.hr2gyjl.mongodb.net/?retryWrites=true&w=majority"



# DB connect
def connect_product_collection():
    try:
        client = MongoClient(uri, connect=False)
        database = client.get_database('products')
        collection = database.get_collection('products')
        return collection
    except (errors.ConnectionFailure, errors.ServerSelectionTimeoutError) as e:
        raise e


def connect_scraprequest_collection():
    try:
        client = MongoClient(uri)
        database = client.get_database('products')
        collection = database.get_collection('scraprequest')
        return collection
    except (errors.ConnectionFailure, errors.ServerSelectionTimeoutError) as e:
        context = {"text": f"{e}"}
        return context


# URL Regexpressions 
def get_id_from_url(url):
    print(f' this is get id from url : {url}')
    pattern = re.compile(r'https://www\.myauto\.ge/ka/pr/(\d+)/')
    match = pattern.match(url)

    if match:
        id = match.group(1)
        return id
    else:
        return ("The url does not match the pattern. Please provide the valid url.")


def check_url_matching_pattern(url):
    pattern = re.compile(r'https://www\.myauto\.ge/ka/pr/(\d+)/')
    match = pattern.match(url)

    if match:
        return True
    else:
        return False


# Products
def check_product(pk):
    collection = connect_product_collection()
    product = collection.find_one({'car_id': int(pk)})
    if product:
        return product
    else:
        return False


def compare_prices(LOCAL_HOST, car_id, car_in_db, link):
    api = "https://api2.myauto.ge/ka/products/" + f"{car_id}"
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Accept':'*/*'
            } 
    response = requests.get(api, headers=headers)
    car = response.json().get('data').get('info')

    if (car) and (car['price_usd'] != car_in_db['price_usd']):
        try:
            update_car = requests.put(
                url=f'{LOCAL_HOST}/api/update_product/{car_id}/',
                json={"price_usd": car['price_usd']})
            update_car()
            # scrap_request_success(link)
            context = {"text": "Updated car data"}
            return Response(context)
        except:
            return Response(scrap_request_failure(link))
    elif (car) and (car['price_usd'] == car_in_db['price_usd']):
        # scrap_request_success(link)
        context = {"text": "No changes needed."}
        return Response(context)


def create_car(LOCAL_HOST, link):
    # try:
        create_product = requests.post(
            url=f'{LOCAL_HOST}/api/create_ind_product/',
            json={"url": link})
        # scrap_request_success(link)
    # except:
    #     scrap_request_failure(link)


def car_average_price(car, link, car_id=None):
    collection = connect_product_collection()
    cars = list(collection.find({"model_id": car["model_id"], "prod_year": car["prod_year"]}))
    if not cars:
        context = {"text": "Sorry there are no cars with similar model and production year."}
        scrap_request_failure(link)
        return Response(context)
    
    cars_list = 0
    for item in cars:
        cars_list = cars_list + (item["price_usd"])
    average_price = cars_list/len(cars)
    scrap_request_success(link)
    context = {"average price": average_price}
    return Response(context)


# SCRAP request status updated
# In progress
def scrap_request_progress(link):
    collection = connect_scraprequest_collection()
    request = collection.find_one({'link': link})
    if request:
        current_state = {'status': request['status']}
        update = {'$set': {'status': 'Inprogress'}}
        try:
            collection.update_one(current_state, update)
            context = {'text': 'Successfully updated request status to Inprogress.'}
            return Response(context)
        except:
            context = {'text': 'Could not update request status.'}
            return Response(context)
    else:
        context = {'text': 'No  scrap request found to update the status.'}
        return Response(context)   


# Success
def scrap_request_success(link):
    collection = connect_scraprequest_collection()
    request = collection.find_one({'link': link})
    if request:
        current_state = {'status': request['status']}
        update = {'$set': {'status': 'Success'}}
        try:
            collection.update_one(current_state, update)
        except:
            pass

# Faillure
def scrap_request_failure(link):
    collection = connect_scraprequest_collection()
    request = collection.find_one({'link': link})
    if request:
        current_state = {'status': request['status']}
        update = {'$set': {'status': 'Failure'}}
        try:
            collection.update_one(current_state, update)
        except:
            pass