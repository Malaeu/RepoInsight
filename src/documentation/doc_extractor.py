import re

class DocExtractor:
    def extract_info(self, content):
        info = {
            'project_name': self.extract_project_name(content),
            'description': self.extract_description(content),
            'installation': self.extract_installation(content),
            'usage': self.extract_usage(content),
            'contributing': self.extract_contributing(content),
        }
        return info

    def extract_project_name(self, content):
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1) if match else None

    def extract_description(self, content):
        match = re.search(r'^#.*\n+(.+?)(\n#|\Z)', content, re.DOTALL | re.MULTILINE)
        return match.group(1).strip() if match else None

    def extract_installation(self, content):
        match = re.search(r'(?:^|\n)##?\s*Installation\s*\n+(.+?)(\n#|\Z)', content, re.DOTALL | re.MULTILINE | re.IGNORECASE)
        return match.group(1).strip() if match else None

    def extract_usage(self, content):
        match = re.search(r'(?:^|\n)##?\s*Usage\s*\n+(.+?)(\n#|\Z)', content, re.DOTALL | re.MULTILINE | re.IGNORECASE)
        return match.group(1).strip() if match else None

    def extract_contributing(self, content):
        match = re.search(r'(?:^|\n)##?\s*Contributing\s*\n+(.+?)(\n#|\Z)', content, re.DOTALL | re.MULTILINE | re.IGNORECASE)
        return match.group(1).strip() if match else None