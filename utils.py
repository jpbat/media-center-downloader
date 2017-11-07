# author: jpbat @ 18:53 01/11/2017
# !/usr/bin/python


import datetime
import json
import platform
import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Logger(object):

    def __init__(self, filename):
        self.file = open(filename, "a")

    def log(self, data):
        now = datetime.datetime.now()
        log = "{} {}".format("[{:%Y-%b-%d %H:%M:%S}]".format(now), data)
        self.file.write(log + "\n")
        self.file.flush()
        print(log)

    def destroy(self):
        self.file.close()


class Database(object):

    def __init__(self, filename):
        self.filename = filename

    def load_data(self):
        try:
            with open(self.filename) as f:
                return json.loads(f.read())
        except IOError:
            print("Unable to find the file {}".format(self.filename))
            return None

    def save_data(self, series):
        with open(self.filename, "w") as f:
            json.dump(
                series, f, sort_keys=True,
                indent=4, separators=(',', ': ')
            )


class Notification(object):

    def __init__(self, to_addr, login, password):
        self.to_addr = to_addr
        self.login = login
        self.password = password

    def send_email(self, body):
        now = datetime.datetime.now()
        fromaddr = "Home Media Center"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = self.to_addr
        msg['Subject'] = "New Episodes {}/{}".format(now.day, now.month)

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.login, self.password)
        text = msg.as_string()
        server.sendmail(fromaddr, self.to_addr, text)
        server.quit()


    def notify(self, data, logger):

        if not data:
            return

        logger.log("### Sending email notification")

        body = "Some new episodes have came out.\n"

        for serie, torrent_list in data.items():
            for torrent in torrent_list:
                body += "{}\n".format(torrent["title"])
        self.send_email(body)


class Constants(object):

    def load_constants():
        path = os.path.dirname(os.path.realpath(__file__))

        if platform.system() == "Windows":
            splitter = "\\"
        else:
            splitter = "/"

        path += splitter

        data = None
        with open(path + "config.json") as f:
            data = json.loads(f.read())

        for key in data["directories"].keys():
            data["directories"][key] = path + data["directories"][key]

        data["directories"]["torrent"] = data["directories"]["torrent"] + splitter

        return data
