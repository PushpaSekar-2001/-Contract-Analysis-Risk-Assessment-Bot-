"""
GenAI Contract Analysis & Risk Assessment Bot
A sophisticated legal assistant for SME contract analysis
"""

import streamlit as st
import json
from datetime import datetime
from backend.main import analyze_contract, get_summary_report
import os
import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


# Page configuration
st.set_page_config(
    page_title="⚖️ GenAI Contract Analysis Bot",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1e3a8a;
        margin-bottom: 30px;
    }
    .risk-high {
        color: #dc2626;
        font-weight: bold;
    }
    .risk-medium {
        color: #f59e0b;
        font-weight: bold;
    }
    .risk-low {
        color: #10b981;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f3f4f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.markdown("## 📋 About This Tool")
st.sidebar.info("""
This is a GenAI-powered legal assistant designed to help SME owners:
- Analyze contracts for legal risks
- Understand complex clauses in simple language
- Identify unfavorable terms
- Get renegotiation suggestions
- Track compliance with Indian laws

Supported formats: PDF, DOCX, TXT
""")

# Check for API key
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    st.sidebar.warning("⚠️ ANTHROPIC_API_KEY not set. Some features may be limited.")

# Main title
st.markdown("<h1 class='main-title'>⚖️ GenAI Contract Analysis & Risk Assessment Bot</h1>", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📤 Upload & Analyze",
    "📊 Risk Dashboard",
    "📋 Clause Review",
    "🔍 Entity Extraction",
    "💾 Reports & Export"
])

# Initialize session state
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None


# ==================== TAB 1: UPLOAD & ANALYZE ====================
with tab1:
    st.header("📤 Upload Your Contract")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload Contract (TXT / DOCX / PDF)",
            type=["txt", "docx", "pdf"],
            help="Select your contract file in PDF, DOCX, or TXT format"
        )
    
    with col2:
        analyze_button = st.button("🚀 Analyze Contract", use_container_width=True, type="primary")
    
    if analyze_button and uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        
        with st.spinner("🔄 Analyzing contract... This may take a moment."):
            try:
                analysis_result = analyze_contract(uploaded_file)
                st.session_state.analysis_result = analysis_result
                
                if analysis_result.get("success"):
                    st.success("✅ Contract analysis complete!")
                    
                    # Display file info
                    st.subheader("📄 File Information")
                    file_info = analysis_result.get("file_info", {})
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("File Name", file_info.get("name", "Unknown")[:30])
                    with col2:
                        metadata = file_info.get("metadata", {})
                        st.metric("Word Count", f"{metadata.get('word_count', 0):,}")
                    with col3:
                        st.metric("Est. Pages", metadata.get("page_estimate", 1))
                
                else:
                    st.error(f"❌ {analysis_result.get('error', 'Analysis failed')}")
            
            except Exception as e:
                st.error(f"❌ Error analyzing contract: {str(e)}")
    
    elif uploaded_file is None and analyze_button:
        st.warning("Please upload a file first")


