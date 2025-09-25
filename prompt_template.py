class PromptTemplate:
    def __init__(self, template: str):
        """
        Initialize with a template string containing placeholders like {context}, {web}, etc.
        """
        self.template = template

    def build_prompt(self, **kwargs) -> str:
        """
        Fill the template with provided keyword arguments.
        Raises a clear error if any variable is missing.
        """
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            missing = e.args[0]
            raise ValueError(f"Missing value for variable: {missing}")
