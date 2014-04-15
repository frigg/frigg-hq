# coding=utf-8
import json
import os
import re

from django.db import models
from fabric.context_managers import lcd
from fabric.operations import local

from fabric.api import settings as fabric_settings

from django.conf import settings
import requests

def github_api_request(url, data):

    url = "https://api.github.com/repos/" + url + "?access_token=%s" % settings.GITHUB_ACCESS_TOKEN

    headers = {'Content-type': 'application/json', 'Accept': 'application/vnd.github.she-hulk-preview+json',}
    print requests.post(url, data=json.dumps(data), headers=headers)._content


class Project(models.Model):
    git_repository = models.CharField(max_length=150, verbose_name="git@github.com:owner/repo.git")
    pull_request_id = models.IntegerField(max_length=150, default=0)
    branch = models.CharField(max_length=100, default="master")

    def get_git_repo_owner_and_name(self):
        """Returns repo owner, repo name"""
        rex = "git@github.com:(\w*)/(\w*).git"
        match = re.match(rex, self.git_repository)

        return match.group(1), match.group(2)

    def run_tests(self):

        self._clone_repo()
        self._run_tox()
        self._set_commit_status()
        self._delete_tmp_folder()

    def _clone_repo(self):
        #Cleanup old if exists..
        self._delete_tmp_folder()
        local("mkdir -p %s" % self.frigg_tmp_directory())
        local("git clone %s %s" % (self.git_repository, self.working_directory()))
        self._run("git checkout %s" % self.branch)

    def _run_tox(self):

        with fabric_settings(warn_only=True):
            result = self._run("tox")

        if result.failed:
            self.add_comment_to_pull_request("Be careful.. the tests failed")
            self._set_commit_status("failure")

        else:
            self.add_comment_to_pull_request("All gooodie good")
            self._set_commit_status("success")

    def get_current_commit_hash(self):
        with lcd(self.working_directory()):
            result = local("git rev-parse HEAD", capture=True)
        return result

    def _run(self, command):
        with lcd(self.working_directory()):
            result = local(command, capture=True)
        return result

    def add_comment_to_pull_request(self, message):
        owner, repo = self.get_git_repo_owner_and_name()

        url = "%s/%s/issues/%s/comments" % (owner, repo, self.pull_request_id, )

        data = {'body': message}

        github_api_request(url, data)

    def _set_commit_status(self, status, description="Done"):
        owner, repo = self.get_git_repo_owner_and_name()
        hash = self.get_current_commit_hash()

        url = "%s/%s/statuses/%s" % (owner, repo, hash)

        data = {'state': status,
                'target_url': 'https://frigg.tind.io',
                'description': description,
                'context': 'build'}

        github_api_request(url, data)

    def _delete_tmp_folder(self):
        if os.path.exists(self.working_directory()):
            local("rm -rf %s" % self.working_directory())

    def working_directory(self):
        return os.path.join(self.frigg_tmp_directory(), str(self.id))

    def frigg_tmp_directory(self):
        return os.path.join(settings.PROJECT_TMP_DIRECTORY, "frigg_working_dir", )
