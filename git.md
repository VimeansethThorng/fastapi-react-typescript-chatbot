# 🔀 Git Commands Reference

## Branch Management

### Basic Branch Operations
```bash
# Check current branch
git branch
git status

# Switch to existing branch
git checkout main
git checkout docker

# Create and switch to new branch
git checkout -b feature/new-feature

# List all branches (local and remote)
git branch -a

# Delete local branch
git branch -d branch-name

# Force delete local branch
git branch -D branch-name
```

### Repository Synchronization
```bash
# Pull latest changes from remote main
git checkout main
git pull origin main

# Pull latest changes from remote docker branch
git checkout docker  
git pull origin docker

# Push current branch to remote
git push origin branch-name

# Push and set upstream for new branch
git push -u origin branch-name
```

## Project-Specific Branches

### Main Branch (Clean Development)
```bash
# Switch to main branch (no Docker files)
git checkout main

# Features available:
# - Full FastAPI backend
# - React TypeScript frontend  
# - Local development setup
# - Python dependencies configuration
# - No Docker configuration
```

### Docker Branch (Containerized Setup)
```bash
# Switch to docker branch (full Docker setup)
git checkout docker

# Additional features:
# - Complete Docker configuration
# - Docker Compose setup
# - Multi-stage Dockerfile
# - Development and production profiles
# - Health checks and monitoring
```

## Branch Differences

| Feature | Main Branch | Docker Branch |
|---------|-------------|---------------|
| Backend | ✅ FastAPI | ✅ FastAPI |
| Frontend | ✅ React TS | ✅ React TS |
| Local Dev | ✅ Native | ✅ Native |
| Docker Support | ❌ None | ✅ Complete |
| Docker Compose | ❌ None | ✅ Yes |
| Health Checks | ❌ None | ✅ Built-in |
| Static Serving | ❌ Basic | ✅ Integrated |

## Working with Branches

### Switching Between Setups
```bash
# For local development
git checkout main
./start.sh

# For Docker development  
git checkout docker
docker-compose --profile dev up -d

# For Docker production
git checkout docker
docker-compose up -d
```

### Merging Changes
```bash
# Merge main into docker (add new features to Docker setup)
git checkout docker
git merge main

# Resolve any conflicts in Docker-specific files
# Common conflicts: Dockerfile, compose.yml, .dockerignore

# Merge docker into main (add Docker support to main)
git checkout main
git merge docker
```

### Creating Feature Branches
```bash
# From main branch (no Docker)
git checkout main
git checkout -b feature/backend-improvement

# From docker branch (with Docker)
git checkout docker
git checkout -b feature/docker-optimization

# Work on feature and merge back
git checkout docker
git merge feature/docker-optimization
```

## Backup and Safety

### Creating Backup Branches
```bash
# Create backup of current state
git checkout main
git checkout -b main-backup-$(date +%Y%m%d-%H%M%S)

# Create backup before major changes
git checkout docker
git checkout -b docker-backup-before-update
```

### Existing Backup Branches
```bash
# Available backup branches:
git checkout main-backup-clean           # Clean main branch backup
git checkout main-backup-20250815-171926 # Timestamped backup
```

## Troubleshooting

### Common Issues
```bash
# Uncommitted changes when switching branches
git stash
git checkout target-branch
git stash pop

# Branch diverged from remote
git fetch origin
git rebase origin/branch-name

# Accidental commit to wrong branch
git log --oneline -5  # Find commit hash
git checkout correct-branch
git cherry-pick commit-hash
git checkout wrong-branch
git reset --hard HEAD~1  # Remove from wrong branch
```

### Reset Operations
```bash
# Discard all local changes
git reset --hard HEAD

# Reset to specific commit
git reset --hard commit-hash

# Reset to remote state
git fetch origin
git reset --hard origin/branch-name
```

## Remote Operations

### Working with GitHub
```bash
# Add remote if not already set
git remote add origin https://github.com/username/repo.git

# Check remote URLs
git remote -v

# Fetch all remote branches
git fetch --all

# Push all branches
git push --all origin

# Create pull request (after pushing branch)
# Use GitHub web interface or GitHub CLI
gh pr create --title "Feature: Description" --body "Details"
```

### Collaboration
```bash
# Update local repository with all remote changes
git fetch --all --prune

# See what others have pushed
git log --oneline --graph --all

# Create branch from remote branch
git checkout -b local-branch origin/remote-branch
```

## Advanced Git Operations

### Interactive Rebase
```bash
# Clean up commit history before merging
git rebase -i HEAD~3

# Squash multiple commits
# In editor: change 'pick' to 'squash' for commits to combine
```

### Cherry Picking
```bash
# Apply specific commit from another branch
git checkout target-branch
git cherry-pick commit-hash

# Cherry pick multiple commits
git cherry-pick commit1 commit2 commit3
```

### Tags and Releases
```bash
# Create tag for release
git tag -a v1.0.0 -m "Version 1.0.0 - Docker support added"

# Push tags to remote
git push origin --tags

# List all tags
git tag -l
```

## Best Practices

### Commit Messages
```bash
# Good commit message format:
git commit -m "feat: add Docker health checks to backend

- Add /health endpoint for container monitoring
- Include database connectivity check
- Update Docker Compose with health check configuration"

# Conventional commit types:
# feat: new feature
# fix: bug fix
# docs: documentation changes
# style: formatting changes
# refactor: code restructuring
# test: adding tests
# chore: maintenance tasks
```

### Branch Naming
```bash
# Good branch names:
feature/docker-optimization
bugfix/cors-headers
hotfix/security-patch
docs/update-readme
chore/dependency-updates
```

### Workflow Tips
```bash
# Always check status before operations
git status

# Use descriptive commit messages
git commit -m "Clear description of what changed"

# Keep branches focused and small
# One feature or fix per branch

# Regular syncing with remote
git fetch origin
git status  # Check if behind remote
```
