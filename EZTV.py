# author: jpbat @ 18:53 01/11/2017
# !/usr/bin/python

import json
import requests


class EZTV(object):

    API_ENDPOINT = "http://eztv.ag/api/get-torrents"

    def __init__(self, torrent_directory):
        self.torrent_directory = torrent_directory

    def get_serie_feed(self, imdb_id):

        response = requests.get(
            self.API_ENDPOINT, params={
                "imdb_id": imdb_id,
                "limit": 100,
            }
        )

        if response.status_code != 200:
            return None

        return response.json()

    def download_torrent(self, torrent):
        url = torrent["torrent_url"]
        local_filename = self.torrent_directory + url.split('/')[-1]
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return local_filename

    def process_torrents(self, new_torrents, logger):

        overview = {}
        downloads = []

        for serie, torrent_list in new_torrents.items():
            logger.log("### Processing torrents for {}".format(serie))
            to_download = {}
            for torrent in torrent_list:
                key = "{}.{}".format(torrent["season"], torrent["episode"])
                to_download[key] = self.solve_conflict(torrent, to_download.get(key))
            overview[serie] = [torrent for _, torrent in to_download.items()]
            downloads += overview[serie]

        logger.log("### Downloading {} torrents".format(len(downloads)))
        for torrent in downloads:
            self.download_torrent(torrent)

        return overview

    def solve_conflict(self, torrent1, torrent2):
        if torrent2 is None:
            return torrent1
        if "1080p" in torrent1:
            return torrent1
        if "1080p" in torrent2:
            return torrent2
        if "720p" in torrent1:
            return torrent1
        if "720p" in torrent2:
            return torrent2
        return torrent1

