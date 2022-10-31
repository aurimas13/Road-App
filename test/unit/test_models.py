import glob
import unittest
import sys
import os
topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)
from app.models import Story, Task, Developer, TaskActualTimes


def test_new_story():
    """
    GIVEN a Story model
    WHEN a new Story is created
    THEN check the name, status, description, estimated_time
    """
    story = Story(
        story_name='John',
        status=True,
        description='I\'m awesome',
        estimated_points=11
    )
    assert story.story_name == 'John'
    assert story.status != False
    assert story.description == 'I\'m awesome'
    assert story.estimated_points == 11


def test_new_task():
    """
    GIVEN a Task model
    WHEN a new Task is created
    THEN check story id, name, status, description, estimated_time,. developer id, iteration
    """
    task = Task(
        story_id=1,
        task_name='Emma',
        status=True,
        description='She\'s awesome',
        estimated_points=15,
        developer_id=1,
        iteration="Story #1"
    )
    assert task.story_id == 1
    assert task.task_name == 'Emma'
    assert task.status != False
    assert task.description == 'She\'s awesome'
    assert task.estimated_points == 15
    assert task.developer_id == 1
    assert task.iteration == "Story #1"


def test_new_actual_task_time():
    """
    GIVEN a TaskActualTimes model
    WHEN a new TaskActualTimes is created
    THEN check task id, actual_time
    """
    task_actual = TaskActualTimes(
        task_id=1,
        actual_time=7
    )
    assert task_actual.task_id == 1
    assert task_actual.actual_time == 7


def test_new_developer():
    """
    GIVEN a Developer model
    WHEN a new Developer is created
    THEN check name
    """
    developer = Developer(name = 'Rocky')

    assert developer.name == 'Rocky'

if __name__ == '__main__':
    unittest.main()