import os
import logging
import asyncio
from typing import Dict, Any, Optional
from api.github_api import GitHubAPI
from analysis.code_analyzer import CodeAnalyzer
from utils.file_utils import is_code_file, is_text_file
from documentation.doc_extractor import DocExtractor
from generation.insight_generator import InsightGenerator
from config.config_manager import ConfigManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RepoInsight:
    def __init__(self, config: ConfigManager):
        self.github_api = GitHubAPI(config.github_token)
        self.code_analyzer = CodeAnalyzer()
        self.doc_extractor = DocExtractor()
        self.insight_generator = InsightGenerator(api_key=config.openai_api_key)

    async def analyze_repository(self, repo_url: str) -> str:
        logger.info(f"Starting analysis for repository: {repo_url}")
        try:
            repo = await self.github_api.get_repository(repo_url)
            if not repo:
                logger.error("Failed to access repository.")
                return "Failed to access repository."

            structure = await self.github_api.get_repository_structure(repo)
            if not structure:
                logger.error("Failed to retrieve repository structure.")
                return "Failed to retrieve repository structure."

            analysis_result = self.analyze_structure(structure)
            code_analysis = await self.analyze_code_files(repo, structure)
            doc_analysis = await self.analyze_documentation(repo, structure)
            api_analysis = await self.analyze_api(repo, structure)
            issues = await self.github_api.get_issues(repo)
            pull_requests = await self.github_api.get_pull_requests(repo)

            combined_analysis = {
                "structure": analysis_result,
                "code": code_analysis,
                "documentation": doc_analysis,
                "api": api_analysis,
                "issues": issues,
                "pull_requests": pull_requests
            }

            return await self.insight_generator.generate_insights(combined_analysis)

        except GitHubAPIError as e:
            logger.error(f"GitHub API error: {str(e)}")
            return f"GitHub API error: {str(e)}"
        except InsightGenerationError as e:
            logger.error(f"Error generating insights: {str(e)}")
            return f"Error generating insights: {str(e)}"
        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            return f"An unexpected error occurred: {str(e)}"

    def analyze_structure(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug("Analyzing repository structure.")
        return {'structure': structure}

    async def analyze_code_files(self, repo: Any, structure: Dict[str, Any]) -> Dict[str, Any]:
        code_analysis = {}
        logger.debug("Analyzing code files.")
        tasks = []
        for file_path, file_type in structure.items():
            if file_type == "file" and is_code_file(file_path):
                tasks.append(self.analyze_single_file(repo, file_path))
        results = await asyncio.gather(*tasks)
        for file_path, analysis in results:
            if analysis:
                code_analysis[file_path] = analysis
                logger.debug(f"Analysis for {file_path}: {analysis}")
        return {'code_analysis': code_analysis}

    async def analyze_single_file(self, repo: Any, file_path: str):
        content = await self.github_api.get_file_content(repo, file_path)
        if content:
            analysis = self.code_analyzer.analyze_python_file(content)
            return file_path, analysis
        return file_path, None

    async def analyze_documentation(self, repo: Any, structure: Dict[str, Any]) -> Dict[str, Any]:
        doc_analysis = {}
        logger.debug("Analyzing documentation files.")
        tasks = []
        for file_path, file_type in structure.items():
            if file_type == "file" and is_text_file(file_path):
                tasks.append(self.analyze_single_doc(repo, file_path))
        results = await asyncio.gather(*tasks)
        for file_path, info in results:
            if info:
                doc_analysis[file_path] = info
                logger.debug(f"Documentation extracted from {file_path}")
        return {'doc_analysis': doc_analysis}

    async def analyze_single_doc(self, repo: Any, file_path: str):
        content = await self.github_api.get_file_content(repo, file_path)
        if content:
            info = self.doc_extractor.extract_info(content)
            return file_path, info
        return file_path, None

    async def analyze_api(self, repo: Any, structure: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug("Analyzing API endpoints.")
        api_analysis = {}
        # Implement API analysis logic here
        return {'api_analysis': api_analysis}

async def main():
    config = ConfigManager()
    if not config.is_valid():
        logger.error("Invalid configuration. Please check your environment variables.")
        return

    repo_insight = RepoInsight(config)

    repo_url = input("Enter the GitHub repository URL: ").strip()
    if not repo_url:
        logger.error("No repository URL provided.")
        print("Repository URL cannot be empty.")
        return

    if not repo_url.startswith("https://github.com/"):
        logger.error("Invalid repository URL provided.")
        print("Please enter a valid GitHub repository URL.")
        return

    result = await repo_insight.analyze_repository(repo_url)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())