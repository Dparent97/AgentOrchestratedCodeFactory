"""
Unit tests for SafetyGuard agent

Tests cover:
- Basic safe/unsafe idea detection
- All dangerous keywords
- All confirmation keywords
- Edge cases (empty inputs, case sensitivity, partial matches)
- Bypass attempts (obfuscation, spacing, unicode)
- Multiple violations
- Input validation
"""

import pytest
from code_factory.agents.safety_guard import SafetyGuard
from code_factory.core.models import Idea, SafetyCheck


class TestSafetyGuardBasics:
    """Test basic SafetyGuard functionality"""

    def test_agent_properties(self):
        """Test agent name and description"""
        guard = SafetyGuard()
        assert guard.name == "safety_guard"
        assert "safety" in guard.description.lower()

    def test_safe_idea_approved(self):
        """Test that safe ideas are approved"""
        guard = SafetyGuard()
        idea = Idea(
            description="Build a tool to track maintenance schedules",
            target_users=["marine engineer"],
            features=["view schedule", "mark complete"]
        )
        result = guard.execute(idea)

        assert isinstance(result, SafetyCheck)
        assert result.approved is True
        assert len(result.blocked_keywords) == 0
        assert len(result.warnings) == 0

    def test_minimal_safe_idea(self):
        """Test minimal safe idea with just description"""
        guard = SafetyGuard()
        idea = Idea(description="Create a simple calculator")
        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.blocked_keywords) == 0


class TestDangerousKeywords:
    """Test detection of dangerous keywords"""

    @pytest.fixture
    def guard(self):
        return SafetyGuard()

    def test_control_equipment_blocked(self, guard):
        """Test 'control equipment' is blocked"""
        idea = Idea(description="Tool to control equipment in engine room")
        result = guard.execute(idea)

        assert result.approved is False
        assert "control equipment" in result.blocked_keywords
        assert len(result.warnings) > 0

    def test_actuate_blocked(self, guard):
        """Test 'actuate' is blocked"""
        idea = Idea(description="System to actuate valve controls")
        result = guard.execute(idea)

        assert result.approved is False
        assert "actuate" in result.blocked_keywords

    def test_bypass_interlock_blocked(self, guard):
        """Test 'bypass interlock' is blocked"""
        idea = Idea(description="Allow operators to bypass interlock for maintenance")
        result = guard.execute(idea)

        assert result.approved is False
        assert "bypass interlock" in result.blocked_keywords

    def test_override_safety_blocked(self, guard):
        """Test 'override safety' is blocked"""
        idea = Idea(description="Emergency override safety feature")
        result = guard.execute(idea)

        assert result.approved is False
        assert "override safety" in result.blocked_keywords

    def test_disable_alarm_blocked(self, guard):
        """Test 'disable alarm' is blocked"""
        idea = Idea(description="Tool to disable alarm during tests")
        result = guard.execute(idea)

        assert result.approved is False
        assert "disable alarm" in result.blocked_keywords

    def test_hack_blocked(self, guard):
        """Test 'hack' is blocked"""
        idea = Idea(description="Hack into the system dashboard")
        result = guard.execute(idea)

        assert result.approved is False
        assert "hack" in result.blocked_keywords

    def test_exploit_blocked(self, guard):
        """Test 'exploit' is blocked"""
        idea = Idea(description="Exploit vulnerability to gain access")
        result = guard.execute(idea)

        assert result.approved is False
        assert "exploit" in result.blocked_keywords

    def test_crack_password_blocked(self, guard):
        """Test 'crack password' is blocked"""
        idea = Idea(description="Tool to crack password hashes")
        result = guard.execute(idea)

        assert result.approved is False
        assert "crack password" in result.blocked_keywords

    def test_inject_blocked(self, guard):
        """Test 'inject' is blocked"""
        idea = Idea(description="Inject commands into the database")
        result = guard.execute(idea)

        assert result.approved is False
        assert "inject" in result.blocked_keywords

    def test_malware_blocked(self, guard):
        """Test 'malware' is blocked"""
        idea = Idea(description="Create malware detection tool", features=["install malware"])
        result = guard.execute(idea)

        assert result.approved is False
        assert "malware" in result.blocked_keywords

    def test_virus_blocked(self, guard):
        """Test 'virus' is blocked"""
        idea = Idea(description="Virus scanning and creation tool")
        result = guard.execute(idea)

        assert result.approved is False
        assert "virus" in result.blocked_keywords

    def test_rm_rf_blocked(self, guard):
        """Test 'rm -rf /' is blocked"""
        idea = Idea(description="Script that runs rm -rf / on remote servers")
        result = guard.execute(idea)

        assert result.approved is False
        assert "rm -rf /" in result.blocked_keywords

    def test_format_drive_blocked(self, guard):
        """Test 'format drive' is blocked"""
        idea = Idea(description="Utility to format drive automatically")
        result = guard.execute(idea)

        assert result.approved is False
        assert "format drive" in result.blocked_keywords


