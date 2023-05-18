from flask_restful import Resource, abort
from flask import jsonify
from data.contests import Contest
from data import db_session
from requests import get


db_session.global_init("database/db.sqlite")

def abort_if_task_not_found(contest_id):
    db_sess = db_session.create_session()
    contest = db_sess.query(Contest).get(contest_id)
    task_data = contest.tasks
    if not contest or not task_data:
        abort(404, message=f"Contest or task not found {contest} {task_data}")


class TaskResource(Resource):
    def get(self, contest_id):
        abort_if_task_not_found(contest_id)
        db_sess = db_session.create_session()
        contest = db_sess.query(Contest).get(contest_id)
        tasks_data = contest.tasks
        json_file = {}
        for task in tasks_data:
            json_file.update({f'{tasks_data.index(task) + 1}': 
                              {
                                  'input': task.input, 
                                  'output': task.output
                              }})

        return jsonify(json_file)
