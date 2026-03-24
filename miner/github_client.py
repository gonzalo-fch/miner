import requests
import time

from config import HEADERS, REQUEST_DELAY


def get_popular_repositories(language, limit=10):

    url = f"https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page={limit}"

    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        print("GitHub API error:", r.text)
        return []

    data = r.json()

    return data["items"]


def get_repository_tree(repo_full_name):

    url = f"https://api.github.com/repos/{repo_full_name}/git/trees/HEAD?recursive=1"

    r = requests.get(url, headers=HEADERS)

    time.sleep(REQUEST_DELAY)

    if r.status_code != 200:
        return None

    return r.json()["tree"]


def get_code_files(tree):

    py_files = []
    java_files = []

    for item in tree:

        if item["type"] != "blob":
            continue

        path = item["path"]

        if path.endswith(".py"):
            py_files.append(path)

        if path.endswith(".java"):
            java_files.append(path)

    return py_files, java_files


def download_file(repo_full_name, path):

    url = f"https://raw.githubusercontent.com/{repo_full_name}/HEAD/{path}"

    r = requests.get(url, headers=HEADERS)

    time.sleep(REQUEST_DELAY)

    if r.status_code != 200:
        return ""

    if len(r.text) > 200000:
        return ""

    return r.text