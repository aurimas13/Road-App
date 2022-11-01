def test_check_weather_endpoint(test_client):
    response = test_client.get("/weather_conditions?ids=363&period_start=2022-10-30%252012:00:00")
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/weather_conditions"


def test_check_traffic_endpoint(test_client):
    response_delete = test_client.get("/traffic_intensity?ids=3611&period_start=2022-10-30%252012:00:00")
    assert response_delete.status_code == 200
    assert response_delete.request.path == "/traffic_intensity"




