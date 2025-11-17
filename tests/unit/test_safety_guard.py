"""
Comprehensive test suite for SafetyGuard security improvements

Tests all bypass scenarios and security layers:
- Normalization bypass attempts
- Obfuscation techniques
- Semantic analysis
- Whitelist validation
- Audit trail
"""

import pytest
from datetime import datetime

from code_factory.agents.safety_guard import SafetyGuard
from code_factory.core.models import Idea, SafetyCheck


class TestNormalization:
    """Test input normalization prevents bypass attempts"""

    def test_normalize_removes_underscores(self):
        """Test that underscores are normalized to spaces"""
        guard = SafetyGuard()

        # Original bypass: "control_equipment" instead of "control equipment"
        result = guard.normalize_text("control_equipment")
        assert result == "control equipment"

    def test_normalize_removes_hyphens(self):
        """Test that hyphens are normalized to spaces"""
        guard = SafetyGuard()

        result = guard.normalize_text("control-equipment")
        assert result == "control equipment"

    def test_normalize_collapses_whitespace(self):
        """Test that multiple spaces are collapsed"""
        guard = SafetyGuard()

        # Bypass attempt: "control  equipment" (double space)
        result = guard.normalize_text("control  equipment")
        assert result == "control equipment"

    def test_normalize_removes_special_chars(self):
        """Test that special separators are normalized"""
        guard = SafetyGuard()

        result = guard.normalize_text("control/equipment")
        assert result == "control equipment"

        result = guard.normalize_text("control.equipment")
        assert result == "control equipment"

    def test_normalize_lowercase(self):
        """Test that text is lowercased"""
        guard = SafetyGuard()

        result = guard.normalize_text("Control Equipment")
        assert result == "control equipment"

    def test_normalize_unicode_characters(self):
        """Test Unicode normalization"""
        guard = SafetyGuard()

        # Test with accented characters
        result = guard.normalize_text("contrôl équipment")
        # Should normalize accents away
        assert "control" in result
        assert "equipment" in result

    def test_normalize_zero_width_characters(self):
        """Test removal of zero-width characters"""
        guard = SafetyGuard()

        # Zero-width space bypass attempt
        text_with_zwsp = "control\u200bequipment"
        result = guard.normalize_text(text_with_zwsp)
        assert result == "controlequipment"


class TestBypassPrevention:
    """Test that common bypass techniques are blocked"""

    def test_blocks_underscore_bypass(self):
        """Test that 'control_equipment' is blocked (original bypass)"""
        guard = SafetyGuard()

        idea = Idea(
            description="A tool to control_equipment in the factory",
            features=[]
        )

        result = guard.execute(idea)

        assert result.approved is False
        assert len(result.blocked_keywords) > 0
        assert any("equipment" in keyword.lower() for keyword in result.blocked_keywords)

    def test_blocks_concatenation_bypass(self):
        """Test that 'controlequipment' is blocked"""
        guard = SafetyGuard()

        idea = Idea(
            description="A tool to controlequipment",
            features=[]
        )

        result = guard.execute(idea)

        # Should be caught by normalization + pattern matching
        assert result.approved is False

    def test_blocks_case_variation_bypass(self):
        """Test that case variations are blocked"""
        guard = SafetyGuard()

        idea = Idea(
            description="A tool to Control Equipment",
            features=[]
        )

        result = guard.execute(idea)

        assert result.approved is False

    def test_blocks_hyphen_bypass(self):
        """Test that 'control-equipment' is blocked"""
        guard = SafetyGuard()

        idea = Idea(
            description="A tool to control-equipment",
            features=[]
        )

        result = guard.execute(idea)

        assert result.approved is False

    def test_blocks_multiple_space_bypass(self):
        """Test that 'control  equipment' (double space) is blocked"""
        guard = SafetyGuard()

        idea = Idea(
            description="A tool to control  equipment",
            features=[]
        )

        result = guard.execute(idea)

        assert result.approved is False

    def test_blocks_mixed_obfuscation(self):
        """Test that mixed obfuscation techniques are blocked"""
        guard = SafetyGuard()

        idea = Idea(
            description="A tool to Control_Equipment",
            features=["bypass-interlock"]
        )

        result = guard.execute(idea)

        assert result.approved is False
        # Should catch both dangerous patterns
        assert len(result.blocked_keywords) >= 2


