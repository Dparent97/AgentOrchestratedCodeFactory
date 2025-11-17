# Claude Code - AI Development Assistant Guide
**MacBook Pro M4 - Work Profile (dp)**
**Last Updated:** November 17, 2025
**Purpose:** Complete reference for Claude Code capabilities, workflows, and best practices

---

## Table of Contents
1. [What is Claude Code?](#what-is-claude-code)
2. [Available Tools & Capabilities](#available-tools--capabilities)
3. [Best Practices](#best-practices)
4. [Common Workflows](#common-workflows)
5. [Project-Specific Use Cases](#project-specific-use-cases)
6. [Integration with Your Stack](#integration-with-your-stack)
7. [Tips & Tricks](#tips--tricks)
8. [Troubleshooting](#troubleshooting)

---

## What is Claude Code?

**Claude Code** is Anthropic's official CLI tool that brings AI assistance directly into your development workflow. It's like having an expert pair programmer who can:
- Read, write, and edit code across your entire project
- Execute terminal commands and scripts
- Search codebases and documentation
- Debug issues and suggest solutions
- Automate repetitive tasks
- Learn your project structure and coding patterns

**Version:** 2.0.29
**Model:** Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
**Knowledge Cutoff:** January 2025

---

## Available Tools & Capabilities

### Core File Operations

#### **Read** - View Files
```bash
# What it does: Read any file on your system
# When to use: Understanding code, reviewing configs, reading documentation
# Capabilities:
- Reads text files, code, configs
- Supports images (PNG, JPG) - I can see them!
- Reads PDFs (extracts text and visual content)
- Reads Jupyter notebooks (.ipynb) with outputs
- Shows line numbers for easy reference
```

**Examples:**
```bash
claude  # Start in project directory
# I can read:
Read /Users/dp/Developer/projects/my-app/src/main.py
Read /Users/dp/Desktop/screenshot.png  # I'll see the image!
Read /Users/dp/Documents/report.pdf
```

#### **Write** - Create New Files
```bash
# What it does: Create new files from scratch
# When to use: Generating new code, configs, documentation
# Best practice: I prefer EDITING existing files over creating new ones
```

**Examples:**
```bash
# I can create:
- New Python scripts
- Configuration files
- Documentation
- Test files
- HTML/CSS/JS files
```

#### **Edit** - Modify Existing Files
```bash
# What it does: Make precise edits to existing files
# When to use: Fixing bugs, adding features, refactoring
# How it works: I find exact strings and replace them
# Best practice: I ALWAYS read files before editing
```

**Key Features:**
- Preserves indentation perfectly
- Can replace single instances or all occurrences
- Safer than rewriting entire files
- Works with any text file format

#### **Glob** - Find Files by Pattern
```bash
# What it does: Fast pattern-based file searching
# When to use: Finding files by name/extension
# Supports: Standard glob patterns like *.js, **/*.py
```

**Examples:**
```bash
# Find all Python files
Glob **/*.py

# Find config files
Glob **/config.*

# Find all TypeScript components
Glob src/components/**/*.tsx
```

#### **Grep** - Search File Contents
```bash
# What it does: Search through file contents (powered by ripgrep)
# When to use: Finding code, TODO comments, error messages
# Features:
- Full regex support
- Fast across large codebases
- Can filter by file type
- Show context around matches
```

**Examples:**
```bash
# Find all TODO comments in JavaScript files
Grep "TODO" --type js

# Find function definitions
Grep "def login" --type py

# Case-insensitive search
Grep "error" -i

# Show 3 lines of context
Grep "import" -C 3
```

---

### Terminal & Command Execution

#### **Bash** - Execute Commands
```bash
# What it does: Run any terminal command
# When to use: Git operations, running scripts, installing packages, testing
# Features:
- Persistent shell session
- Can run background processes
- Supports chaining commands
- 2-minute default timeout (up to 10 min)
```

**What I Can Do:**
```bash
# Git operations (approved - no permission needed)
git status
git add .
git commit -m "message"
git push
git diff

# Python operations (approved)
python3 script.py
pip install package
poetry install
source venv/bin/activate

# Node operations
npm install
npm run dev
node script.js

# System operations
ls -la
mkdir new-folder
cd /path/to/project

# Testing
pytest tests/
npm test
python -m unittest
```

**Pre-Approved Commands (I can run without asking):**
- `poetry *` - All Poetry commands
- `pip3 install/list` - Python package management
- `python3 -m venv` - Virtual environment creation
- `python analyze_receipts.py` - Your receipt analysis script
- `python extract_images.py` - Your image extraction script
- `mkdir` - Creating directories
- `brew list` - Checking installed packages
- Git commands (standard operations)

---

### Advanced Search & Analysis

#### **Task** - Launch Specialized Agents
```bash
# What it does: Launch specialized sub-agents for complex tasks
# When to use: Multi-step workflows, codebase exploration, research

# Available Agents:
1. Explore Agent - Fast codebase exploration
   - Find files by patterns
   - Search for keywords
   - Answer "how does X work?" questions
   - Thoroughness levels: quick, medium, very thorough

2. General-Purpose Agent - Complex multi-step tasks
   - Research questions
   - Multi-step automation
   - Code searching across many files

3. Plan Agent - Same as Explore, for planning tasks
```

**When to Use Task vs Direct Tools:**
```bash
# Use Task (Explore agent) when:
- "Where are errors handled in the codebase?"
- "How does authentication work?"
- "What's the project structure?"
- "Find all API endpoints"

# Use Direct Tools (Grep/Glob) when:
- You know the exact file/class: "Find class Foo"
- Searching within 2-3 specific files
- Looking for specific pattern like "*.tsx"
```

---

### Development Workflow Tools

#### **WebFetch** - Fetch & Analyze Web Content
```bash
# What it does: Fetch URLs and analyze with AI
# When to use: Reading documentation, API research, checking live sites
# Features:
- Converts HTML to markdown
- Analyzes content with prompt
- 15-minute cache for repeated requests
```

**Examples:**
```bash
WebFetch https://docs.python.org/3/library/asyncio.html
  prompt: "Explain asyncio basics"

WebFetch https://api.github.com
  prompt: "What endpoints are available?"
```

#### **WebSearch** - Search the Web
```bash
# What it does: Search the internet for current information
# When to use: Finding latest docs, troubleshooting errors, research
# Features:
- Domain filtering (include/block sites)
- US-only availability
- Returns formatted results
```

**Examples:**
```bash
WebSearch "Python asyncio best practices 2025"
WebSearch "Claude Agent SDK examples"
  allowed_domains: ["docs.anthropic.com"]
```

---

### Project Management Tools

#### **TodoWrite** - Task Management
```bash
# What it does: Create and track task lists
# When to use: Complex multi-step projects, tracking progress
# Features:
- Task states: pending, in_progress, completed
- Only ONE task in_progress at a time
- Real-time updates as I work
```

**When I Use This:**
- 3+ step tasks
- Complex features
- Multiple related changes
- User provides a list of tasks

**When I Don't Use This:**
- Single simple tasks
- Quick questions
- Just reading/exploring

**Example Task Flow:**
```
1. "Implement dark mode for the app"
   - Create dark mode CSS variables (in_progress)
   - Add theme toggle component (pending)
   - Update existing components (pending)
   - Test across browsers (pending)
```

#### **AskUserQuestion** - Interactive Decisions
```bash
# What it does: Ask you questions during work
# When to use: Unclear requirements, design choices, ambiguous requests
# Features:
- Multiple choice questions
- Multi-select support
- "Other" option always available
```

**When I Ask Questions:**
- Ambiguous requirements
- Design/architecture choices
- Multiple valid approaches
- Need your preference

---

### Git & GitHub Integration

#### **GitHub CLI (gh)** - Via Bash Tool
```bash
# What it does: Full GitHub integration via terminal
# When to use: Creating PRs, issues, repo management

# Common Operations:
gh repo create              # Create new repository
gh pr create                # Create pull request
gh pr list                  # List pull requests
gh issue create             # Create issue
gh issue list               # List issues
gh pr view                  # View PR details
```

#### **Creating Pull Requests** - My Workflow
When you ask me to create a PR, I:
1. Check git status and diff
2. Review all commits since branch diverged
3. Analyze ALL changes (not just latest commit)
4. Create comprehensive PR description
5. Push to remote if needed
6. Open PR with gh CLI

**PR Format I Use:**
```markdown
## Summary
- Bullet point overview

## Test plan
- [ ] Testing checklist
- [ ] Step by step

Generated with Claude Code
```

#### **Creating Git Commits** - My Workflow
When you ask me to commit, I:
1. Run `git status` and `git diff` in parallel
2. Check recent commit messages for style
3. Draft appropriate commit message
4. Stage relevant files
5. Create commit with proper format
6. Run `git status` to verify

**Commit Format I Use:**
```
Brief description of changes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Git Safety Rules I Follow:**
- NEVER update git config
- NEVER force push (unless you explicitly ask)
- NEVER skip hooks (--no-verify)
- Only commit when you ask
- Check authorship before amending
- Never use interactive flags (-i)

---

## Best Practices

### General Guidelines

**DO:**
- Start Claude Code in your project directory (`cd ~/Developer/project && claude`)
- Be specific about what you want
- Let me read files before editing
- Ask me to explain my changes
- Use `/rewind` if I make mistakes
- Press ESC to pause me if needed

**DON'T:**
- Run Claude Code in random directories
- Ask me to do destructive operations without confirming
- Expect me to access external APIs without keys
- Ask me to modify system files without sudo access

### Working with Code

**Best Workflow:**
```bash
# 1. Navigate to project
cd ~/Developer/projects/my-app

# 2. Start Claude Code
claude

# 3. Be specific
"Add a login function to auth.py that uses JWT tokens"
# NOT: "make auth better"

# 4. Let me propose changes before executing
"Show me what you'd change first"

# 5. Review and iterate
"That looks good, but use bcrypt instead of hashlib"
```

### File Operations

**I Prefer:**
- EDITING existing files over creating new ones
- Reading files before making changes
- Making minimal, focused changes
- Preserving your code style and structure

**File Reading:**
```bash
# I automatically read files before editing
# But you can ask me to read files:
"Read auth.py and explain the login flow"
"Show me the contents of config.json"
"What's in the README?"
```

### Multi-Step Tasks

**How I Break Down Work:**
```bash
# You ask: "Build a user authentication system"

# I create todos:
1. Create User model with password hashing (in_progress)
2. Add login/logout routes (pending)
3. Implement JWT token generation (pending)
4. Add authentication middleware (pending)
5. Write tests (pending)
6. Update documentation (pending)

# Then work through them one by one, updating status
```

---

## Common Workflows

### 1. Starting a New Project

```bash
# Navigate to projects folder
cd ~/Developer/projects

# Start Claude Code
claude

# Ask me to set up project
"Create a new Flask API project with Poetry for dependency management.
Include user authentication, SQLAlchemy, and basic project structure."

# I will:
- Create directory structure
- Set up pyproject.toml with Poetry
- Create initial files (app.py, models.py, etc.)
- Initialize git repository
- Create .gitignore
- Write basic README
```

### 2. Debugging Issues

```bash
cd ~/Developer/projects/my-app
claude

"I'm getting a 500 error when submitting the login form.
The error message in the console says 'KeyError: username'.
Can you help debug this?"

# I will:
- Read relevant files (routes, forms, templates)
- Search for the error pattern
- Analyze the code flow
- Identify the issue
- Suggest and implement fix
- Explain what was wrong
```

### 3. Adding New Features

```bash
cd ~/Developer/projects/ship-MTA-draft
claude

"Add a feature to export work items to Excel format,
similar to how we currently export to DOCX"

# I will:
- Read existing DOCX export code
- Install required library (openpyxl)
- Create new Excel export function
- Add route handler
- Update UI with export button
- Test the implementation
- Update documentation
```

### 4. Code Review & Refactoring

```bash
cd ~/Developer/projects/my-app
claude

"Review the authentication code in auth.py and suggest improvements
for security and code quality"

# I will:
- Read and analyze the code
- Check for security issues
- Suggest improvements
- Offer to implement changes
- Explain trade-offs
```

### 5. Learning & Exploration

```bash
cd ~/Developer/learning/claude-agents
claude

"I want to learn how to build an AI agent that can analyze CSV files
and answer questions about the data. Walk me through it step by step."

# I will:
- Explain the concepts
- Create example code with comments
- Build a working demo
- Suggest exercises to practice
- Provide resources for deeper learning
```

### 6. Git Workflows

```bash
cd ~/Developer/projects/my-app
claude

# Creating a feature branch
"Create a new feature branch called 'add-dark-mode' and
implement dark mode support with a toggle button"

# Making commits
"Commit these changes with an appropriate message"

# Creating PRs
"Create a pull request for the dark-mode feature"

# I will handle all git operations
```

### 7. Working with APIs

```bash
cd ~/Developer/projects/api-integration
claude

"Create a Python script that fetches weather data from OpenWeatherMap API
and saves it to a SQLite database. Handle errors gracefully."

# I will:
- Create the script
- Add error handling
- Set up database schema
- Add environment variable for API key
- Create .env.example
- Write usage instructions
```

### 8. Testing & Quality

```bash
cd ~/Developer/projects/my-app
claude

"Write unit tests for the user authentication functions in auth.py
using pytest. Include tests for successful login, failed login,
and edge cases."

# I will:
- Analyze the auth code
- Create test file
- Write comprehensive tests
- Add fixtures if needed
- Run tests to verify
- Suggest additional test cases
```

---

## Project-Specific Use Cases

### Ship MTA Draft Application

**Context:** Flask app for maintenance tracking (Railway deployment)

```bash
cd ~/Developer/projects/ship-MTA-draft
claude

# Common Tasks:
"Add a new status option to the work item dropdown"
"Fix the photo upload issue on mobile Safari"
"Update the admin dashboard to show status statistics"
"Add email notifications when work items are submitted"
"Create a backup script for the PostgreSQL database"
"Optimize image resizing for better performance"

# I understand:
- Flask-SQLAlchemy models
- Jinja2 templates
- Photo upload to Railway volumes
- DOCX generation with python-docx
- PostgreSQL database
- Admin vs crew workflows
```

### Model Behavior (SORA Content)

**Context:** AI content creation project

```bash
cd ~/Developer/model-behavior
claude

# Common Tasks:
"Create a script to batch process videos with ffmpeg"
"Build a prompt generator for SORA using Claude API"
"Organize video assets by theme/category"
"Create thumbnails from video files automatically"
"Generate metadata for video library"
"Build a simple web interface to browse videos"

# I can help with:
- ffmpeg video processing
- OpenAI/Anthropic API integration
- File organization automation
- Metadata extraction
- Web interface (Flask/Node.js)
```

### Claude Agent SDK Projects

**Context:** Learning to build AI agents

```bash
cd ~/Developer/learning/claude-agents
claude

# Common Tasks:
"Create an agent that reads CSV files and answers questions"
"Build a code review agent using the SDK"
"Implement a research agent that searches and summarizes"
"Add file operations to my existing agent"
"Create a conversational agent with memory"

# I understand:
- claude_agent_sdk query() vs ClaudeSDKClient
- Async operations with asyncio
- Tool integration
- Context management
- Best practices from SDK docs
```

### Maritime Documentation

**Context:** Work-related maritime engineering docs

```bash
cd ~/Documents/maritime
claude

# Common Tasks:
"Convert this equipment manual PDF to markdown"
"Create a maintenance schedule spreadsheet"
"Generate a parts list from these documents"
"Organize technical specifications by system"
"Create a searchable index of all manuals"
"Extract tables from PDF documents"

# I can help with:
- PDF processing
- Document conversion
- Data extraction
- Organization systems
- Automation scripts
```

---

## Integration with Your Stack

### Python Ecosystem

**What I Know:**
- Python 3.14 (your current version)
- pyenv for version management
- Poetry for dependencies
- Virtual environments
- Flask web framework
- SQLAlchemy ORM
- pandas, numpy for data
- pytest for testing
- Jupyter notebooks

**Common Commands I Use:**
```bash
# Virtual environments
python3 -m venv venv
source venv/bin/activate

# Poetry
poetry new project-name
poetry add package-name
poetry install
poetry run python script.py

# Testing
pytest tests/
pytest -v tests/test_auth.py
python -m unittest discover

# Running scripts
python3 script.py
python3 -m module.submodule
```

### Node.js Ecosystem

**What I Know:**
- Node.js 25.1.0
- npm, pnpm, yarn
- TypeScript
- Modern JS (ES6+)
- Package.json scripts

**Common Commands I Use:**
```bash
# Package management
npm install
pnpm install
yarn install

# Running scripts
npm run dev
npm run build
npm test

# TypeScript
tsc --init
ts-node script.ts
```

### Databases

**What I Know:**
- PostgreSQL 16.10 (your setup)
- Redis 8.2.2 (your setup)
- SQLite 3.51.0
- SQLAlchemy ORM
- Database migrations
- Query optimization

**Common Tasks:**
```bash
# I can help with:
- Creating database schemas
- Writing complex queries
- Optimizing database performance
- Setting up migrations (Alembic)
- Backup/restore scripts
- Database connection pooling
```

### Git & Version Control

**What I Know:**
- Git fundamentals
- GitHub workflows
- Branch strategies
- git-delta (your pretty diffs)
- lazygit (your visual interface)
- Pull request best practices

**I Can:**
- Create feature branches
- Make commits with proper messages
- Create pull requests
- Manage merges
- Resolve conflicts (with your guidance)
- Set up git hooks
- Configure .gitignore

### Docker & Containers

**What I Know:**
- OrbStack (your Docker alternative)
- Docker Compose
- Container best practices
- Multi-stage builds

**Common Tasks:**
```bash
# I can help with:
- Creating Dockerfiles
- Writing docker-compose.yml
- Container optimization
- Environment configuration
- Volume management
```

---

## Tips & Tricks

### Speed Up Your Workflow

**Use Parallel Operations:**
```bash
# Instead of:
"Read auth.py, then read config.py, then read routes.py"

# Say:
"Read auth.py, config.py, and routes.py"
# I'll read them all at once!
```

**Be Specific About Context:**
```bash
# Less effective:
"Fix the login bug"

# More effective:
"The login function in auth.py is returning 401 even with correct
credentials. The error happens after the password check on line 45."
```

**Let Me Explore First:**
```bash
# For unfamiliar codebases:
"Explore the project structure and explain how authentication works"
# Then ask me to make changes
```

### Keyboard Shortcuts

**In Claude Code:**
- `ESC` - Pause my current operation
- `/rewind` - Undo my recent changes
- `/help` - Get help
- `Ctrl+C` - Cancel (in terminal)

### Project Setup Tips

**Always Start in Project Root:**
```bash
# Good:
cd ~/Developer/projects/my-app
claude

# Not ideal:
cd ~
claude
"Navigate to ~/Developer/projects/my-app"
```

**Initialize New Projects with Context:**
```bash
claude

"Create a new Python project for analyzing CSV sales data.
Use Poetry for dependencies, include pandas and matplotlib,
set up pytest for testing, and create a basic CLI interface."
```

### Code Quality

**Ask for Best Practices:**
```bash
"Implement user authentication following security best practices"
"Refactor this code following Python PEP 8 style guide"
"Add type hints to all functions in this module"
```

**Request Documentation:**
```bash
"Add docstrings to all functions following Google style"
"Create a comprehensive README for this project"
"Add inline comments explaining the complex logic"
```

### Learning & Understanding

**Ask "Why" Questions:**
```bash
"Why did you use asyncio instead of threading here?"
"Explain the trade-offs between these two approaches"
"What are the security implications of this implementation?"
```

**Request Explanations:**
```bash
"Explain this code like I'm new to Python"
"Walk me through how this authentication flow works"
"What does each line in this function do?"
```

---

## Troubleshooting

### Common Issues & Solutions

#### "I can't access that file"
**Possible causes:**
- File permissions issue
- Wrong path (use absolute paths)
- File doesn't exist

**Solutions:**
```bash
# Check if file exists
ls -la /path/to/file

# Check permissions
stat /path/to/file

# Use absolute paths
pwd  # See where you are
```

#### "Command not found"
**Possible causes:**
- Tool not installed
- Not in PATH
- Wrong command name

**Solutions:**
```bash
# Check if installed
which command-name
brew list | grep tool-name

# Install if missing
brew install tool-name
pipx install tool-name
```

#### "Git operation failed"
**Possible causes:**
- Not in a git repository
- Uncommitted changes
- Merge conflicts
- Authentication issues

**Solutions:**
```bash
# Check git status
git status

# Check remote
git remote -v

# Check SSH keys
ssh -T git@github.com
```

#### "Python import errors"
**Possible causes:**
- Package not installed
- Wrong virtual environment
- Python path issues

**Solutions:**
```bash
# Check virtual environment
which python
python --version

# List installed packages
pip list
poetry show

# Install missing package
pip install package-name
poetry add package-name
```

#### "Port already in use"
**Possible causes:**
- Server already running
- Another app using port

**Solutions:**
```bash
# Find what's using port
lsof -i :5000

# Kill process
kill -9 PID
```

### When Things Go Wrong

**If I Make a Mistake:**
```bash
# Rewind recent changes
/rewind

# Or manually:
git status
git checkout -- filename  # Discard changes
git reset HEAD~1  # Undo last commit (keep changes)
```

**If I'm Confused:**
```bash
# Provide more context
"Let me clarify: I want to..."

# Show me examples
"Here's an example of what I'm looking for: ..."

# Break it down
"Let's do this step by step. First, just..."
```

**If I'm Stuck:**
```bash
# Ask me to explain my thinking
"What's your understanding of the problem?"

# Ask me to explore
"Search the codebase for similar implementations"

# Redirect my approach
"Try a different approach using..."
```

---

## Advanced Features

### Working with Images

**I Can See Images:**
```bash
"Read /path/to/screenshot.png and explain what you see"
"Analyze this diagram and create a text description"
"Read this photo and extract any visible text"
```

**Use Cases:**
- Design review
- Error message screenshots
- Diagram analysis
- OCR text extraction

### Working with PDFs

**I Can Read PDFs:**
```bash
"Read technical-manual.pdf and summarize the key points"
"Extract the table on page 15 from report.pdf"
"Convert this PDF to markdown format"
```

### Working with Jupyter Notebooks

**I Understand Notebooks:**
```bash
"Read analysis.ipynb and explain the data transformations"
"Add a new cell that visualizes this data"
"Fix the error in cell 5 of the notebook"
```

### Background Processes

**I Can Run Long Tasks:**
```bash
"Run the test suite in the background and let me know when it finishes"
"Start the development server in background mode"
```

**Monitor with:**
- `BashOutput` tool to check progress
- `KillShell` to stop if needed

### Web Integration

**Fetch Documentation:**
```bash
"Fetch the latest pandas documentation and explain DataFrame.groupby()"
"Search for recent articles about FastAPI best practices"
"Get the API documentation from this URL and create examples"
```

---

## What I Can't Do (Current Limitations)

**No Network Access (Except WebFetch/WebSearch):**
- Can't directly call APIs
- Can't download files (but I can write wget/curl commands)
- Can't authenticate to services

**No Interactive CLI:**
- Can't use interactive tools (like `git add -i`)
- Can't use text editors (vim, nano)
- Can't use interactive prompts

**No System-Level Operations (Without sudo):**
- Can't install system packages
- Can't modify system files
- Can't change permissions

**No Real-Time Monitoring:**
- Can't watch logs continuously
- Can't run interactive debuggers

**Workarounds:**
```bash
# For APIs: I write the code, you run it
"Create a script that calls the OpenAI API"

# For downloads: I write commands
"Write a command to download this file"

# For system ops: I write commands, you run with sudo
"Write the command to install this system package"

# For monitoring: Use background tasks
"Run this in background and check output"
```

---

## Quick Reference Card

### Starting Claude Code
```bash
cd ~/Developer/projects/my-project
claude
```

### Most Common Requests
```bash
# Read and understand
"Read auth.py and explain how it works"
"Explore the project structure"

# Create new code
"Create a Python script that processes CSV files"
"Add a new route to handle user registration"

# Modify existing code
"Fix the bug in the login function"
"Refactor this code to use async/await"
"Add error handling to this function"

# Git operations
"Commit these changes"
"Create a pull request"
"Create a new feature branch"

# Testing
"Write tests for this function"
"Run the test suite"

# Documentation
"Add docstrings to all functions"
"Create a README for this project"

# Learning
"Explain how this works"
"Show me best practices for..."
"Walk me through this step by step"
```

### Emergency Commands
```bash
/rewind              # Undo recent changes
ESC                  # Pause current operation
/help                # Get help
Ctrl+C               # Cancel (in terminal)
```

---

## Integration with Your Existing Tools

### Works Great With:

**Cursor:**
- Use Claude Code for terminal/automation tasks
- Use Cursor for interactive coding with AI
- Complementary, not competing

**VS Code:**
- Claude Code for file operations
- VS Code for visual editing
- Both can work on same project simultaneously

**Warp:**
- Claude Code runs in Warp terminal
- Warp's AI features + Claude Code = powerful combo

**lazygit:**
- I handle commits/PRs
- You use lazygit for visual git operations
- Both work with same repository

**Postman:**
- I create API client code
- You test with Postman
- I can generate Postman collections

---

## Your Specific Setup Integration

### Homebrew
```bash
"What packages are installed?"
"Install tree via Homebrew"
"Update all Homebrew packages"
```

### Python & Poetry
```bash
"Create a new Poetry project for web scraping"
"Add FastAPI and uvicorn dependencies"
"Update all project dependencies"
```

### PostgreSQL & Redis
```bash
"Create SQLAlchemy models for user management"
"Write a Redis caching layer for API responses"
"Create a database migration script"
```

### Docker & OrbStack
```bash
"Create a Dockerfile for this Flask app"
"Write a docker-compose.yml with PostgreSQL and Redis"
"Optimize this Dockerfile for production"
```

### Git & GitHub
```bash
"Create a feature branch for dark mode"
"Write a comprehensive commit message"
"Create a pull request with detailed description"
```

---

## Resources & Learning

### Claude Code Documentation
```bash
# I can fetch latest docs:
"Fetch Claude Code documentation and explain [feature]"
"Search for Claude Code examples for [use case]"
```

### Project-Specific Learning
```bash
# Ship MTA Draft
"Explain the Flask Blueprint structure"
"How does photo upload work in this app?"

# Claude Agent SDK
"Show me examples of using query() vs ClaudeSDKClient"
"Explain context management in the SDK"

# General Python
"Teach me about Python async/await"
"Explain SQLAlchemy relationship patterns"
```

### Keep Learning
```bash
"Create a learning project to practice [technology]"
"Build a simple example demonstrating [concept]"
"Explain the difference between [A] and [B]"
```

---

## Appendix: Tool Decision Tree

**Need to find files by name?**
→ Use Glob: `**/*.py`

**Need to search file contents?**
→ Use Grep: `"search term" --type py`

**Need to understand "how X works"?**
→ Use Task (Explore agent)

**Need to read a specific file?**
→ Use Read: `/path/to/file`

**Need to modify existing file?**
→ Use Edit (I'll read first, then edit)

**Need to create new file?**
→ Use Write (but I prefer editing existing files)

**Need to run commands?**
→ Use Bash: `git status`, `python script.py`

**Need to create tasks/track progress?**
→ Use TodoWrite (for 3+ step tasks)

**Need to ask the user something?**
→ Use AskUserQuestion

**Need web content?**
→ Use WebFetch or WebSearch

---

## Your Custom Workflows

### Morning Startup Routine
```bash
cd ~/Developer/projects/ship-MTA-draft
claude

"Check for any issues in production logs,
review open pull requests,
and summarize what needs attention today"
```

### Code Review Before Push
```bash
cd ~/Developer/projects/my-project
claude

"Review all changes since last commit,
check for security issues,
suggest improvements,
then create a commit if everything looks good"
```

### Learning New Technology
```bash
cd ~/Developer/learning
claude

"I want to learn [technology].
Create a project that teaches me through hands-on examples.
Start with basics and gradually increase complexity."
```

### Maritime Documentation Task
```bash
cd ~/Documents/maritime
claude

"Organize all equipment manuals by system type,
create an index markdown file,
and extract key specifications to a CSV"
```

---

## Conclusion

Claude Code is your AI pair programmer that lives in your terminal. I'm here to:
- **Automate** repetitive tasks
- **Accelerate** development workflows
- **Assist** with debugging and problem-solving
- **Educate** through examples and explanations

**Best way to use me:**
1. Be specific about what you want
2. Let me read and understand first
3. Work iteratively
4. Ask questions when unclear
5. Use `/rewind` when I make mistakes

**Remember:**
- I work best when started in your project directory
- I read files before editing
- I prefer editing over creating new files
- I follow your coding style
- I ask questions when unclear
- I track complex tasks with todos
- I explain my thinking when asked

---

**Questions? Issues? Ideas?**

Just ask me! I'm here to help you build better software, faster.

Start Claude Code: `cd ~/Developer/your-project && claude`

⚓ **Let's build something amazing!** 🚀

---

**Last Updated:** November 17, 2025
**Model:** Claude Sonnet 4.5
**Version:** 2.0.29

**Your Setup:**
- MacBook Pro M4
- Python 3.14, Node.js 25.1.0
- PostgreSQL 16.10, Redis 8.2.2
- Poetry, pnpm, Docker/OrbStack
- Git with delta, lazygit, gh CLI
- See: My-Mac-Users-Guide.md for complete setup
