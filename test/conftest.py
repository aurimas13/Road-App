import pytest
from dotenv import load_dotenv

load_dotenv(".env.testing")

import app
from app.models import Story, Developer, Task


def add_data_fixtures():
    fixture_developer = Developer(name='Alex')
    fixture_story = Story(
        estimated_points=10,
        story_name='Story One',
        status=True,
        description='0'
    )
    fixture_task = Task(
        estimated_points=8,
        task_name='Task Two',
        status=True,
        description='Cool Two',
        iteration='Story One',
        story_id=1,
        developer_id=1
    )
    app.db.session.add(fixture_task)
    app.db.session.add(fixture_developer)
    app.db.session.add(fixture_story)
    app.db.session.commit()


@pytest.fixture(scope="module", autouse=True)
def test_client():
    app.db.create_all()
    add_data_fixtures()
    testing_client = app.app.test_client()
    ctx = app.app.app_context()
    ctx.push()

    yield testing_client

    with app.app.app_context():
        app.db.session.remove()
        app.db.drop_all()

    ctx.pop()
