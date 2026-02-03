"""
Risk Engine Module - Analyzes contracts and clauses for legal risks
Integrates with Anthropic Claude for advanced legal reasoning
"""
import os
from typing import Dict, List
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class RiskAnalyzer:
    """
    Advanced risk analyzer using Claude AI for legal reasoning
    """
    
    def __init__(self):
        self.client = Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.conversation_history = []
    
    def analyze_clause(self, clause_text: str, clause_type: str) -> Dict:
        """
        Analyze a single clause for risks using Claude
        """
        try:
            # Build the prompt
            analysis_prompt = f"""You are an expert legal advisor specializing in contract analysis for Indian SMEs.

Analyze the following {clause_type} clause from a contract and provide:
1. Risk Level (Low/Medium/High) with reasoning
2. Whether it's unfavorable to the company (Yes/No)
3. Plain English explanation (max 2 sentences)
4. Specific concerns if any
5. Suggested improvement or alternative wording

CLAUSE:
{clause_text}

Provide your analysis in a structured format."""

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": analysis_prompt}
                ]
            )
            
            analysis_text = response.content[0].text
            
            return {
                "risk": self._extract_risk_level(analysis_text),
                "unfavorable": self._is_unfavorable(analysis_text),
                "explanation": self._extract_explanation(analysis_text),
                "suggestion": self._extract_suggestion(analysis_text),
                "concerns": self._extract_concerns(analysis_text),
                "full_analysis": analysis_text
            }
        
        except Exception as e:
            # Fallback to rule-based analysis
            return self._fallback_analysis(clause_text, clause_type)
    
    def analyze_contract_overview(self, contract_text: str) -> Dict:
        """
        Provide high-level contract analysis
        """
        try:
            prompt = f"""As a legal expert for Indian SMEs, analyze this contract and provide:
1. Contract Type (Employment/Vendor/Lease/Partnership/Service/Other)
2. Key Risks (list top 3)
3. Overall Risk Score (Low/Medium/High)
4. Top 5 Clauses to Review Carefully
5. Compliance Status with Indian Laws (if identifiable)

CONTRACT EXCERPT (first 2000 chars):
{contract_text[:2000]}

Keep your response concise and actionable."""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            analysis = response.content[0].text
            
            return {
                "contract_type": self._extract_contract_type(analysis),
                "key_risks": self._extract_key_risks(analysis),
                "overall_risk": self._extract_overall_risk(analysis),
                "priority_clauses": self._extract_priority_clauses(analysis),
                "compliance_notes": self._extract_compliance(analysis),
                "full_analysis": analysis
            }
        
        except Exception as e:
            return self._fallback_contract_analysis(contract_text)
    
    def get_renegotiation_suggestions(self, clauses: List[Dict]) -> List[str]:
        """
        Get suggestions for renegotiation
        """
        high_risk_clauses = [c for c in clauses if c.get("risk") == "High"]
        
        if not high_risk_clauses:
            return ["All clauses are acceptable. No renegotiation needed."]
        
        suggestions = []
        for clause in high_risk_clauses[:3]:
            suggestions.append(f"Review '{clause.get('title', 'Clause')}' - {clause.get('suggestion', 'Consider getting legal review')}")
        
        return suggestions
    
    # Helper methods for text extraction
    @staticmethod
    def _extract_risk_level(text: str) -> str:
        """Extract risk level from Claude response"""
        text_lower = text.lower()
        if "high" in text_lower.split('\n')[0:2]:
            return "High"
        elif "medium" in text_lower.split('\n')[0:2]:
            return "Medium"
        return "Low"
    
    @staticmethod
    def _is_unfavorable(text: str) -> bool:
        """Determine if clause is unfavorable"""
        unfav_indicators = ["unfavorable", "unfavorably", "disadvantageous", "risky", "high risk"]
        return any(ind in text.lower() for ind in unfav_indicators)
    
    @staticmethod
    def _extract_explanation(text: str) -> str:
        """Extract plain English explanation"""
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if "explanation" in line.lower() or "summary" in line.lower():
                return lines[i+1] if i+1 < len(lines) else lines[0]
        return lines[0][:200]
    
    @staticmethod
    def _extract_suggestion(text: str) -> str:
        """Extract suggested improvement"""
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if "suggest" in line.lower() or "improvement" in line.lower() or "alternative" in line.lower():
                return lines[i+1] if i+1 < len(lines) else "Consult with legal advisor"
        return "Consult with legal advisor for improvements"
    
    @staticmethod
    def _extract_concerns(text: str) -> List[str]:
        """Extract specific concerns"""
        lines = text.split('\n')
        concerns = []
        for line in lines:
            if "concern" in line.lower() or "issue" in line.lower():
                concerns.append(line.strip())
        return concerns[:3]
    
    @staticmethod
    def _extract_contract_type(text: str) -> str:
        """Extract contract type from analysis"""
        types = ["Employment", "Vendor", "Lease", "Partnership", "Service"]
        for ctype in types:
            if ctype.lower() in text.lower():
                return ctype
        return "General"
    
    @staticmethod
    def _extract_key_risks(text: str) -> List[str]:
        """Extract key risks"""
        risks = []
        for line in text.split('\n'):
            if any(indicator in line.lower() for indicator in ["risk", "concern", "issue"]):
                cleaned = line.strip().lstrip('•-').strip()
                if cleaned and len(cleaned) > 10:
                    risks.append(cleaned)
        return risks[:5]
    
    @staticmethod
    def _extract_overall_risk(text: str) -> str:
        """Extract overall risk score"""
        text_lower = text.lower()
        if "high" in text_lower:
            return "High"
        elif "medium" in text_lower:
            return "Medium"
        return "Low"
    
    @staticmethod
    def _extract_priority_clauses(text: str) -> List[str]:
        """Extract clauses to review"""
        clauses = []
        for line in text.split('\n'):
            if "clause" in line.lower():
                cleaned = line.strip().lstrip('•-').strip()
                if cleaned and len(cleaned) > 5:
                    clauses.append(cleaned)
        return clauses[:5]
    
    @staticmethod
    def _extract_compliance(text: str) -> str:
        """Extract compliance notes"""
        for line in text.split('\n'):
            if "compliance" in line.lower() or "indian law" in line.lower():
                return line.strip().lstrip('•-').strip()
        return "Compliance status unclear - recommend legal review"
    
    def _fallback_analysis(self, clause_text: str, clause_type: str) -> Dict:
        """Fallback rule-based analysis with intelligent scoring"""
        text_lower = clause_text.lower()
        
        # Define risk keywords with weights
        critical_high_risk = {
            "unlimited liability": 3,
            "perpetual": 3,
            "irrevocable": 3,
            "sole discretion": 2.5,
            "unilateral termination": 2.5,
            "non-compete": 2,
            "unlimited damages": 2,
            "terminate at will": 2,
            "indemnify": 2,
        }
        
        medium_risk_words = {
            "termination": 1,
            "liability cap": 1,
            "confidentiality": 1,
            "jurisdiction": 1,
            "arbitration": 1,
            "notice period": 0.5,
            "dispute resolution": 0.5,
        }
        
        low_risk_words = {
            "compensation": 0.2,
            "payment terms": 0.2,
            "standard": 0.1,
        }
        
        # Calculate risk score
        risk_score = 0
        found_concerns = []
        
        for keyword, weight in critical_high_risk.items():
            if keyword in text_lower:
                risk_score += weight
                found_concerns.append(f"Critical: {keyword}")
        
        for keyword, weight in medium_risk_words.items():
            if keyword in text_lower:
                risk_score += weight
        
        for keyword, weight in low_risk_words.items():
            if keyword in text_lower:
                risk_score = max(0, risk_score - weight)
        
        # Determine risk level based on score
        if risk_score >= 2.5:
            risk = "High"
        elif risk_score >= 1:
            risk = "Medium"
        else:
            risk = "Low"
        
        unfav = risk in ["High", "Medium"]
        
        return {
            "risk": risk,
            "unfavorable": unfav,
            "explanation": clause_text[:200] + "..." if len(clause_text) > 200 else clause_text,
            "suggestion": self._get_improvement_suggestion(clause_type, risk),
            "concerns": found_concerns[:3] if found_concerns else [],
            "full_analysis": f"Risk Score: {risk_score:.2f}\nClause Type: {clause_type}\nRisk Level: {risk}"
        }
    
    @staticmethod
    def _get_improvement_suggestion(clause_type: str, risk_level: str) -> str:
        """Get specific improvement suggestions based on clause type"""
        suggestions = {
            "termination": {
                "High": "Negotiate clear notice period and severance details",
                "Medium": "Clarify termination conditions and notice requirements",
                "Low": "Clause is reasonable"
            },
            "non-compete": {
                "High": "Narrow the scope, duration, and geographic limitations",
                "Medium": "Define geographical and time-based restrictions clearly",
                "Low": "Standard non-compete language"
            },
            "liability": {
                "High": "Add liability caps and exclusions for indirect damages",
                "Medium": "Specify monetary caps on total liability",
                "Low": "Liability clause is balanced"
            },
            "confidentiality": {
                "High": "Limit duration and scope of confidentiality obligations",
                "Medium": "Clarify what constitutes confidential information",
                "Low": "Standard confidentiality provisions"
            },
        }
        
        clause_lower = clause_type.lower()
        for key, levels in suggestions.items():
            if key in clause_lower:
                return levels.get(risk_level, "Consult legal advisor")
        
        return "Consult with legal advisor for improvements" if risk_level == "High" else "Clause appears acceptable"
    
    def _fallback_contract_analysis(self, contract_text: str) -> Dict:
        """Fallback contract analysis"""
        return {
            "contract_type": "Unknown",
            "key_risks": ["Unable to analyze - please review manually"],
            "overall_risk": "Unknown",
            "priority_clauses": [],
            "compliance_notes": "Manual review recommended",
            "full_analysis": ""
        }


