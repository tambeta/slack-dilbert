
# Post the daily Dilbert to Slack

A simple Python script to scrape the Dilbert strip from the Estonian daily
newspaper [Postimees](https://www.postimees.ee/comics) and post it to the
configured [Slack](https://slack.com/) channel. Guards against posting more
than once on a given date.

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

A `Dockerfile` is provided for simple deployment via Docker. The build
requires the `webhook_url` argument (Slack incoming webhook, see below). To
avoid duplicates, the build sets the guard timestamp to the current date -
remove or change `/root/.cache/dilbertts` in the container to enable posting
immediately. Example:

```
docker build --build-arg webhook_url=$SLACK_WEBHOOK_URL -t dilbert .
docker run dilbert /opt/dilbert/dilbert.py
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

* Run `dilbert.py` manually, from a cron job or via another method of your
  preference. The daily strip should be posted to your configured Slack
  channel.

