# ci.frigg.io
[![Build status](https://ci.frigg.io/badges/frigg/frigg/)](https://ci.frigg.io/frigg/frigg/last/)
[![Coverage status](https://ci.frigg.io/badges/coverage/frigg/frigg/)](https://ci.frigg.io/frigg/frigg/last/)
[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/frigg/frigg?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Requirements Status](https://requires.io/github/frigg/frigg/requirements.svg?branch=master)](https://requires.io/github/frigg/frigg/requirements/?branch=master)

# Setup
```
make
```

### Settings that need to be setup
Add these to `frigg.settings.local`.

* `PROJECT_TMP_DIRECTORY` - The location you want frigg to clone and test projects.
* `SERVER_ADDRESS` - To get the correct domain in comments on Github etc.
* `GITHUB_ACCESS_TOKEN` - Token needed to make the project able to post comments on Github.

# Add projects
Add `http://<your frigg domain>/github-webhook` to the projects webhooks on Github.

## Config file
Frigg supports config file to give details about what kind of tasks to perform. The file
should be named `.frigg.yml` and placed in the root of the project. More information about
the config file can be found on [frigg.io/docs/](https://frigg.io/docs/).