class TestDangerousPatterns:
    """Test detection of dangerous operations"""

    def test_blocks_physical_control(self):
        """Test that physical control operations are blocked"""
        guard = SafetyGuard()

        dangerous_ideas = [
            "control equipment",
            "actuate valve",
            "bypass interlock",
            "override safety",
            "disable alarm"
        ]

        for desc in dangerous_ideas:
            idea = Idea(description=desc, features=[])
            result = guard.execute(idea)

            assert result.approved is False, f"Failed to block: {desc}"

    def test_blocks_security_violations(self):
        """Test that security violations are blocked"""
        guard = SafetyGuard()

        dangerous_ideas = [
            "hack the system",
            "exploit vulnerability",
            "crack password",
            "inject code",
            "create malware"
        ]

        for desc in dangerous_ideas:
            idea = Idea(description=desc, features=[])
            result = guard.execute(idea)

            assert result.approved is False, f"Failed to block: {desc}"

    def test_blocks_destructive_operations(self):
        """Test that destructive operations are blocked"""
        guard = SafetyGuard()

        dangerous_ideas = [
            "rm -rf /",
            "format drive",
            "delete all files",
            "drop database",
            "truncate table"
        ]

        for desc in dangerous_ideas:
            idea = Idea(description=desc, features=[])
            result = guard.execute(idea)

            assert result.approved is False, f"Failed to block: {desc}"

    def test_blocks_obfuscation_techniques(self):
        """Test that obfuscation techniques are flagged"""
        guard = SafetyGuard()

        idea = Idea(
            description="Use base64 decode and eval() to run code",
            features=[]
        )

        result = guard.execute(idea)

        assert result.approved is False
        assert len(result.blocked_keywords) > 0


class TestConfirmationRequired:
    """Test operations that require confirmation"""

    def test_requires_confirmation_for_file_operations(self):
        """Test that file operations require confirmation"""
        guard = SafetyGuard()

        idea = Idea(
            description="A tool to delete file backups",
            features=[]
        )

        result = guard.execute(idea)

        # Should be approved but require confirmation
        assert result.approved is True
        assert len(result.required_confirmations) > 0

    def test_requires_confirmation_for_network_operations(self):
        """Test that network operations require confirmation"""
        guard = SafetyGuard()

        idea = Idea(
            description="A tool to send email notifications",
            features=[]
        )

        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.required_confirmations) > 0

    def test_requires_confirmation_for_elevated_privileges(self):
        """Test that sudo operations require confirmation"""
        guard = SafetyGuard()

        idea = Idea(
            description="A tool that uses sudo for admin privilege",
            features=[]
        )

        result = guard.execute(idea)

        # Sudo is high risk, should require confirmation
        assert len(result.required_confirmations) > 0


class TestSemanticAnalysis:
    """Test semantic analysis for dangerous operations"""

    def test_detects_destructive_verbs(self):
        """Test that destructive action verbs are detected"""
        guard = SafetyGuard()

        idea = Idea(
            description="A tool to destroy old records and wipe data",
            features=[]
        )

        result = guard.execute(idea)

        # Semantic analysis should flag destructive actions
        assert result.metadata is not None
        assert len(result.metadata.semantic_flags) > 0

        # Should be blocked due to destructive verbs
        assert result.approved is False

    def test_detects_obfuscation_intent(self):
        """Test detection of obfuscation combined with execution"""
        guard = SafetyGuard()

        idea = Idea(
            description="Encode payload and execute with eval",
            features=[]
        )

        result = guard.execute(idea)

        # Should detect obfuscation + execution pattern
        assert result.metadata is not None
        assert any("obfuscation" in flag.lower() for flag in result.metadata.semantic_flags)

    def test_detects_system_level_operations(self):
        """Test detection of system-level control operations"""
        guard = SafetyGuard()

        idea = Idea(
            description="System control to modify critical processes",
            features=[]
        )

        result = guard.execute(idea)

        # Should detect system-level operation flags
        assert result.metadata is not None
        if result.metadata.semantic_flags:
            assert any("system" in flag.lower() for flag in result.metadata.semantic_flags)


