from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson import ObjectId
from . funcs import \
    connect_scraprequest_collection, \
    connect_product_collection, \
    check_product, \
    get_id_from_url, \
    compare_prices, \
    create_car, \
    check_url_matching_pattern, \
    scrap_request_progress, \
    car_average_price
from .tasks import create_product_task
from pymongo import errors
from .serializers import ScrapperSerializer, ProductSerializer
import requests
from redis import Redis
from rq import Queue


# Products
# get all products from DB ORIGINAL
@api_view(['GET'])
def get_all_products(request):
    try:
        collection = connect_product_collection()
        products = list(collection.find({}))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except:
        context = {"message": "Unable to fetch all cars. Try again later."}
        return Response(context)


# get individual product from DB ORIGINAL
@api_view(['GET'])
def get_ind_product(request, pk):
    try:
        collection = connect_product_collection()
        product = collection.find_one({'car_id': int(pk)})
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)
    except:
        context = {"message": "Unable to fetch individual car. Try again later."}
        return Response(context)


# create product in DB ORIGINAL
@api_view(['POST'])
def create_ind_product(request):
    id = get_id_from_url(request.data["url"])
    api = "https://api2.myauto.ge/ka/products/" + f"{id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Accept':'*/*'
        } 
    car_in_db = check_product(id)
    
    if car_in_db:
        context = {"Car already exists in DB"}
        return Response(context)
    else:
        try:
            response = requests.get(api, headers=headers)
            product = response.json().get('data').get('info')
            collection = connect_product_collection()
            collection.insert_one({
                "car_id": product['car_id'],
                'man_id': product['man_id'],
                "model_id": product['model_id'],
                "prod_year": product['prod_year'],
                "price_usd": product['price_usd'],
                "price_value": product['price_value'],
            })
            context = {'text': 'Car successfully created'}
            return Response(context)
        except (errors.ConnectionFailure, errors.ServerSelectionTimeoutError) as e:
            context = {"error": f'{e}'}
            return Response(context)


# update product in DB
@api_view(['PUT'])
def update_ind_product(request, pk):
    collection = connect_product_collection()
    current = collection.find_one({'car_id': int(pk)})
    for item in request.data:
        current_state = {item: int(current[item])}
        update = {'$set': {f'{item}': int(request.data[f'{item}'])}}
        try:
            collection.update_one(current_state, update)
            context = {'message': 'Updated successfully'}
            return Response(context)
        except:
            context = {'message': 'Culd not update the product.'}
            return Response(context)



# SCRAPPERS
# request a scrap
@api_view(['POST'])
def request_scrapper(request):
    url = request.data['url']
    if check_url_matching_pattern(url):
        collection = connect_scraprequest_collection()
        existing = collection.find_one({'link': url})
        if existing:
            context = {'text': "Sorry this scrap request already exists in DB"}
            return Response(context)
        else:
            collection.insert({
                "link": f"{request.data['url']}",
                "status": "Pending"
            })
            context = {"text": "Successfully created scrap request"}
            return Response(context)
    else:
        return Response({"message": "Please provide a valud url"})


# get all scrap requests
@api_view(['GET'])
def get_all_scrap_requests(request):
    collection = connect_scraprequest_collection()
    data = list(collection.find({}))
    print(data)
    for item in data:
        item['_id'] = str(item['_id'])
    serializer = ScrapperSerializer(data, many=True)
    return Response(serializer.data)


# get individual scrap requests
@api_view(['GET'])     
def get_ind_scrap_request(request, pk):
    try:
        collection = connect_scraprequest_collection()
        data = collection.find_one({'_id': ObjectId(pk)})
        serializer = ScrapperSerializer(data, many=False)
        return Response(serializer.data)
    except:
        context = {"message": "Was unable to fetch individual scrap request."}
        return Response(context)


# executing scrap on the li
#@api_view(['GET'])
# def scrapper2(request):
#     collection = connect_scraprequest_collection()
#     scrap_reqs = list(collection.find({"status": "Pending"}))
#     LOCAL_HOST = "http://127.0.0.1:8000/"

#     for item in scrap_reqs:
#         car_id = get_id_from_url(item['link'])
#         carindb = check_product(car_id)
#         if carindb:
#             print('Car exists')
#             # If car exists in DB, we need to compare 'price_usd' in DB and in API   
#             scrap_request_progress(item['link'])
#             return compare_prices(LOCAL_HOST, car_id, carindb, item['link'])
#         else: 
#             print('Creating new car.')
#             #If car does not exist in DB, create one.
#             scrap_request_progress(item['link'])
#             create_car(LOCAL_HOST, item['link'])
#             # q = Queue(connection=Redis())
#             # q.enqueue(create_car, *(LOCAL_HOST, item['link']))
#     return Response({'text': 'createed new product'})




@api_view(['GET'])
def scrapper2(request):
    collection = connect_scraprequest_collection()
    scrap_reqs = list(collection.find({"status": "Pending"}))
    LOCAL_HOST = "http://127.0.0.1:8000/"

    if not scrap_reqs:
        return Response({"text": "Not found."})
    
    for item in scrap_reqs:
        car_id = get_id_from_url(item['link'])
        carindb = check_product(car_id)
        if carindb:
            # If car exists in DB, we need to compare 'price_usd' in DB and in API   
            scrap_request_progress(item['link'])
            compare_prices(LOCAL_HOST, car_id, carindb, item['link'])
            return car_average_price(carindb, item['link'])
        else: 
            scrap_request_progress(item['link'])
            q = Queue(connection=Redis())
            q.enqueue(create_car, *(LOCAL_HOST, item['link']))
            return Response({"text": "Car with this car_id does not exist. We are creating it now. Please try again later."})
    
