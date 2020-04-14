# Zappo
   
### Docker Setup  (Optional)
1. Using docker compose   
To start, you will have to build the docker image so use ```docker-compose build```.   
To run the docker image, please use ```docker-compose up```.   
To re-run, after making changes please use ```docker-compose build``` before ```docker-compose up```.   
  
2. Using dockerfile     
In our parent directory, if you notice there is a *Dockerfile* as well. You can use this to build your image as well      
```docker build -t <tag> .```   
```docker run <tag>```   
  
To check all your docker images use:  
```docker ps```  


### Running locally
To run the development server, use: ```FLASK_DEBUG=1 flask run```.   

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
     
    
# To run test cases

```python -m unittest discover -s web -p "*_test.py"```


# 3rd Party Connections
All files which maintain any sort of connection with another service is maintained under the connections directory. Presently the MemSQL connection (DBconnections.py) and S3 connection (s3_connection.py) is maintained under this directory. 

This has been done so that our parent directory is as clean as possible.


# Configuration to run S3 APIs
```
pip3 install web/requirements.txt
```

Before you can begin using Boto 3, you should set up authentication credentials. Credentials for your AWS account can be found in the IAM Console. You can create or use an existing user. Go to manage access keys and generate a new set of keys.


```
aws configure
```

Sample URL for S3 on local:

```
http://localhost:5000/s3-connect?file_name=113375995671546834861/0aa281948fvbq2v/2020/April/05e73376-7ec3-471e-b1e1-59919b660501.json
```

