#!/usr/bin/env python3

import os
import json
import re
from pathlib import Path
from datetime import datetime

def extract_apk_metadata(apk_path):
    """Extract basic metadata from APK filename"""
    filename = os.path.basename(apk_path)
    # Format: aniyomi-{package}.{name}-v{version}.apk
    match = re.match(r'aniyomi-(.+)-v([\d.]+)\.apk', filename)
    
    if match:
        package = match.group(1)
        version = match.group(2)
        return {
            "name": package.split('.')[-1],
            "package": package,
            "version": version,
            "apk": f"apk/{filename}"
        }
    return None

def generate_index():
    """Generate index.json and index.min.json from built APKs"""
    
    build_dir = Path("build")
    apk_files = list(build_dir.glob("**/*.apk"))
    
    extensions = []
    
    for apk in apk_files:
        metadata = extract_apk_metadata(str(apk))
        if metadata:
            extensions.append({
                "name": metadata["name"],
                "package": metadata["package"],
                "version": metadata["version"],
                "url": metadata["apk"],
                "icon": f"icon/{metadata['package']}.png"
            })
    
    # Create index structure
    index_data = {
        "repo": {
            "name": "Depo - Extensões de Anime",
            "description": "Repositório de extensões de anime para Aniyomi",
            "owner": "Diogo-Pereira-Ribeiro",
            "url": "https://github.com/Diogo-Pereira-Ribeiro/Depo",
            "logo": None
        },
        "extensions": extensions,
        "generated": datetime.utcnow().isoformat() + "Z"
    }
    
    # Write full index
    with open("index.json", "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    # Write minified index
    with open("index.min.json", "w", encoding="utf-8") as f:
        json.dump(index_data, f, separators=(',', ':'), ensure_ascii=False)
    
    # Write repo metadata
    repo_data = {
        "name": "Depo - Extensões de Anime",
        "description": "Repositório de extensões de anime para Aniyomi",
        "owner": "Diogo-Pereira-Ribeiro",
        "url": "https://github.com/Diogo-Pereira-Ribeiro/Depo",
        "logo": None,
        "extensions": len(extensions),
        "updated": datetime.utcnow().isoformat() + "Z"
    }
    
    with open("repo.json", "w", encoding="utf-8") as f:
        json.dump(repo_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Index gerado com {len(extensions)} extensões")
    print(f"📄 Ficheiros criados: index.json, index.min.json, repo.json")

if __name__ == "__main__":
    generate_index()
