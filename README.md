Python backend engineer
You are working as a Python backend engineer at a company that is creating Lithuania roads information aggregation system (roads traffic intensity and weather conditions on the road). You have been given two APIs that produce real-time information:
1. Weather conditions on the road - https://eismoinfo.lt/weather-conditions-service (https://data.gov.lt/dataset/keliu-oru-salygu-duomenys )
2. Traffic intensity - https://eismoinfo.lt/traffic-intensity-service (https://data.gov.lt/dataset/transporto-priemoniu-eismo-duomenys )
The product owner of the roads information aggregation system has asked you to:
3. Store data from real-time APIs in the database
4. Create two endpoints (weather conditions and traffic intensity) that can be used for
sharing aggregated information with other companies
Aggregated information, that the product owner wants services to return are averages of numeric metrics (metrics that are changing, like weather temperature, wind speed, number of vehicles, etc.) for a given period. So API endpoints should accept the id (or multiple ids) of the device and the period for which to calculate the averages.
