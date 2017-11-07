# author: jpbat @ 18:53 01/11/2017
# !/usr/bin/python


import json
import time

from EZTV import EZTV
from utils import Database, Notification, Logger, Constants

constants = Constants.load_constants()
database = Database(
    filename=constants["directories"]["database"]
)
notifications = Notification(
    to_addr=constants["notification"]["toAddr"],
    login=constants["notification"]["login"],
    password=constants["notification"]["password"],
)
eztv = EZTV(
    torrent_directory=constants["directories"]["torrent"]
)
logger = Logger(
    filename=constants["directories"]["log"]
)


def process_series(data):

    new_torrents = {}
    last_run = data.get("lastRun", int(time.time()))

    for i in range(len(data["series"])):
        serie = data["series"][i]

        logger.log("### Processing {}".format(serie["name"]))

        try:
            id = serie["imdbId"]
        except KeyError:
            logger.log("No IMDB Id for serie {}".format(serie["name"]))
            continue

        feed = eztv.get_serie_feed(id)

        for torrent in feed["torrents"]:

            if torrent["date_released_unix"] < last_run:
                break

            if serie["name"] not in new_torrents:
                new_torrents[serie["name"]] = []
            new_torrents[serie["name"]].append(torrent)

    data["lastRun"] = int(time.time())

    return data, new_torrents


def main():
    data = database.load_data()
    data, new_torrents = process_series(data)
    overview = eztv.process_torrents(new_torrents, logger)
    database.save_data(data)
    notifications.notify(overview, logger)
    logger.destroy()


if __name__ == '__main__':
    main()
