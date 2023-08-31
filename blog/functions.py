from blog import app
from werkzeug.utils import secure_filename
from secrets import token_hex
import os
# import hashlib
from PIL import Image


def save_profile_picture(profile_pic_form):
    """ Save profile picture changed by user to database and static/profile_pic folder.

        :param profile_pic_form: just type picture form without any methods after dot.
    """

    picture_size = (128, 128)

    # The underscore character is used here to pass a variable that we will not use.
    _, picture_file_extension = os.path.splitext(profile_pic_form.picture.data.filename)

    random_pic_file_name = token_hex(9)

    # Uncomment and use hashlib library instead of token_hex function if needed.
    # file_name = hashlib.sha256().hexdigest()

    # You need to use secure_filename function to prevent unauthorized upload files.
    secured_pic_file_name = secure_filename(random_pic_file_name + picture_file_extension)

    picture_path = os.path.join(app.config['UPLOAD_FOLDER'], secured_pic_file_name)

    with Image.open(profile_pic_form.picture.data) as i:
        i.thumbnail(picture_size)
        i.save(picture_path)

    return secured_pic_file_name
