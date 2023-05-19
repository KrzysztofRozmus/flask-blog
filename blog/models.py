from blog import db, admin, current_datetime
from flask_login import UserMixin
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import abort
from flask_pagedown.fields import PageDownField
from markdown import markdown
import bleach


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=True)
    email = db.Column(db.String(30), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=current_datetime)
    _is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, username, email, password, _is_admin=None):
        self.username = username
        self.email = email
        self.password = password
        self._is_admin = _is_admin

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Stores markdown post text as HTML
    content_in_html = db.Column(db.Text, nullable=False)

    date_posted = db.Column(db.DateTime, nullable=False, default=current_datetime)
    author = db.Column(db.String, nullable=False, default="Admin")

    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author

    def __repr__(self):
        return f"User('{self.title}', '{self.content}', '{self.author}')"

    # Method converts markdown post text as HTML to database in body_html column.
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.content_in_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


# Grants access to Admin Panel only to Admin.
class UserView(ModelView):
    column_exclude_list = ["password"]
    form_excluded_columns = ["date_joined"]

    def is_accessible(self):
        try:
            if current_user.username == "Admin" and current_user._is_admin == True:
                return current_user.is_authenticated
            else:
                return abort(404)

        except AttributeError:
            return abort(404)


class PostView(ModelView):
    # Extends default admin/model/create.html template.
    create_template = "admin/post_create.html"

    # Extends default admin/model/edit.html template.
    edit_template = "admin/post_edit.html"

    # Replacing TextAreaField for PageDownField.
    def scaffold_form(self):
        form_class = super(PostView, self).scaffold_form()
        form_class.content = PageDownField()
        return form_class

    column_exclude_list = ["content", "content_in_html"]
    form_excluded_columns = ["author", "date_posted", "content_in_html"]
    form_widget_args = {"content": {"rows": 20}}


admin.add_view(UserView(User, db.session))
admin.add_view(PostView(Post, db.session))
db.event.listen(Post.content, 'set', Post.on_changed_body)
