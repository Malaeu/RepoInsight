import os
from api.github_api import GitHubAPI
from analysis.code_analyzer import CodeAnalyzer
from utils.file_utils import is_code_file, is_text_file
from documentation.doc_extractor import DocExtractor
from generation.insight_generator import InsightGenerator

class RepoInsight:
    def __init__(self, github_token):
        self.github_api = GitHubAPI(github_token)
        self.code_analyzer = CodeAnalyzer()
        self.doc_extractor = DocExtractor()
        self.insight_generator = InsightGenerator()

    def analyze_repository(self, repo_url):
        # 1. Input GitHub Repository URL
        repo = self.github_api.get_repository(repo_url)
        if not repo:
            return "Failed to access repository"

        # 2. Repository Data Retrieval
        structure = self.github_api.get_repository_structure(repo)

        # 3. Analyze Repository Structure
        analysis_result = self.analyze_structure(structure)

        # 4. Extract and Analyze Code Files
        code_analysis = self.analyze_code_files(repo, structure)

        # 5. Extract and Analyze Documentation
        doc_analysis = self.analyze_documentation(repo, structure)

        # 6. API Analysis (if applicable)
        api_analysis = self.analyze_api(repo, structure)

        # 7. External Documentation Gathering (to be implemented)

        # 8. Aggregate Information
        aggregated_info = self.aggregate_information(
            analysis_result, code_analysis, doc_analysis, api_analysis
        )

        # 9. Generate Comprehensive Description
        description = self.insight_generator.generate_description(aggregated_info)

        # 10. Validation and Formatting (to be implemented)

        # 11. Output Final Documentation
        return description

    def analyze_structure(self, structure):
        # Implement structure analysis logic
        pass

    def analyze_code_files(self, repo, structure):
        code_analysis = {}
        for file_path, file_type in structure.items():
            if file_type == "file" and is_code_file(file_path):
                content = self.github_api.get_file_content(repo, file_path)
                if content:
                    code_analysis[file_path] = self.code_analyzer.analyze_file(content)
        return code_analysis

    def analyze_documentation(self, repo, structure):
        doc_analysis = {}
        for file_path, file_type in structure.items():
            if file_type == "file" and is_text_file(file_path):
                content = self.github_api.get_file_content(repo, file_path)
                if content:
                    doc_analysis[file_path] = self.doc_extractor.extract_info(content)
        return doc_analysis

    def analyze_api(self, repo, structure):
        # Implement API analysis logic
        pass

    def aggregate_information(self, structure_analysis, code_analysis, doc_analysis, api_analysis):
        # Implement information aggregation logic
        pass

def main():
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("Please set the GITHUB_TOKEN environment variable")
        return

    repo_insight = RepoInsight(github_token)
    repo_url = input("Enter the GitHub repository URL: ")
    result = repo_insight.analyze_repository(repo_url)
    print(result)

if __name__ == "__main__":
    main()