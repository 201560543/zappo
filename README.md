# Zappo

To run, please use docker-compose up. 
To re-run, after making changes please user docker-compose build before docker-compose up. 


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