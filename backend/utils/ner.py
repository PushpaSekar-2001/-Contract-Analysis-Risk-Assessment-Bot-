"""
Named Entity Recognition (NER) Module - Extracts key information from contracts
"""
import re
from typing import Dict, List
from datetime import datetime


class ContractNER:
    """
    Extract Named Entities from contracts:
    - Parties (Company names, individuals)
    - Dates
    - Amounts
    - Locations
    - Percentages
    """
    
    @staticmethod
    def extract_all_entities(text: str) -> Dict[str, List[str]]:
        """Extract all entities from contract"""
        return {
            "parties": ContractNER.extract_parties(text),
            "dates": ContractNER.extract_dates(text),
            "amounts": ContractNER.extract_amounts(text),
            "locations": ContractNER.extract_locations(text),
            "percentages": ContractNER.extract_percentages(text),
            "contact_info": ContractNER.extract_contact_info(text)
        }
    
    @staticmethod
    def extract_parties(text: str) -> List[str]:
        """Extract party names (organizations and individuals)"""
        parties = []
        
        # Pattern: "between", "by and between", "by and between"
        between_pattern = r'(?:between|by and between|entered into by and between)\s+([A-Z][A-Za-z\s&,\.]+?)(?:\s+and\s+|,)'
        matches = re.findall(between_pattern, text)
        parties.extend([m.strip() for m in matches])
        
        # Pattern: "Company", "Corporation", "Limited", "Inc.", "Ltd."
        company_pattern = r'([A-Z][A-Za-z\s&\.]+(?:Company|Corporation|Limited|Inc\.|Ltd\.|LLP|Pvt)\.?)'
        matches = re.findall(company_pattern, text[:2000])  # Check first 2000 chars
        parties.extend([m.strip() for m in matches if len(m) > 5])
        
        # Remove duplicates and filter
        parties = list(set(parties))
        parties = [p for p in parties if len(p) > 3 and not any(skip in p for skip in ["The", "This", "That"])]
        
        return parties[:5]  # Return top 5
    
    @staticmethod
    def extract_dates(text: str) -> List[str]:
        """Extract dates from contract"""
        dates = []
        
        # Pattern: DD/MM/YYYY or DD-MM-YYYY
        date_pattern1 = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
        matches = re.findall(date_pattern1, text)
        dates.extend(matches)
        
        # Pattern: Month Day, Year (e.g., "January 15, 2024")
        date_pattern2 = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
        matches = re.findall(date_pattern2, text)
        dates.extend(matches)
        
        # Pattern: Day Month Year (e.g., "15 January 2024")
        date_pattern3 = r'\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}'
        matches = re.findall(date_pattern3, text)
        dates.extend(matches)
        
        return list(set(dates))[:10]  # Return unique dates
    
    @staticmethod
    def extract_amounts(text: str) -> List[str]:
        """Extract financial amounts"""
        amounts = []
        
        # Pattern: Currency amounts (₹, $, €, £, etc.)
        amount_pattern = r'(?:₹|Rs|INR|Rs\.|\$|USD|€|EUR|£|GBP)\s*[\d,]+(?:\.\d{2})?'
        matches = re.findall(amount_pattern, text, re.IGNORECASE)
        amounts.extend(matches)
        
        # Pattern: Number followed by currency
        amount_pattern2 = r'[\d,]+(?:\.\d{2})?\s*(?:rupees|dollars|euros|pounds|cr|lakhs|thousands|crores)'
        matches = re.findall(amount_pattern2, text, re.IGNORECASE)
        amounts.extend(matches)
        
        return list(set(amounts))[:15]  # Return unique amounts
    
    @staticmethod
    def extract_locations(text: str) -> List[str]:
        """Extract locations and jurisdictions"""
        locations = []
        
        # Common Indian states
        indian_states = [
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
            "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
            "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
            "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
            "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
            "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata", "Hyderabad"
        ]
        
        for state in indian_states:
            if state in text:
                locations.append(state)
        
        # Pattern: City, Country
        location_pattern = r'([A-Z][a-z]+),\s*([A-Z][a-z]+)'
        matches = re.findall(location_pattern, text[:2000])
        for match in matches:
            locations.append(f"{match[0]}, {match[1]}")
        
        return list(set(locations))[:10]
    
    @staticmethod
    def extract_percentages(text: str) -> List[str]:
        """Extract percentages"""
        percentages = []
        
        # Pattern: Number followed by %
        percent_pattern = r'\d+(?:\.\d+)?%'
        matches = re.findall(percent_pattern, text)
        percentages.extend(matches)
        
        # Pattern: "X percent"
        percent_pattern2 = r'(\d+(?:\.\d+)?)\s+(?:percent|%)'
        matches = re.findall(percent_pattern2, text, re.IGNORECASE)
        percentages.extend([m + '%' for m in matches])
        
        return list(set(percentages))[:10]
    
    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, List[str]]:
        """Extract email and phone information"""
        contact = {
            "emails": [],
            "phone_numbers": []
        }
        
        # Email pattern
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        contact["emails"] = list(set(re.findall(email_pattern, text)))[:5]
        
        # Phone pattern (Indian format)
        phone_pattern = r'(?:\+91|0)?[\s\-]?\d{10}|\d{10}|\+\d{1,3}\s?\d{1,14}'
        contact["phone_numbers"] = list(set(re.findall(phone_pattern, text)))[:5]
        
        return contact


def extract_entities(text: str) -> Dict:
    """Wrapper function to extract all entities"""
    return ContractNER.extract_all_entities(text)