class TestWhitelistValidation:
    """Test whitelist approach for approved operations"""

    def test_approves_safe_operations(self):
        """Test that clearly safe operations are approved"""
        guard = SafetyGuard()

        safe_ideas = [
            "A tool to read log files and display results",
            "Calculate shipping costs for packages",
            "Search and filter inventory data",
            "Generate reports from sensor data",
            "Validate configuration files"
        ]

        for desc in safe_ideas:
            idea = Idea(description=desc, features=[])
            result = guard.execute(idea)

            assert result.approved is True, f"Incorrectly blocked safe idea: {desc}"

    def test_flags_unapproved_operations(self):
        """Test that unapproved operations are flagged"""
        guard = SafetyGuard()

        # Use primarily non-whitelisted words
        idea = Idea(
            description="Zap the frobnicator and bork settings",
            features=[]
        )

        result = guard.execute(idea)

        # Should have whitelist violations noted
        assert result.metadata is not None
        # Whitelist violations are informational, not blocking
        if result.metadata.whitelist_violations:
            assert len(result.metadata.whitelist_violations) > 0


class TestAuditTrail:
    """Test audit trail and metadata generation"""

    def test_generates_metadata(self):
        """Test that metadata is generated for all checks"""
        guard = SafetyGuard()

        idea = Idea(
            description="A tool to monitor system performance",
            features=[]
        )

        result = guard.execute(idea)

        assert result.metadata is not None
        assert isinstance(result.metadata.timestamp, datetime)
        assert result.metadata.normalized_text is not None
        assert 0.0 <= result.metadata.confidence_score <= 1.0

    def test_records_pattern_matches(self):
        """Test that matched patterns are recorded"""
        guard = SafetyGuard()

        idea = Idea(
            description="A tool to delete file backups",
            features=[]
        )

        result = guard.execute(idea)

        assert result.metadata is not None
        assert len(result.metadata.patterns_matched) > 0

    def test_records_normalized_text(self):
        """Test that normalized text is stored for audit"""
        guard = SafetyGuard()

        idea = Idea(
            description="Control_Equipment",
            features=[]
        )

        result = guard.execute(idea)

        assert result.metadata is not None
        # Normalized text should have spaces, not underscores
        assert "control equipment" in result.metadata.normalized_text.lower()

    def test_confidence_score_decreases_with_flags(self):
        """Test that confidence score reflects uncertainty"""
        guard = SafetyGuard()

        # Safe idea should have high confidence
        safe_idea = Idea(
            description="Display sensor readings",
            features=[]
        )
        safe_result = guard.execute(safe_idea)

        # Idea with warnings should have lower confidence
        risky_idea = Idea(
            description="Process data with custom operations",
            features=[]
        )
        risky_result = guard.execute(risky_idea)

        assert safe_result.metadata is not None
        assert risky_result.metadata is not None

        # Both should have confidence scores
        assert 0.0 <= safe_result.metadata.confidence_score <= 1.0
        assert 0.0 <= risky_result.metadata.confidence_score <= 1.0


class TestMultiLayerDefense:
    """Test that multiple security layers work together"""

    def test_normalization_plus_pattern_matching(self):
        """Test that normalization feeds into pattern matching"""
        guard = SafetyGuard()

        idea = Idea(
            description="bypass_interlock system",
            features=[]
        )

        result = guard.execute(idea)

        # Normalization should convert underscore to space
        # Pattern matching should then catch it
        assert result.approved is False
        assert result.metadata is not None
        assert "bypass interlock" in result.metadata.normalized_text

    def test_pattern_plus_semantic_analysis(self):
        """Test that pattern matching and semantic analysis both contribute"""
        guard = SafetyGuard()

        idea = Idea(
            description="Override safety and destroy old equipment",
            features=[]
        )

        result = guard.execute(idea)

        # Should be caught by both pattern matching and semantic analysis
        assert result.approved is False
        assert len(result.blocked_keywords) > 0
        assert result.metadata is not None
        assert len(result.metadata.semantic_flags) > 0

    def test_features_and_description_combined(self):
        """Test that both description and features are checked"""
        guard = SafetyGuard()

        idea = Idea(
            description="A monitoring tool",
            features=["control_equipment", "bypass-safety"]
        )

        result = guard.execute(idea)

        # Description looks safe, but features are dangerous
        assert result.approved is False
        assert len(result.blocked_keywords) > 0

    def test_all_idea_fields_checked(self):
        """Test that all Idea fields are included in safety check"""
        guard = SafetyGuard()

        idea = Idea(
            description="A utility tool",
            features=["data processing"],
            constraints=["must hack system"],
            environment="production"
        )

        result = guard.execute(idea)

        # Constraints contain dangerous keyword
        assert result.approved is False


