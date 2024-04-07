#!/usr/bin/env python3

if __name__ == '__main__':
    from models.post import Post
    from models.user import User
    from models.comment import Comment
    from models.basemodel import db, app

    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(e)
        exit(1)
