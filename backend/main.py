"""
Main Analysis Pipeline - Orchestrates contract analysis workflow
"""
import io
from typing import Dict, List
from backend.utils.file_reader import extract_text, clean_text, extract_metadata
from backend.utils.clause_extractor import (
    extract_clauses,
    identify_obligations,
    identify_rights,
    detect_ambiguities
)
from backend.utils.risk_engine import (
    analyze_clause,
    overall_risk,
    get_contract_summary
)
from backend.utils.ner import extract_entities
from backend.utils.contract_classifier import classify_contract_type


def analyze_contract(uploaded_file) -> Dict:
    """
    Complete contract analysis pipeline
    Extracts clauses, analyzes risks, identifies entities, and provides recommendations
    """
    try:
        # Step 1: Extract text from file
        text, file_type = extract_text(uploaded_file)
        
        if not text or len(text.strip()) < 100:
            return {
                "success": False,
                "error": "Contract file appears to be empty or unreadable",
                "overall_risk": "Unknown",
                "clauses": []
            }
        
        # Step 2: Clean and normalize text
        cleaned_text = clean_text(text)
        
        # Step 3: Classify contract type
        contract_info = classify_contract_type(cleaned_text)
        
        # Step 4: Extract named entities
        entities = extract_entities(cleaned_text)
        
        # Step 5: Get contract overview
        contract_summary = get_contract_summary(cleaned_text)
        
        # Step 6: Extract clauses
        clauses = extract_clauses(cleaned_text, max_clauses=15)
        
        # Step 7: Analyze each clause
        analyzed_clauses = []
        for clause in clauses:
            try:
                risk_analysis = analyze_clause(clause.get("full_text", clause.get("text", "")), clause.get("type", "General"))
                
                # Use risk_analysis risk if available, otherwise fallback to clause extraction risk
                final_risk = risk_analysis.get("risk", clause.get("risk_level", "Unknown"))
                
                analyzed_clause = {
                    "type": clause.get("type", "General"),
                    "title": clause.get("title", "Untitled Clause"),
                    "text": clause.get("text", "")[:500],
                    "risk": final_risk,
                    "unfavorable": risk_analysis.get("unfavorable", False),
                    "explanation": risk_analysis.get("explanation", ""),
                    "suggestion": risk_analysis.get("suggestion", ""),
                    "obligations": identify_obligations(clause.get("full_text", "")),
                    "rights": identify_rights(clause.get("full_text", "")),
                    "ambiguities": detect_ambiguities(clause.get("full_text", ""))
                }
                analyzed_clauses.append(analyzed_clause)
            except Exception as e:
                # Continue with next clause if one fails
                continue
        
        # Step 8: Calculate overall risk
        overall_risk_score = overall_risk(analyzed_clauses, cleaned_text)
        
        # Prepare comprehensive report
        report = {
            "success": True,
            "file_info": {
                "name": uploaded_file.name,
                "type": file_type,
                "metadata": extract_metadata(cleaned_text)
            },
            "contract_classification": contract_info,
            "entities": entities,
            "overall_risk": overall_risk_score,
            "contract_summary": contract_summary,
            "clauses": analyzed_clauses,
            "high_risk_clauses": [c for c in analyzed_clauses if c.get("risk") == "High"],
            "unfavorable_clauses": [c for c in analyzed_clauses if c.get("unfavorable")],
            "recommendations": generate_recommendations(analyzed_clauses)
        }
        
        return report
    
    except Exception as e:
        return {
            "success": False,
            "error": f"Error analyzing contract: {str(e)}",
            "overall_risk": "Unknown",
            "clauses": []
        }


def generate_recommendations(clauses: List[Dict]) -> List[str]:
    """
    Generate renegotiation and review recommendations
    """
    recommendations = []
    
    # Check high-risk clauses
    high_risk = [c for c in clauses if c.get("risk") == "High"]
    if high_risk:
        recommendations.append(f"🚨 URGENT: Found {len(high_risk)} high-risk clause(s). Recommend immediate legal review.")
        for clause in high_risk[:3]:
            recommendations.append(f"  - {clause.get('title', 'Clause')}: {clause.get('suggestion', 'Seek legal advice')}")
    
    # Check unfavorable clauses
    unfav = [c for c in clauses if c.get("unfavorable")]
    if unfav:
        recommendations.append(f"\n⚠️ Found {len(unfav)} unfavorable clause(s) that may disadvantage you.")
        for clause in unfav[:3]:
            recommendations.append(f"  - Consider renegotiating '{clause.get('title', 'Clause')}'")
    
    # Check for ambiguities
    ambig_clauses = [c for c in clauses if c.get("ambiguities")]
    if ambig_clauses:
        recommendations.append(f"\n❓ Found vague language in {len(ambig_clauses)} clause(s) - clarification recommended.")
    
    # Check for missing elements
    if len(clauses) < 5:
        recommendations.append("\n📋 Contract appears to have fewer clauses than typical. Ensure all key terms are covered.")
    
    if not recommendations:
        recommendations.append("✅ No major issues detected. Contract appears reasonably balanced.")
    
    return recommendations


def get_summary_report(analysis_result: Dict) -> str:
    """
    Generate a human-readable summary report
    """
    if not analysis_result.get("success"):
        return f"Error: {analysis_result.get('error', 'Unknown error')}"
    
    report = []
    report.append("=" * 60)
    report.append("CONTRACT ANALYSIS REPORT")
    report.append("=" * 60)
    
    # File info
    file_info = analysis_result.get("file_info", {})
    report.append(f"\nFile: {file_info.get('name', 'Unknown')}")
    metadata = file_info.get("metadata", {})
    report.append(f"Size: {metadata.get('word_count', 0)} words, {metadata.get('page_estimate', 1)} estimated pages")
    
    # Contract classification
    contract_class = analysis_result.get("contract_classification", {})
    report.append(f"\nContract Type: {contract_class.get('type', 'Unknown')}")
    report.append(f"Confidence: {contract_class.get('confidence', 0)}%")
    
    # Risk assessment
    report.append(f"\n{'=' * 60}")
    report.append(f"OVERALL RISK LEVEL: {analysis_result.get('overall_risk', 'Unknown')}")
    report.append(f"{'=' * 60}")
    
    # Key entities
    entities = analysis_result.get("entities", {})
    if entities.get("parties"):
        report.append(f"\nParties: {', '.join(entities.get('parties', []))}")
    if entities.get("dates"):
        report.append(f"Key Dates: {', '.join(entities.get('dates', [])[:3])}")
    if entities.get("amounts"):
        report.append(f"Key Amounts: {', '.join(entities.get('amounts', [])[:3])}")
    
    # Clauses summary
    clauses = analysis_result.get("clauses", [])
    report.append(f"\nClauses Analyzed: {len(clauses)}")
    
    high_risk = len([c for c in clauses if c.get("risk") == "High"])
    medium_risk = len([c for c in clauses if c.get("risk") == "Medium"])
    low_risk = len([c for c in clauses if c.get("risk") == "Low"])
    
    report.append(f"  - High Risk: {high_risk}")
    report.append(f"  - Medium Risk: {medium_risk}")
    report.append(f"  - Low Risk: {low_risk}")
    
    # Recommendations
    recommendations = analysis_result.get("recommendations", [])
    if recommendations:
        report.append(f"\nRECOMMENDATIONS:")
        for rec in recommendations[:5]:
            report.append(f"  {rec}")
    
    report.append("\n" + "=" * 60)
    report.append("For detailed analysis of each clause, review the clauses section below.")
    report.append("=" * 60)
    
    return "\n".join(report)


