def test_add_developer_post(test_client):
    value = {'developer_name': 'Adam'}
    response = test_client.post("/add_developer", data=value, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/story"


def test_create_delete_story_post(test_client):
    value = {
            'story_name': 'Story Two',
            'status': True,
            'story_description': 'Great one',
            'estimated_points': 5
    }
    response = test_client.post("/add_story", data=value, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/story"
    assert response.get_data(as_text=True).count("<h1>Stories</h1>") == 1
    response_delete = test_client.post("/story/2/delete_story", data=value, follow_redirects=True)
    assert response_delete.status_code == 200
    assert response_delete.request.path == "/story"
    assert response_delete.get_data(as_text=True).count("<div><p>Total time to complete the story <b>Story Two</b>") == 0


def test_story_render_template(test_client):
    response = test_client.get('/story')
    assert '<td>Story One</td>' in response.get_data(as_text=True)
    assert '<b class="padding">Want to create a story?</b>' in response.get_data(as_text=True)
    assert '<b class="padding">Want to add a developer? </b>' in response.get_data(as_text=True)


def test_add_story_render_template(test_client):
    response = test_client.get('/add_story')
    assert '<label for="name">Story name:</label>' in response.get_data(as_text=True)
    assert '<input type="submit" value="Add Story">' in response.get_data(as_text=True)


def test_update_story_post(test_client):
    value = {
        'estimated_points': 10,
        'story_name': 'Story Zero',
        'status': False,
        'story_description': 'Let\'s go',
    }
    response = test_client.post("/story/1/update_story", data=value, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/story"
    assert response.get_data(as_text=True).count("<td>Story Zero</td>") == 1


def test_create_delete_task_post(test_client):
    value = {
        'story_id': 1,
        'task_name': 'Task 1',
        'check': True,
        'task_description': 'Great One',
        'estimated_points': 5,
        'developer': 1,
        'iter': 'From Story 1',
        'actual_time': '1',
    }
    response = test_client.post("/story/1/add_task", data=value, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/story/1"
    assert response.get_data(as_text=True).count("<td>Great One</td>") == 1
    response_delete = test_client.post("/story/1/delete_task/2", data=value, follow_redirects=True)
    assert response_delete.status_code == 200
    assert response_delete.request.path == "/story/1"
    assert response_delete.get_data(as_text=True).count("<td>Great One</td>") == 0


def test_update_task_post(test_client):
    value = {
        'story_id': 1,
        'task_name': 'Task Two',
        'check': True,
        'task_description': 'Updated task',
        'estimated_points': 5,
        'developer': 1,
        'iter': 'From Story One',
        'actual_time': '1',
    }
    response = test_client.post("/story/1/update_task/1", data=value, follow_redirects=True)
    assert response.status_code == 200
    assert len(response.history) == 1
    assert response.request.path == "/story/1"
    assert response.get_data(as_text=True).count("<td>Updated task</td>") == 1


def test_add_task_render_template(test_client):
    response = test_client.get('/story/1/add_task')
    assert '<label for="name">Task name</label>' in response.get_data(as_text=True)
    assert '<span class="input-group-addon text_margin">Please select a developer:</span>' in response.get_data(as_text=True)


def test_update_task_render_template(test_client):
    response = test_client.get('/story/1/update_task/1')
    assert '<label for="estimated_points">Estimated points of the task:</label>' in response.get_data(as_text=True)
    assert '<input id="act" type="checkbox" name="check" value="True">' in response.get_data(as_text=True)
