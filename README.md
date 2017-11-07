# Media Center Downloader

## What is It?

This is a script that downloads *torrent* files using EZTV API.

The main goal of said script is to be ran at given time intervals using cron jobs.


## Configuration
In order to make the service work you will need to change two files, _config.json_ and _series.json_.

I will briefly explain what each file should contain.

**config.json**
```
{
    "directories": {
        "torrent": "torrents",
        "database": "series.json",
        "log": "logs.txt"
    },
    "notification": {
        "toAddr": "personal.email@gmail.com",
        "login": "botemail@gmail.com",
        "password": "mySecre7Passw0rd"
    }
}
```

- Directories:
    - torrent: folder to which torrent files will be downloaded.
    - database: name of the file where the required data for the script is stored
    - log: file where logs are written with debug purposes
- Notification:
    - toAddr: email destination for the notification
    - login: login email for the account sending the notification
    - password: password for the provided email

**series.json**
```
{
    "series": [
        {
            "imdbId": "0944947",
            "name": "Game Of Thrones"
        },
        ...
    ]
}
```

This file should a *json* object with a list on which each object contains a name property and the respective imdb ID for that serie. Above we can see the example for Game of Thrones.