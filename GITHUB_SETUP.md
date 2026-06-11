# GitHub Setup Guide

## Step 1: Create a GitHub Repository

1. Go to [github.com](https://github.com)
2. Click the **+** icon → **New repository**
3. Name: `ecommerce-recommendation`
4. Description: `AI-powered e-commerce recommendation engine with Django`
5. Choose **Public** or **Private**
6. **DO NOT** initialize with README (we already have one)
7. Click **Create repository**

## Step 2: Initialize Git in Your Project

Open terminal in your project folder:

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - E-commerce recommendation engine"

# Add remote (replace with your actual URL)
git remote add origin https://github.com/YOUR_USERNAME/ecommerce-recommendation.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify Upload

Refresh your GitHub repository page. You should see all files uploaded.

## Step 4: Enable GitHub Pages (Optional)

For static site hosting:

1. Go to repository **Settings**
2. Scroll to **Pages** section
3. Source: **Deploy from a branch**
4. Branch: **main** / **root**
5. Click **Save**

Your site will be at: `https://yourusername.github.io/ecommerce-recommendation/`

## Step 5: GitHub Actions (Auto-CI/CD)

The repository includes GitHub Actions workflows:
- **Django CI**: Runs tests on every push
- **Deploy to Pages**: Auto-deploys static files

## Common Git Commands

| Command | Description |
|---------|-------------|
| `git status` | Check changes |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Commit changes |
| `git push` | Push to GitHub |
| `git pull` | Pull latest changes |
| `git log` | View commit history |

## Updating Your Repository

After making changes:

```bash
git add .
git commit -m "Update description"
git push origin main
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `fatal: not a git repository` | Run `git init` first |
| `Permission denied` | Check SSH keys or use HTTPS |
| `failed to push` | Run `git pull` first, then push |
| Large files rejected | Add to `.gitignore` |

## Next Steps

- Add repository topics: `django`, `machine-learning`, `recommendation-system`
- Enable Discussions for Q&A
- Add issue templates
- Set up branch protection rules
