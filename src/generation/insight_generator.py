import openai

class InsightGenerator:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_description(self, aggregated_info):
        prompt = self.create_prompt(aggregated_info)
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1000,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()

    def create_prompt(self, aggregated_info):
        prompt = f"""
        Based on the following information about a GitHub repository, generate a comprehensive description:

        Project Name: {aggregated_info.get('project_name', 'Unknown')}
        Description: {aggregated_info.get('description', 'No description available')}

        Repository Structure:
        {self.format_structure(aggregated_info.get('structure', {}))}

        Code Analysis:
        {self.format_code_analysis(aggregated_info.get('code_analysis', {}))}

        Documentation Analysis:
        {self.format_doc_analysis(aggregated_info.get('doc_analysis', {}))}

        API Analysis:
        {self.format_api_analysis(aggregated_info.get('api_analysis', {}))}

        Please provide a detailed description of the project, including its purpose, main features, architecture, and how to use it.
        """
        return prompt

    def format_structure(self, structure):
        # Implement structure formatting logic
        pass

    def format_code_analysis(self, code_analysis):
        # Implement code analysis formatting logic
        pass

    def format_doc_analysis(self, doc_analysis):
        # Implement documentation analysis formatting logic
        pass

    def format_api_analysis(self, api_analysis):
        # Implement API analysis formatting logic
        pass