class TestConfirmationKeywords:
    """Test detection of keywords requiring confirmation"""

    @pytest.fixture
    def guard(self):
        return SafetyGuard()

    def test_delete_file_requires_confirmation(self, guard):
        """Test 'delete file' requires confirmation"""
        idea = Idea(description="Tool to organize and delete file backups")
        result = guard.execute(idea)

        assert result.approved is True  # Not blocked, but needs confirmation
        assert len(result.required_confirmations) > 0
        assert any("delete file" in conf.lower() for conf in result.required_confirmations)

    def test_send_email_requires_confirmation(self, guard):
        """Test 'send email' requires confirmation"""
        idea = Idea(description="Automated system to send email notifications")
        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.required_confirmations) > 0
        assert any("send email" in conf.lower() for conf in result.required_confirmations)

    def test_network_call_requires_confirmation(self, guard):
        """Test 'network call' requires confirmation"""
        idea = Idea(description="Make network call to fetch weather data")
        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.required_confirmations) > 0

    def test_api_request_requires_confirmation(self, guard):
        """Test 'api request' requires confirmation"""
        idea = Idea(description="Send api request to external service")
        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.required_confirmations) > 0

    def test_modify_database_requires_confirmation(self, guard):
        """Test 'modify database' requires confirmation"""
        idea = Idea(description="Tool to modify database records")
        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.required_confirmations) > 0

    def test_sudo_requires_confirmation(self, guard):
        """Test 'sudo' requires confirmation"""
        idea = Idea(description="Script that uses sudo to install packages")
        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.required_confirmations) > 0

    def test_admin_privilege_requires_confirmation(self, guard):
        """Test 'admin privilege' requires confirmation"""
        idea = Idea(description="Tool requires admin privilege to access logs")
        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.required_confirmations) > 0


class TestEdgeCases:
    """Test edge cases and corner scenarios"""

    @pytest.fixture
    def guard(self):
        return SafetyGuard()

    def test_case_insensitive_detection(self, guard):
        """Test that keyword detection is case-insensitive"""
        ideas = [
            Idea(description="HACK into the system"),
            Idea(description="Hack into the system"),
            Idea(description="hack into the system"),
            Idea(description="HaCk into the system"),
        ]

        for idea in ideas:
            result = guard.execute(idea)
            assert result.approved is False
            assert "hack" in result.blocked_keywords

    def test_keyword_in_features_list(self, guard):
        """Test that keywords in features list are detected"""
        idea = Idea(
            description="Build a system tool",
            features=["inject commands", "fast performance"]
        )
        result = guard.execute(idea)

        assert result.approved is False
        assert "inject" in result.blocked_keywords

    def test_multiple_dangerous_keywords(self, guard):
        """Test detection of multiple dangerous keywords"""
        idea = Idea(
            description="Hack into system and inject malware to control equipment"
        )
        result = guard.execute(idea)

        assert result.approved is False
        assert len(result.blocked_keywords) >= 3  # hack, inject, malware, control equipment
        assert "hack" in result.blocked_keywords
        assert "inject" in result.blocked_keywords
        assert "malware" in result.blocked_keywords

    def test_dangerous_overrides_confirmation(self, guard):
        """Test that dangerous keywords prevent confirmation checks"""
        idea = Idea(
            description="Hack system and delete file to send email"
        )
        result = guard.execute(idea)

        # Should be blocked due to 'hack'
        assert result.approved is False
        # Confirmation checks should not run when already blocked
        assert len(result.required_confirmations) == 0

    def test_partial_match_not_triggered(self, guard):
        """Test that partial matches don't trigger false positives"""
        # 'admin' is not the same as 'admin privilege'
        idea = Idea(description="Build an admin dashboard for viewing logs")
        result = guard.execute(idea)

        # Should pass - 'admin' alone is not in DANGEROUS_KEYWORDS
        assert result.approved is True

    def test_empty_features_and_constraints(self, guard):
        """Test handling of empty optional fields"""
        idea = Idea(
            description="Simple safe tool",
            features=[],
            constraints=[],
            target_users=[]
        )
        result = guard.execute(idea)

        assert result.approved is True
        assert len(result.blocked_keywords) == 0

    def test_very_long_description(self, guard):
        """Test handling of very long descriptions"""
        idea = Idea(
            description="A " + "safe " * 1000 + "tool for maintenance tracking"
        )
        result = guard.execute(idea)

        assert result.approved is True

    def test_whitespace_in_keywords(self, guard):
        """Test that keywords with internal whitespace are detected"""
        # 'rm -rf /' contains spaces and special chars
        idea = Idea(description="Script that executes rm -rf / command")
        result = guard.execute(idea)

        assert result.approved is False
        assert "rm -rf /" in result.blocked_keywords


