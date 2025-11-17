"""
DocWriterAgent - Generates project documentation

Creates README files, usage guides, API documentation,
and other user-facing documentation.
"""

import logging
from typing import Dict

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import ProjectSpec
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DocOutput(BaseModel):
    """Output containing generated documentation files"""
    files: Dict[str, str]  # file_path -> content


class DocWriterAgent(BaseAgent):
    """Generates user-facing documentation"""
    
    @property
    def name(self) -> str:
        return "doc_writer"
    
    @property
    def description(self) -> str:
        return "Generates comprehensive documentation and usage guides"
    
    def execute(self, input_data: BaseModel) -> BaseModel:
        """
        Generate documentation
        
        Args:
            input_data: ProjectSpec
            
        Returns:
            DocOutput: Generated documentation files
        """
        spec = self.validate_input(input_data, ProjectSpec)
        logger.info(f"Generating documentation for: {spec.name}")
        
        # TODO: Implement comprehensive doc generation
        # For now, return basic README
        readme_content = f"""# {spec.name}

{spec.description}

## Installation

```bash
pip install -e .
```

## Usage

```bash
python {spec.entry_point}
```

## Features

- Feature 1
- Feature 2
- Feature 3

## License

MIT
"""
        
        files = {
            "README.md": readme_content,
            "docs/usage.md": "# Usage Guide\n\nComing soon...\n"
        }
        
        logger.info(f"Generated {len(files)} documentation files")
        return DocOutput(files=files)
