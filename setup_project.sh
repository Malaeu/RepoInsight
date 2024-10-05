#!/bin/bash

# Create main project directories
mkdir -p src/{api,analysis,documentation,generation,utils} tests/{unit,integration} docs config .github/workflows

# Create main application file
touch src/main.py

# Create __init__.py files
touch src/__init__.py
touch src/api/__init__.py
touch src/analysis/__init__.py
touch src/documentation/__init__.py
touch src/generation/__init__.py
touch src/utils/__init__.py

# Create module files
touch src/api/github_api.py
touch src/analysis/code_analyzer.py
touch src/analysis/doc_analyzer.py
touch src/documentation/doc_extractor.py
touch src/documentation/markdown_generator.py
touch src/generation/insight_generator.py
touch src/utils/file_utils.py

# Create configuration files
touch config/config.yaml
touch requirements.txt
touch .github/workflows/ci.yml

# Update README.md
cat << EOF > README.md
# RepoInsight

RepoInsight is an automatic GitHub repository exploration and documentation tool. It analyzes GitHub repositories to generate comprehensive documentation and insights.

## Features (Planned)

- Automated repository structure analysis
- Code analysis and summarization
- Documentation extraction and parsing
- API detection and documentation
- Markdown report generation

## Installation

1. Clone the repository:
   \`\`\`
   git clone https://github.com/your-username/RepoInsight.git
   cd RepoInsight
   \`\`\`

2. Set up a virtual environment:
   \`\`\`
   python -m venv venv
   source venv/bin/activate  # On Windows, use \`venv\Scripts\activate\`
   \`\`\`

3. Install dependencies:
   \`\`\`
   pip install -r requirements.txt
   \`\`\`

## Usage

(To be added as the project develops)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
EOF

# Create initial config.yaml
cat << EOF > config/config.yaml
github:
  api_token: "your_github_api_token_here"

openai:
  api_key: "your_openai_api_key_here"

analysis:
  max_file_size: 1000000  # in bytes
  supported_languages: ["python", "javascript", "java"]
EOF

# Create initial CI workflow
cat << EOF > .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: python -m unittest discover tests
EOF

# Create initial requirements.txt
cat << EOF > requirements.txt
requests
PyGithub
pyyaml
openai
beautifulsoup4
EOF

# Initialize git repository
git add .
git commit -m "Initial project setup"
git push origin main
EOF
^+x

