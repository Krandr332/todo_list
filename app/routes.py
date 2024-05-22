from flask import Blueprint, request, jsonify, abort
from . import db
from .models import Task

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()

    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at,
        'updated_at': task.updated_at
    }), 201

@bp.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at,
        'updated_at': task.updated_at
    } for task in tasks])

@bp.route('/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at,
        'updated_at': task.updated_at
    })

@bp.route('/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if title:
        task.title = title
    if description:
        task.description = description

    db.session.commit()

    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'created_at': task.created_at,
        'updated_at': task.updated_at
    })

@bp.route('/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})
