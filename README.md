company-crawler
===============

A simple webcrawler that scrapes data from companies' public pages on Linkedin.


Installation
-----------
1. Install the required packages and its dependencies.
    ```bash
    pip install -r requirements.txt
    ```
2. Start a Mongo database. Take a look at settings.py if you want to change the address and/or the port. By default, the crawler expects the database to be listening on localhost:27017.

3. From the root of the repository, run the crawler with the following command.
    ```bash
    scrapy crawl linkedin
    ```
4. Enjoy, but note that in this version the crawler will eventually be banned. Increase the **DOWNLOAD_DELAY** to avoid that, or supply a valid proxy list. See configuration options below to know more details.

Configuration
-------------

In order to configure the scraper's behaviour, the file ***settings.py*** must be edited.
The file is a set of key/value pairs. Although the file is commented enough, here we
will explain the most important variables. Please note that this variables
shouldn't, in any case, be removed. 

1. **DOWNLOAD_DELAY**. It sets the waiting time among requests. By default it's set to two seconds. A lower value will 
yield less throughput, but a higher one will result in the crawler being banned.
2. **DOWNLOAD_TIMEOUT**. The time that must pass before considering the request as 
3. **MONGODB_SERVER**. The ip address where the database is located. By default it points to localhost.
4. **MONGODB_PORT**. The same as above, but in this case it refers to the port where the server is listening.
5. **MONGODB_DB**. The name of the database in the server.
6. **MONGODB_COLLECTION**. The name of the collection into which the information will be stored.
7. **MONGODB_UNIQ_KEY**. The field that's used as key. In this example, the URL of the company is the key.
8. **PROXY_FILE_PATH**. This field references the absolute path of the proxy list. Each line in this file should contain a proxy address, in the form IP:PORT. If the value is set to None, the proxy will be disabled.
9. **MINIMUM_LEVEL_FOR_PROXY**. It indicates at which level could be an option to use a proxy. If the value is set to zero, every resquest will be eligible for proxy forwarding.
10. **PROXY_CHANCE**. It goes from zero to ten. Zero means that a proxy will never be used, and ten means otherwise.
11. **MIN_ATTEMPTS**. The maximum number of times that a proxy can fail to answer. Once this threshold is surpassed, the proxy will no longer be used.
12. **COMPANY_LETTERS**. A string that contains all the letters that will be used to look up the companies in Linkedin. For example, if COMPANY_LETTERS='axz', the crawler will retrieve all the companies which have either 'a' or 'x' or 'z' as the first letter in their name. 
13. **LOG_LEVEL**. The level of detail at which the log will be printed. The variable should take either 'DEBUG' or 'INFO'.


TODO's
------

- [ ] Better handling of failing proxies.
- [ ] Enable real-time proxy gathering.
- [ ] Migrate the project towards a standalone script.
- [ ] Create several spiders and distribute the task among them.
