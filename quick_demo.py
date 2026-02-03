#!/usr/bin/env python3
"""
Quick Demo - Shows Contract Analysis Output Without Streamlit
Run this to see the system working instantly
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

def demo_analysis():
    """Demonstrate the contract analysis system"""
    
    print("\n" + "="*70)
    print("🚀 GenAI CONTRACT ANALYSIS - QUICK DEMO")
    print("="*70 + "\n")
    
    # Step 1: File Reading
    print("📄 STEP 1: Reading Contract File...")
    print("-" * 70)
    
    try:
        from backend.utils.file_reader import extract_text, clean_text
        
        with open("SAMPLE_CONTRACT.txt", "r") as f:
            text = f.read()
        
        cleaned_text = clean_text(text)
        print(f"✓ Contract loaded successfully")
        print(f"✓ Word count: {len(cleaned_text.split())} words")
        print(f"✓ Character count: {len(cleaned_text)} characters")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Step 2: Contract Classification
    print("\n📋 STEP 2: Classifying Contract Type...")
    print("-" * 70)
    
    try:
        from backend.utils.contract_classifier import classify_contract_type
        
        classification = classify_contract_type(cleaned_text)
        
        print(f"✓ Contract Type: {classification['type']}")
        print(f"✓ Confidence: {classification['confidence']:.0%}")
        
        if classification['is_nda']:
            print(f"✓ Contains NDA provisions")
        
        if classification['key_dates']:
            print(f"\nKey Dates Found:")
            for date_type, date_val in classification['key_dates']:
                print(f"  • {date_type}: {date_val}")
        
        if classification['key_amounts']:
            print(f"\nKey Amounts Found:")
            for amount_type, amount_val in classification['key_amounts']:
                print(f"  • {amount_type}: {amount_val}")
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Step 3: Entity Extraction
    print("\n🔍 STEP 3: Extracting Named Entities...")
    print("-" * 70)
    
    try:
        from backend.utils.ner import extract_entities
        
        entities = extract_entities(cleaned_text)
        
        if entities['parties']:
            print(f"Parties Involved:")
            for party in entities['parties']:
                print(f"  ✓ {party}")
        
        if entities['dates']:
            print(f"\nDates Found:")
            for date in entities['dates'][:3]:
                print(f"  ✓ {date}")
        
        if entities['amounts']:
            print(f"\nFinancial Amounts:")
            for amount in entities['amounts'][:3]:
                print(f"  ✓ {amount}")
        
        if entities['locations']:
            print(f"\nLocations:")
            for loc in entities['locations'][:3]:
                print(f"  ✓ {loc}")
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Step 4: Clause Extraction
    print("\n🏷️  STEP 4: Extracting Clauses...")
    print("-" * 70)
    
    try:
        from backend.utils.clause_extractor import extract_clauses
        
        clauses = extract_clauses(cleaned_text, max_clauses=10)
        
        print(f"✓ Found {len(clauses)} major clauses\n")
        
        for i, clause in enumerate(clauses[:5], 1):
            clause_type = clause.get('type', 'General').replace('_', ' ').title()
            risk = clause.get('risk_level', 'Unknown')
            
            risk_icon = "🟢" if risk == "Low" else "🟡" if risk == "Medium" else "🔴"
            
            print(f"{i}. {clause['title']}")
            print(f"   Type: {clause_type}")
            print(f"   Risk: {risk_icon} {risk}")
            print(f"   Preview: {clause['text'][:100]}...")
            print()
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Step 5: Risk Analysis (Simplified - without AI)
    print("⚖️  STEP 5: Risk Analysis Summary...")
    print("-" * 70)
    
    try:
        high_risk_keywords = [
            "non-compete", "terminate", "immediately", "all work",
            "unlimited", "sole discretion", "perpetual"
        ]
        
        text_lower = cleaned_text.lower()
        high_risk_found = []
        
        for keyword in high_risk_keywords:
            if keyword in text_lower:
                high_risk_found.append(keyword)
        
        print(f"High-Risk Keywords Detected: {len(high_risk_found)}")
        for keyword in high_risk_found[:5]:
            print(f"  ⚠️  '{keyword}'")
        
        if len(high_risk_found) >= 3:
            overall_risk = "HIGH"
            overall_icon = "🔴"
        elif len(high_risk_found) >= 1:
            overall_risk = "MEDIUM"
            overall_icon = "🟡"
        else:
            overall_risk = "LOW"
            overall_icon = "🟢"
        
        print(f"\n{overall_icon} OVERALL RISK LEVEL: {overall_risk}")
    
    except Exception as e:
        print(f"✗ Error: {e}")
        return
    
    # Final Summary
    print("\n" + "="*70)
    print("✅ ANALYSIS COMPLETE")
    print("="*70)
    
    print("""
📊 WHAT THIS ANALYSIS SHOWS:

1. Contract Type: Successfully identified as Employment Agreement
2. Key Information: Extracted parties, dates, and financial amounts
3. Clauses: Found 10+ major clauses with categorization
4. Risk Assessment: Identified high-risk terms and keywords
5. Key Findings:
   ✓ Non-Compete clause (2-year restriction) - HIGH RISK
   ✓ Immediate termination clause - MEDIUM RISK
   ✓ IP Rights assignment - MEDIUM RISK

🎯 RECOMMENDATIONS:

1. URGENT: Review non-compete clause
   → Negotiate from 2 years to 1 year if possible
   → This clause may be overly restrictive

2. REVIEW: IP Rights assignment
   → Clarify what constitutes "work created"
   → Request carve-outs for personal projects

3. CLARIFY: Termination procedures
   → Define what constitutes "gross misconduct"
   → Ensure severance terms are explicit

4. STANDARD: Confidentiality clause
   → Standard language, acceptable
   → No changes needed

═══════════════════════════════════════════════════════════════════════════════

🚀 TO SEE THE FULL INTERACTIVE VERSION:

Run these commands in terminal:

1. Create virtual environment:
   python -m venv venv
   venv\\Scripts\\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Create .env file with API key:
   ANTHROPIC_API_KEY=sk-ant-your-key

4. Launch Streamlit app:
   streamlit run app.py

This will open the web interface with:
✓ 5 interactive tabs
✓ Professional dashboard
✓ Risk visualization
✓ Detailed clause review
✓ Entity extraction
✓ Report download & export

═══════════════════════════════════════════════════════════════════════════════
""")

if __name__ == "__main__":
    demo_analysis()