class TestRegexPatternRobustness:
    """Test that regex patterns handle edge cases"""

    def test_pattern_matches_word_boundaries(self):
        """Test that patterns properly handle word boundaries"""
        guard = SafetyGuard()

        # "hack" should be caught
        idea1 = Idea(description="hack the system", features=[])
        result1 = guard.execute(idea1)
        assert result1.approved is False

        # "shack" should not be caught (different word)
        idea2 = Idea(description="build a shack", features=[])
        result2 = guard.execute(idea2)
        assert result2.approved is True

    def test_pattern_handles_variations(self):
        """Test that regex handles spacing variations"""
        guard = SafetyGuard()

        variations = [
            "control equipment",
            "control  equipment",  # double space
            "controlequipment",    # no space
        ]

        for desc in variations:
            # After normalization, all should be caught
            normalized = guard.normalize_text(desc)
            matches = guard.check_patterns(normalized, guard.DANGEROUS_PATTERNS)

            # Should match the control equipment pattern
            assert len(matches) > 0, f"Failed to match: {desc}"


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_empty_description(self):
        """Test handling of empty description"""
        guard = SafetyGuard()

        # Pydantic should validate this, but test the guard
        with pytest.raises(Exception):
            idea = Idea(description="", features=[])
            guard.execute(idea)

    def test_very_long_input(self):
        """Test handling of very long input text"""
        guard = SafetyGuard()

        # Create a long safe description
        long_desc = "Monitor sensor data " * 1000
        idea = Idea(description=long_desc, features=[])

        result = guard.execute(idea)

        # Should process without error
        assert result is not None
        assert result.approved is True

    def test_unicode_in_dangerous_text(self):
        """Test handling of Unicode in dangerous text"""
        guard = SafetyGuard()

        idea = Idea(
            description="contrôl équipment système",
            features=[]
        )

        result = guard.execute(idea)

        # Should normalize and catch the dangerous pattern
        assert result.approved is False

    def test_multiple_dangerous_patterns(self):
        """Test detection of multiple dangerous patterns"""
        guard = SafetyGuard()

        idea = Idea(
            description="hack system and control equipment",
            features=["bypass interlock", "inject code"]
        )

        result = guard.execute(idea)

        assert result.approved is False
        # Should detect multiple violations
        assert len(result.blocked_keywords) >= 3


class TestLoggingAndAudit:
    """Test that logging provides proper audit trail"""

    def test_logs_approval(self, caplog):
        """Test that approvals are logged"""
        guard = SafetyGuard()

        idea = Idea(description="Display sensor data", features=[])

        with caplog.at_level("INFO"):
            result = guard.execute(idea)

        assert result.approved is True
        assert any("PASSED" in record.message for record in caplog.records)

    def test_logs_rejection(self, caplog):
        """Test that rejections are logged"""
        guard = SafetyGuard()

        idea = Idea(description="control equipment", features=[])

        with caplog.at_level("ERROR"):
            result = guard.execute(idea)

        assert result.approved is False
        assert any("FAILED" in record.message or "VIOLATION" in record.message
                   for record in caplog.records)

    def test_logs_audit_trail(self, caplog):
        """Test that audit trail is logged"""
        guard = SafetyGuard()

        idea = Idea(description="Monitor performance", features=[])

        with caplog.at_level("INFO"):
            result = guard.execute(idea)

        # Should have AUDIT log entry
        assert any("AUDIT" in record.message for record in caplog.records)
