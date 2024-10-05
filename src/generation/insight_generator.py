import os
import openai
import logging
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InsightGenerator:
    """
    A class to generate comprehensive descriptions of GitHub repositories
    using OpenAI's ChatCompletion API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 1000,
        temperature: float = 0.7,
    ):
        """
        Initialize the InsightGenerator.

        Args:
            api_key (Optional[str]): OpenAI API key. If None, it will try to use the OPENAI_API_KEY environment variable.
            model (str): OpenAI model to use.
            max_tokens (int): Maximum number of tokens in the generated response.
            temperature (float): Sampling temperature.

        Raises:
            ValueError: If no OpenAI API key is provided.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.error("OpenAI API key must be provided.")
            raise ValueError("OpenAI API key must be provided.")
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(min=1, max=60),
        retry=retry_if_exception_type(openai.error.RateLimitError),
    )
    def generate_description(self, aggregated_info: Dict[str, Any]) -> str:
        """
        Generate a detailed project description based on the aggregated information.

        Args:
            aggregated_info (Dict[str, Any]): Aggregated data about the repository.

        Returns:
            str: The generated project description.
        """
        if not isinstance(aggregated_info, dict):
            logger.error("aggregated_info must be a dictionary.")
            return "Invalid input data."

        prompt = self.create_prompt(aggregated_info)
        try:
            response = openai.ChatCompletion.create(
                api_key=self.api_key,
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )
            description = response.choices[0].message['content'].strip()
            logger.info("Description generated successfully.")
            return description
        except openai.error.OpenAIError as e:
            logger.error(f"An error occurred: {e}")
            return "An error occurred while generating the description."

    def create_prompt(self, aggregated_info: Dict[str, Any]) -> str:
        """
        Create a prompt for the AI model based on the aggregated repository information.

        Args:
            aggregated_info (Dict[str, Any]): Aggregated data about the repository.

        Returns:
            str: The prompt to be used with the AI model.
        """
        project_name = aggregated_info.get('project_name', 'Unknown')
        description = aggregated_info.get('description', 'No description available')

        prompt_sections = [
            "Please generate a comprehensive description of the following GitHub project:",
            f"**Project Name:** {project_name}",
            f"**Description:** {description}",
            f"**Repository Structure:**\n{self.format_structure(aggregated_info.get('structure', {}))}",
            f"**Code Analysis:**\n{self.format_code_analysis(aggregated_info.get('code_analysis', {}))}",
            f"**Documentation Analysis:**\n{self.format_doc_analysis(aggregated_info.get('doc_analysis', {}))}",
            f"**API Analysis:**\n{self.format_api_analysis(aggregated_info.get('api_analysis', {}))}",
            "Please include the project's purpose, main features, architecture, and usage instructions in the description."
        ]

        prompt = '\n\n'.join(prompt_sections)
        logger.debug("Prompt created for AI model.")
        return prompt

    def format_structure(self, structure: Dict[str, Any], indent_level: int = 0) -> str:
        """
        Recursively format the repository structure into a tree-like representation.

        Args:
            structure (Dict[str, Any]): Nested dictionary representing the repository structure.
            indent_level (int): Current indentation level for recursive calls.

        Returns:
            str: Formatted repository structure.
        """
        formatted = ""
        indent = "  " * indent_level
        for name, content in structure.items():
            name_str = str(name)
            if isinstance(content, dict):
                formatted += f"{indent}- {name_str}/\n"
                formatted += self.format_structure(content, indent_level + 1)
            else:
                content_str = str(content)
                formatted += f"{indent}- {name_str} ({content_str})\n"
        return formatted.strip()

    def format_code_analysis(self, code_analysis: Dict[str, Any]) -> str:
        """
        Format the code analysis section.

        Args:
            code_analysis (Dict[str, Any]): Code analysis data.

        Returns:
            str: Formatted code analysis.
        """
        if not code_analysis:
            return "No code analysis available."

        formatted_entries = []
        for file, analysis in code_analysis.items():
            if not isinstance(analysis, dict):
                continue
            entry = [f"- **File:** {file}"]
            for key, value in analysis.items():
                entry.append(f"  - {key}: {value}")
            formatted_entries.append('\n'.join(entry))
        return '\n\n'.join(formatted_entries)

    def format_doc_analysis(self, doc_analysis: Dict[str, Any]) -> str:
        """
        Format the documentation analysis section.

        Args:
            doc_analysis (Dict[str, Any]): Documentation analysis data.

        Returns:
            str: Formatted documentation analysis.
        """
        if not doc_analysis:
            return "No documentation analysis available."

        formatted_entries = []
        for file, analysis in doc_analysis.items():
            if not isinstance(analysis, dict):
                continue
            entry = [f"- **File:** {file}"]
            for key, value in analysis.items():
                entry.append(f"  - {key}: {value}")
            formatted_entries.append('\n'.join(entry))
        return '\n\n'.join(formatted_entries)

    def format_api_analysis(self, api_analysis: Dict[str, Any]) -> str:
        """
        Format the API analysis section.

        Args:
            api_analysis (Dict[str, Any]): API analysis data.

        Returns:
            str: Formatted API analysis.
        """
        if not api_analysis:
            return "No API analysis available."

        formatted_entries = []
        for endpoint, details in api_analysis.items():
            if not isinstance(details, dict):
                continue
            entry = [f"- **Endpoint:** {endpoint}"]
            for key, value in details.items():
                entry.append(f"  - {key}: {value}")
            formatted_entries.append('\n'.join(entry))
        return '\n\n'.join(formatted_entries)
