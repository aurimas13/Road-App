<p align=center>
  <img height="300px" src="https://github.com/aurimas13/Tracker/blob/main/public/logo/time_tracker.png"/>
</p>

<p align="center" > <b> Time Tracker </b> </p>
<br>
<p align=center>
  <a href="https://github.com/aurimas13/Tracker/blob/main/LICENSE"><img alt="license" src="https://img.shields.io/npm/l/express"></a>
  <a href="https://twitter.com/aurimasnausedas"><img alt="twitter" src="https://img.shields.io/twitter/follow/aurimasnausedas?style=social"/></a>
</p>

The app tracks the time of stories and tasks. Details of the usage are under [Usage](#usage).
Please refer to [Requirements](#requirements) for importing required libraries before looking at how to use it.

# Table of contents

[//]: # (- [Birthday Reminder App]&#40;#birthday-reminder-app&#41;)

- [Table of contents](#table-of-contents)
- [Requirements](#requirements)
- [Usage](#usage)
- [Navigation](#navigation)
- [Docker](#docker)
- [Tests](#tests)
- [Public](#public)
- [Logo](#photo)
- [License](#license)

# Requirements


[//]: # (`IMPORTANT NOTE:` To run the services you might need to use the virtual environment:)

[//]: # (```)

[//]: # (virtualenv my_env)

[//]: # (source my_env/bin/activate)

[//]: # (```)

**Python 3.10.6** is required to properly execute package's modules, imported libraries and defined functions. 
To install the necessary libraries run [requirements.txt](https://github.com/aurimas13/Tracker/blob/main/requirements.txt) file as shown: `pip install -r requirements.txt`.

For proper usage of the program you might need to run **python3** rather than proposed **python**.<sup>1</sup>


<br><sup>1</sup>**python** or **python3** depends on the way how you installed python of version 3.* on your machine. </br>

# Usage

After the requirements are met, the app package is set at your directory and terminal is run you have to run the flask app:
```
>>> conda create --name tracker 
>>> conda activate tracker 
>>> pip install -r requirements.txt
>>> flask db upgrade 
>>> flask run
```

To look at the functionalities of the app refer to [Navigation](#navigation).


# Navigation

When you run `flask run` you will have a localhost name on terminal like ` Running on http://127.0.0.1:5000`. 
Navigating to **http://localhost:5000/** or **http://localhost:5000/story** will open the web page that at the top has four names:
`Stories`, `Add Story`, `Add Developer`, `Developer summary` and at the bottom questions of whether you want to add a story (`Add Story`)
or add a developer (`Add Developer`).

When you add a developer or two of them a dropdown will appear when creating or updating a task (`Add task` or`Update task`) that will allow to choose developers to be assigned to the task of the story:

- After you press `See Story` you will be redirected to add tasks for it. If you wish to update a story press `Update Story`.
- below if a story has been created or delete it by pressing `Delete Story` at the bottom.
- When you press `See Story` you will be given an option to `Add Task` or if one exists already `Update Task`.
Each task also has `Delete Task` button to delete a task for that story.
- `Developer summary` gives a summary of all developers assigned to do the tasks of stories. 
It estimates points for how long it is estimated to complete the tasks of stories while the actual time taken to 
complete the tasks are calculated for each developer and summarised at `Developer summary`.

# Docker

To build & run docker do these commands: 
`docker build -t tracker .` & `docker run --name tracker_docker -p 5000:5000 tracker`

To run the app ten got and follow what is said at [Navigation](#navigation).

# Tests

By navigating to the program/app folder where it is extracted - [Tracker](https://github.com/aurimas13/Tracker) - one folder before where test folder is held one can run these test commands:

1) To run unit tests in the project folder run:
```
>>> python -m pytest test/unit/test.py

```

2) To run functional tests in the project folder run:
```
>>> python -m pytest test/functional/test.py

```

3) Or run it with `pytest test/functional/test.py` or `pytest test/unit/test.py`

# Public

Public folder contains [todolist text file](https://github.com/aurimas13/Tracker/blob/main/public/todolist.txt) and a Logo folder.

[//]: # (- [task.pdf]&#40;https://github.com/aurimas13/BirthdayReminderApp/blob/main/Public/task.pdf&#41; - the problem for which this program was implemented.)

# Logo

The logo of the Time Tracker can be found [here](https://github.com/aurimas13/Tracker/blob/main/public/logo/time_tracker.png).

# License

The MIT [LICENSE](https://github.com/aurimas13/Tracker/blob/main/LICENSE)
The app

RoadApp (To be updated)
crontab -e (create) only one?
crontab -r (remove)
crontab -l (list)

CRONTAB: 0 * * * * cd ~/Documents/Python/RoadApp && ~/opt/miniconda3/envs/RoadApp/bin/python fetch.py
>>> 0 * * * * cd <directory_to_app> && <directory_to_python>  fetch.py
