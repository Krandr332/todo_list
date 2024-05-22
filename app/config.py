import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/todo_list'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
