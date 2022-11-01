RoadApp (To be updated)
crontab -e (create) only one?
crontab -r (remove)
crontab -l (list)

CRONTAB: 0 * * * * cd ~/Documents/Python/RoadApp && ~/opt/miniconda3/envs/RoadApp/bin/python fetch.py
>>> 0 * * * * cd <directory_to_app> && <directory_to_python>  fetch.py
