"""
Contract Classifier Module - Classifies contract types
"""
from typing import Tuple


class ContractClassifier:
    """
    Classify contract types and characteristics
    """
    
    EMPLOYMENT_KEYWORDS = [
        "employment", "salary", "wages", "compensation", "benefits",
        "job", "position", "employee", "staff", "resignation",
        "probation", "severance", "appraisal", "work experience"
    ]
    
    VENDOR_KEYWORDS = [
        "vendor", "supplier", "purchase", "supply", "goods",
        "invoice", "procurement", "delivery", "terms of supply",
        "quality", "price", "discount"
    ]
    
    LEASE_KEYWORDS = [
        "lease", "rent", "landlord", "tenant", "premises",
        "property", "lease period", "security deposit", "maintenance",
        "renewal", "eviction"
    ]
    
    PARTNERSHIP_KEYWORDS = [
        "partnership", "partner", "profit sharing", "equity",
        "joint venture", "partnership agreement", "capital",
        "partner contribution", "shareholding"
    ]
    
    SERVICE_KEYWORDS = [
        "service", "services", "provider", "client", "consulting",
        "professional", "engagement", "deliverables", "fee",
        "scope of work", "timeline"
    ]
    
    NDA_KEYWORDS = [
        "non-disclosure", "confidential", "nda", "secret",
        "proprietary", "disclosure", "confidentiality agreement"
    ]
    
    @staticmethod
    def classify_contract(text: str) -> Tuple[str, float]:
        """
        Classify contract type and return confidence score (0-1)
        Returns: (contract_type, confidence)
        """
        text_lower = text.lower()
        
        # Count keyword matches for each type
        type_scores = {
            "Employment Agreement": ContractClassifier._count_keywords(text_lower, ContractClassifier.EMPLOYMENT_KEYWORDS),
            "Vendor/Supply Agreement": ContractClassifier._count_keywords(text_lower, ContractClassifier.VENDOR_KEYWORDS),
            "Lease Agreement": ContractClassifier._count_keywords(text_lower, ContractClassifier.LEASE_KEYWORDS),
            "Partnership Agreement": ContractClassifier._count_keywords(text_lower, ContractClassifier.PARTNERSHIP_KEYWORDS),
            "Service Agreement": ContractClassifier._count_keywords(text_lower, ContractClassifier.SERVICE_KEYWORDS),
        }
        
        # Find the highest scoring type
        max_type = max(type_scores, key=type_scores.get)
        max_score = type_scores[max_type]
        
        # Calculate confidence (normalize by total possible matches)
        max_possible = max(len(keywords) for keywords in [
            ContractClassifier.EMPLOYMENT_KEYWORDS,
            ContractClassifier.VENDOR_KEYWORDS,
            ContractClassifier.LEASE_KEYWORDS,
            ContractClassifier.PARTNERSHIP_KEYWORDS,
            ContractClassifier.SERVICE_KEYWORDS
        ])
        
        confidence = min(1.0, max_score / (max_possible * 0.3))  # Normalize
        
        # If confidence is too low, return generic
        if max_score == 0:
            return "General Contract", 0.3
        
        return max_type, confidence
    
    @staticmethod
    def is_nda(text: str) -> Tuple[bool, float]:
        """
        Detect if contract is an NDA
        Returns: (is_nda, confidence)
        """
        text_lower = text.lower()
        score = ContractClassifier._count_keywords(text_lower, ContractClassifier.NDA_KEYWORDS)
        
        is_nda = score >= 2
        confidence = min(1.0, score / 3)
        
        return is_nda, confidence
    
    @staticmethod
    def _count_keywords(text: str, keywords: list) -> int:
        """Count how many keywords appear in text"""
        count = 0
        for keyword in keywords:
            if keyword in text:
                count += 1
        return count
    
    @staticmethod
    def get_key_dates(text: str) -> list:
        """Get important dates for the contract type"""
        import re
        
        dates = []
        
        # Effective date
        if "effective date" in text.lower():
            match = re.search(r'effective date[:\s]+([^\n]+)', text, re.IGNORECASE)
            if match:
                dates.append(("Effective Date", match.group(1).strip()[:50]))
        
        # Expiry/End date
        if any(term in text.lower() for term in ["expiry", "end date", "termination date", "expires"]):
            match = re.search(r'(?:expiry|end date|termination date|expires)[:\s]+([^\n]+)', text, re.IGNORECASE)
            if match:
                dates.append(("End Date", match.group(1).strip()[:50]))
        
        # Renewal date
        if "renewal" in text.lower():
            match = re.search(r'renewal[:\s]+([^\n]+)', text, re.IGNORECASE)
            if match:
                dates.append(("Renewal Date", match.group(1).strip()[:50]))
        
        return dates
    
    @staticmethod
    def get_key_amounts(text: str) -> list:
        """Extract key financial amounts"""
        import re
        
        amounts = []
        
        # Total value/consideration
        if any(term in text.lower() for term in ["total consideration", "total amount", "total value"]):
            match = re.search(r'(?:total|consideration)[:\s]+([^\n]+)', text, re.IGNORECASE)
            if match:
                amounts.append(("Total Consideration", match.group(1).strip()[:50]))
        
        # Salary/Payment
        if any(term in text.lower() for term in ["salary", "compensation", "payment", "fees", "price"]):
            match = re.search(r'(?:salary|compensation|payment|fees|price)[:\s]+([^\n]+)', text, re.IGNORECASE)
            if match:
                amounts.append(("Payment Terms", match.group(1).strip()[:50]))
        
        # Security deposit/Advance
        if any(term in text.lower() for term in ["security deposit", "advance", "earnest"]):
            match = re.search(r'(?:security|advance|earnest)[:\s]+([^\n]+)', text, re.IGNORECASE)
            if match:
                amounts.append(("Deposit/Advance", match.group(1).strip()[:50]))
        
        return amounts


def classify_contract_type(text: str) -> dict:
    """Wrapper function to classify contract"""
    contract_type, confidence = ContractClassifier.classify_contract(text)
    is_nda, nda_confidence = ContractClassifier.is_nda(text)
    
    return {
        "type": contract_type,
        "confidence": round(confidence, 2),
        "is_nda": is_nda,
        "nda_confidence": round(nda_confidence, 2),
        "key_dates": ContractClassifier.get_key_dates(text),
        "key_amounts": ContractClassifier.get_key_amounts(text)
    }
