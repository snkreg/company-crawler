company-crawler
===============

A simple webcrawler that scrapes data from companies' public pages on Linkedin.


Installation
-----------
1. Install the required packages and its dependencies.
    ```bash
    pip install -r requirements.txt
    ```
2. Start a Mongo database. 

3. From the root, run the scraper.
    ```bash
    scrapy crawl linkedin
    ```
4. Enjoy.

Configuration
-------------

In order to configure the scraper's behaviour, the file ***settings.py*** must be edited.
The file is a set of key/value pairs. Although the file is commented enough, here we
will explain the most important.

1. **DOWNLOAD_DELAY**. It sets the waiting time among requests. By default it's set to two seconds. A lower value will 
yield less throughput, but a higher one will result in the crawler being banned.
2. **DOWNLOAD_TIMEOUT**. The time that must pass before considering the request as 
3. **MONGODB_SERVER**. The ip address where the database is located. By default it points to localhost.
4. **MONGODB_PORT**. The same as above, but in this case it refers to the port where the server is listening.
5. **MONGODB_DB**. The name of the database in the server.
6. **MONGODB_COLLECTION**. The name of the collection into which the information will be stored.
7. **MONGODB_UNIQ_KEY**. The field that's used as key. In this example, the URL of the company is the key.

TODO's
------

- [ ] Enable real-time proxy gathering.
- [ ] Balance load by using Google's cache.

