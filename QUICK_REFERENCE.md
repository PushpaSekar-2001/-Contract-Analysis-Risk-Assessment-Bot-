# ⚖️ Quick Reference Card

## 🚀 Installation (Choose One)

### **Option 1: Automated (Recommended)**
```bash
# Windows
double-click setup.bat

# macOS/Linux
chmod +x setup.sh && ./setup.sh
```

### **Option 2: Manual**
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
```

## 🔑 Configuration

**Step 1:** Get API Key
- Visit: https://console.anthropic.com/api_keys
- Create new key

**Step 2:** Create .env file
```
ANTHROPIC_API_KEY=sk-ant-xxxxx
```

**Step 3:** Verify Setup
```bash
python validate.py
```

## ▶️ Running

```bash
streamlit run app.py
```

Then open: http://localhost:8501

## 📋 Using the App

| Tab | Purpose |
|-----|---------|
| 📤 Upload & Analyze | Upload contract, start analysis |
| 📊 Risk Dashboard | View overall risk & stats |
| 📋 Clause Review | Analyze individual clauses |
| 🔍 Entity Extraction | View extracted information |
| 💾 Reports & Export | Download analysis & reports |

## ⚡ Quick Analysis Flow

1. **Upload** → Select contract file
2. **Analyze** → Click "Analyze Contract"
3. **Review** → Check Risk Dashboard
4. **Explore** → Read clause details
5. **Export** → Download report

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| "Python not found" | Install Python 3.9+ from python.org |
| "ANTHROPIC_API_KEY not set" | Create .env with your API key |
| "Module not found" | Run: `pip install -r requirements.txt` |
| "Connection timeout" | Check internet connection |
| "Slow analysis" | Large contracts take 2-4 minutes |

## 📊 Risk Levels

- 🟢 **Green (Low)** - Standard clause, minimal risk
- 🟡 **Yellow (Medium)** - Review carefully, consider clarification
- 🔴 **Red (High)** - Significant risk, recommend renegotiation

## 💾 Export Options

- **TXT** - Summary report for sharing
- **JSON** - Full data for record-keeping
- **Screen** - Take screenshots for documentation

## 📞 Help Resources

| Question | Answer |
|----------|--------|
| How to install? | See GETTING_STARTED.md |
| Full features? | See README.md |
| Troubleshooting? | See GETTING_STARTED.md |
| System requirements? | Python 3.9+, 2GB RAM, internet |
| File formats? | PDF, DOCX, TXT |
| Max file size? | 50MB |

## ⚠️ Important Notes

- Always consult a lawyer for final decisions
- API key is sensitive - never share it
- Keep contracts confidential
- Use for initial assessment only
- Review recommendations carefully

## 🎯 Typical Use Cases

- ✓ Employment contract review
- ✓ Vendor agreement analysis
- ✓ Lease agreement evaluation
- ✓ Partnership deed review
- ✓ Service contract analysis
- ✓ NDA assessment

## 📈 What You Get

- Risk scores (High/Medium/Low)
- Clause explanations in plain language
- Identified obligations and rights
- Ambiguous term flagging
- Renegotiation suggestions
- Exportable reports

## 🔐 Security

- Your contracts stay local
- Only text sent to Claude API
- No data stored on servers
- .env keeps credentials secure
- All analysis logged locally

## ✅ Validation

Before first use:
```bash
python validate.py
```

Should show: ✓ All checks passed!

## 📱 Browser Support

Works on:
- ✓ Chrome/Edge
- ✓ Firefox
- ✓ Safari
- ✓ Any modern browser

## 💡 Tips

1. Start with small contracts (5-10 pages)
2. Use searchable PDFs, not scanned images
3. Download reports for your records
4. Share reports with legal advisor
5. Keep audit trail for compliance

## 🎓 Learning Resources

- **README.md** - Full documentation
- **GETTING_STARTED.md** - Step-by-step guide
- **IMPLEMENTATION_SUMMARY.md** - Technical details
- **Online Help** - In-app tooltips and info boxes

## 🆘 Emergency Help

**Setup issues?**
→ Run: `python validate.py`

**Can't upload?**
→ Check file is PDF/DOCX/TXT

**Slow analysis?**
→ Contracts take 2-4 minutes

**API errors?**
→ Verify .env has valid key

**Still stuck?**
→ Review GETTING_STARTED.md

---

## Quick Commands

```bash
# Setup
setup.bat              # Windows
./setup.sh            # macOS/Linux

# Validate
python validate.py

# Run
streamlit run app.py

# View docs
README.md
GETTING_STARTED.md
IMPLEMENTATION_SUMMARY.md
```

---

**Ready to analyze contracts? Let's go! 🚀**

*For detailed help, see the full documentation in README.md*
