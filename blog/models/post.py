from blog import db, current_datetime, app, admin
from flask import Markup
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask_admin.form import ImageUploadField
from blog.functions import name_and_save_post_picture
from flask_wtf.file import FileAllowed
from sqlalchemy.orm import mapped_column, relationship


class Post(db.Model):
    id = mapped_column(db.Integer, primary_key=True)
    title = mapped_column(db.String(120), nullable=False)
    content = mapped_column(db.Text, nullable=False)
    author = mapped_column(db.String, nullable=False, default="Admin")
    post_title_pic = mapped_column(db.String(40), nullable=False, default="default_post_title_pic.png")
    date_posted = mapped_column(db.DateTime, nullable=False, default=current_datetime)

    user_id = mapped_column(db.ForeignKey("user.id"))
    user = relationship('User', backref='posts', lazy=True)

    def __init__(self, title, content, author, user_id, user, date_posted=None):
        self.title = title
        self.content = content
        self.author = author
        self.user_id = user_id
        self.user = user
        self.date_posted = date_posted

    def __repr__(self):
        return f"User('{self.title}', '{self.content}', '{self.author}', '{self.date_posted}')"


class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)


class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class PostView(ModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {"content": CKTextAreaField}

    # Exclude columns from create post panel
    form_excluded_columns = ["author", "date_posted", "post_title_pic"]

    # Exclude columns from list of posts panel
    column_exclude_list = ["author", "post_title_pic"]

    form_extra_fields = {"post_title_picture": ImageUploadField(label="Post title picture",
                                                                validators=[FileAllowed(["jpg", "png", "gif"])],
                                                                base_path=app.config['UPLOAD_FOLDER2'],
                                                                namegen=name_and_save_post_picture,
                                                                max_size=(320, 240, True))}

    # Display html text as Markup text on Admin Panel and only 150 characters to save space.
    column_formatters = {'content': lambda view, column, model, parameters: Markup(model.content[:150])}

    def on_model_change(self, form, model, is_created):
        """Method adds created post picture file name by name_and_save_post_picture function to database"""
        if form.post_title_picture.data:
            post_pic_file_name = form.post_title_picture.data.filename
            model.post_title_pic = post_pic_file_name

        return super().on_model_change(form, model, is_created)


admin.add_view(PostView(Post, db.session))
