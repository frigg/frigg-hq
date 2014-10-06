# -*- coding: utf8 -*-
import json

import requests
from django.conf import settings


def parse_comment_payload(data):
    if data['comment']['body'] == "retest now please":
        url = data['issue']['pull_request']['url'][29:]
        pr_data = json.loads(github_api_request(url))
        repo_url = "git@github.com:%s/%s.git" % (
            data['repository']['owner']['name'],
            data['repository']['name']
        )

        return {
            'repo_url': repo_url,
            'repo_name': pr_data['head']['repo']['name'],
            'repo_owner': pr_data['head']['repo']['owner']['login'],
            'pull_request_id': pr_data['number'],
            'branch': pr_data['head']['ref'],
            "sha": pr_data['head']['sha']
        }


def parse_pull_request_payload(data):
    if data['action'] == "closed":  # Do nothing if the pull request is being closed
        return None

    repo_url = "git@github.com:%s/%s.git" % (
        data['repository']['owner']['name'],
        data['repository']['name']
    )
    return {
        'repo_url': repo_url,
        'repo_name': data['repository']['name'],
        'repo_owner': data['repository']['owner']['login'],
        'pull_request_id': data['number'],
        'branch': data['pull_request']['head']['ref'],
        "sha": data['pull_request']['head']['sha']
    }


def parse_push_payload(data):
    if data['ref'] == "refs/heads/master":
        repo_url = "git@github.com:%s/%s.git" % (
            data['repository']['owner']['name'],
            data['repository']['name']
        )
        return {
            'repo_url': repo_url,
            'repo_name': data['repository']['name'],
            'repo_owner': data['repository']['owner']['name'],
            'pull_request_id': 0,
            'branch': 'master',
            "sha": data['after']
        }


def comment_on_commit(build, message):
    url = "%s/%s/commits/%s/comments" % (build.project.owner, build.project.name, build.sha)
    return github_api_request(url, {'body': message, 'sha': build.sha})


def get_pull_request_url(build):
    if build.branch == "master":
        return "https://github.com/%s/%s/" % (build.project.owner, build.project.name)

    return "https://github.com/%s/%s/pull/%s" % (build.project.owner, build.project.name,
                                                     build.pull_request_id)


def set_commit_status(build, status, description="Done"):
        url = "%s/%s/statuses/%s" % (build.project.owner, build.project.name, build.sha)

        return github_api_request(url, {
            'state': status,
            'target_url': build.get_absolute_url(),
            'description': description,
            'context': 'build'
        })


def github_api_request(url, data=None):
    url = "https://api.github.com/repos/%s?access_token=%s" % (url, settings.GITHUB_ACCESS_TOKEN)
    if data is None:
        return requests.get(url).text
    else:
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/vnd.github.she-hulk-preview+json'
        }
        return requests.post(url, data=json.dumps(data), headers=headers).text
