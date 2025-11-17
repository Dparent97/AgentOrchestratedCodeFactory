"""
SafetyGuard - Enforces safety boundaries and prevents dangerous operations

Validates all project ideas before execution to ensure they don't
violate safety rules or attempt dangerous operations.

Security Improvements:
- Multi-layer validation with normalization
- Regex-based pattern matching resistant to obfuscation
- Semantic analysis for dangerous operation detection
- Whitelist approach for approved operations
- Comprehensive audit logging
"""

import logging
import re
import unicodedata
from datetime import datetime
from typing import List, Tuple, Set

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import Idea, SafetyCheck, SafetyCheckMetadata

logger = logging.getLogger(__name__)


class SafetyGuard(BaseAgent):
    """
    Validates ideas for safety and enforces security boundaries

    This class implements defense-in-depth security with multiple validation layers:
    1. Input normalization to prevent bypass via encoding/obfuscation
    2. Regex-based pattern matching for dangerous operations
    3. Semantic analysis for context-aware detection
    4. Whitelist validation for approved operations
    """

    # Dangerous operation patterns (regex-based for robustness)
    # Format: (pattern, description, severity)
    DANGEROUS_PATTERNS = [
        # Physical system control
        (r'control\s*equipment', "Physical equipment control", "critical"),
        (r'\bactuate\b', "Actuator control", "critical"),
        (r'bypass\s*interlock', "Safety interlock bypass", "critical"),
        (r'override\s*safety', "Safety override", "critical"),
        (r'disable\s*alarm', "Alarm disabling", "critical"),
        (r'physical\s*control', "Physical control system", "critical"),

        # Security violations (use word boundaries to avoid false positives)
        (r'\bhack\b', "Hacking/unauthorized access", "critical"),
        (r'\bexploit\b', "Exploit development", "critical"),
        (r'crack\s*password', "Password cracking", "critical"),
        (r'\binject\b', "Code/SQL injection", "critical"),
        (r'\bmalware\b', "Malware development", "critical"),
        (r'\bvirus\b', "Virus development", "critical"),
        (r'\bbackdoor\b', "Backdoor installation", "critical"),
        (r'privilege\s*escalation', "Privilege escalation", "critical"),

        # Destructive operations
        (r'rm\s+r?f?\b', "Recursive deletion (rm -rf)", "critical"),
        (r'format\s*drive', "Drive formatting", "critical"),
        (r'delete\s*all', "Mass deletion", "critical"),
        (r'drop\s*database', "Database deletion", "critical"),
        (r'truncate\s*table', "Table truncation", "critical"),

        # Obfuscation attempts (common bypass techniques)
        (r'b[a4]se\s*64\s*decode', "Base64 decode (potential obfuscation)", "high"),
        (r'eval\s*\(', "Dynamic code evaluation", "high"),
        (r'exec\s*\(', "Dynamic code execution", "high"),
        (r'__import__', "Dynamic import (potential obfuscation)", "medium"),
        (r'compile\s*\(', "Dynamic compilation", "medium"),
    ]

    # Operations requiring confirmation (medium risk)
    CONFIRMATION_PATTERNS = [
        (r'delete\s*file', "File deletion", "medium"),
        (r'send\s*email', "Email sending", "medium"),
        (r'network\s*call', "Network communication", "medium"),
        (r'api\s*request', "API request", "medium"),
        (r'modify\s*database', "Database modification", "medium"),
        (r'sudo', "Elevated privileges", "high"),
        (r'admin\s*privilege', "Admin privileges", "high"),
        (r'system\s*call', "System call", "medium"),
        (r'subprocess', "Subprocess execution", "medium"),
    ]

    # Approved safe operations (whitelist approach)
    APPROVED_OPERATIONS = {
        'read', 'display', 'show', 'list', 'view', 'get', 'fetch',
        'calculate', 'compute', 'analyze', 'parse', 'validate',
        'format', 'convert', 'transform', 'encode', 'decode',
        'log', 'track', 'monitor', 'measure', 'report',
        'search', 'find', 'filter', 'sort', 'query',
        'create', 'generate', 'build', 'make', 'initialize',
        'test', 'verify', 'check', 'inspect', 'scan',
        'update', 'modify', 'edit', 'change', 'adjust',  # Safe when scoped
        'help', 'guide', 'assist', 'support', 'document',
    }

    # Keywords indicating destructive intent
    DESTRUCTIVE_INDICATORS = {
        'destroy', 'wipe', 'erase', 'corrupt', 'damage', 'break',
        'crash', 'kill', 'terminate', 'force', 'bypass', 'override',
        'disable', 'circumvent', 'evade', 'hide', 'obfuscate',
    }

    @property
    def name(self) -> str:
        return "safety_guard"

    @property
    def description(self) -> str:
        return "Validates ideas for safety compliance and security with multi-layer protection"

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text to prevent bypass attempts via obfuscation

        Normalization steps:
        1. Unicode normalization (NFKD)
        2. Convert to lowercase
        3. Remove accents and diacritics
        4. Replace special separators with spaces
        5. Collapse multiple whitespaces
        6. Remove zero-width characters

        Args:
            text: Raw input text

        Returns:
            Normalized text
        """
        # Unicode normalization
        text = unicodedata.normalize('NFKD', text)

        # Remove accents and convert to ASCII
        text = ''.join(c for c in text if not unicodedata.combining(c))

        # Convert to lowercase
        text = text.lower()

        # Replace various separators with spaces
        separators = ['_', '-', '.', '/', '\\', '|', '\t', '\n', '\r']
        for sep in separators:
            text = text.replace(sep, ' ')

        # Remove zero-width characters and other invisible Unicode
        text = re.sub(r'[\u200b-\u200f\u202a-\u202e\u2060-\u206f\ufeff]', '', text)

        # Collapse multiple spaces
        text = re.sub(r'\s+', ' ', text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    @staticmethod
    def extract_verbs(text: str) -> Set[str]:
        """
        Extract verbs and action words from text for semantic analysis

        Uses simple heuristics to identify action words without requiring
        complex NLP dependencies.

        Args:
            text: Normalized text

        Returns:
            Set of potential action verbs
        """
        words = text.split()

        # Common verb suffixes and patterns
        verb_indicators = ['ing', 'ate', 'ify', 'ize', 'ise']

        verbs = set()
        for word in words:
            # Add words that end with verb indicators
            if any(word.endswith(indicator) for indicator in verb_indicators):
                verbs.add(word)
            # Add words that are likely verbs (simple heuristic)
            if len(word) > 3 and word.isalpha():
                verbs.add(word)

        return verbs

    def check_patterns(
        self,
        normalized_text: str,
        patterns: List[Tuple[str, str, str]]
    ) -> List[Tuple[str, str, str]]:
        """
        Check text against regex patterns

        Args:
            normalized_text: Normalized input text
            patterns: List of (pattern, description, severity) tuples

        Returns:
            List of matched patterns with their metadata
        """
        matches = []

        for pattern, description, severity in patterns:
            # Compile with IGNORECASE for extra safety
            regex = re.compile(pattern, re.IGNORECASE)

            if regex.search(normalized_text):
                matches.append((pattern, description, severity))
                logger.warning(
                    f"Pattern match: '{description}' (severity: {severity})"
                )

        return matches

    def semantic_analysis(self, normalized_text: str) -> List[str]:
        """
        Perform semantic analysis to detect dangerous operations

        Analyzes the text for combinations of action verbs and destructive
        indicators that suggest dangerous intent.

        Args:
            normalized_text: Normalized input text

        Returns:
            List of semantic flags detected
        """
        flags = []

        # Extract action verbs
        verbs = self.extract_verbs(normalized_text)

        # Check for destructive verb combinations
        destructive_verbs = verbs & self.DESTRUCTIVE_INDICATORS
        if destructive_verbs:
            flags.append(f"Destructive actions detected: {', '.join(destructive_verbs)}")

        # Check for lack of approved operations
        approved_verbs = verbs & self.APPROVED_OPERATIONS
        if not approved_verbs and len(normalized_text) > 20:
            flags.append("No clearly approved operations detected")

        # Check for multiple high-risk combinations
        if 'system' in normalized_text and any(
            word in normalized_text for word in ['control', 'access', 'modify', 'override']
        ):
            flags.append("System-level operation with control verbs")

        # Check for encoding/obfuscation indicators
        if any(indicator in normalized_text for indicator in ['encode', 'decode', 'obfuscate', 'hide']):
            if any(risky in normalized_text for risky in ['execute', 'eval', 'run', 'exec']):
                flags.append("Potential code obfuscation for execution")

        return flags

    def whitelist_check(self, normalized_text: str) -> List[str]:
        """
        Check if operations are in the approved whitelist

        Args:
            normalized_text: Normalized input text

        Returns:
            List of whitelist violations (operations not approved)
        """
        violations = []

        # Extract words that look like operations
        words = set(normalized_text.split())

        # Check if text contains primarily non-approved operations
        operation_words = words - {'the', 'a', 'an', 'to', 'for', 'with', 'and', 'or', 'in', 'on', 'at'}

        if operation_words:
            non_approved = operation_words - self.APPROVED_OPERATIONS

            # If most operations are not approved, flag it
            if non_approved and len(non_approved) > len(operation_words) * 0.3:
                violations.append(
                    f"Contains unapproved operations: {', '.join(list(non_approved)[:5])}"
                )

        return violations

    def execute(self, input_data: Idea) -> SafetyCheck:
        """
        Validate idea for safety with multi-layer protection

        Security layers:
        1. Input normalization
        2. Dangerous pattern detection
        3. Confirmation-required pattern detection
        4. Semantic analysis
        5. Whitelist validation

        Args:
            input_data: Idea to validate

        Returns:
            SafetyCheck: Safety validation result with detailed metadata
        """
        idea = self.validate_input(input_data, Idea)

        # Build combined text from all idea fields
        text_parts = [idea.description] + idea.features + idea.constraints
        if idea.environment:
            text_parts.append(idea.environment)

        raw_text = ' '.join(text_parts)

        logger.info(f"Safety check initiated for: {idea.description[:50]}...")
        logger.info(f"Full input length: {len(raw_text)} characters")

        # LAYER 1: Normalize input to prevent bypass
        normalized_text = self.normalize_text(raw_text)
        logger.debug(f"Normalized text: {normalized_text[:100]}...")

        # Initialize tracking variables
        warnings = []
        required_confirmations = []
        blocked_keywords = []
        approved = True
        patterns_matched = []
        semantic_flags = []
        whitelist_violations = []

        # LAYER 2: Check dangerous patterns
        dangerous_matches = self.check_patterns(normalized_text, self.DANGEROUS_PATTERNS)

        for pattern, description, severity in dangerous_matches:
            blocked_keywords.append(description)
            patterns_matched.append(f"{description} (pattern: {pattern})")
            approved = False
            warnings.append(
                f"BLOCKED: Dangerous operation detected - {description} (severity: {severity})"
            )
            logger.error(f"SECURITY VIOLATION: {description} - Pattern: {pattern}")

        # LAYER 3: Check confirmation-required patterns (only if not already blocked)
        if approved:
            confirmation_matches = self.check_patterns(normalized_text, self.CONFIRMATION_PATTERNS)

            for pattern, description, severity in confirmation_matches:
                patterns_matched.append(f"{description} (pattern: {pattern})")
                required_confirmations.append(
                    f"This tool may perform: {description}. Human confirmation required (risk: {severity})."
                )
                logger.warning(f"Confirmation required: {description}")

        # LAYER 4: Semantic analysis
        semantic_flags = self.semantic_analysis(normalized_text)

        for flag in semantic_flags:
            logger.warning(f"Semantic flag: {flag}")

            # Critical semantic flags can block approval
            if any(critical in flag.lower() for critical in ['destructive', 'obfuscation', 'system level']):
                if approved:  # Don't override existing blocks
                    approved = False
                    warnings.append(f"BLOCKED: Semantic analysis detected: {flag}")
                    logger.error(f"SEMANTIC VIOLATION: {flag}")
            else:
                warnings.append(f"Warning: {flag}")

        # LAYER 5: Whitelist validation
        whitelist_violations = self.whitelist_check(normalized_text)

        for violation in whitelist_violations:
            logger.info(f"Whitelist check: {violation}")
            # Whitelist violations are informational, not blocking
            warnings.append(f"Note: {violation}")

        # Add general safety warning if blocked
        if not approved:
            warnings.append(
                "Idea violates safety guidelines. See docs/safety.md for approved operations."
            )

        # Calculate confidence score
        confidence_score = 1.0
        if semantic_flags:
            confidence_score -= 0.1 * len(semantic_flags)
        if whitelist_violations:
            confidence_score -= 0.05 * len(whitelist_violations)
        confidence_score = max(0.0, min(1.0, confidence_score))

        # Create metadata for audit trail
        metadata = SafetyCheckMetadata(
            timestamp=datetime.now(),
            normalized_text=normalized_text,
            patterns_matched=patterns_matched,
            semantic_flags=semantic_flags,
            whitelist_violations=whitelist_violations,
            confidence_score=confidence_score
        )

        # Build result
        result = SafetyCheck(
            approved=approved,
            warnings=warnings,
            required_confirmations=required_confirmations,
            blocked_keywords=blocked_keywords,
            metadata=metadata
        )

        # Audit logging
        if approved:
            logger.info(
                f"Safety check PASSED (confidence: {confidence_score:.2f}, "
                f"confirmations: {len(required_confirmations)})"
            )
        else:
            logger.error(
                f"Safety check FAILED - {len(blocked_keywords)} critical violations detected"
            )
            logger.error(f"Blocked operations: {', '.join(blocked_keywords)}")

        # Log audit trail
        logger.info(
            f"AUDIT: timestamp={metadata.timestamp.isoformat()}, "
            f"approved={approved}, violations={len(blocked_keywords)}, "
            f"confirmations={len(required_confirmations)}"
        )

        return result
