import uuid
from io import BytesIO
from os import path

import telegram


def get_file(sent_file: telegram.File) -> BytesIO:
    attachment = BytesIO()
    attachment.name = str(uuid.uuid4()) + '.' + path.splitext(sent_file.file_path)[1]

    sent_file.download(out=attachment)
    attachment.seek(0, 0)

    return attachment
