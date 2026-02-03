#!/usr/bin/env python3
"""
Validation Script - Checks if all components are properly installed and configured
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.9 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print(f"❌ Python version too old: {version.major}.{version.minor}")
        print("   Required: Python 3.9 or higher")
        return False
    
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if all required packages are installed"""
    required = [
        'streamlit',
        'anthropic',
        'nltk',
        'textblob',
        'docx',
        'pdfplumber',
        'pandas',
        'pydantic',
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True


def check_file_structure():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        'GETTING_STARTED.md',
        '.env.example',
        'backend/main.py',
        'backend/__init__.py',
        'backend/utils/__init__.py',
        'backend/utils/file_reader.py',
        'backend/utils/clause_extractor.py',
        'backend/utils/risk_engine.py',
        'backend/utils/ner.py',
        'backend/utils/contract_classifier.py',
    ]
    
    missing = []
    for file_path in required_files:
        full_path = Path(file_path)
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing.append(file_path)
    
    if missing:
        print(f"\n❌ Missing files: {', '.join(missing)}")
        return False
    
    return True


def check_env_file():
    """Check if .env file exists and has API key"""
    if not Path('.env').exists():
        print("⚠️  .env file not found")
        print("   Create .env file with: ANTHROPIC_API_KEY=your-key")
        print("   You can copy from .env.example")
        return False
    
    try:
        with open('.env', 'r') as f:
            content = f.read()
            if 'ANTHROPIC_API_KEY' in content and '=sk-ant-' in content:
                print("✓ .env file configured with API key")
                return True
            else:
                print("⚠️  .env file exists but may not have valid API key")
                print("   Format: ANTHROPIC_API_KEY=sk-ant-xxxxx")
                return False
    except Exception as e:
        print(f"❌ Error reading .env: {e}")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("GenAI Contract Analysis Bot - Validation Check")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Environment Setup", check_env_file),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n{check_name}:")
        print("-" * 60)
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error during check: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)
    
    all_passed = True
    for check_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✅ All checks passed! Ready to run:")
        print("   streamlit run app.py")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        print("\nFor help, see GETTING_STARTED.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())
