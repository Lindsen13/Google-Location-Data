# Google-Location-Data
A simple script that converts Google's Location Data from JSON format to a csv.

Read more about it [here](https://python-everything.com/post/136/Google-is-tracking-you%2C-and-you-can-pitch-in-to-analyse-the-data%21.html)


# Google is tracking you, and you can pitch in to analyse the data!

## Requesting your personal data from google to create a Pandas DataFrame with all the locations you have visited

I wasn't aware, but you are able to [download](https://takeout.google.com/) the data that Google collects on you! This is both incredible interesting and terrifying at the same time. Let us for now focus on mainly the first part, that it's incredibly interesting.

I requested all my location data from above's link, which was send to me after 24 hours of waiting. What I got back, was a zipped folder with the following files:

    GoogleLocationData
    ├── Location History
    │   ├── Location History.json
    │   └── Semantic Location History
    │       ├── 2018
    │       │    ├── 2013_DECEMBER.json
    │       │    ├── 2013_NOVEMBER.json
    │       │    ├── ...
    │       │    ├── 2013_FEBRUAR.json
    │       │    └── 2013_JANUARY.json
    │       ├── ...
    │       ├── ...
    │       └── 2019
    │       │    ├── 2019_DECEMBER.json
    │       │    ├── 2019_NOVEMBER.json
    │       │    ├── ...
    │       │    ├── 2019_FEBRUAR.json
    │       │    └── 2019_JANUARY.json
    └── archive_browser.html

Let's have a look at the **GoogleLocationData/Location History/Location History.json** file:

    {
    "locations" : [ {
        "timestampMs" : "1379618430096",
        "latitudeE7" : 518930356,
        "longitudeE7" : 58892968,
        "accuracy" : 13,
        "activity" : [ {
        "timestampMs" : "1379614128129",
        "activity" : [ {
            "type" : "TILTING",
            "confidence" : 100
        } ]
        } ]
    }, {
        "timestampMs" : "1379618431446",
        "latitudeE7" : 518930354,
        "longitudeE7" : 58892966,
        "accuracy" : 13
    }, {
        "timestampMs" : "1379618432387",
        "latitudeE7" : 518930353,
        "longitudeE7" : 58892962,
        "accuracy" : 12
    }, 
    ...
    ,{
        "timestampMs" : "1379618477706",
        "latitudeE7" : 518930486,
        "longitudeE7" : 58893072,
        "accuracy" : 9
    }]

Interesting! We have a **timestampMs** variable (which is the timestamp at that moment in ms), a latitudeE7 variable (which is the latitude multiplied by 10^7) and a longitudeE7 variable (which is the Longitude multiplied by 10^7 as well).

I'd like to convert the **JSON** file to a csv file, for future analysis. I'll do this with the **JSON** library, the **datetime** library and the **pandas** library.

    import json
    import datetime
    import pandas as pd

First, I would like to read in the data, and return a Python dictionary.

    with open('Location History.json') as json_file:
        data = json.load(json_file)

Now, we have a dictionary, but there are some more key-values in there then we need. Therefore, I will loop over each element in the dictionary and append the time and location to a list.

    output_list = []
    for loc in data.get('locations'):
        output_list.append({
            'timestamp':datetime.datetime.fromtimestamp(int(loc.get('timestampMs'))/1000),
            'latitude':loc.get('latitudeE7') / 10**7,
            'longitude':loc.get('longitudeE7') / 10**7
            })

The **output_list** contains all the data I need, in a list of dictionaries. This is easy to convert to a Panda's DataFrame, which allows us to output the data into a csv.

    df = pd.DataFrame(data = output_json)
    df.to_csv('output.csv',index=False)

We now have a csv, consisting of the following:

    print(df.head)

| id     | timestamp               | latitude   | longitude  |
|--------|------------------------ |------------|------------|
| 0      | 2013-05-16 05:45:36.035 | 51,8930356 | 58,892968  |
| 1      | 2013-05-16 05:46:37.225 | 51,8930354 | 58,892966  |
| 2      | 2013-05-16 05:47:37.668 | 51,8930353 | 58,892962  |
| 3      | 2013-05-16 05:48:37.755 | 51,8930486 | 58,893072  |
| 4      | 2013-05-16 05:49:37.772 | 51,8930464 | 58,892999  |
| ...    | ...                     | ...        | ...        |
| 262204 | 2015-02-03 07:45:01.722 | 51,8930057 | 58,892884  |
| 262205 | 2015-02-03 07:50:08.003 | 51,8930093 | 58,892654  |
| 262206 | 2015-02-03 07:55:21.345 | 51,8930008 | 58,893248  |
| 262207 | 2015-04-17 23:36:40.367 | 51,8929410 | 58,892963  |
| 262208 | 2015-04-17 23:39:12.629 | 51,8929137 | 58,892798  |


This is just a sub-section of the data I downloaded and processed. There is much more (location) data available. I have downloaded 5 MB out of 19 GB available of data. Curious to see what more information we can retrieve about ourselves!

This is a little sample of what I did on the 14th of October in 2013:

![Sample usage of Google's data](https://python-everything.com/static/blogpost_content/Google%20Data/output_of_google_data.png)
