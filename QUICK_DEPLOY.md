# ⚡ QUICK DEPLOYMENT - 3 Steps to Live Link

## 🎯 Your Goal
Get your app publicly accessible with a live URL in **15-20 minutes**

---

## ⚙️ STEP 1: Push Code to GitHub (5 minutes)

### 1.1 Create GitHub Account
→ Go to https://github.com/signup (if you don't have one)

### 1.2 Create New Repository
→ Go to https://github.com/new
- **Name**: `GenAI_Contract_Analysis_Bot`
- **Visibility**: Public
- Click "Create repository"

### 1.3 Push Your Code
Run these commands in PowerShell:

```bash
cd c:\Users\saranraj.s\OneDrive\Desktop\GenAI_Contract_Analysis_FULL
git init
git add .
git commit -m "GenAI Contract Analysis Bot - Initial Release"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/GenAI_Contract_Analysis_Bot.git
git push -u origin main
```

**Replace `YOUR_USERNAME` with your GitHub username**

✅ **Done!** Your code is now on GitHub

---

## 🚀 STEP 2: Deploy to Streamlit Cloud (5 minutes)

### 2.1 Sign Up for Streamlit Cloud
→ Go to https://streamlit.io/cloud
- Click "Sign up"
- Use your GitHub account
- Authorize Streamlit to access GitHub

### 2.2 Deploy Your App
1. Click **"New app"** button
2. Select:
   - Repository: `GenAI_Contract_Analysis_Bot`
   - Branch: `main`
   - File: `app.py`
3. Click **"Deploy"**

⏳ Wait 2-3 minutes for deployment...

### 2.3 Add Your API Key
1. After deployment, click **3-dot menu** (top right)
2. Go to **Settings**
3. Click **"Secrets"**
4. Add:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
   ```
   (Get your API key from https://console.anthropic.com)
5. Save

App will restart automatically ✅

---

## 📹 STEP 3: Get Your Live URL & Create Demo (5 minutes)

### 3.1 Copy Your Live URL
After deployment completes, you'll see:
```
https://genai-contract-analysis-bot-[random].streamlit.app
```

**This is your LIVE LINK** - share this URL!

### 3.2 Create Demo Video (Optional but Recommended)
1. Use Windows Screen Recorder or OBS Studio (free)
2. Record yourself:
   - Opening the live link
   - Uploading SAMPLE_CONTRACT.txt
   - Showing risk analysis
   - Demonstrating PDF export
3. Upload to YouTube (unlisted) or Google Drive
4. Get shareable link

---

## ✅ SUBMISSION READY!

You now have:

```
✅ Live URL:
   https://genai-contract-analysis-bot-[your-link].streamlit.app

✅ GitHub Repo:
   https://github.com/YOUR_USERNAME/GenAI_Contract_Analysis_Bot

✅ Project Description:
   See PROJECT_DESCRIPTION.md in your repository

✅ Demo Video (Optional):
   https://youtu.be/[your-video-id]
```

---

## 🔗 Quick Links

| Item | URL |
|------|-----|
| **GitHub** | https://github.com/signup |
| **Streamlit Cloud** | https://streamlit.io/cloud |
| **Anthropic API** | https://console.anthropic.com |
| **Your Code Location** | `c:\Users\saranraj.s\OneDrive\Desktop\GenAI_Contract_Analysis_FULL` |

---

## 📊 Verification Checklist

Before sharing your links:

- [ ] **Live URL** loads in browser
- [ ] **File upload** works
- [ ] **Analysis** completes
- [ ] **GitHub repo** is public
- [ ] **All files** are in GitHub
- [ ] **API key** is in Streamlit secrets
- [ ] **PROJECT_DESCRIPTION.md** is in repo

---

## 🆘 Troubleshooting

### "Repository Not Found" in Streamlit
→ Make sure repository is **PUBLIC**

### API Key Error in App
→ Add `ANTHROPIC_API_KEY` to Streamlit Cloud Secrets

### App Won't Deploy
→ Check requirements.txt and ensure `app.py` exists

### File Upload Fails
→ Use supported formats: PDF, DOCX, TXT

---

## 💡 Pro Tips

1. **Test Locally First**: Run `streamlit run app.py` locally to ensure it works
2. **Use Good File**: Test with SAMPLE_CONTRACT.txt
3. **Auto-Updates**: Once deployed, changes on GitHub auto-update the live link
4. **Keep It Simple**: Your live link is permanent - bookmark it!

---

## 🎁 You're Done!

Your submission now includes:
- ✅ Live deployed application (24/7 accessible)
- ✅ Public GitHub repository (version control)
- ✅ Complete documentation (PROJECT_DESCRIPTION.md)
- ✅ Working demo ready to share

**Total Time Investment**: ~20 minutes
**Cost**: FREE 🎉

**Share your live link and impress the judges!**

---

## Next: Demo Video (Optional Enhancement)

To further impress:
1. Record a 3-5 minute demo showing your app
2. Upload to YouTube or Google Drive
3. Share the video link with your submission

This shows your solution in action! 🎬

---

**Happy Deploying!** 🚀
