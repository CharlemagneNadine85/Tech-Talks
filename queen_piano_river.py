#!/usr/bin/env python

#pylint: disable=C0103

import os
import time
import sys

# Setting up the database
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
db = SQLAlchemy(app)

# Creating the database
class Forum(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False)
	title = db.Column(db.String(100), nullable=False)
	content = db.Column(db.Text, nullable=False)
	created_at = db.Column(db.DateTime, default=time.time)

db.create_all()

# Index page
@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		# Get the data from the form 
		username = request.form['username']
		title = request.form['title']
		content = request.form['content']
 
		# Store the data in the database
		post = Forum(username=username, title=title, content=content)
		db.session.add(post)
		db.session.commit()
 
		# Redirect to the home page
		return redirect(url_for('index'))

	return render_template('index.html')

# Posts page
@app.route('/posts')
def posts():
	# Get all the posts from the database
	posts = Forum.query.all()

	return render_template('posts.html', posts=posts)

# Post page
@app.route('/post/<int:post_id>')
def post(post_id):
	# Get the post from the database
	post = Forum.query.filter_by(id=post_id).one()

	return render_template('post.html', post=post)

# Edit post 
@app.route('/post/<int:post_id>/edit')
def edit(post_id):
	if request.method == 'POST':
		# Get the form data
		title = request.form['title']
		content = request.form['content']

		# Update post
		post = Forum.query.filter_by(id=post_id).one()
		post.title = title
		post.content = content
		db.session.commit()

		return redirect(url_for('post', post_id=post_id))
	
	# Get the post from the database
	post = Forum.query.filter_by(id=post_id).one()
	return render_template('edit.html', post=post)

# Delete post
@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete(post_id):
	# Delete the post from the database
	post = Forum.query.filter_by(id=post_id).one()
	db.session.delete(post)
	db.session.commit()

	return redirect(url_for('index'))

# Handle errors
@app.errorhandler(500)
def server_error(e):
	return """
	An internal error occurred: <pre>{}</pre>
	See logs for full stacktrace.
	""".format(e), 500

# Run the server
if __name__ == '__main__':
	# if os.name == 'nt':
	# 	app.run(debug=False)
	# else:
	# 	app.run(host='0.0.0.0', debug=False)

	app.run(debug=True)