# Singleton instance
_analyzer = None


def get_analyzer():
    """Get or create analyzer instance"""
    global _analyzer
    if _analyzer is None:
        _analyzer = RiskAnalyzer()
    return _analyzer


def analyze_clause(clause_text: str, clause_type: str = "General") -> Dict:
    """Wrapper function for clause analysis"""
    analyzer = get_analyzer()
    return analyzer.analyze_clause(clause_text, clause_type)


def overall_risk(clauses: List[Dict], contract_text: str = "") -> str:
    """
    Calculate overall contract risk with intelligent scoring
    Considers: number of high-risk clauses, severity, frequency of risk keywords
    """
    if not clauses:
        return "Low"
    
    # Count risk levels
    high_risk_count = sum(1 for c in clauses if c.get("risk") == "High")
    medium_risk_count = sum(1 for c in clauses if c.get("risk") == "Medium")
    low_risk_count = sum(1 for c in clauses if c.get("risk") == "Low")
    
    total_clauses = len(clauses)
    
    # Calculate risk percentage
    high_risk_percent = (high_risk_count / total_clauses * 100) if total_clauses > 0 else 0
    medium_risk_percent = (medium_risk_count / total_clauses * 100) if total_clauses > 0 else 0
    
    # Risk scoring: Higher weight to high-risk clauses
    risk_score = (high_risk_count * 3) + (medium_risk_count * 1)
    
    # Check for critical keywords in contract text
    critical_keywords = [
        "unlimited liability", "perpetual", "irrevocable",
        "sole discretion", "unilateral termination",
        "non-compete", "confidentiality", "indemnify",
        "penalty", "terminate at will"
    ]
    
    if contract_text:
        text_lower = contract_text.lower()
        critical_count = sum(1 for kw in critical_keywords if kw in text_lower)
        risk_score += critical_count
    
    # Determine overall risk based on scoring
    if high_risk_count >= 2 or risk_score >= 6 or high_risk_percent >= 30:
        return "High"
    elif high_risk_count == 1 or medium_risk_count >= 3 or risk_score >= 3 or medium_risk_percent >= 50:
        return "Medium"
    else:
        return "Low"


def get_contract_summary(contract_text: str) -> Dict:
    """Get contract summary"""
    analyzer = get_analyzer()
    return analyzer.analyze_contract_overview(contract_text)
