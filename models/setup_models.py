#!/usr/bin/env python3

if __name__ == '__main__':
    from post import Post
    from user import User
    from comment import Comment
    from basemodel import db, app

    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(e)
        exit(1)
