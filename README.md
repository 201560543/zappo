# Zappo
   
### Docker Setup  (Optional)
1. Using docker compose   
To start, you will have to build the docker image so use ```docker-compose build```.   
To run the docker image, please use ```docker-compose up```.   
To re-run, after making changes please use ```docker-compose build``` before ```docker-compose up```.   
  
2. Using dockerfile     
In our parent directory, if you notice there is a *Dockerfile* as well. You can use this to build your image as well      
```docker build -t <tag> .```   
```docker run -p 5000:5000 <tag>```   
  
To check all your docker images use:  
```docker ps```  


### To run migrations:
1. First time init
```python3 manage.py db init``` (This is a one time task.)

2. Migrate new changes
```python3 manage.py db migrate```

3. Upgrade / Get new changes
```python3 manage.py db upgrade```


### Running locally
To run the development server, use: ```FLASK_DEBUG=1 flask run```.  Even ```python3 run.py``` works. 

Please do make sure to change the directory to web before running the flask run
as the main application is inside web. ```cd web ```  

Remember to set environment variables.

For local, kindly run the following command to get the mysql port:  
```
ps aux | grep mysql
```
  
followed by. 

```
export DB_PORT=3306
```

Also create a database for the migrations to run.

```
create database zapoo;
```
     
    
# To run test cases

```python -m unittest discover -s app -p "*_test.py"```


# 3rd Party Connections
All files which maintain any sort of connection with another service is maintained under the connections directory. Presently the MemSQL connection (DBweb.connections.py) and S3 connection (s3_connection.py) is maintained under this directory. 

This has been done so that our parent directory is as clean as possible.

# Circle CI
We have a circle CI setup to validate all our tests when we push our code and create a pull request. You can also validate the tests locally. You can also run circleci locally:

```
circleci config process .circleci/config.yml > process.yml
```

```
circleci local execute -c process.yml --job build
```

# Configuration to run S3 APIs
```
pip3 install app/requirements.txt
```

Before you can begin using Boto 3, you should set up authentication credentials. Credentials for your AWS account can be found in the IAM Console. You can create or use an existing user. Go to manage access keys and generate a new set of keys.


```
aws configure
```

Sample URL for S3 on local:

```
http://localhost:5000/api/s3-connect?file_name=113375995671546834861/0aa281948fvbq2v/2020/April/05e73376-7ec3-471e-b1e1-59919b660501.json
```

# API Reference

## API Utility (Non-DB)

All routes here are preceded with `/api/` (e.g. `/api/s3-connect`)

`/connection`
- Method: GET
- Desc: Test database connection by running `SHOW DATABASES`

`/s3-connect`
- Method: GET
- Params:
    - file_name: filename/key of the json object within the S3 Bucket "uploads-results-prod.zappotrack.com"
- Desc: Preprocess and display the output of Textract's json invoice scan

`/s3-upload`
- Method: POST
- Header: Content-Type:application/json
- Body params:
    - file_name:  filename/key of the json object within the S3 Bucket "uploads-results-prod.zappotrack.com"
- Desc: Preprocess and upload Textract's json invoice scan. Upload will go to S3 Bucket "invoiceupload-memsql"
    - The file naming convention is as follows:
        - export/`header or lineitem`/`account_number`/`year`/`month`/`day`-`hour`-`minute`-`millisecond`\_`random integer`\_`invoice number`

## DB General GETs
- `/account/`
- `/address/`
- `/organization/`
- `/supplier/`
- `/person/`
- `/person_account/`
- `/restaurant/`

## DB POSTs

`/account/new_account`
- Method: POST
- Header: Content-Type:application/json
- Body params:
    - organization_name
    - org_country_id
    - org_street_address
    - org_postal_code
    - org_provice_state (As of 5/11, this field has not yet been added to DB table. Do not use)
    - org_city
    - loc_country_id
    - loc_street_address
    - loc_postal_code
    - loc_provice_state (As of 5/11, this field has not yet been added to DB table. Do not use)
    - loc_city
    - account_name
    - first_name
    - last_name
    - email
    - auth0_id (As of 5/11, this field has not yet been added to DB table. Do not use)
    - is_admin
    - role_name

`/account/add_account`
- Method: POST
- Header: Content-Type:application/json
- Body params:
    - organization_id
    - loc_country_id
    - loc_street_address
    - loc_postal_code
    - loc_provice_state (As of 5/11, this field has not yet been added to DB table. Do not use)
    - loc_city
    - account_name
