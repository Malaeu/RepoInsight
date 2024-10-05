import re
import logging
from typing import Optional, Dict, Any
import markdown
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class DocExtractor:
    def extract_info(self, content: str) -> Dict[str, Optional[Any]]:
        """
        Extract specific sections from documentation content.

        Args:
            content (str): The content of the documentation file.

        Returns:
            Dict[str, Optional[Any]]: Extracted information for various sections.
        """
        if not content:
            logger.warning("No content provided to extract info.")
            return {}

        html_content = markdown.markdown(content)
        soup = BeautifulSoup(html_content, "html.parser")

        info = {
            'project_name': self.extract_project_name(soup),
            'description': self.extract_description(soup),
            'installation': self.extract_section(soup, 'Installation'),
            'usage': self.extract_section(soup, 'Usage'),
            'contributing': self.extract_section(soup, 'Contributing'),
        }
        return info

    def extract_project_name(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the project name from the documentation.

        Args:
            soup (BeautifulSoup): Parsed HTML content.

        Returns:
            Optional[str]: The project name if found, else None.
        """
        header = soup.find(['h1'])
        if header:
            project_name = header.get_text(strip=True)
            logger.debug(f"Project Name Found: {project_name}")
            return project_name
        logger.info("Project name not found.")
        return None

    def extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the project description from the documentation.

        Args:
            soup (BeautifulSoup): Parsed HTML content.

        Returns:
            Optional[str]: The project description if found, else None.
        """
        header = soup.find(['h1'])
        if header:
            description_elements = []
            for sibling in header.next_siblings:
                if sibling.name and sibling.name.startswith('h'):
                    break
                if getattr(sibling, 'get_text', None):
                    description_elements.append(sibling.get_text(strip=True))
            description = ' '.join(description_elements).strip()
            if description:
                logger.debug("Description extracted.")
                return description
        logger.info("Description not found.")
        return None

    def extract_section(self, soup: BeautifulSoup, section_title: str) -> Optional[str]:
        """
        Extract a specific section from the documentation.

        Args:
            soup (BeautifulSoup): Parsed HTML content.
            section_title (str): The title of the section to extract.

        Returns:
            Optional[str]: The section content if found, else None.
        """
        header = soup.find(['h2', 'h3'], string=lambda text: text and section_title.lower() in text.lower())
        if header:
            content_elements = []
            for sibling in header.next_siblings:
                if sibling.name and sibling.name.startswith('h'):
                    break
                if getattr(sibling, 'get_text', None):
                    content_elements.append(sibling.get_text(strip=True))
            section_content = ' '.join(content_elements).strip()
            if section_content:
                logger.debug(f"Section '{section_title}' extracted.")
                return section_content
        logger.info(f"Section '{section_title}' not found.")
        return None