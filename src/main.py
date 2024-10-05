import os
import logging
from typing import Dict, Any, Optional
from api.github_api import GitHubAPI
from analysis.code_analyzer import CodeAnalyzer
from utils.file_utils import is_code_file, is_text_file
from documentation.doc_extractor import DocExtractor
from generation.insight_generator import InsightGenerator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RepoInsight:
    def __init__(self, github_token: str, openai_api_key: str):
        """
        Initialize RepoInsight with GitHub and OpenAI API tokens.

        Args:
            github_token (str): GitHub API token.
            openai_api_key (str): OpenAI API key.
        """
        self.github_api = GitHubAPI(github_token)
        self.code_analyzer = CodeAnalyzer()
        self.doc_extractor = DocExtractor()
        self.insight_generator = InsightGenerator(api_key=openai_api_key)

    def analyze_repository(self, repo_url: str) -> str:
        """
        Analyze a GitHub repository and generate a comprehensive description.

        Args:
            repo_url (str): The URL of the GitHub repository.

        Returns:
            str: The generated repository description or an error message.
        """
        logger.info(f"Starting analysis for repository: {repo_url}")
        try:
            repo = self.github_api.get_repository(repo_url)
            if not repo:
                logger.error("Failed to access repository.")
                return "Failed to access repository."

            structure = self.github_api.get_repository_structure(repo)
            if not structure:
                logger.error("Failed to retrieve repository structure.")
                return "Failed to retrieve repository structure."

            analysis_result = self.analyze_structure(structure)
            code_analysis = self.analyze_code_files(repo, structure)
            doc_analysis = self.analyze_documentation(repo, structure)
            api_analysis = self.analyze_api(repo, structure)

            aggregated_info = self.aggregate_information(
                analysis_result, code_analysis, doc_analysis, api_analysis
            )

            description = self.insight_generator.generate_description(aggregated_info)
            logger.info("Repository analysis completed successfully.")
            return description
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return "An unexpected error occurred during repository analysis."

    def analyze_structure(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the structure of the repository.

        Args:
            structure (Dict[str, Any]): The repository structure.

        Returns:
            Dict[str, Any]: Analysis results.
        """
        logger.debug("Analyzing repository structure.")
        return {'structure': structure}

    def analyze_code_files(self, repo: Any, structure: Dict[str, Any]) -> Dict[str, Any]:
"""
        Analyze code files in the repository.
        
        Args:
            repo (Any): The GitHub repository object.
            structure (Dict[str, Any]): The repository structure.
        
        Returns:
            Dict[str, Any]: Code analysis results.
        """
                """
        Analyze code files in the repository.

        Args:
            repo (Any): The GitHub repository object.
            structure (Dict[str, Any]): The repository structure.

        Returns:
            Dict[str, Any]: Code analysis results.
        """
        code_analysis = {}
        logger.debug("Analyzing code files.")
        for file_path, file_type in structure.items():
            if file_type == "file" and is_code_file(file_path):
                content = self.github_api.get_file_content(repo, file_path)
                if content:
                    analysis = self.code_analyzer.analyze_python_file(content)
                    if analysis:
                        code_analysis[file_path] = analysis
                        logger.debug(f"Analysis for {file_path}: {analysis}")
        return {'code_analysis': code_analysis}

    def analyze_documentation(self, repo: Any, structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze documentation files in the repository.

        Args:
            repo (Any): The GitHub repository object.
            structure (Dict[str, Any]): The repository structure.

        Returns:
            Dict[str, Any]: Documentation analysis results.
        """
        doc_analysis = {}
        logger.debug("Analyzing documentation files.")
        for file_path, file_type in structure.items():
            if file_type == "file" and is_text_file(file_path):
                content = self.github_api.get_file_content(repo, file_path)
                if content:
                    info = self.doc_extractor.extract_info(content)
                    if info:
                        doc_analysis[file_path] = info
                        logger.debug(f"Documentation extracted from {file_path}")
        return {'doc_analysis': doc_analysis}

    def analyze_api(self, repo: Any, structure: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze API endpoints in the repository.

        Args:
            repo (Any): The GitHub repository object.
            structure (Dict[str, Any]): The repository structure.

        Returns:
            Dict[str, Any]: API analysis results.
        """
        logger.debug("Analyzing API endpoints.")
        # Placeholder for actual API analysis
        api_analysis = {}
        # Implement API analysis logic here
        return {'api_analysis': api_analysis}

    def aggregate_information(
        self,
        structure_analysis: Dict[str, Any],
        code_analysis: Dict[str, Any],
        doc_analysis: Dict[str, Any],
        api_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Aggregate all analysis information into a single dictionary.

        Args:
            structure_analysis (Dict[str, Any]): Structure analysis results.
            code_analysis (Dict[str, Any]): Code analysis results.
            doc_analysis (Dict[str, Any]): Documentation analysis results.
            api_analysis (Dict[str, Any]): API analysis results.

        Returns:
            Dict[str, Any]: Aggregated information.
        """
        logger.debug("Aggregating analysis information.")
        aggregated = {}
        aggregated.update(structure_analysis)
        aggregated.update(code_analysis)
        aggregated.update(doc_analysis)
        aggregated.update(api_analysis)
        return aggregated

def main():
    github_token = os.environ.get('GITHUB_TOKEN')
    openai_api_key = os.environ.get('OPENAI_API_KEY')

    if not github_token:
        logger.error("GITHUB_TOKEN environment variable is not set.")
        print("Please set the GITHUB_TOKEN environment variable.")
        return

    if not openai_api_key:
        logger.error("OPENAI_API_KEY environment variable is not set.")
        print("Please set the OPENAI_API_KEY environment variable.")
        return

    repo_insight = RepoInsight(github_token, openai_api_key)

    repo_url = input("Enter the GitHub repository URL: ").strip()
    if not repo_url:
        logger.error("No repository URL provided.")
        print("Repository URL cannot be empty.")
        return

    # Simple validation of the repository URL
    if not repo_url.startswith("https://github.com/"):
        logger.error("Invalid repository URL provided.")
        print("Please enter a valid GitHub repository URL.")
        return

    result = repo_insight.analyze_repository(repo_url)
    print(result)

if __name__ == "__main__":
    main()