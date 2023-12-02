# CommSchoolPythonChallenge

You need to install the following prerequisits:
1. Python
2. Django
3. Redis
4. Postman

### POSTMAN Usage
You need to add the following API-s:
1. Scrap - http://127.0.0.1:8000/api/execute_scrapper/
2. Place new scrap  request - http://127.0.0.1:8000/api/request_scrapper/ 
3. Get all scrap requests - http://127.0.0.1:8000/api/scrapper_requests/ 
4. Individual scrap request - http://127.0.0.1:8000/api/scrapper_requests/656b00b25528ebdfcc2d9e79/ 
5. Get all cars - http://127.0.0.1:8000/api/products/ 
6. Get individual car - http://127.0.0.1:8000/api/products/98265302/ 
7. Update car - http://127.0.0.1:8000/api/update_product/98733118/ 
8. Create car - http://127.0.0.1:8000/api/create_ind_product/ 


### Activating the project

1. Run Redis engine on default port.

2. Clone the project from GIT repository.
```
$ git clone https://annamaisuradze1122@github.com/annamaisuradze1122/CommSchoolPythonChallenge.git
```
#### Open terminal. 
```
$ cd CommSchoolPythonChallenge.git
$ pip install -r requirements.txt
$ python manage.py runserver
```

3. Open another terminal as a separate process.
```
$ export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
$ rq worker
```

4. Process flow
- Create scrap request, using, Place new scrap  request API and sending link in the following format: 
```
 {"url" : "https://www.myauto.ge/ka/pr/90611866/qiravdeba-manqanebi-jipi-mazda-cx-5-2015-benzini-tbilisi?offerType=superVip" }
 ```
- Execute scrap request call, using Scrap API.




