# import os
#
# import werkzeug
# import sys
# from flask import render_template, flash, redirect, url_for, request, Response
# from app import app, db
# from app.models import Weather, Traffic
# from app.developer_service import adding_developer
# from app.developer_summary import summarize_developers
# from app.story_service import get_story_values
# from app.task_service import get_task_values
#
#
# APP_BASE_URL = os.getenv("APP_BASE_URL")
# PORT = os.getenv("PORT")
# @app.route('/', methods=['GET'])
# @app.route('/weather_conditions', methods=['POST', 'GET'])
# def weather_conditions():
#     """
#     This is the method to show stories.
#
#     Query models of Story, Task & TaskActualTimes in query_result and
#     returns a list (stories) after they are filtered.
#
#     return:
#         render_template (str) for getting template
#     """
#     if request.method == 'GET':
#         query_result = db.session.query(Story, Task, TaskActualTimes).join(
#             Task, Story.id == Task.story_id, isouter=True).join(
#             TaskActualTimes, Task.task_id == TaskActualTimes.task_id, isouter=True).all()
#         stories = get_story_values(query_result)
#         return render_template('story.html', title='Stories', stories=stories, host=APP_BASE_URL)
#     if request.method == 'POST':
#         """
#         This is the method for creating a story.
#
#         If request is GET then template is rendered while for POST request
#         it takes the values from frond end, assigns them to Story variables
#         and saves to database.
#
#
#         returns:
#             if GET:
#                 render_template (str) for getting template
#             elif POST:
#                 redirect (werkzeug.wrappers.response.Response)
#         """
#         story = request.form
#         add_story = Story(story_name=story['story_name'],
#                           status='check' in story,
#                           description=story['story_description'],
#                           estimated_points=story['estimated_points'])
#         db.session.add(add_story)
#         db.session.commit()
#         return redirect(url_for('story'))
#
#     return render_template('add_story.html', title='Tracker', host=APP_BASE_URL)
#
#
# @app.route('/traffic_intensity', methods=['POST', 'GET'])
# def traffic_intensity():
#     """
#     This is the method for looking at specific story.
#
#     Query models of Task & TaskActualTimes in query_result and
#     Story, Task & TaskActualTimes in query_result2 while
#     returning lists (tasks & stories) after they are filtered.
#
#     args:
#         id (str) for retrieving story id
#
#     return:
#         render_template (str) for getting template
#     """
#     if request.method == 'GET':
#         query_result = db.session.query(Task, TaskActualTimes).filter(
#             Task.story_id == id).filter(
#             Task.task_id == TaskActualTimes.task_id).all()
#         story = Story.query.filter_by(id=id).first()
#         story = story.__dict__
#         story['actual_times_sum'] = 0
#         tasks = get_task_values(query_result)
#         for task in tasks:
#             story['actual_times_sum'] += task['actual_times_sum']
#         return render_template('task.html', title='Story', id=id, story=story, tasks=tasks, host=APP_BASE_URL)
#     """
#        This is the method for updating a story.
#
#        If request is GET then template is rendered while for POST request
#        it updates the values from frond end, assigns them to Story variables
#        and saves to database.
#
#        args:
#            id (str) for retrieving story id
#
#        returns:
#            if GET:
#                render_template (str) for getting template
#            elif POST:
#                redirect (werkzeug.wrappers.response.Response)
#        """
#     if request.method == 'GET':
#         story = Story.query.get(id)
#         return render_template('update_story.html', title='Tracker', story=story, host=APP_BASE_URL)
#
#     elif request.method == 'POST':
#         item = Story.query.get(id)
#         item.story_name = request.form['story_name']
#         item.status = 'check' in request.form
#         item.description = request.form['story_description']
#         item.estimated_points = request.form['estimated_points']
#         db.session.add(item)
#         db.session.commit()
#         return redirect(url_for('story'))