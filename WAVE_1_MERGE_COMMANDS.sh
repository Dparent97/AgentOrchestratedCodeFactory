#!/bin/bash
# Wave 1 Integration - Merge Commands
# Generated: November 18, 2025
# See WAVE_1_REVIEW.md for full details

echo "═══════════════════════════════════════════════════════════"
echo "  WAVE 1 MERGE SCRIPT"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Step 1: Create Pull Requests
echo "Step 1: Creating Pull Requests..."
echo ""

gh pr create \
  --base main \
  --head claude/implement-foundation-agents-01WWKQq66j8awapgksYX1ykZ \
  --title "Wave 1: Implement PlannerAgent and ArchitectAgent" \
  --body "## Wave 1: Agent Foundation Developer

### Changes
- Implemented PlannerAgent with 7-step intelligent algorithm
- Implemented ArchitectAgent with domain analysis and blue-collar scoring
- Added PlanResult and ArchitectResult models
- Added comprehensive unit and integration tests

### Metrics
- 618 lines of agent logic
- 5 files modified
- All Wave 1 success criteria met

### Quality
⭐⭐⭐⭐⭐ EXCEPTIONAL

See WAVE_1_REVIEW.md for complete details."

gh pr create \
  --base main \
  --head claude/agent-test-harness-01Wx4FwFSDMmsg2y3U9Q6EMU \
  --title "Wave 1: Add comprehensive agent test harness infrastructure" \
  --body "## Wave 1: QA Engineer

### Changes
- Created AgentTestHarness framework (reusable for all agents)
- Added 5 test utility modules (2,273 lines)
- Comprehensive integration tests for Wave 1 pipeline
- Real-world test scenarios (marine engineer, etc.)

### Metrics
- 1,449 lines of test code
- 2,273 lines of test utilities
- 8 files created

### Quality
⭐⭐⭐⭐⭐ EXCEPTIONAL

See WAVE_1_REVIEW.md for complete details."

gh pr create \
  --base main \
  --head claude/docs-framework-wave-1-01NESJD2Ux1WU42CijBFWeYs \
  --title "Wave 1: Add documentation framework and agent documentation" \
  --body "## Wave 1: Technical Writer

### Changes
- 843-line agent integration guide with ASCII diagrams
- Complete API documentation for PlannerAgent and ArchitectAgent
- 736-line test harness documentation
- Documentation template for future agents
- 5 test utility documentation files

### Metrics
- 3,589 lines of documentation
- 12 files created

### Quality
⭐⭐⭐⭐⭐ EXCEPTIONAL

See WAVE_1_REVIEW.md for complete details."

echo ""
echo "Step 2: List PRs to get PR numbers..."
gh pr list --state open

echo ""
echo "Step 3: Review PRs (replace [PR_NUMBER] with actual numbers)"
echo "  gh pr view [PR_NUMBER_FOUNDATION]"
echo "  gh pr view [PR_NUMBER_TEST]"
echo "  gh pr view [PR_NUMBER_DOCS]"

echo ""
echo "Step 4: Merge PRs in order (replace [PR_NUMBER] with actual numbers)"
echo ""
echo "# Merge 1: Foundation agents"
echo "gh pr merge [PR_NUMBER_FOUNDATION] --squash --delete-branch"
echo ""
echo "# Merge 2: Test harness"
echo "gh pr merge [PR_NUMBER_TEST] --squash --delete-branch"
echo ""
echo "# Merge 3: Documentation"
echo "gh pr merge [PR_NUMBER_DOCS] --squash --delete-branch"

echo ""
echo "Step 5: Verification"
echo ""
echo "git checkout main"
echo "git pull origin main"
echo "pytest tests/ -v --cov=src/code_factory --cov-report=term-missing"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "  For complete review, see: WAVE_1_REVIEW.md"
echo "═══════════════════════════════════════════════════════════"
