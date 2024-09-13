Prerequisites - Node (v18.16.0) and Python 3.7+

To install node modules (most likely wont be needed since the zip file comes with the required packages):-

```npm install -y```

To install all necessary python packages :-

```pip install -r requirements.txt```

To run the nodejs app:-

```node index.js```

The app will spin off at localhost:3000

You can individually run the python script using:

```python3 scrape_data.py```


Notes:

Did not create a virtual env (venv) for python packages since sending the packages would increase total filesize to be sent through mail.

The post images are stored in their respective folders after scraping.

User data is stored in the all_user_scrape_data.csv but this gets overwritten everytime the script runs.

The posts have been given serialized numbering since the data for posts is nested.

The users to be scraped can be added by adding values to modifying the users_to_scrape variable in scrape_data.py