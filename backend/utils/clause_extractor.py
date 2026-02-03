"""
Clause Extractor Module - Identifies and extracts clauses from contracts using NLP
"""
import re
from typing import List, Dict
import nltk
from nltk.tokenize import sent_tokenize
from textblob import TextBlob

# Download required NLTK data
import os
nltk_data_dir = os.path.expanduser('~/nltk_data')
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir, exist_ok=True)

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    try:
        nltk.download('punkt_tab', quiet=True)
    except:
        pass

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    try:
        nltk.download('punkt', quiet=True)
    except:
        pass


IMPORTANT_CLAUSES = {
    "termination": ["termination", "terminate", "end of contract", "cancellation"],
    "compensation": ["compensation", "salary", "wages", "payment", "remuneration"],
    "confidentiality": ["confidential", "confidentiality", "nda", "non-disclosure"],
    "non-compete": ["non-compete", "non-compete clause", "non-competition", "restriction"],
    "liability": ["liability", "liable", "indemnify", "indemnification", "hold harmless"],
    "intellectual_property": ["intellectual property", "ip rights", "copyright", "patent", "trademark"],
    "jurisdiction": ["jurisdiction", "governing law", "applicable law", "venue"],
    "auto_renewal": ["auto-renew", "renewal", "automatic renewal", "renew"],
    "severance": ["severance", "separation", "layoff", "redundancy"],
    "notice": ["notice", "notification", "notified"],
    "arbitration": ["arbitration", "dispute resolution", "mediation"],
    "penalties": ["penalty", "penalties", "fine", "breach damage"],
    "force_majeure": ["force majeure", "unforeseen", "circumstances beyond control"],
    "warranty": ["warranty", "warrant", "guarantee", "representation"],
    "assignment": ["assignment", "assign", "transfer of rights"],
    "entire_agreement": ["entire agreement", "supersede", "integration clause"],
}

HIGH_RISK_KEYWORDS = [
    "penalty", "terminate at will", "unilateral termination", "unlimited liability",
    "indemnify", "non-compete", "sole discretion", "at any time",
    "unlimited damages", "perpetual", "irrevocable"
]

MEDIUM_RISK_KEYWORDS = [
    "termination", "arbitration", "jurisdiction", "confidential",
    "liability cap", "insurance", "notice period", "notice requirement"
]


def extract_clauses(text: str, max_clauses: int = 20) -> List[Dict[str, any]]:
    """
    Extract meaningful legal clauses from contract text
    Uses multiple strategies: numbering, keywords, and sentence segmentation
    """
    clauses = []
    seen_content = set()
    
    # Strategy 1: Split by numbered sections (1., 2., 3., etc.)
    sections = re.split(r"\n\s*(?:\d+[\.\)]\s+|[A-Z]\.\s+)", text)
    
    for section in sections:
        section = section.strip()
        if len(section) < 50:  # Lowered from 100
            continue
        
        # Find matching clause category
        clause_type = None
        for ctype, keywords in IMPORTANT_CLAUSES.items():
            if any(kw in section.lower() for kw in keywords):
                clause_type = ctype
                break
        
        if not clause_type:
            clause_type = "General"  # Don't skip, mark as General
        
        # Extract title
        first_line = section.split('\n')[0][:100]
        
        # Avoid duplicates
        content_hash = hash(section[:200])
        if content_hash in seen_content:
            continue
        seen_content.add(content_hash)
        
        # Extract sentences for better readability
        try:
            sentences = sent_tokenize(section)
            clause_text = " ".join(sentences[:5])  # First 5 sentences
        except:
            clause_text = section[:500]
        
        risk_level = calculate_clause_risk(section)
        
        clauses.append({
            "type": clause_type,
            "title": first_line if first_line else f"{clause_type.replace('_', ' ').title()} Clause",
            "text": clause_text[:1000],  # Limit length
            "full_text": section[:2000],
            "risk_level": risk_level
        })
        
        if len(clauses) >= max_clauses:
            break
    
    # Ensure minimum clauses extracted (fallback strategy)
    if len(clauses) < 5:
        additional_clauses = extract_clauses_by_keywords(text, max_clauses - len(clauses))
        clauses.extend(additional_clauses)
    
    return clauses


def extract_clauses_by_keywords(text: str, max_clauses: int) -> List[Dict[str, any]]:
    """
    Fallback method: Extract clauses by keyword matching
    """
    clauses = []
    seen = set()
    
    # Find sentences containing important keywords
    sentences = sent_tokenize(text)
    
    for ctype, keywords in IMPORTANT_CLAUSES.items():
        for sentence in sentences:
            if any(kw.lower() in sentence.lower() for kw in keywords):
                sent_hash = hash(sentence[:100])
                if sent_hash not in seen:
                    seen.add(sent_hash)
                    clauses.append({
                        "type": ctype,
                        "title": f"{ctype.replace('_', ' ').title()} Clause",
                        "text": sentence[:1000],
                        "full_text": sentence,
                        "risk_level": calculate_clause_risk(sentence)
                    })
                if len(clauses) >= max_clauses:
                    break
        if len(clauses) >= max_clauses:
            break
    
    return clauses


def calculate_clause_risk(clause_text: str) -> str:
    """
    Calculate risk level of a clause
    Returns: 'High', 'Medium', 'Low'
    """
    text_lower = clause_text.lower()
    
    # High risk keywords
    if any(kw in text_lower for kw in HIGH_RISK_KEYWORDS):
        return "High"
    
    # Medium risk keywords
    if any(kw in text_lower for kw in MEDIUM_RISK_KEYWORDS):
        return "Medium"
    
    return "Low"


def identify_obligations(clause_text: str) -> List[str]:
    """
    Identify obligations in a clause
    """
    obligations = []
    obligation_starters = [
        "shall", "must", "required to", "responsible for",
        "obligated to", "shall not", "may not", "prohibited"
    ]
    
    sentences = sent_tokenize(clause_text)
    for sent in sentences:
        for starter in obligation_starters:
            if starter.lower() in sent.lower():
                obligations.append(sent.strip())
                break
    
    return obligations[:3]  # Return top 3


def identify_rights(clause_text: str) -> List[str]:
    """
    Identify rights in a clause
    """
    rights = []
    right_starters = [
        "may", "has the right to", "entitled to", "authorized to",
        "permitted to", "can", "allowed to", "shall have"
    ]
    
    sentences = sent_tokenize(clause_text)
    for sent in sentences:
        for starter in right_starters:
            if starter.lower() in sent.lower():
                rights.append(sent.strip())
                break
    
    return rights[:3]  # Return top 3


def detect_ambiguities(clause_text: str) -> List[str]:
    """
    Detect ambiguous language in clauses
    """
    ambiguities = []
    ambiguous_phrases = [
        "reasonable", "as appropriate", "suitable",
        "appropriate manner", "best efforts", "commercially reasonable",
        "upon request", "if necessary", "may vary",
        "subject to", "without limitation"
    ]
    
    for phrase in ambiguous_phrases:
        if phrase.lower() in clause_text.lower():
            ambiguities.append(f"'{phrase}' - vague term that could be interpreted differently")
    
    return ambiguities
