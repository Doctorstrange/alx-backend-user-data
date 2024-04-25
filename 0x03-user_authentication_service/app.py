#!/usr/bin/env python3
"""simple Flask app with user authentication
"""
import logging

from flask import Flask, abort, jsonify, redirect, request

from auth import Auth

logging.disable(logging.WARNING)


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """Flask app that has a single GET route ("/")
    and use flask.jsonify to return a JSON
    """
    return jsonify({"message": "Bienvenue"})