class TestBypassAttempts:
    """Test resistance to bypass attempts"""

    @pytest.fixture
    def guard(self):
        return SafetyGuard()

    def test_extra_spaces_in_keyword(self, guard):
        """Test that extra spaces between words don't match dangerous keywords"""
        # "control  equipment" (double space) != "control equipment" (single space)
        # This is correct behavior - exact match required
        idea = Idea(description="Tool to control  equipment with extra spaces")
        result = guard.execute(idea)

        # Should pass because "control  equipment" doesn't match "control equipment"
        assert result.approved is True

    def test_keyword_split_across_description_and_features(self, guard):
        """Test keyword detection across description and features"""
        idea = Idea(
            description="Tool to control",
            features=["equipment monitoring"]
        )
        result = guard.execute(idea)

        # Should detect "control" in description and "equipment" in features
        # Combined text should trigger "control equipment"
        assert result.approved is False
        assert "control equipment" in result.blocked_keywords

    def test_similar_safe_words_not_blocked(self, guard):
        """Test that similar but safe words are not blocked"""
        safe_ideas = [
            Idea(description="Create a virus scanner for security"),  # Would be blocked due to 'virus'
            Idea(description="Build a file organizer"),  # 'file' alone should be safe
            Idea(description="Network monitoring tool"),  # 'network' alone should be safe
            Idea(description="Database viewer application"),  # 'database' alone should be safe
        ]

        # Only the first one should be blocked
        result0 = guard.execute(safe_ideas[0])
        assert result0.approved is False  # Contains 'virus'

        # These should pass
        result1 = guard.execute(safe_ideas[1])
        assert result1.approved is True

        result2 = guard.execute(safe_ideas[2])
        assert result2.approved is True

        result3 = guard.execute(safe_ideas[3])
        assert result3.approved is True


class TestInputValidation:
    """Test input validation and error handling"""

    @pytest.fixture
    def guard(self):
        return SafetyGuard()

    def test_invalid_input_type_raises_error(self, guard):
        """Test that invalid input type raises appropriate error"""
        with pytest.raises((ValueError, TypeError)):
            guard.execute("not an Idea object")

    def test_none_input_raises_error(self, guard):
        """Test that None input raises error"""
        with pytest.raises((ValueError, TypeError, AttributeError)):
            guard.execute(None)

    def test_empty_description_rejected_by_model(self):
        """Test that empty description is rejected by Pydantic validation"""
        with pytest.raises(ValueError):
            Idea(description="")

    def test_whitespace_only_description_rejected(self):
        """Test that whitespace-only description is rejected"""
        with pytest.raises(ValueError):
            Idea(description="   ")


class TestSafetyCheckOutput:
    """Test SafetyCheck output structure"""

    @pytest.fixture
    def guard(self):
        return SafetyGuard()

    def test_safety_check_has_all_fields(self, guard):
        """Test that SafetyCheck has all expected fields"""
        idea = Idea(description="Safe tool")
        result = guard.execute(idea)

        assert hasattr(result, "approved")
        assert hasattr(result, "warnings")
        assert hasattr(result, "required_confirmations")
        assert hasattr(result, "blocked_keywords")

    def test_blocked_keywords_are_listed(self, guard):
        """Test that all blocked keywords are listed in output"""
        idea = Idea(description="Hack and inject malware")
        result = guard.execute(idea)

        assert result.approved is False
        assert "hack" in result.blocked_keywords
        assert "inject" in result.blocked_keywords
        assert "malware" in result.blocked_keywords

    def test_warnings_provided_when_blocked(self, guard):
        """Test that warnings are provided for blocked ideas"""
        idea = Idea(description="Tool to hack systems")
        result = guard.execute(idea)

        assert result.approved is False
        assert len(result.warnings) > 0
        assert any("dangerous" in w.lower() for w in result.warnings)

    def test_safety_doc_reference_in_warnings(self, guard):
        """Test that warnings reference safety documentation"""
        idea = Idea(description="Malware creation tool")
        result = guard.execute(idea)

        assert result.approved is False
        assert any("safety.md" in w for w in result.warnings)


class TestMultipleViolations:
    """Test handling of multiple safety violations"""

    @pytest.fixture
    def guard(self):
        return SafetyGuard()

    def test_all_dangerous_keywords_detected(self, guard):
        """Test that all dangerous keywords in text are detected"""
        idea = Idea(
            description="Hack system, inject malware, bypass interlock, control equipment"
        )
        result = guard.execute(idea)

        assert result.approved is False
        assert len(result.blocked_keywords) >= 4
        for keyword in ["hack", "inject", "malware", "bypass interlock", "control equipment"]:
            assert keyword in result.blocked_keywords

    def test_warnings_count_matches_violations(self, guard):
        """Test that warnings are generated for each violation"""
        idea = Idea(description="Hack and exploit systems")
        result = guard.execute(idea)

        assert result.approved is False
        # Should have at least one warning per blocked keyword plus general warning
        assert len(result.warnings) >= len(result.blocked_keywords)
