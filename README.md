<p align=center>
  <img height="300px" src="https://github.com/aurimas13/RoadApp/blob/main/public/images/road_vehicle.jpg"/>
</p>

<p align="center" > <b> Road Analysis App </b> </p>
<br>
<p align=center>
  <a href="https://github.com/aurimas13/RoadApp/blob/main/LICENSE"><img alt="license" src="https://img.shields.io/npm/l/express"></a>
  <a href="https://twitter.com/aurimasnausedas"><img alt="twitter" src="https://img.shields.io/twitter/follow/aurimasnausedas?style=social"/></a>
</p>

The app looks into the API request data of [weather conditions](https://eismoinfo.lt/weather-conditions-service?id=%271166%27)
and [traffic intensities](https://eismoinfo.lt/traffic-intensity-service#) from Lithuanian roads, then analyses it and returns the averages of numerical values.
Details of the usage are under [Usage](#usage). Please refer to [Requirements](#requirements) for importing required libraries before looking at how to use it.

# Table of contents

- [Table of contents](#table-of-contents)
- [Requirements](#requirements)
- [Usage](#usage)
- [Data](#data)
- [API Documentation](#api-documentation)
- [Output](#output)
- [Docker](#docker)
- [Cron Job](#cron-job)
- [Tests](#tests)
- [Public](#public)
- [Logo](#logo)
- [License](#license)
- [Citation](#citation)

# Requirements

**Python 3.10.6** is required to properly execute package's modules, imported libraries and defined functions. 
To install the necessary libraries run [requirements.txt](https://github.com/aurimas13/Tracker/blob/main/requirements.txt) file as shown: `pip install -r requirements.txt`.

For proper usage of the program you might need to run **python3** rather than proposed **python**.<sup>1</sup>

# Usage

After the requirements are met, the app package is set at your directory and terminal. First, to create the database (SQLite for now), run:
```
>>> flask db upgrade 
```

Then you populate the database with some data using `fetch.py`:

```
>>> python fetch.py
```

Afterwards to enable users to run the Flask API, you do that by running:

```
>>> flask run
```

To look at the functionalities of data ingestion refer to [Data](#data), and for the API refer to [API Documentation](#api-documentation).

# Data

- Fetch data from API of [weather conditions](https://eismoinfo.lt/weather-conditions-service?id=%271166%27)
and [traffic intensities](https://eismoinfo.lt/traffic-intensity-service#) to the created database by running `python fetch.py` 
at the directory of the app or simultaneously refer to [Cron Job](#cron-job) to make the data be fetched regularly.

- Look into the SQLite database to identify vehicle ids as ids that you wish to get the averages of through `sqlite3 app.db` 
by running basic SQL command like `select * from weather` or `select * from traffic` and record either a single id like `ids=1222`
or multiple like `ids=415,1015,1068,1222` in the query used for the API (further documentation in [API Documentation](#api-documentation))

The way the ingestion works is that we will ingest only the latest data that was not ingested in a previous batch. The way to determine the
date to ingest from is stored in the **batch_update** table. The diagram of the process is shown below:

<p align=center>
  <img height="500px" src="https://github.com/aurimas13/RoadApp/blob/main/public/images/ingestion-logic.jpg"/>
</p>

<INSERT IMAGE>

# API Documentation

When you run flask you will have a localhost name on terminal like `Running on http://127.0.0.1:5000`. 
Make note of the localhost. While using Docker it may be `0.0.0.0`.
The API endpoints that can be used are:

```GET /weather_conditions```
- this endpoint will return the average numerical metrics for a time period of weather conditions. More visual information about it is [here](#output).

Query Parameters:
ids (required) - this is the list of vehicle ids you want to query
period_start (required) - this is the start date you want to get the average numerical metrics from (format: ```%Y-%m-%d %X```)
period_end (optional) - this is the end date you want to get the average numerical metrics until (format: ```%Y-%m-%d %X```)

Example queries:
```
/weather_conditions?ids=415&period_start=2022-11-01%252012:00:00
/weather_conditions?ids=1015,1068&period_start=2022-11-01%252012:00:00
/weather_conditions?ids=1068,1222,2903&period_start=2022-11-01%252012:00:00&period_end=2022-11-02%252023:00:00
```

```GET /traffic_intensity```
- this endpoint will return the average numerical metrics for a time period of traffic intensity. More visual information about it is [here](#output).

Query Parameters:
ids (required) - this is the list of vehicle ids you want to query
period_start (required) - this is the start date you want to get the average numerical metrics from (format: ```%Y-%m-%d %X```)
period_end (optional) - this is the end date you want to get the average numerical metrics until (format: ```%Y-%m-%d %X```)

Example queries:
```
/traffic_intensity?ids=29&period_start=2022-10-30%252012:00:00
/traffic_intensity?ids=29,140,4400&period_start=2022-11-01%252012:00:00
/traffic_intensity?ids=29,3581,4400&period_start=2022-11-01%252012:00:00&period_end=2022-11-02%252020:00:00
```


# Output

The visual outputs after you follow [Usage](#usage) and [API Documentation](#api-documentation) steps:<sup>2</sup>

- Example of averages from weather conditions for individual ID
<p align=center>
  <img height="550px" src="https://github.com/aurimas13/RoadApp/blob/main/public/images/weather_415.png"/>
</p>

- Example of averages from traffic intensities for individual ID
<p align=center>
  <img height="350px" src="https://github.com/aurimas13/RoadApp/blob/main/public/images/traffic_29.png"/>
</p>

- Examples of averages from weather conditions for multiple IDs
<p align=center>
  <img height="700px" src="https://github.com/aurimas13/RoadApp/blob/main/public/images/weather_1015_1068.png"/>
</p>
<p align=center>
  <img height="700px" src="https://github.com/aurimas13/RoadApp/blob/main/public/images/weather_1068_1222_2903.png"/>
</p>


- Examples of averages from traffic intensities for multiple IDs
<p align=center>
  <img height="700px" src="https://github.com/aurimas13/RoadApp/blob/main/public/images/traffic_29_4400_140.png"/>
</p>
<p align=center>
  <img height="700px" src="https://github.com/aurimas13/RoadApp/blob/main/public/images/traffic_29_4400_3581.png"/>
</p>

# Docker

To build & run docker do these commands: 
```
>>> docker build -t roadapp .
>>> docker run --name roadapp_docker -p 5000:5000 roadapp
```

To run the app then go and follow what is said at [API Documentation](#api-documentation).

# Cron Job

To build cron job run `crontab -e` while to fetch data each hour, 
the syntax could look like this: `0 * * * * cd <directory_to_app> && <directory_to_python> fetch.py`.

Syntax customization for Cron Job can be checked [here](https://crontab.guru/).

# Tests

To run the test, run the following"

1) To run model tests in the project folder run:
```
>>> python -m pytest test/test_models.py

```

2) To run functional tests in the project folder run:
```
>>> python -m pytest test/test_functional.py

```

3) Or run it with `pytest test/test_functional.py` or `pytest test/test_models.py`

# Public

Public folder contains [todolist](https://github.com/aurimas13/RoadApp/blob/main/public/totdolist.txt) text file and
[images](https://github.com/aurimas13/RoadApp/tree/main/public/images) folder.

# Logo

The logo of the RoadApp can be found [here](https://github.com/aurimas13/RoadApp/blob/main/public/images/road_vehicle.jpg).

# License

The [MIT LICENSE](https://github.com/aurimas13/RoadApp/blob/main/LICENSE)

# Citation

<br><sup>1 - **python** or **python3** depends on the way how you installed python of version 3.* on your machine. </sup></br>
<sup>2 - to get the same visualisations of the output use Chrome, download 
[this extension](https://chrome.google.com/webstore/detail/json-viewer-pro/eifflpmocdbdmepbjaopkkhbfmdgijcc)
and in extension settings select theme: Default(Dark).
</sup>
