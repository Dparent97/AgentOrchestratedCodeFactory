#!/bin/bash
# Test script for phase4-agent-launcher

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER="$SCRIPT_DIR/../phase4-agent-launcher/scripts/launcher.py"
TEST_DIR="$SCRIPT_DIR/test_project"

echo "🧪 Testing Phase 4 Agent Launcher"
echo "=================================="
echo ""

# Create test project directory
echo "📁 Setting up test project..."
rm -rf "$TEST_DIR"
mkdir -p "$TEST_DIR/AGENT_PROMPTS/WAVE_1"

# Copy example state file
cp "$SCRIPT_DIR/example_workflow_state.json" "$TEST_DIR/WORKFLOW_STATE.json"

# Create dummy agent prompt files
cat > "$TEST_DIR/AGENT_PROMPTS/WAVE_1/1_backend_developer.md" << 'EOF'
# Agent 1: Backend Developer

## Role
You are the backend developer for this project.

## Tasks
- Implement REST APIs
- Set up database
- Add authentication

## Tech Stack
- Python, FastAPI, PostgreSQL
EOF

cat > "$TEST_DIR/AGENT_PROMPTS/WAVE_1/2_frontend_developer.md" << 'EOF'
# Agent 2: Frontend Developer

## Role
You are the frontend developer for this project.

## Tasks
- Build UI components
- Integrate with APIs
- Implement routing

## Tech Stack
- React, Tailwind CSS
EOF

cat > "$TEST_DIR/AGENT_PROMPTS/WAVE_1/3_qa_engineer.md" << 'EOF'
# Agent 3: QA Engineer

## Role
You are the QA engineer for this project.

## Tasks
- Write tests
- Set up CI/CD
- Perform code reviews

## Tech Stack
- Pytest, Playwright
EOF

echo "✅ Test project created"
echo ""

# Test 1: Show status
echo "Test 1: Show Status"
echo "-------------------"
python3 "$LAUNCHER" "$TEST_DIR" status
echo ""

# Test 2: Launch agents
echo "Test 2: Launch Agents"
echo "--------------------"
python3 "$LAUNCHER" "$TEST_DIR" launch 60
echo ""

# Test 3: Evaluate progress
echo "Test 3: Evaluate Progress"
echo "-------------------------"
python3 "$LAUNCHER" "$TEST_DIR" evaluate "$SCRIPT_DIR/example_progress_reports.txt" 60
echo ""

# Test 4: Show final status
echo "Test 4: Final Status"
echo "-------------------"
python3 "$LAUNCHER" "$TEST_DIR" status
echo ""

echo "✅ All tests passed!"
echo ""
echo "Test project remains at: $TEST_DIR"
echo "You can clean it up with: rm -rf $TEST_DIR"
