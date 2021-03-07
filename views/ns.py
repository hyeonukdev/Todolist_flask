import os
from flask import Flask, flash, render_template, session, url_for, request, redirect, send_from_directory, escape
from werkzeug.utils import secure_filename
from flask import Blueprint
import pymysql
from datetime import datetime
import app

ns = Blueprint('ns', __name__, url_prefix='/api')


@app.route('/', methods=['GET'])
def root():
    return "This is root"