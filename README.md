# CommSchoolPythonChallenge

You need to install the following:
asgiref             3.7.2
beautifulsoup4      4.12.2
certifi             2023.7.22
charset-normalizer  3.3.2
click               8.1.7
Django              4.2.7
djangorestframework 3.14.0
dnspython           1.16.0
idna                3.4
lxml                4.9.3
pip                 23.3.1
pymongo             3.11.0
pytz                2023.3.post1
redis               5.0.1
requests            2.31.0
rq                  1.15.1
setuptools          68.2.2
soupsieve           2.5
sqlparse            0.4.4
urllib3             2.0.7
wheel               0.41.3
Postman




POSTMAN: 
You need to add the following API-s:
Scrap - http://127.0.0.1:8000/api/execute_scrapper/
Place new scrap  request - http://127.0.0.1:8000/api/request_scrapper/ 
Get all scrap requests - http://127.0.0.1:8000/api/scrapper_requests/ 
Individual scrap request - http://127.0.0.1:8000/api/scrapper_requests/656b00b25528ebdfcc2d9e79/ 
Get all cars - http://127.0.0.1:8000/api/products/ 
Get individual car - http://127.0.0.1:8000/api/products/98265302/ 
Update car - http://127.0.0.1:8000/api/update_product/98733118/ 
Create car - http://127.0.0.1:8000/api/create_ind_product/ 



Docker 
Inside of docker implement “redis:latest”.



Activating the project

1.
Run Redis engine on default port.

2.
Clone the project from GIT repository.
$ git clone https://annamaisuradze1122@github.com/annamaisuradze1122/CommSchoolPythonChallenge.git

Open terminal. 
$ cd CommSchoolPythonChallenge.git
$ python manage.py runserver


3.
Open another terminal as a separate process.
$ rexport OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
$ rq worker


4. Process flow
- Create scrap request, using, Place new scrap  request API and sending link in the following format: 
	{"url" : "https://www.myauto.ge/ka/pr/90611866/qiravdeba-manqanebi-jipi-mazda-cx-5-2015-	benzini-tbilisi?offerType=superVip" }

- Execute scrap request call, using Scrap API.




