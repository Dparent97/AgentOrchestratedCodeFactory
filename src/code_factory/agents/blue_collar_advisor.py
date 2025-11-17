"""
BlueCollarAdvisor - Ensures solutions fit real-world technician workflows

Reviews project specifications to ensure the generated tool will be
practical and usable in actual field conditions.
"""

import logging

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import AdvisoryReport, Idea, ProjectSpec
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AdvisoryInput(BaseModel):
    """Input for blue-collar advisory"""
    idea: Idea
    spec: ProjectSpec


class BlueCollarAdvisor(BaseAgent):
    """Provides practical usability advice for field workers"""
    
    @property
    def name(self) -> str:
        return "blue_collar_advisor"
    
    @property
    def description(self) -> str:
        return "Ensures solutions are practical for blue-collar workers in field conditions"
    
    def execute(self, input_data: BaseModel) -> BaseModel:
        """
        Review project for field usability
        
        Args:
            input_data: AdvisoryInput with idea and spec
            
        Returns:
            AdvisoryReport: Recommendations and warnings
        """
        advisory_input = self.validate_input(input_data, AdvisoryInput)
        logger.info(f"Reviewing usability for: {advisory_input.spec.name}")
        
        recommendations = []
        warnings = []
        
        # Check for common field-usability issues
        if "web" in advisory_input.spec.tech_stack.get("framework", "").lower():
            recommendations.append("Consider CLI version for offline use")
        
        if advisory_input.idea.environment and "offline" in advisory_input.idea.environment.lower():
            recommendations.append("Ensure all features work without internet connection")
        
        # TODO: Implement comprehensive usability checks
        
        report = AdvisoryReport(
            recommendations=recommendations or ["Design looks good for field use"],
            warnings=warnings,
            environment_fit="good",
            accessibility_score=8
        )
        
        logger.info(f"Advisory complete: {len(report.recommendations)} recommendations")
        return report
