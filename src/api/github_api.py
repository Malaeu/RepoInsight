import os
import requests
from github import Github
from github.GithubException import GithubException

class GitHubAPI:
    def __init__(self, token=None):
        self.token = token or os.environ.get('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token is required")
        self.github = Github(self.token)

    def get_repository(self, repo_url):
        try:
            # Extract owner and repo name from URL
            parts = repo_url.split('/')
            owner, repo_name = parts[-2], parts[-1]
            return self.github.get_repo(f"{owner}/{repo_name}")
        except GithubException as e:
            print(f"Error accessing repository: {e}")
            return None

    def get_file_content(self, repo, file_path):
        try:
            content = repo.get_contents(file_path)
            return content.decoded_content.decode('utf-8')
        except GithubException as e:
            print(f"Error accessing file {file_path}: {e}")
            return None

    def get_repository_structure(self, repo):
        structure = {}
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            structure[file_content.path] = file_content.type
        return structure

# Usage example:
# api = GitHubAPI('your_github_token')
# repo = api.get_repository('https://github.com/username/repo')
# structure = api.get_repository_structure(repo)
# print(structure)