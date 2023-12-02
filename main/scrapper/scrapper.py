from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson import ObjectId
from ..funcs import \
    connect_scraprequest_collection, \
    connect_product_collection, \
    check_product, \
    get_id_from_url, \
    compare_prices, \
    create_car, \
    check_url_matching_pattern, \
    scrap_request_progress 
from pymongo import errors
from ..serializers  import ScrapperSerializer, ProductSerializer
import requests



# SCRAPPERS
# request a scrap
@api_view(['POST'])
def request_scrapper(request):
    url = request.data['url']
    if check_url_matching_pattern(url):
        collection = connect_scraprequest_collection()
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
    for item in data:
        print(item['_id'])
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
        print(serializer.data)
        return Response(serializer.data)
    except:
        context = {"message": "Was unable to fetch individual scrap request."}
        return Response(context)


# executing scrap on the link given
@api_view(['GET'])
def scrapper(request):
    link = request.data["url"]                  # getting url from request
    car_id = get_id_from_url(link)              # checking url and return a car id
    car_in_db = check_product(car_id)           # cheking if product already exists in db
    LOCAL_HOST = "http://127.0.0.1:8000/"       # localhost api for product creation

    if car_in_db: # If car exists in DB, we need to compare 'price_usd' in DB and in API   
        scrap_request_progress(link)
        return compare_prices(LOCAL_HOST, car_id, car_in_db, link)

    else: # If car does not exist in DB, create one.
        scrap_request_progress(link)
        return create_car(LOCAL_HOST, link)
