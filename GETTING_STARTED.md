# Getting Started Guide

## 🚀 5-Minute Quick Start

### Step 1: Install Python
If you don't have Python installed:
1. Visit https://www.python.org
2. Download Python 3.9 or higher
3. Run installer with "Add Python to PATH" checked

### Step 2: Run Setup Script

#### **Windows Users:**
```bash
double-click setup.bat
```

#### **macOS/Linux Users:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Get API Key
1. Go to https://console.anthropic.com/api_keys
2. Create an account (free tier available)
3. Generate a new API key
4. Copy the key

### Step 4: Create .env File
In the project folder, create a file named `.env` (without any extension):

```
ANTHROPIC_API_KEY=your-api-key-here
```

Replace `your-api-key-here` with the key from Step 3.

### Step 5: Start Application
Open terminal/command prompt in the project folder and run:

```bash
streamlit run app.py
```

The application will open at http://localhost:8501

---

## 📋 Manual Setup (If Scripts Don't Work)

### Windows:
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
# Then run:
streamlit run app.py
```

### macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
# Then run:
streamlit run app.py
```

---

## ✅ Verify Installation

After setup, verify everything works:

```bash
# Check Python version
python --version

# Check pip packages
pip list | grep streamlit

# Test import
python -c "import anthropic; print('✓ Anthropic SDK installed')"
```

---

## 🔧 API Key Setup in Detail

### Getting Your Free API Key:

1. **Visit Anthropic Console:**
   - Go to https://console.anthropic.com
   - Click "Sign Up" (or log in if you have an account)

2. **Create API Key:**
   - Navigate to the "API Keys" section
   - Click "Create Key"
   - Give it a name (e.g., "Contract Analysis Bot")
   - Copy the generated key immediately

3. **Add to .env File:**
   - Open `.env` file in the project folder
   - Paste: `ANTHROPIC_API_KEY=sk-ant-xxxxxxx...`
   - Save the file

4. **Verify:**
   - Run the app with `streamlit run app.py`
   - Upload a test contract to verify it works

---

## 🔍 Troubleshooting Installation

### "Python not found"
```
Solution:
1. Reinstall Python from https://www.python.org
2. Check "Add Python to PATH" during installation
3. Restart your computer
4. Try again
```

### "pip: command not found"
```
Solution:
1. Try: python -m pip install -r requirements.txt
2. Or: py -m pip install -r requirements.txt (Windows)
```

### "ModuleNotFoundError: No module named 'streamlit'"
```
Solution:
1. Verify virtual environment is activated (should see (venv) in prompt)
2. Run: pip install -r requirements.txt
3. Wait for all packages to install
```

### ".env file not working"
```
Solution:
1. Ensure .env file is in the project root directory
2. Check file has no extension (.env, not .env.txt)
3. Verify exact format: ANTHROPIC_API_KEY=your-key
4. No quotes around the key
5. Save file and restart application
```

### "ANTHROPIC_API_KEY not found"
```
Solution:
1. Check .env file exists and is readable
2. Verify API key is valid at console.anthropic.com
3. No extra spaces around the = sign
4. Restart the application completely
```

---

## 📦 System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: Version 3.9 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Storage**: 500MB for dependencies
- **Internet**: Required for API calls
- **Browser**: Any modern browser (Chrome, Safari, Firefox, Edge)

---

## 🌐 First Run Checklist

- [ ] Python installed (version 3.9+)
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API key obtained from Anthropic
- [ ] .env file created with API key
- [ ] Application starts (`streamlit run app.py`)
- [ ] Browser opens to http://localhost:8501
- [ ] Can upload a test contract

---

## 📱 Using the Application

1. **Upload Tab:**
   - Click "Upload & Analyze" tab
   - Select your contract file
   - Click "Analyze Contract" button
   - Wait for analysis to complete (2-4 minutes)

2. **Review Results:**
   - Check "Risk Dashboard" for overall assessment
   - Review "Clause Analysis" for details
   - Check "Entity Extraction" for key information
   - Download reports from "Reports & Export"

3. **Export & Share:**
   - Download summary as TXT
   - Export full analysis as JSON
   - Share with legal professionals

---

## 💡 Tips for Best Results

1. **Clear PDF Files**: Use searchable PDFs (text-based, not scanned images)
2. **Standard Formats**: Contracts in standard business formats work best
3. **English Contracts**: Currently optimized for English contracts
4. **Reasonable Size**: Keep contracts under 50 pages for faster analysis
5. **Multiple Clauses**: Works best with contracts that have distinct sections

---

## 🔐 Security Notes

- Your API key is sensitive - never share it
- Contracts are only sent to Anthropic API for analysis
- No data is stored on our servers
- Keep .env file secure and never commit to version control
- Use a read-only API key if possible

---

## 📞 Need Help?

1. **Check README.md** for detailed documentation
2. **Review Troubleshooting** section in README
3. **Verify .env setup** is correct
4. **Test with sample contract** first
5. **Check internet connection**

---

## ✨ What to Try Next

After setup works:
1. Test with a simple 2-3 page contract first
2. Try different contract types (employment, lease, vendor)
3. Review the risk dashboard to understand the analysis
4. Explore clause-by-clause review
5. Generate and download sample reports

---

**Congratulations! You're all set to analyze contracts! 🎉**

For detailed feature documentation, see the main README.md file.
