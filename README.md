# Scheduled Toots

This is a small container to regularly check for and send scheduled toots.

It uses a simple filesystem heirachy - files in `new` are checked and their text used as the toot body if needed. Files are then moved into either `done` or `error` depending on their result



### Text format

The file consists of a send time and the body:

```text
time: 11:34

This is a multiline

toot
```

Or, to schedule days into the future
```text
date: 2024-10-21T10:00:00Z

This is a toot which was scheuled quite a while ago
```

If there's need for a content warning, it can also be added
```text
time: 12:30
cw: This is a very bad joke


Two guys walk into a bar. Ouch
```


---

### Running

The script is intended to be run as a cronjob. If done via docker, it looks like

```sh
docker run \
--rm \
-v /home/ben/tmp/jobs:/jobs \
-e MASTODON_TOKEN="<redacted>" \
-e MASTODON_URL="https://mastodon.bentasker.co.uk" \
bentasker12/scheduled-toots::0.1.1
```

Though my instance runs on Kubernetes instead


---

### License

Copyright (c) 2024 B Tasker
Released under [MIT License](https://www.bentasker.co.uk/pages/licenses/mit-license.html)
