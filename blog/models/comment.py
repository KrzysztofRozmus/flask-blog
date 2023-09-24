from blog import db, current_datetime
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import ForeignKey


class Comment(db.Model):
    id = mapped_column(db.Integer, primary_key=True)
    content = mapped_column(db.Text, nullable=False)
    date_posted = mapped_column(db.DateTime, nullable=False, default=current_datetime)

    user_id = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id = mapped_column(ForeignKey("post.id"), nullable=False)

    # user = relationship('user', backref='comments', lazy=True)
    # post = relationship('Post', backref='comments', lazy=True)

    user = relationship("User", back_populates="comment")
    post = relationship("Post", back_populates="comment")

    def __init__(self, content, user_id, post_id, date_posted=None):
        self.content = content
        self.date_posted = date_posted
        self.user_id = user_id
        self.post_id = post_id

    def __repr__(self):
        return f"User('{self.content}', '{self.date_posted}', '{self.user_id}', '{self.post_id}')"
