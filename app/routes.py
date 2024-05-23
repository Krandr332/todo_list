from flask import Blueprint, request, jsonify, abort
from marshmallow import ValidationError

from app import db
from app.models import Task
from app.schemas.task import TaskSchema
from datetime import datetime

bp = Blueprint('tasks', __name__)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


# Создание задачи
@bp.route('/tasks', methods=['POST'])
def create_task():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    # Валидация данных
    try:
        data = task_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    task = Task(title=data['title'], description=data.get('description', ''))
    db.session.add(task)
    db.session.commit()

    result = task_schema.dump(task)
    return jsonify(result), 201


# Получение списка задач
@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    result = tasks_schema.dump(tasks)
    return jsonify(result), 200


# Получение информации о задаче
@bp.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    result = task_schema.dump(task)
    return jsonify(result), 200


# Обновление задачи
@bp.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    json_data = request.get_json()
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400

    # Валидация данных
    try:
        data = task_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 422

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    task.updated_at = datetime.utcnow()

    db.session.commit()

    result = task_schema.dump(task)
    return jsonify(result), 200


# Удаление задачи
@bp.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task successfully deleted'}), 200
