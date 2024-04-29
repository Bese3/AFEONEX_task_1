# Twitt-Buzz

[![Coverage Status](https://coveralls.io/repos/github/Bese3/AFEONEX_task_1/badge.svg?branch=main)](https://coveralls.io/github/Bese3/AFEONEX_task_1?branch=main)

A simple blog post platform that can create users to create, update or delete a post.

## Requirment

+ Flask
+ Flask-SQLAlchemy
+ Flask-JWT-Extended
+ Redis
+ bcrypt
+ MySQLDB
+ SQLAlchemy
+ use the [Requirment.txt](https://github.com/Bese3/AFEONEX_task_1/blob/main/requirment.txt)

## Application

+ Python3/Flask


## API
### First Level

#### User
```/api/v1/user/create``` Create user using neccassary fields

```/api/vi/user/update/<id>``` Update user

```/api/v1/user/delete/<id>``` Delete user

```/api/v1/user/me/<id>``` get the user

```/api/v1/user/check``` checks if the user is authorized


#### Post
```/api/v1/post/create/<user_id>``` Creates post based on user_id using neccassary fields

```/api/vi/post/update/<user_id>/<post_id>``` Update post

```/api/v1/post/delete/<user_id>/<post_id>``` Delete post

```/api/v1/post/<user_id>``` get all the user's post

```/api/v1/posts``` gets all posts


#### Comment
```/api/v1/comment/create/<post_id>``` Creates comment based on post_id using neccassary fields

```/api/vi/comment/update/<comment_id>``` Update comment

```/api/v1/comment/delete/<user_id>/<comment_id>``` Delete comment of the user


## Installation

After cloning this repository navigate into the root of the project repository and run:
```
$python3 venv your_virtual_env_name
$source your_virtual_env_name/bin/activate
$pip3 install -r requirment..txt
```

## Usage

In order to use the project we have to run the servers, and mysql database
+ note that the below step is only to be executed once to create database and relational tables in mysql
```
$cat set_up_mysql_dev.sql | mysql
$python3 setup_models.py
```

Run servers
```
$python3 -m api.v1.app
```
on another terminal
```
$python3 -m web_api.server
```

then run on your browser
```
http://localhost:5001/
```
