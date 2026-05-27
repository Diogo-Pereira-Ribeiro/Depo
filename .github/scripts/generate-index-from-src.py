#!/usr/bin/env python3
"""
Generate Aniyomi index from src/ folder structure
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

def extract_gradle_info(gradle_path):
    """Extract extName, extVersionCode, isNsfw from build.gradle"""
    info = {
        'name': 'Unknown',
        'version_code': 1,
        'nsfw': 0
    }
    
    if not os.path.exists(gradle_path):
        return info
    
    with open(gradle_path, 'r') as f:
        content = f.read()
        
    # Extract extName
    ext_name_match = re.search(r"extName\s*=\s*['\"]([^'\"]+)['\"]", content)
    if ext_name_match:
        info['name'] = ext_name_match.group(1)
    
    # Extract extVersionCode
    version_code_match = re.search(r"extVersionCode\s*=\s*(\d+)", content)
    if version_code_match:
        info['version_code'] = int(version_code_match.group(1))
    
    # Extract isNsfw
    nsfw_match = re.search(r"isNsfw\s*=\s*(true|false)", content, re.IGNORECASE)
    if nsfw_match:
        info['nsfw'] = 1 if nsfw_match.group(1).lower() == 'true' else 0
    
    return info

def extract_manifest_info(manifest_path):
    """Extract host from AndroidManifest.xml"""
    if not os.path.exists(manifest_path):
        return None
    
    with open(manifest_path, 'r') as f:
        content = f.read()
    
    # Extract android:host
    host_match = re.search(r'android:host="([^"]+)"', content)
    if host_match:
        return f"https://{host_match.group(1)}"
    
    return None

def get_language_name(lang_code):
    """Map language code to full name"""
    lang_map = {
        'pt': 'pt-BR',
        'en': 'en',
        'es': 'es',
        'ar': 'ar',
        'de': 'de',
        'fr': 'fr',
        'it': 'it',
        'ru': 'ru',
        'ja': 'ja',
        'zh': 'zh',
    }
    return lang_map.get(lang_code, lang_code)

def generate_index():
    """Generate index from src folder structure"""
    src_path = Path(__file__).parent.parent.parent / 'src'
    extensions = []
    
    if not src_path.exists():
        print(f"❌ src path not found: {src_path}")
        return None
    
    # Iterate through language folders (pt, en, es, etc.)
    for lang_folder in src_path.iterdir():
        if not lang_folder.is_dir():
            continue
        
        lang_code = lang_folder.name
        
        # Iterate through extension folders
        for ext_folder in lang_folder.iterdir():
            if not ext_folder.is_dir():
                continue
            
            ext_name = ext_folder.name
            gradle_path = ext_folder / 'build.gradle'
            manifest_path = ext_folder / 'AndroidManifest.xml'
            
            # Extract info
            gradle_info = extract_gradle_info(str(gradle_path))
            base_url = extract_manifest_info(str(manifest_path))
            
            if not base_url:
                base_url = ''
            
            # Build package name
            package_name = f'eu.kanade.tachiyomi.animeextension.{lang_code}.{ext_name}'
            
            # Create extension entry
            # Generate stable ID from package name
            id_hash = int(hash(package_name + gradle_info['name'])) & 0x7fffffffffffffff
            
            extension = {
                'name': f'Aniyomi: {gradle_info["name"]}',
                'pkg': package_name,
                'apk': f'aniyomi-{lang_code}.{ext_name}-v1.{gradle_info["version_code"]}.apk',
                'lang': get_language_name(lang_code),
                'code': gradle_info['version_code'],
                'version': f'1.{gradle_info["version_code"]}',
                'nsfw': gradle_info['nsfw'],
                'sources': [
                    {
                        'name': gradle_info['name'],
                        'lang': get_language_name(lang_code),
                        'id': str(id_hash),
                        'baseUrl': base_url
                    }
                ]
            }
            
            extensions.append(extension)
    
    # Create index structure
    now = datetime.utcnow().isoformat() + 'Z'
    
    index = {
        'repo': {
            'name': 'Depo - Extensões de Anime',
            'description': 'Repositório de extensões de anime para Aniyomi',
            'owner': 'Diogo-Pereira-Ribeiro',
            'url': 'https://github.com/Diogo-Pereira-Ribeiro/Depo',
            'logo': 'https://github.com/Diogo-Pereira-Ribeiro.png'
        },
        'extensions': sorted(extensions, key=lambda x: x['name']),
        'generated': now
    }
    
    return index

def main():
    print("🔄 Generating index from src/ folder...")
    
    index = generate_index()
    if not index:
        print("❌ Failed to generate index")
        return
    
    # Get workspace root
    script_path = Path(__file__).parent.parent.parent
    
    # Write index.min.json
    index_min_path = script_path / 'index.min.json'
    with open(index_min_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, separators=(',', ':'))
    print(f"✅ Created {index_min_path}")
    
    # Write index.json (formatted)
    index_path = script_path / 'index.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"✅ Created {index_path}")
    
    # Write repo.json
    repo_info = {
        'name': index['repo']['name'],
        'description': index['repo']['description'],
        'owner': index['repo']['owner'],
        'url': index['repo']['url'],
        'logo': index['repo']['logo'],
        'extensions': len(index['extensions']),
        'updated': index['generated']
    }
    
    repo_path = script_path / 'repo.json'
    with open(repo_path, 'w', encoding='utf-8') as f:
        json.dump(repo_info, f, ensure_ascii=False, indent=2)
    print(f"✅ Created {repo_path}")
    
    # Summary
    print(f"\n📊 Index Summary:")
    print(f"   Extensions: {len(index['extensions'])}")
    print(f"   Generated: {index['generated']}")
    print(f"\nExtensions:")
    for ext in index['extensions']:
        print(f"   - {ext['name']} ({ext['lang']})")

if __name__ == '__main__':
    main()
