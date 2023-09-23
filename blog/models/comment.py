from blog import db, current_datetime
from flask_login import UserMixin
from sqlalchemy.orm import mapped_column, relationship


class Comment(db.Model):
    id = mapped_column(db.Integer, primary_key=True)
    content = mapped_column(db.Text, nullable=False)
    date_posted = mapped_column(db.DateTime, nullable=False, default=current_datetime)

    user_id = mapped_column(db.ForeignKey("user.id"))
    post_id = mapped_column(db.ForeignKey("post.id"))
    user = relationship('User', backref='comments', lazy=True)
    post = relationship('Post', backref='comments', lazy=True)

    def __init__(self, content,  date_posted=None):
        self.content = content
        self.date_posted = date_posted

    def __repr__(self):
        return f"User('{self.content}', '{self.date_posted}')"
