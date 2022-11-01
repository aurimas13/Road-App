import json
import unittest


def test_check_weather_endpoint_one_result(test_client):
    """
    GIVEN weather_conditions is queried
    WHEN a request with valid parameters matches one record in database
    THEN we expect a valid response with averages calculated
    """
    expected_response = [{
        'id': 363,
        'period_start': 'Sun, 30 Oct 2022 12:00:00 GMT',
        'period_end': None,
        'statistics': {
            'dangos_temperatura_avg': 7.6,
            'oro_temperatura_avg': 5.9,
            'vejo_greitis_vidut_avg': 1.0,
            'vejo_greitis_maks_avg': 1.4,
            'krituliu_kiekis_avg': 0.5,
            'rasos_taskas_avg': 2.7,
            'sukibimo_koeficientas_avg': 0.8,
            'konstrukcijos_temp_007_avg': 9.6,
            'konstrukcijos_temp_020_avg': 10.0,
            'konstrukcijos_temp_050_avg': 10.8,
            'konstrukcijos_temp_080_avg': 11.7,
            'konstrukcijos_temp_110_avg': 12.6,
            'konstrukcijos_temp_130_avg': 7.0,
            'konstrukcijos_temp_140_avg': 12.9,
            'konstrukcijos_temp_170_avg': 12.6,
            'konstrukcijos_temp_200_avg': 12.9,
        }
    }]
    response = test_client.get("/weather_conditions?ids=363&period_start=2022-10-30%252012:00:00")
    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')) == expected_response
    assert response.request.path == "/weather_conditions"


def test_check_weather_endpoint_multiple_results(test_client):
    """
    GIVEN weather_conditions is queried
    WHEN a request with valid parameters matches multiple records in database
    THEN we expect a valid response with averages calculated
    """
    expected_response = [{
        'id': 363,
        'period_start': 'Sun, 30 Oct 2022 11:00:00 GMT',
        'period_end': 'Tue, 01 Nov 2022 11:00:00 GMT',
        'statistics': {
            'dangos_temperatura_avg': 7.6,
            'oro_temperatura_avg': 6.4,
            'vejo_greitis_vidut_avg': 1.3,
            'vejo_greitis_maks_avg': 1.5,
            'krituliu_kiekis_avg': 0.8,
            'rasos_taskas_avg': 2.8,
            'sukibimo_koeficientas_avg': 0.9,
            'konstrukcijos_temp_007_avg': 14.6,
            'konstrukcijos_temp_020_avg': 15.0,
            'konstrukcijos_temp_050_avg': 12.3,
            'konstrukcijos_temp_080_avg': 12.7,
            'konstrukcijos_temp_110_avg': 13.1,
            'konstrukcijos_temp_130_avg': 38.5,
            'konstrukcijos_temp_140_avg': 13.9,
            'konstrukcijos_temp_170_avg': 13.6,
            'konstrukcijos_temp_200_avg': 13.9,
        }
    }]
    response = test_client.get("/weather_conditions?ids=363&period_start=2022-10-30%252011:00:00&period_end=2022-11-01%252011:00:00")
    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')) == expected_response
    assert response.request.path == "/weather_conditions"


def test_check_weather_endpoint_invalid(test_client):
    """
    GIVEN weather_conditions is queried
    WHEN a request with invalid parameters to weather_conditions endpoint
    THEN we expect a validation error
    """
    response = test_client.get("/weather_conditions?ids=363&period_end=2022-11-01%252011:00:00")
    assert response.status_code == 400
    assert response.data.decode('utf-8') == json.dumps({"error": "Your request URL has invalid parameters"})
    assert response.request.path == "/weather_conditions"


def test_check_traffic_endpoint_one_results(test_client):
    """
    GIVEN traffic_intensity is queried
    WHEN a request with valid parameters matches one record in database
    THEN we expect a valid response with averages calculated
    """
    expected_response = [{
        'id': 3611,
        'period_start': 'Sun, 30 Oct 2022 12:00:00 GMT',
        'period_end': 'Mon, 31 Oct 2022 16:55:00 GMT',
        'statistics': {
            'winterSpeed_avg': 60.0,
            'summerSpeed_avg': 80.0,
            'averageSpeed_avg': 106.3,
            'numberOfVehicles_avg': 72.0
        }
    }]
    response = test_client.get("/traffic_intensity?ids=3611&period_start=2022-10-30%252012:00:00&period_end=2022-10-31%252016:55:00")
    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')) == expected_response
    assert response.request.path == "/traffic_intensity"


def test_check_traffic_endpoint_multiple_results(test_client):
    """
    GIVEN traffic_intensity is queried
    WHEN a request with valid parameters matches multiple records in database
    THEN we expect a valid response with averages calculated
    """
    expected_response = [{
        'id': 3611,
        'period_start': 'Sun, 30 Oct 2022 12:00:00 GMT',
        'period_end': 'Tue, 01 Nov 2022 11:00:00 GMT',
        'statistics': {
            'winterSpeed_avg': 65.0,
            'summerSpeed_avg': 85.0,
            'averageSpeed_avg': 95.2,
            'numberOfVehicles_avg': 71.0
        }
    }]
    response = test_client.get("/traffic_intensity?ids=3611&period_start=2022-10-30%252012:00:00&period_end=2022-11-01%252011:00:00")
    assert response.status_code == 200
    assert json.loads(response.data.decode('utf-8')) == expected_response
    assert response.request.path == "/traffic_intensity"


def test_check_traffic_endpoint_invalid(test_client):
    """
    GIVEN traffic_intensity is queried
    WHEN a request with invalid parameters to traffic_intensity endpoint
    THEN we expect a validation error
    """
    response = test_client.get("/traffic_intensity?period_start=2022-10-30%252012:00:00&period_end=2022-11-01%252011:00:00")
    assert response.status_code == 400
    assert response.data.decode('utf-8') == json.dumps({"error": "Your request URL has invalid parameters"})
    assert response.request.path == "/traffic_intensity"


if __name__ == '__main__':
    unittest.main()
