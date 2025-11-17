"""
SafetyGuard - Enforces safety boundaries and prevents dangerous operations

Validates all project ideas before execution to ensure they don't
violate safety rules or attempt dangerous operations.

This module implements multiple layers of security validation:
1. Input normalization to prevent bypass attempts
2. Regex-based pattern matching for dangerous operations
3. Semantic analysis of intent
4. Audit logging for accountability
"""

import logging
import re
import unicodedata
from typing import List, Set, Tuple

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import Idea, SafetyCheck, SafetyCheckMetadata

logger = logging.getLogger(__name__)


class SafetyGuard(BaseAgent):
    """
    Validates ideas for safety and enforces security boundaries

    Uses multi-layer validation to prevent bypass attempts:
    - Input normalization (removes obfuscation)
    - Regex pattern matching (catches variations)
    - Semantic analysis (understands intent)
    """

    # Dangerous operation patterns (compiled regex for performance)
    DANGEROUS_PATTERNS = [
        # Physical equipment control
        (r"control\s*equipment", "control equipment"),
        (r"actuate", "actuate"),
        (r"bypass\s*interlock", "bypass interlock"),
        (r"override\s*safety", "override safety"),
        (r"disable\s*alarm", "disable alarm"),
        (r"disable\s*(?:emergency|safety|protection)", "disable safety system"),
        # Security/hacking
        (r"hack(?:ing)?", "hack"),
        (r"exploit(?:ation)?", "exploit"),
        (r"crack\s*password", "crack password"),
        (r"inject(?:ion)?", "injection attack"),
        (r"malware", "malware"),
        (r"virus", "virus"),
        (r"ransomware", "ransomware"),
        (r"backdoor", "backdoor"),
        (r"privilege\s*escalation", "privilege escalation"),
        (r"buffer\s*overflow", "buffer overflow"),
        (r"sql\s*injection", "SQL injection"),
        (r"xss\s*(?:attack)?", "XSS attack"),
        (r"csrf\s*(?:attack)?", "CSRF attack"),
        # Destructive file operations
        (r"rm\s*-rf\s*/", "destructive delete"),
        (r"format\s*(?:drive|disk)", "format drive"),
        (r"delete\s*(?:all|everything)", "mass deletion"),
        (r"drop\s*(?:database|table)", "drop database"),
        (r"truncate\s*(?:database|table)", "truncate database"),
        # Network attacks
        (r"ddos\s*(?:attack)?", "DDoS attack"),
        (r"dos\s*(?:attack)?", "DoS attack"),
        (r"port\s*scan(?:ning)?", "port scanning"),
        (r"brute\s*force", "brute force attack"),
        # Dangerous system operations
        (r"kill\s*-9\s*-1", "kill all processes"),
        (r"chmod\s*777", "insecure permissions"),
        (r"disable\s*firewall", "disable firewall"),
        (r"disable\s*antivirus", "disable antivirus"),
    ]

    # Confirmation-required patterns
    CONFIRMATION_PATTERNS = [
        (r"delete\s*file", "delete file"),
        (r"remove\s*file", "remove file"),
        (r"send\s*email", "send email"),
        (r"network\s*call", "network call"),
        (r"api\s*request", "API request"),
        (r"(?:modify|update|alter)\s*database", "modify database"),
        (r"sudo", "sudo command"),
        (r"admin\s*privilege", "admin privilege"),
        (r"write\s*(?:to\s*)?(?:disk|file)", "write to disk"),
        (r"execute\s*(?:command|shell)", "execute command"),
    ]

    # Compile patterns at class load time for performance
    _compiled_dangerous: List[Tuple[re.Pattern, str]] = []
    _compiled_confirmation: List[Tuple[re.Pattern, str]] = []

    @classmethod
    def _ensure_compiled(cls):
        """Ensure regex patterns are compiled"""
        if not cls._compiled_dangerous:
            cls._compiled_dangerous = [
                (re.compile(pattern, re.IGNORECASE), desc)
                for pattern, desc in cls.DANGEROUS_PATTERNS
            ]
        if not cls._compiled_confirmation:
            cls._compiled_confirmation = [
                (re.compile(pattern, re.IGNORECASE), desc)
                for pattern, desc in cls.CONFIRMATION_PATTERNS
            ]

    @property
    def name(self) -> str:
        return "safety_guard"

    @property
    def description(self) -> str:
        return "Validates ideas for safety compliance and security"

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text to prevent bypass attempts

        Removes:
        - Unicode variations and accents
        - Special characters and punctuation
        - Extra whitespace
        - Case variations

        This prevents bypasses like:
        - "control_equipment" vs "control equipment"
        - "controlequipment" vs "control equipment"
        - "c0ntr0l equipment" vs "control equipment"
        - "control\u00A0equipment" (non-breaking space)

        Args:
            text: Input text to normalize

        Returns:
            str: Normalized text
        """
        # Convert to lowercase
        text = text.lower()

        # Normalize unicode (decompose accents, etc.)
        text = unicodedata.normalize("NFKD", text)

        # Remove non-ASCII characters (keeps letters, numbers, spaces)
        text = text.encode("ascii", "ignore").decode("ascii")

        # Replace common obfuscation characters
        obfuscation_map = {
            "0": "o",
            "1": "i",
            "3": "e",
            "4": "a",
            "5": "s",
            "7": "t",
            "8": "b",
            "@": "a",
            "$": "s",
            "!": "i",
            "|": "i",
            "()": "o",
        }
        for old, new in obfuscation_map.items():
            text = text.replace(old, new)

        # Replace all non-alphanumeric with spaces
        text = re.sub(r"[^a-z0-9]+", " ", text)

        # Collapse multiple spaces
        text = re.sub(r"\s+", " ", text)

        return text.strip()

    @staticmethod
    def detect_bypass_attempts(original: str, normalized: str) -> List[str]:
        """
        Detect potential bypass attempts by comparing original vs normalized

        Args:
            original: Original input text
            normalized: Normalized version

        Returns:
            List of detected bypass techniques
        """
        bypass_attempts = []

        # Check for excessive special characters (potential obfuscation)
        special_char_count = len(re.findall(r"[^a-zA-Z0-9\s]", original))
        if special_char_count > len(original) * 0.15:  # More than 15% special chars
            bypass_attempts.append("excessive_special_characters")

        # Check for leetspeak / number substitution
        if re.search(r"[0-9]", original) and not re.search(r"[0-9]", normalized):
            bypass_attempts.append("number_substitution")

        # Check for unicode obfuscation
        if len(original) != len(original.encode("ascii", "ignore").decode("ascii")):
            bypass_attempts.append("unicode_obfuscation")

        # Check for excessive underscores (common bypass technique)
        if original.count("_") > 3:
            bypass_attempts.append("underscore_obfuscation")

        # Check for camelCase or PascalCase (attempting to bypass word boundaries)
        if re.search(r"[a-z][A-Z]", original):
            bypass_attempts.append("case_mixing")

        return bypass_attempts

    def check_dangerous_patterns(
        self, normalized_text: str
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Check text against dangerous operation patterns

        Args:
            normalized_text: Normalized input text

        Returns:
            Tuple of (has_violations, matched_patterns, matched_descriptions)
        """
        self._ensure_compiled()

        matched_patterns = []
        matched_descriptions = []

        for pattern, description in self._compiled_dangerous:
            if pattern.search(normalized_text):
                matched_patterns.append(pattern.pattern)
                matched_descriptions.append(description)
                logger.warning(
                    f"Dangerous pattern detected: '{description}' "
                    f"(pattern: {pattern.pattern})"
                )

        return len(matched_patterns) > 0, matched_patterns, matched_descriptions

    def check_confirmation_patterns(
        self, normalized_text: str
    ) -> List[str]:
        """
        Check text against patterns requiring confirmation

        Args:
            normalized_text: Normalized input text

        Returns:
            List of confirmations required
        """
        self._ensure_compiled()

        confirmations = []

        for pattern, description in self._compiled_confirmation:
            if pattern.search(normalized_text):
                confirmations.append(
                    f"This tool may {description}. Human confirmation required."
                )

        return confirmations

    def semantic_analysis(self, idea: Idea) -> Tuple[bool, List[str]]:
        """
        Perform semantic analysis to understand intent

        This goes beyond keyword matching to understand what the user
        is actually trying to build.

        Args:
            idea: Idea to analyze

        Returns:
            Tuple of (is_safe, warnings)
        """
        warnings = []

        # Check if target environment suggests dangerous context
        if idea.environment:
            env_lower = idea.environment.lower()
            dangerous_environments = [
                "production", "live", "critical", "nuclear", "medical",
                "aviation", "automotive", "industrial control"
            ]
            for env in dangerous_environments:
                if env in env_lower:
                    warnings.append(
                        f"Target environment '{env}' requires extra scrutiny. "
                        f"Ensure no safety-critical systems are affected."
                    )

        # Check if target users suggest privileged access
        dangerous_user_roles = ["admin", "root", "sysadmin", "operator", "engineer"]
        for user_role in idea.target_users:
            user_lower = user_role.lower()
            for dangerous_role in dangerous_user_roles:
                if dangerous_role in user_lower:
                    warnings.append(
                        f"Target user '{user_role}' may have privileged access. "
                        f"Ensure proper authorization checks."
                    )
                    break

        # Check constraints for security concerns
        for constraint in idea.constraints:
            if any(word in constraint.lower() for word in ["bypass", "skip", "disable"]):
                warnings.append(
                    f"Constraint mentions bypassing: '{constraint}'. "
                    f"This requires careful review."
                )

        # All semantic checks are warnings, not hard blocks
        return True, warnings

    def execute(self, input_data: Idea) -> SafetyCheck:
        """
        Validate idea for safety

        Multi-layer validation process:
        1. Input normalization
        2. Bypass attempt detection
        3. Dangerous pattern matching
        4. Confirmation pattern matching
        5. Semantic analysis

        Args:
            input_data: Idea to validate

        Returns:
            SafetyCheck: Safety validation result with audit metadata
        """
        idea = self.validate_input(input_data, Idea)
        logger.info(f"Safety check for: {idea.description[:50]}...")

        # Combine all text for analysis
        original_text = f"{idea.description} {' '.join(idea.features)} {' '.join(idea.constraints)}"

        # Layer 1: Normalize input
        normalized_text = self.normalize_text(original_text)
        logger.debug(f"Normalized text: {normalized_text[:100]}...")

        # Layer 2: Detect bypass attempts
        bypass_attempts = self.detect_bypass_attempts(original_text, normalized_text)
        if bypass_attempts:
            logger.warning(
                f"Detected bypass attempts: {', '.join(bypass_attempts)}"
            )

        # Layer 3: Check dangerous patterns
        has_violations, matched_patterns, blocked_keywords = self.check_dangerous_patterns(
            normalized_text
        )

        # Layer 4: Check confirmation patterns
        required_confirmations = []
        if not has_violations:
            required_confirmations = self.check_confirmation_patterns(normalized_text)

        # Layer 5: Semantic analysis
        semantic_safe, semantic_warnings = self.semantic_analysis(idea)

        # Combine warnings
        warnings = []
        if has_violations:
            warnings.append("Idea violates safety guidelines - see docs/safety.md")
            for keyword in blocked_keywords:
                warnings.append(f"Dangerous operation detected: '{keyword}'")
        warnings.extend(semantic_warnings)

        # Calculate confidence score
        confidence = 1.0
        if bypass_attempts:
            confidence -= 0.2 * len(bypass_attempts)
        if semantic_warnings:
            confidence -= 0.1 * len(semantic_warnings)
        confidence = max(0.0, min(1.0, confidence))

        # Create metadata for audit trail
        metadata = SafetyCheckMetadata(
            normalized_input=normalized_text[:500],  # Limit to 500 chars
            patterns_matched=matched_patterns,
            bypass_attempts_detected=bypass_attempts,
            confidence_score=confidence,
        )

        # Final decision
        approved = not has_violations

        result = SafetyCheck(
            approved=approved,
            warnings=warnings,
            required_confirmations=required_confirmations,
            blocked_keywords=blocked_keywords,
            metadata=metadata,
        )

        if approved:
            logger.info(f"Safety check PASSED (confidence: {confidence:.2f})")
        else:
            logger.warning(
                f"Safety check FAILED: {len(blocked_keywords)} violations "
                f"(confidence: {confidence:.2f})"
            )

        return result
