from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from typing import List, Union, Tuple

import aiosmtplib

from config import settings
from infrastructure.utils.s3 import download_file

name = str
file_path = str


async def send_mail(recipient: Union[List[str], str], subject: str, body: str, html: bool = True,
                    files: List[Tuple[name, file_path]] = None, local_files: bool = True):
    config = settings.smtp

    to = recipient if isinstance(recipient, list) else [recipient]

    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = config.user
    message.attach(MIMEText(body, 'html' if html else 'plain'))
    for f in files or []:
        if local_files:
            path = f[1]
        else:
            path = download_file(f[0])
        with open(path, "rb") as file:
            part = MIMEApplication(file.read(), Name=basename(f[0]))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f[0])
        message.attach(part)

    async with aiosmtplib.SMTP(hostname=config.host, port=config.port, use_tls=config.ssl) as smtp:
        await smtp.login(config.user, config.password)
        await smtp.sendmail(config.user, to, message.as_string())
