# coding=utf-8
import json
from django.conf import settings
import requests


def github_api_request(url, data):
    url = "https://api.github.com/repos/" + url + "?access_token=%s" % settings.GITHUB_ACCESS_TOKEN
    headers = {'Content-type': 'application/json',
               'Accept': 'application/vnd.github.she-hulk-preview+json', }

    return requests.post(url, data=json.dumps(data), headers=headers)._content


def github_api_get_request(url):
    url = "https://api.github.com/repos/" + url + "?access_token=%s" % settings.GITHUB_ACCESS_TOKEN
    return requests.get(url)._content