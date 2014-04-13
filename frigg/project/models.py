import os

from django.db import models
from fabric.operations import run, local
from fabric.context_managers import cd

from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=100)
    repo_git = models.CharField(max_length=150)
    branch = models.CharField(max_length=100, default="master")

    def run_tests(self):
        self._create_tmp_folder()
        self._clone_repo()
        self._run_tox()
        self._run_flake8()
        self._set_commit_status()
        self._delete_tmp_folder()

    def _clone_repo(self):
        self._run("rsync -av --exclude='.*' ~/code/balder.tind.io .")
        #self._run("git clone %s" % self.repo_git)
        #self._run("git checkout %s" % self.branch)

    def _run_tox(self):
        self._run("tox")

    def _run_flake8(self):
        self._run("flake8")

    def _run(self, command):
        with cd(self.working_directory()):
            local(command)

    def _create_tmp_folder(self):
        self._run("mkdir -p %s" % self.working_directory())

    def _delete_tmp_folder(self):
        self._run("rm -rf %s" % self.working_directory())

    def working_directory(self):
        return os.path.join(settings.PROJECT_TMP_DIRECTORY, "frigg_working_dir", str(self.id))
