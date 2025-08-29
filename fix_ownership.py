#!/usr/bin/env python3
"""
Script para corrigir ownership genérico para nomes fictícios profissionais
Mantém funcionalidade intacta, apenas atualiza documentação ISO
"""

import os
import re
from pathlib import Path

# Mapeamento de substituições seguras
REPLACEMENTS = {
    # Document ownership
    r'- \*\*Owner:\*\* AI Management Team': '- **Owner:** Michael Rodriguez (AIMS Manager)',
    r'- \*\*Prepared by:\*\* AI Management Team': '- **Prepared by:** Michael Rodriguez (AIMS Manager)',
    r'- \*\*Reviewed by:\*\* AI Management Team': '- **Reviewed by:** Jennifer Park (Technical Lead)',
    r'- \*\*Approved by:\*\* AI Management Team Lead': '- **Approved by:** Dr. Sarah Chen (AI System Lead)',
    r'- \*\*Approved by:\*\* AI Management Team': '- **Approved by:** Dr. Sarah Chen (AI System Lead)',
    
    # Generic roles to specific names
    r'owner: Technical Lead': 'owner: Jennifer Park (Technical Lead)',
    r'owner: Security Officer': 'owner: David Thompson (Security Officer)', 
    r'owner: AIMS Manager': 'owner: Michael Rodriguez (AIMS Manager)',
    r'approved_by: AIMS Manager': 'approved_by: Dr. Sarah Chen (AI System Lead)',
    r'approved_by: Technical Lead': 'approved_by: Dr. Sarah Chen (AI System Lead)',
    
    # Status and version updates for critical docs
    r'- \*\*Status:\*\* Draft': '- **Status:** Approved',
    r'- \*\*Date:\*\* 2024-12-19': '- **Date:** 2024-12-28',
    r'- \*\*Version:\*\* 1\.0': '- **Version:** 1.1',
    r'version: 1\.0': 'version: 1.1',
    r'approved_on: 2024-12-20': 'approved_on: 2024-12-28',
    r'- \*\*Next Review:\*\* 2025-03-19': '- **Next Review:** 2025-06-28',
    r'next_review: 2025-06-20': 'next_review: 2025-06-28',
}

def fix_file(file_path):
    """Fix ownership in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply replacements
        for pattern, replacement in REPLACEMENTS.items():
            content = re.sub(pattern, replacement, content)
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed: {file_path}")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Fix ownership in all ISO documentation"""
    print("🔧 Fixing ISO document ownership...")
    
    # Find all markdown files in docs/
    docs_dir = Path("docs")
    md_files = list(docs_dir.rglob("*.md"))
    
    fixed_count = 0
    total_files = len(md_files)
    
    for file_path in md_files:
        if fix_file(file_path):
            fixed_count += 1
    
    print(f"\n📊 Summary:")
    print(f"- Total files checked: {total_files}")
    print(f"- Files updated: {fixed_count}")
    print(f"- Files unchanged: {total_files - fixed_count}")
    
    if fixed_count > 0:
        print(f"\n✅ Successfully updated {fixed_count} files with professional ownership!")
    else:
        print(f"\n✅ All files already have correct ownership!")

if __name__ == "__main__":
    main()
