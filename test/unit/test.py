from app.models import Story, Task, TaskActualTimes, Developer
from app.developer_service import adding_developer
from app.developer_summary import summarize_developers
from app.story_service import get_story_values
from app.task_service import get_task_values


def test_add_developer():
    test_dev = {'developer_name': 'Adam'}
    assert adding_developer(test_dev) is True
    assert adding_developer(test_dev) is False


def test_developers_summary():
    query = [
        (
            Task(
                story_id=1,
                task_name='Two',
                status=True,
                description='Something is happening again',
                estimated_points=121,
                developer_id=1,
                iteration='Story 1'
            ),
            TaskActualTimes(
                task_id=2,
                actual_time=121
            ),
            Developer(id=1, name='Alex')
        )
    ]
    assert summarize_developers(query) == [{'id': 1, 'name': 'Alex', 'actual_times_sum': 121, 'estimated_points': 121}]


def test_developers_summary_multiple_task_same_developer():
    query = [
        (
            Task(
                story_id=1,
                task_name='Two',
                status=True,
                description='Something is happening again',
                estimated_points=121,
                developer_id=1,
                iteration='Story 1'
            ),
            TaskActualTimes(
                task_id=2,
                actual_time=121
            ),
            Developer(id=1, name='Alex')
        ),
        (
            Task(
                story_id=1,
                task_name='Three',
                status=True,
                description='Something is happening again',
                estimated_points=123,
                developer_id=1,
                iteration='Story 2'
            ),
            TaskActualTimes(
                task_id=2,
                actual_time=125
            ),
            Developer(id=1, name='Alex')
        )
    ]
    assert summarize_developers(query) == [{'id': 1, 'name': 'Alex', 'actual_times_sum': 246, 'estimated_points': 244}]


def test_developers_summary_multiple_tasks_different_developers():
    query = [
        (
            Task(
                story_id=1,
                task_name='Two',
                status=True,
                description='Something is happening again',
                estimated_points=121,
                developer_id=1,
                iteration='Story 1'
            ),
            TaskActualTimes(
                task_id=2,
                actual_time=121
            ),
            Developer(id=1, name='Alex')
        ),
        (
            Task(
                story_id=1,
                task_name='Three',
                status=True,
                description='Something is happening again',
                estimated_points=123,
                developer_id=1,
                iteration='Story 2'
            ),
            TaskActualTimes(
                task_id=3,
                actual_time=125
            ),
            Developer(id=2, name='John')
        )
    ]
    assert summarize_developers(query) == [{'id': 1, 'name': 'Alex', 'actual_times_sum': 121, 'estimated_points': 121},
                                           {'id': 2, 'name': 'John', 'actual_times_sum': 125, 'estimated_points': 123}]


def test_task_values():
    query = [
        (
            Task(
                story_id=1,
                task_name='Two',
                task_id=1,
                status=True,
                description='Something is happening again',
                estimated_points=8,
                developer_id=1,
                iteration='Story 1'
            ),
            TaskActualTimes(
                task_id=1,
                actual_time=5
            )
        )
    ]
    assert get_task_values(query) == [{'story_id': 1,
                                       'task_name': 'Two',
                                       'task_id': 1,
                                       'status': True,
                                       'description': 'Something is happening again',
                                       'estimated_points': 8,
                                       'developer_id': 1,
                                       'iteration': 'Story 1',
                                       'actual_times': [{'task_id': 1, 'actual_time': 5}],
                                       'actual_times_sum': 5}]


def test_story_values():
    query = [
        (
            Story(
                id=1,
                story_name='Story one',
                status=True,
                description='This is great',
                estimated_points=5
            ),
            Task(
                story_id=1,
                task_name='Two',
                task_id=1,
                status=True,
                description='Something is happening again',
                estimated_points=5,
                developer_id=1,
                iteration='Story 1'
            ),
            TaskActualTimes(
                task_id=1,
                actual_time=5
            )
        )
    ]
    assert get_story_values(query) == [{'estimated_points': 5,
                                        'story_name': 'Story one',
                                        'status': True,
                                        'description': 'This is great',
                                        'id': 1,
                                        'actual_times_sum': 5}]
