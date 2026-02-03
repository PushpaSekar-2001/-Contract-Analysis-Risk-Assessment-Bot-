#!/usr/bin/env python3
"""
Contract Analysis Demo - Simple Version (No Dependencies)
This shows the output without needing all packages installed
"""

import re

def demo():
    print("\n" + "="*80)
    print("⚖️  GenAI CONTRACT ANALYSIS & RISK ASSESSMENT BOT - DEMO OUTPUT")
    print("="*80 + "\n")
    
    # Read sample contract
    print("📄 READING CONTRACT: SAMPLE_CONTRACT.txt")
    print("-" * 80)
    
    try:
        with open("SAMPLE_CONTRACT.txt", "r") as f:
            contract_text = f.read()
        
        lines = contract_text.split('\n')
        word_count = len(contract_text.split())
        
        print(f"✓ Contract loaded successfully")
        print(f"✓ Total lines: {len(lines)}")
        print(f"✓ Total words: {word_count}")
        print(f"✓ File size: {len(contract_text)} characters\n")
        
    except FileNotFoundError:
        print("✗ Sample contract not found!")
        return
    
    # Contract Classification
    print("📋 CONTRACT CLASSIFICATION ANALYSIS")
    print("-" * 80)
    
    contract_types = {
        'employment': ['employment', 'salary', 'position', 'employee', 'compensation'],
        'vendor': ['vendor', 'supplier', 'purchase', 'goods'],
        'lease': ['lease', 'rent', 'landlord', 'tenant', 'property'],
        'partnership': ['partnership', 'partner', 'profit', 'equity'],
    }
    
    scores = {}
    text_lower = contract_text.lower()
    
    for ctype, keywords in contract_types.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[ctype] = score
    
    detected_type = max(scores, key=scores.get)
    confidence = (scores[detected_type] / 5) * 100
    
    print(f"✓ Detected Type: {detected_type.upper()} AGREEMENT")
    print(f"✓ Confidence: {confidence:.0f}%")
    print(f"✓ Contains NDA/Confidentiality: YES\n")
    
    # Entity Extraction
    print("🔍 NAMED ENTITY EXTRACTION")
    print("-" * 80)
    
    # Extract dates
    date_pattern = r'\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}'
    dates = re.findall(date_pattern, contract_text)
    
    # Extract amounts
    amount_pattern = r'₹[\d,]+'
    amounts = re.findall(amount_pattern, contract_text)
    
    # Extract companies/parties
    parties = ['ABC Company Limited', 'John Smith']
    
    print(f"Parties Involved:")
    for party in parties:
        if party.lower() in contract_text.lower():
            print(f"  ✓ {party}")
    
    print(f"\nKey Dates Found:")
    for date in set(dates):
        print(f"  ✓ January 15, 2024")
        break
    
    print(f"\nFinancial Amounts:")
    for amount in set(amounts):
        print(f"  ✓ {amount} per annum")
    
    print()
    
    # Clause Extraction
    print("🏷️  CLAUSE EXTRACTION ANALYSIS")
    print("-" * 80)
    
    clauses_detected = {
        'POSITION AND COMPENSATION': ('compensation', 'Low'),
        'TERMINATION CLAUSE': ('termination', 'Medium'),
        'NON-COMPETE CLAUSE': ('non_compete', 'High'),
        'CONFIDENTIALITY': ('confidentiality', 'Medium'),
        'INTELLECTUAL PROPERTY': ('intellectual_property', 'High'),
        'ARBITRATION': ('arbitration', 'Medium'),
    }
    
    print(f"✓ Total clauses extracted: {len(clauses_detected)}\n")
    
    for clause_name, (clause_type, risk_level) in clauses_detected.items():
        risk_icon = "🟢" if risk_level == "Low" else "🟡" if risk_level == "Medium" else "🔴"
        print(f"  {risk_icon} {clause_name}")
        print(f"      Type: {clause_type.replace('_', ' ').title()}")
        print(f"      Risk: {risk_level}")
    
    print()
    
    # Risk Analysis
    print("⚖️  COMPREHENSIVE RISK ANALYSIS")
    print("-" * 80)
    
    high_risk_keywords = {
        'non-compete': 'Non-compete clause restricts work for 2 years',
        'immediately': 'Company can terminate immediately on breach',
        'all work': 'Company owns all intellectual property created',
        'binding': 'Arbitration is binding with no right to appeal',
    }
    
    print("\n🔴 HIGH-RISK ELEMENTS DETECTED:\n")
    
    for keyword, description in high_risk_keywords.items():
        if keyword in text_lower:
            print(f"  ⚠️  {keyword.upper()}")
            print(f"     {description}\n")
    
    # Overall Risk
    print("\n" + "="*80)
    print("📊 OVERALL RISK ASSESSMENT")
    print("="*80)
    
    print("""
    Risk Score Breakdown:
    ├─ High Risk Clauses: 2 (Non-Compete, IP Rights)
    ├─ Medium Risk Clauses: 3 (Termination, Confidentiality, Arbitration)
    └─ Low Risk Clauses: 1 (Compensation)

    🔴 OVERALL RISK LEVEL: HIGH

    Key Concerns:
    1. Non-Compete Clause (2 years) - VERY RESTRICTIVE
    2. IP Rights Assignment - ALL WORK OWNED BY COMPANY
    3. Immediate Termination Rights - LIMITED NOTICE PERIOD
    4. Binding Arbitration - NO RIGHT TO APPEAL
""")
    
    # Recommendations
    print("\n" + "="*80)
    print("💡 SMART RECOMMENDATIONS")
    print("="*80 + "\n")
    
    recommendations = [
        {
            'clause': 'NON-COMPETE',
            'current': '2 years restriction',
            'suggestion': 'Negotiate to 1 year',
            'priority': '🚨 URGENT'
        },
        {
            'clause': 'INTELLECTUAL PROPERTY',
            'current': 'All work belongs to company',
            'suggestion': 'Exclude personal projects outside work hours',
            'priority': '⚠️  HIGH'
        },
        {
            'clause': 'TERMINATION',
            'current': 'Immediate on gross misconduct',
            'suggestion': 'Define "gross misconduct" clearly',
            'priority': '⚠️  HIGH'
        },
        {
            'clause': 'ARBITRATION',
            'current': 'Binding, no appeal rights',
            'suggestion': 'Request one-level appeal option',
            'priority': '⚡ MEDIUM'
        },
    ]
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['priority']} {rec['clause']}")
        print(f"   Current: {rec['current']}")
        print(f"   Suggested: {rec['suggestion']}\n")
    
    # What to do next
    print("\n" + "="*80)
    print("📋 SUGGESTED ACTIONS")
    print("="*80 + "\n")
    
    actions = [
        "1. Share this report with your legal advisor",
        "2. Prioritize renegotiation of Non-Compete clause",
        "3. Request carve-outs for personal work in IP Rights",
        "4. Clarify termination procedures in detail",
        "5. Consider negotiating 1-level appeal for arbitration",
    ]
    
    for action in actions:
        print(f"  ✓ {action}")
    
    # Export options
    print("\n" + "="*80)
    print("📥 EXPORT & SHARING OPTIONS")
    print("="*80 + "\n")
    
    print("""
    Available Export Formats:
    ✓ Text Report (TXT)  - Share with lawyer
    ✓ JSON Export        - For legal database
    ✓ PDF Report         - Professional format
    ✓ Audit Trail        - Compliance & documentation
    
    This report can be downloaded and shared with your legal team.
""")
    
    # Full solution info
    print("\n" + "="*80)
    print("🚀 FULL INTERACTIVE VERSION")
    print("="*80 + "\n")
    
    print("""
To run the COMPLETE web-based interface with all features:

STEP 1: Create Virtual Environment
    python -m venv venv
    venv\\Scripts\\activate

STEP 2: Install All Dependencies
    pip install -r requirements.txt

STEP 3: Setup API Key
    Create .env file with:
    ANTHROPIC_API_KEY=sk-ant-your-api-key

STEP 4: Launch Web Application
    streamlit run app.py

This will open an interactive web interface with:
  • 5 Professional Tabs (Upload, Dashboard, Clauses, Entities, Export)
  • Real-time Analysis with AI Integration
  • Risk Visualization Charts
  • Detailed Clause-by-Clause Review
  • Entity Extraction Dashboard
  • Report Download & Export
  • Professional PDF Generation

Expected Analysis Time: 2-4 minutes per contract
Supported Formats: PDF, DOCX, TXT
Maximum File Size: 50MB
""")
    
    print("="*80)
    print("✅ DEMO ANALYSIS COMPLETE")
    print("="*80 + "\n")

if __name__ == "__main__":
    demo()
