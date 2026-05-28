#!/usr/bin/env python3

import os
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

def extract_apk_metadata(apk_path):
    """Extract basic metadata from APK filename"""
    filename = os.path.basename(apk_path)
    # Format: aniyomi-{lang}.{name}-v{version}.apk or aniyomi-{package}-v{version}.apk
    match = re.match(r'aniyomi-(.+)-v([\d.]+)\.apk', filename)
    
    if match:
        package = match.group(1)
        version = match.group(2)
        # Convert lang.name to proper naming
        if '.' in package:
            parts = package.split('.')
            lang = parts[0]
            name = '.'.join(parts[1:])
        else:
            lang = "all"
            name = package
        
        full_package = f"eu.kanade.tachiyomi.animeextension.{package}"
        
        return {
            "name": name.replace('-', ' ').title(),
            "package": full_package,
            "version": version,
            "apk": f"apk/{filename}",
            "icon": f"icon/{full_package}.png"
        }
    return None

def generate_index():
    """Generate index.json and index.min.json from built APKs"""
    
    print("🔍 Procurando APKs compilados...", file=sys.stderr)
    
    build_dir = Path("build")
    apk_files = list(build_dir.glob("**/*.apk")) if build_dir.exists() else []
    
    print(f"📊 APKs encontrados: {len(apk_files)}", file=sys.stderr)
    for apk in apk_files:
        print(f"   - {apk.name}", file=sys.stderr)
    
    extensions = []
    
    for apk in apk_files:
        metadata = extract_apk_metadata(str(apk))
        if metadata:
            print(f"✅ Parseado: {metadata['name']}", file=sys.stderr)
            extensions.append({
                "name": f"Aniyomi: {metadata['name']}",
                "package": metadata["package"],
                "apk": metadata["apk"],
                "icon": metadata["icon"],
                "lang": "pt-BR",
                "code": int(metadata["version"].split('.')[-1]),
                "version": metadata["version"],
                "nsfw": 0,
                "sources": [
                    {
                        "name": metadata["name"],
                        "lang": "pt-BR",
                        "id": "0",
                        "baseUrl": ""
                    }
                ]
            })
        else:
            print(f"⚠️  Não foi possível fazer parse: {apk.name}", file=sys.stderr)
    
    # Create timestamp
    now = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    
    # Create index structure (compatible com Aniyomi)
    index_data = {
        "repo": {
            "name": "Depo - Extensões de Anime",
            "description": "Repositório de extensões de anime para Aniyomi",
            "owner": "Diogo-Pereira-Ribeiro",
            "url": "https://github.com/Diogo-Pereira-Ribeiro/Depo",
            "logo": None
        },
        "extensions": extensions,
        "generated": now
    }
    
    # Criar diretórios se não existirem
    Path("repo").mkdir(exist_ok=True)
    
    # Before writing, convert apk/icon relative paths to full raw URLs and apply known baseUrl overrides
    raw_base = 'https://raw.githubusercontent.com/Diogo-Pereira-Ribeiro/Depo/repo/'
    overrides = {
        'eu.kanade.tachiyomi.animeextension.pt.animesdrive': 'https://animesdrive.online',
        'eu.kanade.tachiyomi.animeextension.pt.animeq': 'https://animeq.net',
        'eu.kanade.tachiyomi.animeextension.pt.anitube': 'https://anitube.vip',
        'eu.kanade.tachiyomi.animeextension.pt.hentaistube': 'https://www.hentaistube.com'
    }

    for ext in extensions:
        if 'apk' in ext and ext['apk'] and not ext['apk'].startswith('http'):
            ext['apk'] = raw_base + ext['apk'].lstrip('/')
        if 'icon' in ext and ext['icon'] and not ext['icon'].startswith('http'):
            ext['icon'] = raw_base + ext['icon'].lstrip('/')
        # apply overrides for baseUrl
        pkg = ext.get('package') or ext.get('pkg')
        if pkg:
            base = overrides.get(pkg)
            if base:
                try:
                    ext['sources'][0]['baseUrl'] = base
                except Exception:
                    pass

    # Write full index
    with open("index.json", "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    print("✅ index.json criado", file=sys.stderr)
    
    # Write minified index
    with open("index.min.json", "w", encoding="utf-8") as f:
        json.dump(index_data, f, separators=(',', ':'), ensure_ascii=False)
    print("✅ index.min.json criado", file=sys.stderr)
    
    # Write repo metadata
    repo_data = {
        "name": "Depo - Extensões de Anime",
        "description": "Repositório de extensões de anime para Aniyomi",
        "owner": "Diogo-Pereira-Ribeiro",
        "url": "https://github.com/Diogo-Pereira-Ribeiro/Depo",
        "logo": None,
        "extensions": len(extensions),
        "updated": now
    }
    
    with open("repo.json", "w", encoding="utf-8") as f:
        json.dump(repo_data, f, indent=2, ensure_ascii=False)
    print("✅ repo.json criado", file=sys.stderr)
    
    print(f"\n✅ Índice gerado com {len(extensions)} extensões", file=sys.stderr)
    return 0

if __name__ == "__main__":
    sys.exit(generate_index())
