import os
import requests
import time
from tqdm import tqdm


# subreddit to scrape
SUBREDDIT = 'FoodPorn'

# number of total submissions to scrape
numSubmissions = 1000

# designate image folder
download_folder = 'images/'
if not os.path.exists(download_folder):
    os.mkdir(download_folder)

# rate limited to 100, so scrape in batches
batches = int(numSubmissions / 100)

# get current timestamp (for batch checkpointing)
before_ts = str(time.time()).split('.')[0]

# get in batches
for i, batch in enumerate(range(batches)):
    print("Processing batch", i)
    
    # using Pushshift (https://pushshift.io/)
    endpoint = 'https://api.pushshift.io/reddit/search/submission/?subreddit=' + SUBREDDIT + '&fields=preview,created_utc&limit=100&before=' + str(before_ts)
    
    response = requests.get(endpoint)
    
    if response.status_code != 200:
        print("error:", response.status_code)
        continue
    
    response_data = response.json()
    
    for submission in tqdm(response_data['data']):      
        
        if 'preview' in submission:      
            img_url = submission['preview']['images'][0]['resolutions'][0]['url']
            img_url = "http://i."+img_url.split('.', 1)[1]
            r = requests.get(img_url)
            if r.status_code == 200:
                img_filepath = download_folder + submission['preview']['images'][0]['id'] + '.jpg'
                img_data = r.content
                with open(img_filepath, 'wb') as handler:
                    handler.write(img_data)
    before_ts = response_data['data'][-1]['created_utc']
