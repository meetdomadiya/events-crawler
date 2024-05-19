# events-crawler
Python ETL pipeline to crawl lucernefestival events and save them up in postgres DB.

docker-compose for Python Script, Postgres, and pgadmin4

clone the repository using the following command:

```
git clone https://github.com/meetdomadiya/events-crawler.git
```

change to that directory:

```
cd events-crawler
```

run it in detached mode:
```
docker-compose up -d
```

To see the extracted data:

go to this link on your computer http://localhost:5050/browser/

enter the username: admin@admin.com</br>
password: root



Setup database:

1. Open a new terminal in IDE.
2. run the command: ```docker container ls```
3. Copy the container ID of the Postgres container
4. Run the command: ```docker inspect <container_id>```
5. Find the IPAddress.
6. Go to pgadmin4  ``` http://localhost:5050/browser/```
7. Click on "Add New Server".
8. Give Name: ps_db
9. In Connection section host name/address = (IPAdress from 6.), username = root, password = root.
10. You will see the ps_db server and test_db.
11. Find tables in schemas. 


shutting it down: 
```
docker-compose down
```
