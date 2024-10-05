import os
import logging
from typing import Optional, Dict
from github import Github
from github.GithubException import GithubException

logger = logging.getLogger(__name__)

class GitHubAPI:
    def __init__(self, token: Optional[str] = None):
        """
        Initialize the GitHubAPI with a token.

        Args:
            token (Optional[str]): GitHub token. If None, it will use the GITHUB_TOKEN environment variable.

        Raises:
            ValueError: If no GitHub token is provided.
        """
        self.token = token or os.environ.get('GITHUB_TOKEN')
        if not self.token:
            logger.error("GitHub token is required")
            raise ValueError("GitHub token is required")
        self.github = Github(self.token)

    def get_repository(self, repo_url: str):
        """
        Retrieve a repository object from GitHub based on its URL.

        Args:
            repo_url (str): The URL of the GitHub repository.

        Returns:
            Repository or None: The repository object if found, else None.
        """
        try:
            owner, repo_name = self._extract_owner_repo(repo_url)
            repository = self.github.get_repo(f"{owner}/{repo_name}")
            logger.info(f"Repository '{owner}/{repo_name}' accessed successfully.")
            return repository
        except GithubException as e:
            logger.error(f"Error accessing repository: {e}")
            return None
        except ValueError as ve:
            logger.error(ve)
            return None

    def _extract_owner_repo(self, repo_url: str) -> (str, str):
        """
        Extract the owner and repository name from the repository URL.

        Args:
            repo_url (str): The GitHub repository URL.

        Returns:
            Tuple[str, str]: Owner and repository name.

        Raises:
            ValueError: If the URL format is invalid.
        """
        try:
            parts = repo_url.rstrip('/').split('/')
            owner, repo_name = parts[-2], parts[-1]
            return owner, repo_name
        except IndexError:
            raise ValueError("Invalid repository URL format.")

    def get_file_content(self, repo, file_path: str) -> Optional[str]:
        """
        Retrieve the content of a file from the repository.

        Args:
            repo (Repository): The GitHub repository object.
            file_path (str): The path to the file in the repository.

        Returns:
            Optional[str]: The file content if successful, else None.
        """
        try:
            content = repo.get_contents(file_path)
            decoded_content = content.decoded_content.decode('utf-8')
            logger.debug(f"Content retrieved for file: {file_path}")
            return decoded_content
        except GithubException as e:
            logger.error(f"Error accessing file {file_path}: {e}")
            return None

    def get_repository_structure(self, repo) -> Dict[str, str]:
        """
        Retrieve the structure of the repository.

        Args:
            repo (Repository): The GitHub repository object.

        Returns:
            Dict[str, str]: A dictionary with file paths as keys and their types ('file' or 'dir') as values.
        """
        structure = {}
        try:
            contents = repo.get_contents("")
            while contents:
                file_content = contents.pop(0)
                if file_content.type == "dir":
                    contents.extend(repo.get_contents(file_content.path))
                structure[file_content.path] = file_content.type
            logger.info("Repository structure retrieved successfully.")
        except GithubException as e:
            logger.error(f"Error retrieving repository structure: {e}")
        return structure