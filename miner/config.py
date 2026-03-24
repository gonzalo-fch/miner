import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

REQUEST_DELAY = 0.5

REPOS_TO_ANALYZE = 5