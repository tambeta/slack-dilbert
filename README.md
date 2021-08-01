
# Post comic strips to Slack

A Python application to scrape comic strips (or any pictorial resource) from
the web and and post it to the configured [Slack](https://slack.com/) channel.
Guards against posting a stale resource more than once. Resource providers for
[Dilbert](https://dilbert.com/), [Perry Bible
Fellowship](https://pbfcomics.com/), [Saturday Morning Breakfast
Cereal](https://www.smbc-comics.com/) and [XKCD](https://xkcd.com) have been
implemented.

## Installation

### Python Virtual Environment

The easiest method to install the application is using [Python
virtualenvs](https://docs.python.org/3/tutorial/venv.html):

```
$ git clone https://github.com/tambeta/slack-dilbert.git
$ cd slack-dilbert
$ virtualenv3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ ./dilbert.py
```

### Docker

A `Dockerfile` is provided for simple deployment via Docker. Mount the config
and cache (for the guard file) directories from the host. Example:

```
$ docker build -t dilbert .
$ docker run --rm -v $(pwd)/config:/root/.config -v $(pwd)/cache:/root/.cache \
    dilbert /opt/dilbert/dilbert.py
```

Building a fresh image on a remote host is encapsulated in the `deploy` script,
pass the host name as its first argument and the image name as the second:

```
$ ./deploy my.host.com dilbert
```

## Configuration

* Configure an [incoming
  webhook](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks?next_id=0) for
  your Slack workspace and note the generated webhook URL.

* Configuration for the script is stored in `${XDG_CONFIG_HOME}/dilbertrc`.
  `XDG_CONFIG_HOME` is `${HOME}/.config` by default on Linux-based systems;
  see [XDG Base Directory
  Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
  for details. This file should contain your webhook URL, formatted as:

  ```
  [slack]
  webhook_url = YOUR_WEBHOOK_URL
  ```

* The guard file storing latest posted resource IDs is
  `${XDG_CACHE_HOME}/dilbertts`. `XDG_CACHE_HOME` is `${HOME}/.cache` by
  default on Linux-based systems. The file must initially contain a section for
  every provider you intend to run, for example:

  ```
  [dilbert]
  [pbf]
  [smbc]
  [xkcd]
  ```

* Run `dilbert.py` manually, from a cron job or via another method of your
  preference. The daily strip should be posted to your configured Slack
  channel. See `dilbert.py --help` for available command line options.

