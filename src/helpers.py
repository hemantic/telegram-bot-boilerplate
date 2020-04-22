import uuid
import telegram

from io import BytesIO
from os import path


def get_file(file: telegram.File) -> BytesIO:
    attachment = BytesIO()
    attachment.name = str(uuid.uuid4()) + '.' + path.splitext(file.file_path)[1]

    file.download(out=attachment)
    attachment.seek(0, 0)

    return attachment
