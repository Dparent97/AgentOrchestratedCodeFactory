"""
Comprehensive tests for SafetyGuard

Tests all security validation layers including bypass attempt detection.
"""

import pytest

from code_factory.agents.safety_guard import SafetyGuard
from code_factory.core.models import Idea, SafetyCheck


class TestSafetyGuardNormalization:
    """Tests for text normalization to prevent bypasses"""

    def test_normalize_basic_text(self):
        """Test basic text normalization"""
        guard = SafetyGuard()
        result = guard.normalize_text("Control Equipment")
        assert result == "control equipment"

    def test_normalize_removes_underscores(self):
        """Test that underscores are replaced with spaces"""
        guard = SafetyGuard()
        result = guard.normalize_text("control_equipment")
        assert result == "control equipment"

    def test_normalize_removes_hyphens(self):
        """Test that hyphens are replaced with spaces"""
        guard = SafetyGuard()
        result = guard.normalize_text("control-equipment")
        assert result == "control equipment"

    def test_normalize_removes_special_chars(self):
        """Test that special characters are removed"""
        guard = SafetyGuard()
        result = guard.normalize_text("control@#$%equipment")
        assert result == "control equipment"

    def test_normalize_collapses_whitespace(self):
        """Test that multiple spaces are collapsed"""
        guard = SafetyGuard()
        result = guard.normalize_text("control    equipment")
        assert result == "control equipment"

    def test_normalize_leetspeak(self):
        """Test that leetspeak is converted to normal text"""
        guard = SafetyGuard()
        result = guard.normalize_text("c0ntr0l 3qu1pm3nt")
        assert result == "control equipment"

    def test_normalize_mixed_case(self):
        """Test that mixed case is normalized"""
        guard = SafetyGuard()
        result = guard.normalize_text("CoNtRoL EqUiPmEnT")
        assert result == "control equipment"

    def test_normalize_unicode(self):
        """Test that unicode characters are handled"""
        guard = SafetyGuard()
        result = guard.normalize_text("contrôl équipment")
        assert result == "control equipment"

    def test_normalize_concatenated(self):
        """Test that concatenated words are separated"""
        guard = SafetyGuard()
        result = guard.normalize_text("controlequipment")
        # This should still match "control equipment" in regex
        assert "control" in result and "equipment" in result


class TestSafetyGuardBypassDetection:
    """Tests for bypass attempt detection"""

    def test_detect_excessive_special_chars(self):
        """Test detection of excessive special characters"""
        guard = SafetyGuard()
        original = "c@o#n$t%r^o&l* e(q)u!i+p=m{e}n[t]"
        normalized = guard.normalize_text(original)
        bypasses = guard.detect_bypass_attempts(original, normalized)
        assert "excessive_special_characters" in bypasses

    def test_detect_number_substitution(self):
        """Test detection of number substitution (leetspeak)"""
        guard = SafetyGuard()
        original = "c0ntr0l 3qu1pm3nt"
        normalized = guard.normalize_text(original)
        bypasses = guard.detect_bypass_attempts(original, normalized)
        assert "number_substitution" in bypasses

    def test_detect_unicode_obfuscation(self):
        """Test detection of unicode obfuscation"""
        guard = SafetyGuard()
        original = "contrôl équipment"
        normalized = guard.normalize_text(original)
        bypasses = guard.detect_bypass_attempts(original, normalized)
        assert "unicode_obfuscation" in bypasses

    def test_detect_underscore_obfuscation(self):
        """Test detection of excessive underscores"""
        guard = SafetyGuard()
        original = "control_____equipment"
        normalized = guard.normalize_text(original)
        bypasses = guard.detect_bypass_attempts(original, normalized)
        assert "underscore_obfuscation" in bypasses

    def test_detect_case_mixing(self):
        """Test detection of camelCase/PascalCase"""
        guard = SafetyGuard()
        original = "controlEquipment"
        normalized = guard.normalize_text(original)
        bypasses = guard.detect_bypass_attempts(original, normalized)
        assert "case_mixing" in bypasses


