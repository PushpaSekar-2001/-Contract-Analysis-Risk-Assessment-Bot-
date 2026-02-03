# 🚀 Deployment Guide - Creating Live Link

## Step 1: Prepare Your Code for GitHub

### 1.1 Initialize Git Repository (if not already done)
```bash
cd c:\Users\saranraj.s\OneDrive\Desktop\GenAI_Contract_Analysis_FULL
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 1.2 Add and Commit Files
```bash
git add .
git commit -m "Initial commit: GenAI Contract Analysis Bot"
```

---

## Step 2: Create GitHub Repository

### 2.1 Create Account (if needed)
- Go to https://github.com/signup
- Create a free account
- Verify your email

### 2.2 Create New Repository
1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `GenAI_Contract_Analysis_Bot`
   - **Description**: `AI-powered legal assistant for SME contract analysis`
   - **Visibility**: Public
   - **Do NOT** initialize with README (you already have one)

3. Click "Create repository"

### 2.3 Push Code to GitHub
After creating the repository, GitHub will show you commands. Copy and run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/GenAI_Contract_Analysis_Bot.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username.**

---

## Step 3: Prepare for Streamlit Cloud Deployment

### 3.1 Update `requirements.txt`
Make sure all dependencies are listed. Your current file should include:

```
streamlit==1.28.0
python-docx==0.8.11
pdfplumber==0.10.3
spacy==3.7.2
nltk==3.8.1
anthropic==0.7.1
python-dotenv==1.0.0
pandas==2.1.3
numpy==1.24.3
reportlab==4.0.7
requests==2.31.0
textblob==0.17.1
pydantic==2.5.0
unidecode==1.3.0
```

### 3.2 Create `.streamlit/config.toml` (Optional but Recommended)
Create a new file at `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1e3a8a"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#333333"
font = "sans serif"

[client]
showErrorDetails = true

[logger]
level = "info"

[server]
port = 8501
headless = true
runOnSave = true
```

### 3.3 Update `.env.example` (for others to use)
Ensure `.env.example` contains:
```
ANTHROPIC_API_KEY=your_key_here
```

---

## Step 4: Deploy to Streamlit Cloud

### 4.1 Go to Streamlit Cloud
1. Visit https://streamlit.io/cloud
2. Click **"Sign up"** (can use GitHub account)
3. Authorize Streamlit to access your GitHub account

### 4.2 Deploy Your App
1. Click **"New app"** button
2. Fill in deployment details:
   - **Repository**: Select your GitHub repository
   - **Branch**: `main`
   - **Main file path**: `app.py`

3. Click **"Deploy"**

### 4.3 Add Secrets (API Keys)
After deployment initiates:

1. Click the **3-dot menu** (top right) → **Settings**
2. Go to **"Secrets"** section
3. Add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   ```
4. Save and app will restart automatically

---

## Step 5: Get Your Live URL

Your app will be deployed at:
```
https://genai-contract-analysis-bot-[random-string].streamlit.app
```

This URL is:
✅ **Publicly accessible**
✅ **Always live** (24/7)
✅ **Auto-updates** when you push to GitHub
✅ **Free tier** (with some usage limits)

---

## Complete Submission Checklist

### ✅ Live Deployed URL
```
https://genai-contract-analysis-bot-[random-string].streamlit.app
```

### ✅ GitHub Repository Link
```
https://github.com/YOUR_USERNAME/GenAI_Contract_Analysis_Bot
```

### ✅ Project Description
- Already created: `PROJECT_DESCRIPTION.md`
- Explains problem statement, solution, architecture, features

### ✅ Demo Video (YouTube/Google Drive)
**Create a screen recording showing:**
1. Opening the live deployed app
2. Uploading a sample contract (use SAMPLE_CONTRACT.txt)
3. Showing risk analysis results
4. Displaying clause extraction
5. Showing entity recognition
6. Demonstrating PDF export
7. Explaining key features

**How to create video:**
- Use OBS Studio (free) or Windows Screen Recorder
- Record 3-5 minute demo
- Upload to YouTube (unlisted or public) or Google Drive
- Get shareable link

---

## Alternative Deployment Options

### Option 1: Hugging Face Spaces
```
1. Go to https://huggingface.co/spaces
2. Create new space → Streamlit
3. Connect GitHub repository
4. Auto-deploys on push
```

### Option 2: Railway.app
```
1. Go to https://railway.app
2. Deploy from GitHub
3. Free tier with monthly limit
```

### Option 3: Heroku (Paid, but reliable)
```
1. heroku login
2. heroku create your-app-name
3. git push heroku main
```

---

## Troubleshooting Deployment

### Issue: API Key Error
**Solution**: Add ANTHROPIC_API_KEY to Streamlit Cloud secrets

### Issue: Module Not Found
**Solution**: Ensure all imports are in `requirements.txt`

### Issue: Large File Size
**Solution**: Remove venv/ and __pycache__/ before pushing:
```bash
git rm -r --cached venv/
git rm -r --cached **/__pycache__/
git commit -m "Remove large files"
git push
```

### Issue: App Crashes on Streamlit Cloud
**Solution**: Check the logs:
1. Go to app settings
2. View deployment logs
3. Fix errors mentioned in logs

---

## Quick Start Commands Summary

```bash
# 1. Initialize Git
cd c:\Users\saranraj.s\OneDrive\Desktop\GenAI_Contract_Analysis_FULL
git init
git add .
git commit -m "Initial commit"

# 2. Add Remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/GenAI_Contract_Analysis_Bot.git
git branch -M main
git push -u origin main

# 3. Then deploy via Streamlit Cloud dashboard
# (no more commands needed - follow web UI)
```

---

## Final Submission Format

Once deployed, you'll have:

1. **Live URL** (from Streamlit Cloud)
   ```
   https://genai-contract-analysis-bot-[random].streamlit.app
   ```

2. **GitHub Repo** (from GitHub)
   ```
   https://github.com/YOUR_USERNAME/GenAI_Contract_Analysis_Bot
   ```

3. **Demo Video** (YouTube or Google Drive)
   ```
   https://youtu.be/xxxxxxxxxxxxx
   OR
   https://drive.google.com/file/d/xxxxxxxxxxxxx/view
   ```

4. **Project Description**
   ```
   Already in: PROJECT_DESCRIPTION.md
   ```

---

**Next Steps:**
1. Create GitHub account (if needed)
2. Create GitHub repository
3. Push code to GitHub
4. Deploy to Streamlit Cloud
5. Create and upload demo video
6. Submit all links

**Estimated Time**: 15-20 minutes for deployment
**Cost**: FREE ✅

Need help with any specific step?