# ==================== TAB 2: RISK DASHBOARD ====================
with tab2:
    st.header("📊 Risk Assessment Dashboard")
    
    if st.session_state.analysis_result and st.session_state.analysis_result.get("success"):
        result = st.session_state.analysis_result
        
        # Overall Risk Score
        overall_risk = result.get("overall_risk", "Unknown")
        
        st.subheader("Overall Risk Level")
        
        if overall_risk == "High":
            st.markdown(f"<h2 class='risk-high'>🚨 {overall_risk}</h2>", unsafe_allow_html=True)
        elif overall_risk == "Medium":
            st.markdown(f"<h2 class='risk-medium'>⚠️ {overall_risk}</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 class='risk-low'>✅ {overall_risk}</h2>", unsafe_allow_html=True)
        
        # Contract Classification
        st.subheader("Contract Classification")
        contract_info = result.get("contract_classification", {})
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Contract Type", contract_info.get("type", "Unknown"))
        with col2:
            st.metric("Confidence", f"{contract_info.get('confidence', 0):.0%}")
        
        if contract_info.get("is_nda"):
            st.info("🔐 This contract includes NDA/Confidentiality provisions")
        
        # Risk Breakdown
        st.subheader("Risk Breakdown by Clause")
        
        clauses = result.get("clauses", [])
        high_risk = len([c for c in clauses if c.get("risk") == "High"])
        medium_risk = len([c for c in clauses if c.get("risk") == "Medium"])
        low_risk = len([c for c in clauses if c.get("risk") == "Low"])
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Clauses", len(clauses))
        with col2:
            st.metric("🚨 High Risk", high_risk)
        with col3:
            st.metric("⚠️ Medium Risk", medium_risk)
        with col4:
            st.metric("✅ Low Risk", low_risk)
        
        # Risk Distribution Chart
        import pandas as pd
        import plotly.graph_objects as go
        
        high_risk = len([c for c in clauses if c.get("risk") == "High"])
        medium_risk = len([c for c in clauses if c.get("risk") == "Medium"])
        low_risk = len([c for c in clauses if c.get("risk") == "Low"])
        
        # Create interactive bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='High Risk',
            x=['High Risk'],
            y=[high_risk],
            marker_color='#dc2626',
            text=[high_risk],
            textposition='auto',
        ))
        
        fig.add_trace(go.Bar(
            name='Medium Risk',
            x=['Medium Risk'],
            y=[medium_risk],
            marker_color='#f59e0b',
            text=[medium_risk],
            textposition='auto',
        ))
        
        fig.add_trace(go.Bar(
            name='Low Risk',
            x=['Low Risk'],
            y=[low_risk],
            marker_color='#10b981',
            text=[low_risk],
            textposition='auto',
        ))
        
        fig.update_layout(
            title=f"Risk Distribution - {len(clauses)} Total Clauses",
            yaxis_title="Number of Clauses",
            height=400,
            showlegend=True,
            barmode='group',
            template="plotly_white",
            margin=dict(l=50, r=50, t=50, b=50),
            hovermode='x unified'
        )
        
        try:
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error displaying chart: {str(e)}")
        
        # Clause Type Distribution
        st.subheader("Clause Types Found")
        
        clause_types = {}
        for clause in clauses:
            clause_type = clause.get("type", "Other")
            clause_types[clause_type] = clause_types.get(clause_type, 0) + 1
        
        if clause_types:
            # Create pie chart for clause types
            fig2 = go.Figure()
            
            fig2.add_trace(go.Pie(
                labels=list(clause_types.keys()),
                values=list(clause_types.values()),
                hovertemplate="<b>%{label}</b><br>Count: %{value}<extra></extra>",
                marker=dict(
                    colors=["#3b82f6", "#ef4444", "#10b981", "#f59e0b", "#8b5cf6", "#06b6d4", "#ec4899", "#14b8a6"]
                )
            ))
            
            fig2.update_layout(
                title="Clause Type Distribution",
                height=400,
                template="plotly_white",
                margin=dict(l=50, r=50, t=50, b=50)
            )
            
            col1, col2 = st.columns([2, 1])
            with col1:
                try:
                    st.plotly_chart(fig2, use_container_width=True)
                except Exception as e:
                    st.error(f"Error displaying clause chart: {str(e)}")
            with col2:
                st.write("**Clause Types:**")
                for ctype, count in sorted(clause_types.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"• {ctype}: {count}")
        
        # Key Dates and Amounts
        st.subheader("Important Contract Details")
        
        contract_info = result.get("contract_classification", {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Key Dates")
            dates = contract_info.get("key_dates", [])
            if dates:
                for date_type, date_value in dates:
                    st.write(f"**{date_type}**: {date_value}")
            else:
                st.write("No specific dates found")
        
        with col2:
            st.subheader("Key Amounts")
            amounts = contract_info.get("key_amounts", [])
            if amounts:
                for amount_type, amount_value in amounts:
                    st.write(f"**{amount_type}**: {amount_value}")
            else:
                st.write("No financial amounts found")
    
    else:
        st.info("📤 Upload and analyze a contract first to see the risk dashboard")


# ==================== TAB 3: CLAUSE REVIEW ====================
with tab3:
    st.header("📋 Detailed Clause Analysis")
    
    if st.session_state.analysis_result and st.session_state.analysis_result.get("success"):
        result = st.session_state.analysis_result
        clauses = result.get("clauses", [])
        
        if clauses:
            # Filter options
            col1, col2, col3 = st.columns(3)
            
            with col1:
                filter_risk = st.selectbox(
                    "Filter by Risk Level",
                    ["All", "High", "Medium", "Low"]
                )
            
            with col2:
                filter_unfav = st.checkbox("Show Unfavorable Only", value=False)
            
            with col3:
                filter_ambig = st.checkbox("Show Ambiguities Only", value=False)
            
            # Filter clauses
            filtered_clauses = clauses
            
            if filter_risk != "All":
                filtered_clauses = [c for c in filtered_clauses if c.get("risk") == filter_risk]
            
            if filter_unfav:
                filtered_clauses = [c for c in filtered_clauses if c.get("unfavorable")]
            
            if filter_ambig:
                filtered_clauses = [c for c in filtered_clauses if c.get("ambiguities")]
            
            st.write(f"Showing {len(filtered_clauses)} of {len(clauses)} clauses")
            
            # Display clauses
            for i, clause in enumerate(filtered_clauses, 1):
                with st.expander(
                    f"📑 {clause.get('title', f'Clause {i}')} - Risk: {clause.get('risk', 'Unknown')}"
                ):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        risk = clause.get("risk", "Unknown")
                        if risk == "High":
                            st.markdown(f"<span class='risk-high'>Risk: {risk}</span>", unsafe_allow_html=True)
                        elif risk == "Medium":
                            st.markdown(f"<span class='risk-medium'>Risk: {risk}</span>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<span class='risk-low'>Risk: {risk}</span>", unsafe_allow_html=True)
                    
                    with col2:
                        clause_type = clause.get("type", "General").replace("_", " ").title()
                        st.write(f"**Type:** {clause_type}")
                    
                    with col3:
                        if clause.get("unfavorable"):
                            st.markdown("⚠️ **Unfavorable**")
                        else:
                            st.markdown("✅ **Favorable**")
                    
                    # Clause text
                    st.markdown("**Clause Text:**")
                    st.text(clause.get("text", "No text available"))
                    
                    # Explanation
                    st.markdown("**Explanation:**")
                    st.info(clause.get("explanation", "No explanation available"))
                    
                    # Obligations
                    obligations = clause.get("obligations", [])
                    if obligations:
                        st.markdown("**Your Obligations:**")
                        for obl in obligations:
                            st.write(f"• {obl}")
                    
                    # Rights
                    rights = clause.get("rights", [])
                    if rights:
                        st.markdown("**Your Rights:**")
                        for right in rights:
                            st.write(f"• {right}")
                    
                    # Ambiguities
                    ambiguities = clause.get("ambiguities", [])
                    if ambiguities:
                        st.markdown("**⚠️ Ambiguous Language:**")
                        for ambig in ambiguities:
                            st.warning(f"• {ambig}")
                    
                    # Suggestion
                    if clause.get("unfavorable"):
                        st.markdown("**Suggested Action:**")
                        st.success(clause.get("suggestion", "Seek legal advice"))
        
        else:
            st.warning("No clauses extracted from contract")
    
    else:
        st.info("📤 Upload and analyze a contract first")


# ==================== TAB 4: ENTITY EXTRACTION ====================
with tab4:
    st.header("🔍 Extracted Information")
    
    if st.session_state.analysis_result and st.session_state.analysis_result.get("success"):
        result = st.session_state.analysis_result
        entities = result.get("entities", {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Parties Involved")
            parties = entities.get("parties", [])
            if parties:
                for party in parties:
                    st.write(f"• {party}")
            else:
                st.write("No parties identified")
            
            st.subheader("Key Dates")
            dates = entities.get("dates", [])
            if dates:
                for date in dates:
                    st.write(f"• {date}")
            else:
                st.write("No dates found")
            
            st.subheader("Locations & Jurisdiction")
            locations = entities.get("locations", [])
            if locations:
                for loc in locations:
                    st.write(f"• {loc}")
            else:
                st.write("No locations identified")
        
        with col2:
            st.subheader("Financial Amounts")
            amounts = entities.get("amounts", [])
            if amounts:
                for amount in amounts:
                    st.write(f"• {amount}")
            else:
                st.write("No amounts found")
            
            st.subheader("Percentages")
            percentages = entities.get("percentages", [])
            if percentages:
                for perc in percentages:
                    st.write(f"• {perc}")
            else:
                st.write("No percentages found")
            
            st.subheader("Contact Information")
            contact = entities.get("contact_info", {})
            emails = contact.get("emails", [])
            phones = contact.get("phone_numbers", [])
            
            if emails:
                st.write("**Emails:**")
                for email in emails:
                    st.write(f"• {email}")
            
            if phones:
                st.write("**Phone Numbers:**")
                for phone in phones:
                    st.write(f"• {phone}")
    
    else:
        st.info("📤 Upload and analyze a contract first")


# ==================== TAB 5: REPORTS & EXPORT ====================
with tab5:
    st.header("💾 Generate Reports & Export")
    
    if st.session_state.analysis_result and st.session_state.analysis_result.get("success"):
        result = st.session_state.analysis_result
        
        # Summary Report
        st.subheader("Summary Report")
        summary = get_summary_report(result)
        st.text(summary)
        
        # Download summary
        st.download_button(
            label="📥 Download Summary Report (TXT)",
            data=summary,
            file_name=f"contract_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
        
        # Recommendations
        st.subheader("Key Recommendations")
        recommendations = result.get("recommendations", [])
        if recommendations:
            for rec in recommendations:
                st.write(rec)
        
        # Full JSON Export
        st.subheader("Full Analysis (JSON)")
        
        json_export = {
            "analysis_date": datetime.now().isoformat(),
            "file_name": result.get("file_info", {}).get("name", "unknown"),
            "contract_type": result.get("contract_classification", {}).get("type", "Unknown"),
            "overall_risk": result.get("overall_risk", "Unknown"),
            "clause_count": len(result.get("clauses", [])),
            "high_risk_count": len(result.get("high_risk_clauses", [])),
            "unfavorable_count": len(result.get("unfavorable_clauses", [])),
            "recommendations": recommendations,
            "entities": result.get("entities", {})
        }
        
        json_str = json.dumps(json_export, indent=2)
        st.text(json_str)
        
        st.download_button(
            label="📥 Download Full Analysis (JSON)",
            data=json_str,
            file_name=f"contract_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        # Audit Trail
        st.subheader("Audit Trail")
        st.info("All contract analyses are logged for compliance and audit purposes.")
        st.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"File: {result.get('file_info', {}).get('name', 'Unknown')}")
        st.write(f"Status: Analysis Complete ✅")
    
    else:
        st.info("📤 Upload and analyze a contract first to generate reports")


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <p>GenAI Contract Analysis Bot v1.0 | Powered by Claude AI | Built for Indian SMEs</p>
    <p>⚖️ Always consult with a qualified legal professional before making decisions</p>
</div>
""", unsafe_allow_html=True)
