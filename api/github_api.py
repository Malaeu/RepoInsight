import requests
from typing import Dict, List, Optional

class GitHubAPI:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_repository(self, repo_url: str) -> Optional[Dict]:
        # Existing method implementation

    def get_repository_structure(self, repo: Dict) -> Optional[Dict]:
        # Existing method implementation

    def get_issues(self, repo: Dict, state: str = "all") -> List[Dict]:
        issues_url = f"{self.base_url}/repos/{repo['full_name']}/issues"
        params = {"state": state}
        response = requests.get(issues_url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []

    def get_pull_requests(self, repo: Dict, state: str = "all") -> List[Dict]:
        pulls_url = f"{self.base_url}/repos/{repo['full_name']}/pulls"
        params = {"state": state}
        response = requests.get(pulls_url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []

    def get_file_content(self, repo: Dict, file_path: str) -> Optional[str]:
        content_url = f"{self.base_url}/repos/{repo['full_name']}/contents/{file_path}"
        response = requests.get(content_url, headers=self.headers)
        if response.status_code == 200:
            content = response.json()
            if content['type'] == 'file':
                return requests.get(content['download_url']).text
        return None

    def paginate_request(self, url: str) -> List[Dict]:
        results = []
        while url:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                results.extend(response.json())
                url = response.links.get('next', {}).get('url')
            else:
                break
        return results
