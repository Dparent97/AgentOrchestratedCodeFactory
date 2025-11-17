"""
SafetyGuard - Enforces safety boundaries and prevents dangerous operations

Validates all project ideas before execution to ensure they don't
violate safety rules or attempt dangerous operations.
"""

import logging
import re

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import Idea, SafetyCheck

logger = logging.getLogger(__name__)


class SafetyGuard(BaseAgent):
    """Validates ideas for safety and enforces security boundaries"""
    
    # Keywords that trigger automatic rejection
    DANGEROUS_KEYWORDS = [
        "control equipment", "actuate", "bypass interlock", "override safety",
        "disable alarm", "hack", "exploit", "crack password", "inject",
        "malware", "virus", "rm -rf /", "format drive"
    ]
    
    # Keywords that require confirmation
    CONFIRMATION_KEYWORDS = [
        "delete file", "send email", "network call", "api request",
        "modify database", "sudo", "admin privilege"
    ]
    
    @property
    def name(self) -> str:
        return "safety_guard"
    
    @property
    def description(self) -> str:
        return "Validates ideas for safety compliance and security"
    
    def execute(self, input_data: Idea) -> SafetyCheck:
        """
        Validate idea for safety
        
        Args:
            input_data: Idea to validate
            
        Returns:
            SafetyCheck: Safety validation result
        """
        idea = self.validate_input(input_data, Idea)
        logger.info(f"Safety check for: {idea.description[:50]}...")
        
        text = f"{idea.description} {' '.join(idea.features)}".lower()
        
        warnings = []
        required_confirmations = []
        blocked_keywords = []
        approved = True
        
        # Check for dangerous keywords
        for keyword in self.DANGEROUS_KEYWORDS:
            if keyword in text:
                blocked_keywords.append(keyword)
                approved = False
                warnings.append(f"Dangerous operation detected: '{keyword}'")
        
        # Check for confirmation-required keywords
        if approved:
            for keyword in self.CONFIRMATION_KEYWORDS:
                if keyword in text:
                    required_confirmations.append(
                        f"This tool may {keyword}. Human confirmation required."
                    )
        
        # Validate target environment
        if not approved:
            warnings.append("Idea violates safety guidelines - see docs/safety.md")
        
        result = SafetyCheck(
            approved=approved,
            warnings=warnings,
            required_confirmations=required_confirmations,
            blocked_keywords=blocked_keywords
        )
        
        if approved:
            logger.info("Safety check PASSED")
        else:
            logger.warning(f"Safety check FAILED: {len(blocked_keywords)} violations")
        
        return result
