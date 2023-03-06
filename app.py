import os
import requests

from flask import Flask, request
from github import Github, GithubIntegration


app = Flask(__name__)
# MAKE SURE TO CHANGE TO YOUR APP NUMBER!!!!!
app_id = '301827'
# Read the bot certificate
with open(
        os.path.normpath(os.path.expanduser('/Users/jharkar/Downloads/jh-pr-meme-bot-777.2023-03-06.private-key.pem')),
        'r'
) as cert_file:
    app_key = cert_file.read()

# Create an GitHub integration instance
git_integration = GithubIntegration(
    app_id,
    app_key,
)


@app.route("/", methods=['POST'])
def bot():
    # Get the event payload
    payload = request.json

    print("**********xxxxxxxxx*************")

    # Check if the event is a GitHub PR creation event
    if not all(k in payload.keys() for k in ['action', 'pull_request']) and \
            payload['action'] == 'opened':
        return "ok"

    print("**********2222*************")

    owner = payload['repository']['owner']['login']
    print("**********3333*************")
    repo_name = payload['repository']['name']
    print("**********4444*************")
    # Get a git connection as our bot
    # Here is where we are getting the permission to talk as our bot and not
    # as a Python webservice
    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_installation(owner, repo_name).id
        ).token
    )
    print("**********5555*************")
    repo = git_connection.get_repo(f"{owner}/{repo_name}")
    print("**********6666*************")
    issue = repo.get_issue(number=payload['pull_request']['number'])
    print("**********7777*************")
    # Call meme-api to get a random meme
    response = requests.get(url='https://meme-api.herokuapp.com/gimme')
    print("**********8888*************")
    print(response.status_code)
    if response.status_code != 200:
        return 'ok'
    print("**********9999*************")
    # Get the best resolution meme
    meme_url = response.json()['preview'][-1]
    print("**********AAAAA*************")
    # Create a comment with the random meme
    issue.create_comment(f"![Alt Text]({meme_url})")
    print("**********BBBBB*************")
    return "ok"


if __name__ == "__main__":
    app.run(debug=True, port=9000)