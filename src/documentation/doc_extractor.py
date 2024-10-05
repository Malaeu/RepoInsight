import re
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

class DocExtractor:
    def extract_info(self, content: str) -> Dict[str, Optional[str]]:
        """
        Extract specific sections from documentation content.

        Args:
            content (str): The content of the documentation file.

        Returns:
            Dict[str, Optional[str]]: Extracted information for various sections.
        """
        info = {
            'project_name': self.extract_project_name(content),
            'description': self.extract_description(content),
            'installation': self.extract_section(content, 'Installation'),
            'usage': self.extract_section(content, 'Usage'),
            'contributing': self.extract_section(content, 'Contributing'),
        }
        return info

    def extract_project_name(self, content: str) -> Optional[str]:
        """
        Extract the project name from the documentation.

        Args:
            content (str): The documentation content.

        Returns:
            Optional[str]: The project name if found, else None.
        """
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if match:
            logger.debug(f"Project Name Found: {match.group(1)}")
            return match.group(1).strip()
        logger.warning("Project name not found.")
        return None

    def extract_description(self, content: str) -> Optional[str]:
        """
        Extract the project description from the documentation.

        Args:
            content (str): The documentation content.

        Returns:
            Optional[str]: The project description if found, else None.
        """
        match = re.search(r'^#.*\n+(.+?)(\n#|\Z)', content, re.DOTALL | re.MULTILINE)
        if match:
            description = match.group(1).strip()
            logger.debug("Description extracted.")
            return description
        logger.warning("Description not found.")
        return None

    def extract_section(self, content: str, section_title: str) -> Optional[str]:
        """
        Extract a specific section from the documentation.

        Args:
            content (str): The documentation content.
            section_title (str): The title of the section to extract.

        Returns:
            Optional[str]: The section content if found, else None.
        """
        pattern = rf'(?:^|\n)##?\s*{re.escape(section_title)}\s*\n+(.+?)(\n#|\Z)'
        match = re.search(pattern, content, re.DOTALL | re.MULTILINE | re.IGNORECASE)
        if match:
            section = match.group(1).strip()
            logger.debug(f"Section '{section_title}' extracted.")
            return section
        logger.warning(f"Section '{section_title}' not found.")
        return None