# Integration Prompt Files - README

This package contains **3 integration prompt files** for Phase 5 of the Multi-Agent Workflow.

---

## 📦 What's Included

### 1. INTEGRATION_PROMPT.md
**Use this for:** Complete, thorough integration review
**Time:** ~2 hours
**Detail Level:** Comprehensive

**When to use:**
- First time merging agent work
- Complex projects with many dependencies
- When you want detailed analysis
- Production-critical projects

**Features:**
- Step-by-step checklist
- Quality assessment for each PR
- Conflict analysis
- Detailed verification
- Complete documentation
- Next steps recommendation

---

### 2. QUICK_MERGE_PROMPT.md
**Use this for:** Fast integration and merge
**Time:** ~30-45 minutes
**Detail Level:** Essential only

**When to use:**
- Simple projects
- Low-risk changes
- Quick iterations
- When you're confident in agent work
- Time-sensitive merges

**Features:**
- Streamlined process
- Quick checks only
- Fast merge execution
- Basic verification
- Simple summary

---

### 3. INTEGRATION_TEMPLATE.md
**Use this for:** Customized integration for your project
**Time:** ~2 hours (after customization)
**Detail Level:** Comprehensive + project-specific

**When to use:**
- You want project-specific checks
- You have custom test commands
- You need to track specific metrics
- You want to save and reuse

**Features:**
- Customizable sections (marked with [BRACKETS])
- Project-specific test/build commands
- Custom verification steps
- Metrics tracking
- Reusable for future iterations

---

## 🚀 How to Use

### Quick Start (Most Common)

**Step 1:** Choose your file
- New to workflow? → Use `INTEGRATION_PROMPT.md`
- In a hurry? → Use `QUICK_MERGE_PROMPT.md`
- Want to customize? → Use `INTEGRATION_TEMPLATE.md`

**Step 2:** Copy to your project
```bash
cp INTEGRATION_PROMPT.md ~/Projects/your-project/
```

**Step 3:** Create Claude session
- Go to claude.ai
- Create new chat: "Integration Agent"
- Paste the contents of the file
- Send

**Step 4:** Let it work
Claude will:
1. List all PRs
2. Review each one
3. Determine merge order
4. Merge everything
5. Verify the result
6. Recommend next steps

---

## 📋 Customizing the Template

### To Customize INTEGRATION_TEMPLATE.md:

**Step 1:** Open the file
```bash
code INTEGRATION_TEMPLATE.md
# or
nano INTEGRATION_TEMPLATE.md
```

**Step 2:** Replace all [BRACKETED] sections:
```markdown
[PROJECT NAME] → "Ship MTA Draft"
[YOUR_USERNAME] → "Dparent97"
[YOUR_REPO] → "ship-MTA-draft"
[YOUR TEST COMMAND] → "pytest tests/"
[YOUR BUILD COMMAND] → "python setup.py build"
[LIST KEY FEATURES TO TEST] → "Photo upload, DOCX export, Admin dashboard"
```

**Step 3:** Save and use
Now it's customized for your specific project!

**Step 4:** Reuse for future iterations
Keep this customized version for next time.

---

## 🎯 Decision Guide

### Choose INTEGRATION_PROMPT.md if:
✅ You want comprehensive review
✅ This is a production project
✅ You have time for thorough process
✅ You want to learn best practices
✅ It's your first integration

### Choose QUICK_MERGE_PROMPT.md if:
✅ You're experienced with the workflow
✅ The changes are low-risk
✅ You're in a hurry
✅ The project is simple
✅ You trust the agent work

### Choose INTEGRATION_TEMPLATE.md if:
✅ You want to customize for your project
✅ You have specific test procedures
✅ You need to track metrics
✅ You'll do multiple iterations
✅ You want a reusable process

---

## 💡 Pro Tips

### Tip 1: Start with INTEGRATION_PROMPT.md
For your first integration, use the complete prompt to learn the process.

### Tip 2: Save Integration Reports
After integration completes, save the output:
```bash
# Save to your project
~/Projects/your-project/INTEGRATION_REPORTS/2025-11-17.md
```

