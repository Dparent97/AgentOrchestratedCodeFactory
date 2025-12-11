"""
BlueCollarAdvisor - Ensures solutions fit real-world technician workflows

Reviews project specifications to ensure the generated tool will be
practical and usable in actual field conditions.
"""

import logging
from typing import List, Tuple

from code_factory.core.agent_runtime import BaseAgent
from code_factory.core.models import AdvisoryReport, Idea, ProjectSpec
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AdvisoryInput(BaseModel):
    """Input for blue-collar advisory"""
    idea: Idea
    spec: ProjectSpec


class BlueCollarAdvisor(BaseAgent):
    """
    Provides practical usability advice for field workers
    
    Algorithm:
    1. Analyze ProjectSpec for field-worker usability
    2. Check for: offline capability, simple UI, error tolerance
    3. Evaluate: large buttons/text, noisy environment suitability
    4. Score accessibility on scale of 0-10
    5. Return AdvisoryReport with recommendations, warnings, score
    """
    
    # Usability criteria weights
    CRITERIA_WEIGHTS = {
        "offline_capability": 2.0,
        "simple_interface": 1.5,
        "error_tolerance": 1.5,
        "quick_startup": 1.0,
        "minimal_typing": 1.0,
        "clear_feedback": 1.0,
        "low_dependency": 1.0,
        "field_environment": 1.0,
    }
    
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
        
        idea = advisory_input.idea
        spec = advisory_input.spec
        
        recommendations: List[str] = []
        warnings: List[str] = []
        
        # Step 1: Check offline capability
        offline_score, offline_recs, offline_warns = self._check_offline_capability(idea, spec)
        recommendations.extend(offline_recs)
        warnings.extend(offline_warns)
        
        # Step 2: Check interface simplicity
        ui_score, ui_recs, ui_warns = self._check_interface_simplicity(idea, spec)
        recommendations.extend(ui_recs)
        warnings.extend(ui_warns)
        
        # Step 3: Check error tolerance
        error_score, error_recs, error_warns = self._check_error_tolerance(spec)
        recommendations.extend(error_recs)
        warnings.extend(error_warns)
        
        # Step 4: Check startup time impact
        startup_score, startup_recs, startup_warns = self._check_startup_impact(spec)
        recommendations.extend(startup_recs)
        warnings.extend(startup_warns)
        
        # Step 5: Check input requirements
        input_score, input_recs, input_warns = self._check_input_requirements(spec)
        recommendations.extend(input_recs)
        warnings.extend(input_warns)
        
        # Step 6: Check feedback mechanisms
        feedback_score, feedback_recs, feedback_warns = self._check_feedback_mechanisms(idea, spec)
        recommendations.extend(feedback_recs)
        warnings.extend(feedback_warns)
        
        # Step 7: Check dependency complexity
        dep_score, dep_recs, dep_warns = self._check_dependency_complexity(spec)
        recommendations.extend(dep_recs)
        warnings.extend(dep_warns)
        
        # Step 8: Check environment fit
        env_score, env_fit, env_recs, env_warns = self._check_environment_fit(idea, spec)
        recommendations.extend(env_recs)
        warnings.extend(env_warns)
        
        # Calculate overall accessibility score
        scores = {
            "offline_capability": offline_score,
            "simple_interface": ui_score,
            "error_tolerance": error_score,
            "quick_startup": startup_score,
            "minimal_typing": input_score,
            "clear_feedback": feedback_score,
            "low_dependency": dep_score,
            "field_environment": env_score,
        }
        
        accessibility_score = self._calculate_weighted_score(scores)
        
        # Add overall recommendations based on score
        if accessibility_score < 5:
            warnings.append(
                f"Low accessibility score ({accessibility_score}/10) - "
                "this tool may be difficult to use in field conditions"
            )
        elif accessibility_score < 7:
            recommendations.append(
                "Consider additional usability improvements for field use"
            )
        
        # Ensure we have at least one recommendation
        if not recommendations:
            recommendations.append("Design appears suitable for field use")
        
        logger.info(
            f"Advisory complete: score={accessibility_score}/10, "
            f"{len(recommendations)} recommendations, {len(warnings)} warnings"
        )
        
        return AdvisoryReport(
            recommendations=recommendations,
            warnings=warnings,
            environment_fit=env_fit,
            accessibility_score=accessibility_score
        )
    
    def _check_offline_capability(
        self, 
        idea: Idea, 
        spec: ProjectSpec
    ) -> Tuple[float, List[str], List[str]]:
        """
        Check if the tool can work offline
        
        Returns:
            Tuple of (score 0-10, recommendations, warnings)
        """
        recommendations = []
        warnings = []
        score = 10.0
        
        combined_text = f"{idea.description} {' '.join(idea.features)}".lower()
        
        # Check for online requirements in idea
        online_keywords = ["api", "cloud", "sync", "online", "internet", "http", "web"]
        requires_online = any(kw in combined_text for kw in online_keywords)
        
        if requires_online:
            score -= 4.0
            warnings.append(
                "Tool appears to require internet connectivity - "
                "may not work in areas with limited WiFi"
            )
            recommendations.append(
                "Add offline mode with local caching for essential features"
            )
        
        # Check tech stack for web dependencies
        web_deps = ["fastapi", "flask", "django", "requests", "httpx", "aiohttp"]
        has_web_deps = any(dep in spec.dependencies for dep in web_deps)
        
        if has_web_deps:
            score -= 2.0
            if not requires_online:
                recommendations.append(
                    "Consider adding offline fallbacks for web-dependent features"
                )
        
        # Bonus for explicit offline mention
        if "offline" in combined_text or "local" in combined_text:
            score = min(10.0, score + 2.0)
        
        # Check environment for connectivity hints
        if idea.environment:
            env_lower = idea.environment.lower()
            if any(kw in env_lower for kw in ["ship", "offshore", "remote", "field"]):
                if requires_online:
                    warnings.append(
                        f"Environment '{idea.environment}' typically has limited connectivity - "
                        "offline mode is critical"
                    )
        
        return max(0.0, score), recommendations, warnings
    
    def _check_interface_simplicity(
        self, 
        idea: Idea, 
        spec: ProjectSpec
    ) -> Tuple[float, List[str], List[str]]:
        """
        Check if the interface is simple enough for field use
        
        Returns:
            Tuple of (score 0-10, recommendations, warnings)
        """
        recommendations = []
        warnings = []
        score = 10.0
        
        # CLI is generally simpler for field use
        has_cli = spec.tech_stack.get("cli_framework") is not None
        has_web = any(
            "fastapi" in dep or "flask" in dep or "django" in dep 
            for dep in spec.dependencies
        )
        
        if has_cli:
            score += 1.0  # Bonus for CLI
            recommendations.append("CLI interface is good for quick field operations")
        
        if has_web and not has_cli:
            score -= 2.0
            warnings.append(
                "Web-only interface may be harder to use in field conditions"
            )
            recommendations.append(
                "Consider adding a CLI companion for quick field tasks"
            )
        
        # Check for complexity indicators
        if len(spec.folder_structure) > 5:
            score -= 1.0
            recommendations.append(
                "Complex project structure - ensure main commands are easily discoverable"
            )
        
        # Check for rich UI library
        if spec.tech_stack.get("ui_library") == "rich":
            recommendations.append(
                "Rich library provides good visual feedback - "
                "ensure colors are accessible and text is large enough"
            )
        
        return max(0.0, min(10.0, score)), recommendations, warnings
    
    def _check_error_tolerance(
        self, 
        spec: ProjectSpec
    ) -> Tuple[float, List[str], List[str]]:
        """
        Check error handling and recovery capabilities
        
        Returns:
            Tuple of (score 0-10, recommendations, warnings)
        """
        recommendations = []
        warnings = []
        score = 7.0  # Start neutral
        
        # Check for data handling (suggests need for error handling)
        has_data_lib = spec.tech_stack.get("data_library") is not None
        
        if has_data_lib:
            recommendations.append(
                "With data processing, ensure graceful handling of malformed input files"
            )
            recommendations.append(
                "Add progress indicators for long-running data operations"
            )
        
        # Check for database
        has_db = any("sqlite" in dep or "database" in dep for dep in spec.dependencies)
        
        if has_db:
            recommendations.append(
                "Implement database backup before operations to prevent data loss"
            )
            score += 1.0  # Local DB is more reliable than remote
        
        # Generic recommendations
        recommendations.append(
            "Add clear error messages that suggest solutions, not just problems"
        )
        
        return score, recommendations, warnings
    
    def _check_startup_impact(
        self, 
        spec: ProjectSpec
    ) -> Tuple[float, List[str], List[str]]:
        """
        Check impact on startup time
        
        Returns:
            Tuple of (score 0-10, recommendations, warnings)
        """
        recommendations = []
        warnings = []
        score = 10.0
        
        # Heavy dependencies slow startup
        heavy_deps = ["pandas", "numpy", "tensorflow", "torch", "scipy"]
        heavy_count = sum(1 for dep in spec.dependencies if dep in heavy_deps)
        
        if heavy_count > 0:
            score -= heavy_count * 1.5
            warnings.append(
                f"Heavy dependencies ({heavy_count}) may slow startup time - "
                "field workers need quick access"
            )
            recommendations.append(
                "Consider lazy loading of heavy libraries or providing a 'lite' mode"
            )
        
        # Many dependencies also affect startup
        if len(spec.dependencies) > 5:
            score -= 1.0
            recommendations.append(
                "Consider reducing dependencies for faster startup"
            )
        
        return max(0.0, score), recommendations, warnings
    
    def _check_input_requirements(
        self, 
        spec: ProjectSpec
    ) -> Tuple[float, List[str], List[str]]:
        """
        Check input/typing requirements
        
        Returns:
            Tuple of (score 0-10, recommendations, warnings)
        """
        recommendations = []
        warnings = []
        score = 8.0  # Start optimistic
        
        # CLI frameworks typically support flags which reduce typing
        has_cli = spec.tech_stack.get("cli_framework") is not None
        
        if has_cli:
            recommendations.append(
                "Use short command aliases (e.g., '-v' for '--verbose') "
                "for faster field input"
            )
            recommendations.append(
                "Support file paths via drag-and-drop or recent file history"
            )
        else:
            score -= 1.0
            warnings.append(
                "Without CLI, ensure input methods are glove-friendly"
            )
        
        # Generic recommendations
        recommendations.append(
            "Provide sensible defaults to minimize required input"
        )
        
        return score, recommendations, warnings
    
    def _check_feedback_mechanisms(
        self, 
        idea: Idea, 
        spec: ProjectSpec
    ) -> Tuple[float, List[str], List[str]]:
        """
        Check visual/audio feedback for field conditions
        
        Returns:
            Tuple of (score 0-10, recommendations, warnings)
        """
        recommendations = []
        warnings = []
        score = 7.0
        
        # Check environment for noisy conditions
        env_noisy = False
        if idea.environment:
            env_lower = idea.environment.lower()
            noisy_keywords = ["noisy", "loud", "engine", "workshop", "factory", "plant"]
            env_noisy = any(kw in env_lower for kw in noisy_keywords)
        
        if env_noisy:
            score -= 1.0
            warnings.append(
                "Noisy environment detected - audio feedback may be ineffective"
            )
            recommendations.append(
                "Use large, high-contrast visual indicators for success/failure"
            )
            recommendations.append(
                "Consider screen flash or color coding for critical alerts"
            )
        
        # Check for rich library
        has_rich = spec.tech_stack.get("ui_library") == "rich"
        if has_rich:
            score += 1.0
            recommendations.append(
                "Use Rich progress bars for long operations - visible at a glance"
            )
        else:
            recommendations.append(
                "Consider adding visual progress indicators"
            )
        
        # General recommendations
        recommendations.append(
            "Use large fonts and clear symbols for status indicators"
        )
        
        return score, recommendations, warnings
    
    def _check_dependency_complexity(
        self, 
        spec: ProjectSpec
    ) -> Tuple[float, List[str], List[str]]:
        """
        Check dependency complexity for deployment
        
        Returns:
            Tuple of (score 0-10, recommendations, warnings)
        """
        recommendations = []
        warnings = []
        score = 10.0
        
        dep_count = len(spec.dependencies)
        
        if dep_count == 0:
            score = 10.0
            recommendations.append("Minimal dependencies - excellent for deployment")
        elif dep_count <= 3:
            score = 9.0
            recommendations.append("Low dependency count - good for reliability")
        elif dep_count <= 5:
            score = 7.0
        elif dep_count <= 8:
            score = 5.0
            warnings.append(
                f"Moderate dependency count ({dep_count}) - "
                "ensure all can be installed offline"
            )
        else:
            score = 3.0
            warnings.append(
                f"High dependency count ({dep_count}) - "
                "may cause installation issues in field environments"
            )
            recommendations.append(
                "Consider bundling dependencies or creating a standalone executable"
            )
        
        # Check for system dependencies
        system_deps = ["pillow", "opencv", "lxml", "psycopg2"]
        has_system_deps = any(dep in spec.dependencies for dep in system_deps)
        
        if has_system_deps:
            score -= 2.0
            warnings.append(
                "Some dependencies require system libraries - "
                "may complicate installation"
            )
            recommendations.append(
                "Provide pre-built wheels or container image for easy deployment"
            )
        
        return max(0.0, score), recommendations, warnings
    
    def _check_environment_fit(
        self, 
        idea: Idea, 
        spec: ProjectSpec
    ) -> Tuple[float, str, List[str], List[str]]:
        """
        Check overall environment fit
        
        Returns:
            Tuple of (score 0-10, environment_fit, recommendations, warnings)
        """
        recommendations = []
        warnings = []
        score = 8.0
        
        env_fit = "good"
        
        if not idea.environment:
            return score, "unknown", recommendations, warnings
        
        env_lower = idea.environment.lower()
        
        # Maritime/offshore environment
        if any(kw in env_lower for kw in ["ship", "offshore", "maritime", "vessel"]):
            env_fit = "maritime"
            recommendations.append(
                "Maritime environment: ensure data persists through power fluctuations"
            )
            recommendations.append(
                "Consider adding USB export for data transfer"
            )
            if any("web" in dep for dep in spec.dependencies):
                warnings.append(
                    "Web dependencies may not work reliably at sea"
                )
                score -= 2.0
        
        # Industrial/workshop environment
        elif any(kw in env_lower for kw in ["workshop", "factory", "plant", "garage"]):
            env_fit = "industrial"
            recommendations.append(
                "Industrial environment: ensure UI is readable with dirty/oily hands"
            )
            recommendations.append(
                "Support voice commands or large touch targets if possible"
            )
        
        # Outdoor/field environment
        elif any(kw in env_lower for kw in ["field", "outdoor", "site", "remote"]):
            env_fit = "field"
            recommendations.append(
                "Field environment: ensure app works with screen glare"
            )
            recommendations.append(
                "Consider high-contrast mode for outdoor visibility"
            )
            if any("web" in dep for dep in spec.dependencies):
                warnings.append(
                    "Remote field locations may have limited connectivity"
                )
                score -= 1.0
        
        # Check target users
        if idea.target_users:
            users_str = ', '.join(idea.target_users)
            recommendations.append(
                f"Designed for {users_str} - validate UI with actual users"
            )
        
        return score, env_fit, recommendations, warnings
    
    def _calculate_weighted_score(self, scores: dict) -> int:
        """
        Calculate weighted accessibility score
        
        Args:
            scores: Dict of criterion -> score
            
        Returns:
            int: Weighted score 0-10
        """
        total_weight = sum(self.CRITERIA_WEIGHTS.values())
        weighted_sum = sum(
            scores[criterion] * self.CRITERIA_WEIGHTS[criterion]
            for criterion in scores
        )
        
        # Normalize to 0-10
        raw_score = weighted_sum / total_weight
        return int(round(raw_score))
