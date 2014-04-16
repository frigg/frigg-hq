# coding=utf-8
import json
import threading

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from frigg.builds.models import Build
from frigg.utils import github_api_get_request


def build_pull_request(data):
    repo_url = "git@github.com:%s/%s.git" % (data['repo_owner'], data['repo_name'])

    build = Build.objects.create(git_repository=repo_url,
                                 pull_request_id=data['pull_request_id'],
                                 branch=data['branch'],
                                 sha=data["sha"])

    t = threading.Thread(target=build.run_tests)
    t.setDaemon(True)
    t.start()


@csrf_exempt
def github_webhook(request):
    try:
        event = request.META['HTTP_X_GITHUB_EVENT']
    except KeyError:
        return HttpResponse("Missing HTTP_X_GITHUB_EVENT")

    if event == "issue_comment":
        data = json.loads(request.body)

        print data

        if data['comment']['body'] == "retest now please":
            url = data['issue']['pull_request']['url'][29:]
            pr_data = json.loads(github_api_get_request(url))

            pull_request = {'repo_name': pr_data['head']['repo']['name'],
                            'repo_owner': pr_data['head']['repo']['owner']['login'],
                            'pull_request_id': pr_data['number'],
                            'branch': pr_data['head']['ref'],
                            "sha": pr_data['head']['sha']}

            build_pull_request(pull_request)

    if event == "pull_request":

        print request.body

        data = json.loads(request.body)

        pull_request = {'repo_name': data['repository']['name'],
                        'repo_owner': data['repository']['owner']['login'],
                        'pull_request_id': data['number'],
                        'branch': data['pull_request']['head']['ref'],
                        "sha": data['pull_request']['head']['sha']}

        build_pull_request(pull_request)

    else:
        return HttpResponse("Do nothing :)")

    return HttpResponse(event)