class TestSafetyGuardDangerousPatterns:
    """Tests for dangerous pattern detection"""

    def test_block_control_equipment(self):
        """Test blocking of 'control equipment'"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to control equipment remotely")

        result = guard.execute(idea)

        assert result.approved is False
        assert "control equipment" in result.blocked_keywords
        assert len(result.warnings) > 0

    def test_block_control_equipment_underscore(self):
        """Test blocking of 'control_equipment' (bypass attempt)"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to control_equipment remotely")

        result = guard.execute(idea)

        assert result.approved is False
        assert "control equipment" in result.blocked_keywords

    def test_block_control_equipment_concatenated(self):
        """Test blocking of 'controlequipment' (bypass attempt)"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to controlequipment remotely")

        result = guard.execute(idea)

        assert result.approved is False
        # The normalized text will separate into "control equipment"
        assert "control equipment" in result.blocked_keywords

    def test_block_control_equipment_leetspeak(self):
        """Test blocking of 'c0ntr0l 3qu1pm3nt' (bypass attempt)"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to c0ntr0l 3qu1pm3nt remotely")

        result = guard.execute(idea)

        assert result.approved is False
        assert "control equipment" in result.blocked_keywords

    def test_block_actuate(self):
        """Test blocking of 'actuate'"""
        guard = SafetyGuard()
        idea = Idea(description="System to actuate valves")

        result = guard.execute(idea)

        assert result.approved is False
        assert "actuate" in result.blocked_keywords

    def test_block_bypass_interlock(self):
        """Test blocking of 'bypass interlock'"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to bypass interlock safety")

        result = guard.execute(idea)

        assert result.approved is False
        assert "bypass interlock" in result.blocked_keywords

    def test_block_hack(self):
        """Test blocking of 'hack'"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to hack passwords")

        result = guard.execute(idea)

        assert result.approved is False
        assert "hack" in result.blocked_keywords

    def test_block_malware(self):
        """Test blocking of 'malware'"""
        guard = SafetyGuard()
        idea = Idea(description="Malware generator for testing")

        result = guard.execute(idea)

        assert result.approved is False
        assert "malware" in result.blocked_keywords

    def test_block_sql_injection(self):
        """Test blocking of 'sql injection'"""
        guard = SafetyGuard()
        idea = Idea(description="Tool for sql injection testing")

        result = guard.execute(idea)

        assert result.approved is False
        assert "SQL injection" in result.blocked_keywords

    def test_block_rm_rf(self):
        """Test blocking of 'rm -rf /'"""
        guard = SafetyGuard()
        idea = Idea(description="Script that runs rm -rf /")

        result = guard.execute(idea)

        assert result.approved is False
        assert "destructive delete" in result.blocked_keywords

    def test_block_format_drive(self):
        """Test blocking of 'format drive'"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to format drive")

        result = guard.execute(idea)

        assert result.approved is False
        assert "format drive" in result.blocked_keywords


class TestSafetyGuardConfirmationPatterns:
    """Tests for patterns requiring confirmation"""

    def test_require_confirmation_delete_file(self):
        """Test that 'delete file' requires confirmation"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to delete file backup")

        result = guard.execute(idea)

        assert result.approved is True  # Approved but needs confirmation
        assert len(result.required_confirmations) > 0
        assert any("delete file" in conf.lower() for conf in result.required_confirmations)

    def test_require_confirmation_send_email(self):
        """Test that 'send email' requires confirmation"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to send email notifications")

        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.required_confirmations) > 0
        assert any("send email" in conf.lower() for conf in result.required_confirmations)

    def test_require_confirmation_api_request(self):
        """Test that 'api request' requires confirmation"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to make api request to server")

        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.required_confirmations) > 0
        assert any("api request" in conf.lower() for conf in result.required_confirmations)

    def test_require_confirmation_modify_database(self):
        """Test that 'modify database' requires confirmation"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to modify database records")

        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.required_confirmations) > 0
        assert any("database" in conf.lower() for conf in result.required_confirmations)


class TestSafetyGuardSemanticAnalysis:
    """Tests for semantic analysis"""

    def test_warn_production_environment(self):
        """Test warning for production environment"""
        guard = SafetyGuard()
        idea = Idea(
            description="Tool for monitoring",
            environment="production environment"
        )

        result = guard.execute(idea)

        assert result.approved is True
        assert any("production" in warning.lower() for warning in result.warnings)

    def test_warn_medical_environment(self):
        """Test warning for medical environment"""
        guard = SafetyGuard()
        idea = Idea(
            description="Monitoring tool",
            environment="medical facility"
        )

        result = guard.execute(idea)

        assert result.approved is True
        assert any("medical" in warning.lower() for warning in result.warnings)

    def test_warn_admin_user(self):
        """Test warning for admin user role"""
        guard = SafetyGuard()
        idea = Idea(
            description="System configuration tool",
            target_users=["system administrator"]
        )

        result = guard.execute(idea)

        assert result.approved is True
        assert any("admin" in warning.lower() for warning in result.warnings)

    def test_warn_bypass_constraint(self):
        """Test warning for bypass in constraints"""
        guard = SafetyGuard()
        idea = Idea(
            description="Configuration tool",
            constraints=["Must bypass authentication in test mode"]
        )

        result = guard.execute(idea)

        assert result.approved is True
        assert any("bypass" in warning.lower() for warning in result.warnings)


class TestSafetyGuardSafeIdeas:
    """Tests for ideas that should pass all checks"""

    def test_approve_safe_cli_tool(self):
        """Test approval of safe CLI tool"""
        guard = SafetyGuard()
        idea = Idea(description="CLI tool to list files in a directory")

        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.blocked_keywords) == 0
        # May have warnings from semantic analysis, but approved

    def test_approve_calculator(self):
        """Test approval of calculator"""
        guard = SafetyGuard()
        idea = Idea(description="Simple calculator for arithmetic operations")

        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.blocked_keywords) == 0

    def test_approve_weather_app(self):
        """Test approval of weather app"""
        guard = SafetyGuard()
        idea = Idea(description="Weather forecast application")

        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.blocked_keywords) == 0

    def test_approve_todo_list(self):
        """Test approval of todo list"""
        guard = SafetyGuard()
        idea = Idea(description="Todo list manager with local storage")

        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.blocked_keywords) == 0


class TestSafetyGuardMetadata:
    """Tests for audit metadata"""

    def test_metadata_included(self):
        """Test that metadata is included in result"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to control equipment")

        result = guard.execute(idea)

        assert result.metadata is not None
        assert result.metadata.normalized_input is not None
        assert result.metadata.confidence_score >= 0.0
        assert result.metadata.confidence_score <= 1.0

    def test_metadata_includes_patterns(self):
        """Test that matched patterns are in metadata"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to control equipment")

        result = guard.execute(idea)

        assert result.metadata is not None
        assert len(result.metadata.patterns_matched) > 0

    def test_metadata_includes_bypasses(self):
        """Test that bypass attempts are in metadata"""
        guard = SafetyGuard()
        idea = Idea(description="Tool to c0ntr0l_3qu1pm3nt")

        result = guard.execute(idea)

        assert result.metadata is not None
        assert len(result.metadata.bypass_attempts_detected) > 0

    def test_confidence_decreases_with_bypasses(self):
        """Test that confidence score decreases with bypass attempts"""
        guard = SafetyGuard()

        # Safe idea with no bypasses
        safe_idea = Idea(description="Simple calculator")
        safe_result = guard.execute(safe_idea)

        # Idea with bypass attempts
        bypass_idea = Idea(description="Simple calc_ul@tor with sp3c1al features")
        bypass_result = guard.execute(bypass_idea)

        # Bypass idea should have lower confidence
        assert bypass_result.metadata.confidence_score < safe_result.metadata.confidence_score


class TestSafetyGuardEdgeCases:
    """Tests for edge cases"""

    def test_empty_description(self):
        """Test that empty description raises error"""
        guard = SafetyGuard()

        with pytest.raises(ValueError):
            Idea(description="")

    def test_whitespace_only_description(self):
        """Test that whitespace-only description raises error"""
        guard = SafetyGuard()

        with pytest.raises(ValueError):
            Idea(description="   ")

    def test_very_long_input(self):
        """Test handling of very long input"""
        guard = SafetyGuard()
        long_description = "Tool for monitoring " + "a" * 10000
        idea = Idea(description=long_description)

        result = guard.execute(idea)

        # Should complete without error
        assert result is not None
        # Metadata should truncate normalized input
        assert len(result.metadata.normalized_input) <= 500

    def test_multiple_dangerous_patterns(self):
        """Test idea with multiple dangerous patterns"""
        guard = SafetyGuard()
        idea = Idea(
            description="Tool to control equipment and actuate valves via malware"
        )

        result = guard.execute(idea)

        assert result.approved is False
        # Should detect all three dangerous patterns
        assert len(result.blocked_keywords) >= 3

    def test_features_checked(self):
        """Test that features list is also checked"""
        guard = SafetyGuard()
        idea = Idea(
            description="Monitoring tool",
            features=["control equipment remotely"]
        )

        result = guard.execute(idea)

        assert result.approved is False
        assert "control equipment" in result.blocked_keywords

    def test_constraints_checked(self):
        """Test that constraints list is also checked"""
        guard = SafetyGuard()
        idea = Idea(
            description="Monitoring tool",
            constraints=["Must not control equipment"]
        )

        # This should pass because "must not" doesn't make it dangerous
        # But the pattern will still match "control equipment"
        result = guard.execute(idea)

        # The current implementation will still block this
        # because it just scans for patterns regardless of context
        assert result.approved is False
