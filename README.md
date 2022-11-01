<p align=center>
  <img height="300px" src="https://github.com/aurimas13/RoadApp/blob/main/public/logo/road_vehicle.jpg"/>
</p>

<p align="center" > <b> Time Tracker </b> </p>
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
- [Navigation](#navigation)
- [Docker](#docker)
- [Cron Job](#cron-job)
- [Tests](#tests)
- [Public](#public)
- [Logo](#photo)
- [License](#license)

# Requirements

**Python 3.10.6** is required to properly execute package's modules, imported libraries and defined functions. 
To install the necessary libraries run [requirements.txt](https://github.com/aurimas13/Tracker/blob/main/requirements.txt) file as shown: `pip install -r requirements.txt`.

For proper usage of the program you might need to run **python3** rather than proposed **python**.<sup>1</sup>

<br><sup>1</sup>**python** or **python3** depends on the way how you installed python of version 3.* on your machine. </br>

# Usage

After the requirements are met, the app package is set at your directory and terminal is run you have to run the flask app:
```
>>> pip install -r requirements.txt
>>> flask db upgrade 
>>> flask run
```

To look at the functionalities of the app refer to [Navigation](#navigation).

# Navigation

Steps:

1. Run `flask run` on the terminal and make note of the localhost from `Running on http://127.0.0.1:5000.
2. Create the SQLite database by running `flask db init`, `flask db migrate -m "users table"` and `flask db upgrade`.
3. Fetch data from API's of [weather conditions](https://eismoinfo.lt/weather-conditions-service?id=%271166%27)
and [traffic intensities](https://eismoinfo.lt/traffic-intensity-service#) to the created database. by running `python fetch.py` 
at the directory of the app or simultaneously refer to [Cron Job](#cron-job) to make the data be fetched regularly.
4. Look into the SQLite database to identify ids you wish to get averages of through `sqlite3 app.db` by running basic
SQL command like `select * from weather` or `select * from traffic` and record either a single id like `ids=381`
or multiple like `ids=381,404,1222`
5. Define the date you want to start from like `period_start=2022-10-30%252011:00:00` and optionally until
like `period_end=2022-11-01%252011:00:00` where `%25` is simply a space.
6. 'Navigating to **http://127.0.0.1:5000/weather_conditions** or **http://127.0.0.1:5000/traffic_intensity** will return a BAD request
as we need to specify requests like `http://127.0.0.1:5000/weather_conditions?ids=<ids>&period_start=<period_start>&period_end=<period_end>`
or `http://127.0.0.1:5000/traffic_intensity?ids=<ids>&period_start=<period_start>&period_end=<period_end>` where **<ids>** refer to ids as specified in *4<sup>th</sup> step* 
and **<period_start>** with **<period_end>** refer to dates specified in *5<sup>th</sup> step*
7. To analyse weather conditions from [weather API](https://eismoinfo.lt/weather-conditions-service?id=%271166%27) run something like this
`http://127.0.0.1:5000/weather_conditions?ids=381,&period_start=2022-10-30%252011:00:00` or `http://127.0.0.1:5000/weather_conditions?ids=381,404,1222&period_start=2022-10-30%252011:00:00` or 
`http://127.0.0.1:5000/weather_conditions?ids=381,404,1222&period_start=2022-10-30%252011:00:00&period_end=2022-11-01%252011:00:00`.
8. To analyse traffic intensities from [traffic API](https://eismoinfo.lt/traffic-intensity-service#) run something like this
`http://127.0.0.1:5000/traffic_intensity?ids=1545&period_start=2022-10-30%252012:00:00&` or
`http://127.0.0.1:5000/traffic_intensity?ids=1545,2962,4214&period_start=2022-10-30%252012:00:00&` or
`http://127.0.0.1:5000/traffic_intensity?ids=1545,2962,4214&period_start=2022-10-30%252012:00:00&period_end=2022-11-01%252016:55:00`.

# Docker

To build & run docker do these commands: 
`docker build -t roadapp .` & `docker run --name roadapp_docker -p 5000:5000 roadapp`

To run the app then go and follow what is said at [Navigation](#navigation).

# Cron Job

To build cron job in mac terminal run:
``` 
>>> crontab -e
```

The syntax for cronjob when entering terminal could look like this:<sup>1,2,</sup> `0 6 * * * cd <directory_to_app> && <directory_to_python> fetch.py`

<br><sup>1</sup> **<directory_to_app>** - should be the directory where RoadApp folder is like ~/Documents/Python/RoadApp </br>
<br><sup>2</sup> **<directory_to_python>** should be where you installed python on your machine like ~/opt/miniconda3/envs/RoadApp/bin/python </br>

Syntax customization for Cron Job can be checked [here](https://crontab.guru/).

# Tests

By navigating to the program/app folder where it is extracted - [RoadApp](https://github.com/aurimas13/Tracker) - one folder before where test folder is held one can run these test commands:

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

Public folder contains [todolist text file](https://github.com/aurimas13/RoadApp/blob/main/public/totdolist.txt) and a Logo folder.

[//]: # (- [task.pdf]&#40;https://github.com/aurimas13/BirthdayReminderApp/blob/main/Public/task.pdf&#41; - the problem for which this program was implemented.)

# Logo

The logo of the RoadApp can be found [here](https://github.com/aurimas13/RoadApp/blob/main/public/logo/road_vehicle.jpg).

# License

The MIT [LICENSE](https://github.com/aurimas13/Tracker/blob/main/LICENSE)
