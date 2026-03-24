import redis

from config import REPOS_TO_ANALYZE

from github_client import (
    get_popular_repositories,
    get_repository_tree,
    get_code_files,
    download_file
)

from parser import (
    extract_python_functions,
    extract_java_methods
)

from word_splitter import split_words


redis_client = redis.Redis(host="localhost", port=6379)


def process_repository(repo):

    full_name = repo["full_name"]

    print(f"\nProcessing repository: {full_name}")

    tree = get_repository_tree(full_name)

    if not tree:
        print("Could not retrieve repository tree")
        return []

    py_files, java_files = get_code_files(tree)

    py_files = py_files[:50]
    java_files = java_files[:50]

    print(f"Python files: {len(py_files)}")
    print(f"Java files: {len(java_files)}")

    words = []

    for path in py_files:

        code = download_file(full_name, path)

        functions = extract_python_functions(code)

        for f in functions:
            words.extend(split_words(f))

    for path in java_files:

        code = download_file(full_name, path)

        methods = extract_java_methods(code)

        for m in methods:
            words.extend(split_words(m))

    return words


def main():

    print("Starting Miner...")

    repos_python = get_popular_repositories("python", REPOS_TO_ANALYZE)
    repos_java = get_popular_repositories("java", REPOS_TO_ANALYZE)

    repositories = (repos_python + repos_java)[:REPOS_TO_ANALYZE]

    total_words = 0

    for repo in repositories:

        words = process_repository(repo)

        print(f"Extracted {len(words)} words")

        # enviar palabras inmediatamente a redis
        for w in words:
            redis_client.lpush("words", w)

        total_words += len(words)

        print("Words sent to Redis")

    print("\nMining finished")
    print(f"\nTotal words extracted: {total_words}")

if __name__ == "__main__":
    main()