### Tip 3: Iterate with Template
After first integration, customize the template for faster future iterations.

### Tip 4: Use Projects Feature
If you use Claude Projects with GitHub integration, Claude can access your repo directly.

### Tip 5: Manual Verification
Always manually test critical functionality after integration, even if tests pass.

---

## 🔧 Troubleshooting

### Problem: "Can't access GitHub"
**Solution:** Make sure you provide the repository URL in the prompt.

### Problem: "Can't run git commands"
**Solution:** 
- If in web session, Claude will provide commands for you to run
- If in terminal, make sure gh CLI is installed

### Problem: "Merge conflicts"
**Solution:** 
- Let the integration agent analyze first
- It will suggest resolution strategy
- May need manual resolution for complex conflicts

### Problem: "Tests failing after merge"
**Solution:**
- Integration agent will catch this
- Investigate which merge caused the failure
- May need to revert and fix before re-merging

---

## 📊 Expected Timeline

### Using INTEGRATION_PROMPT.md:
- Gathering PRs: 5 minutes
- Reviewing each: 30-45 minutes
- Planning merge: 10 minutes
- Executing merges: 30-60 minutes
- Verification: 15 minutes
- Documentation: 10 minutes
**Total: ~2 hours**

### Using QUICK_MERGE_PROMPT.md:
- List PRs: 2 minutes
- Quick review: 15 minutes
- Merge order: 5 minutes
- Execute merges: 20-30 minutes
- Final check: 5 minutes
**Total: ~45 minutes**

### Using INTEGRATION_TEMPLATE.md:
Similar to INTEGRATION_PROMPT.md but with project-specific additions.
**Total: ~2 hours + customization time**

---

## ✅ Success Checklist

After integration completes, you should have:
- [ ] All 5 PRs merged to base branch
- [ ] Full test suite passing
- [ ] App builds without errors
- [ ] Manual testing confirms improvements work
- [ ] No regressions introduced
- [ ] Documentation updated
- [ ] Clear recommendation for next steps
- [ ] Integration report saved

---

## 🎯 Next Steps After Integration

### Option A: Production Deploy
If everything looks good:
```bash
git checkout main
git merge dev
git push origin main
# Deploy to production
```

### Option B: Start Iteration 2
If more improvements needed:
- Use the Multi-Agent Workflow Kickstart prompt
- Get 5 new improvements
- Run another iteration

### Option C: Add Features
If quality is good, add new functionality:
- Start new agent workflow for features
- Or build features traditionally

### Option D: User Testing
Deploy to staging/TestFlight:
- Get real user feedback
- Identify issues
- Plan next iteration based on feedback

---

## 📞 Questions?

### "Which prompt should I use?"
Start with `INTEGRATION_PROMPT.md` for your first time. Switch to `QUICK_MERGE_PROMPT.md` once comfortable.

### "Can I modify these prompts?"
Yes! They're templates. Customize as needed for your workflow.

### "Do I need all three files?"
No, just use one. They're different versions of the same thing.

### "Can I use this for non-multi-agent projects?"
Yes! The integration prompt works for any project with multiple PRs to merge.

---

## 📁 File Locations

After download, save these to your project:
```
your-project/
├── AGENT_PROMPTS/
│   └── INTEGRATION_PROMPT.md          ← Primary version
├── docs/
│   ├── INTEGRATION_TEMPLATE.md        ← Customized version
│   └── QUICK_MERGE_PROMPT.md          ← Quick version
└── INTEGRATION_REPORTS/               ← Save completed reports here
    └── 2025-11-17_iteration_1.md
```

---

## 🎉 You're Ready!

Choose your prompt file, copy it into a Claude session, and let the integration agent handle the merge!

**Most common path:**
1. Download `INTEGRATION_PROMPT.md`
2. Go to claude.ai
3. Create new chat: "Integration Agent"
4. Paste the prompt
5. Watch it merge everything! 🚀

---

**Version:** 1.0
**Last Updated:** November 17, 2025
**Part of:** Multi-Agent Development Workflow System
