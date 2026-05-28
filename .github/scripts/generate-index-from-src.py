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

    # Extract baseUrl if present in gradle
    baseurl_match = re.search(r"baseUrl\s*=\s*['\"]([^'\"]+)['\"]", content)
    if baseurl_match:
        info['baseUrl'] = baseurl_match.group(1)
    
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
            # If no host in manifest, try gradle baseUrl
            if not base_url:
                gradle_base = gradle_info.get('baseUrl') if gradle_info else None
                base_url = gradle_base or ''
            
            # Build package name
            package_name = f'eu.kanade.tachiyomi.animeextension.{lang_code}.{ext_name}'
            
            # Version should be like 14.X (major.code format)
            version_str = f'14.{gradle_info["version_code"]}'
            
            # Create extension entry
            # Generate stable ID from package name - use long integer
            id_hash = int(hash(package_name)) & 0x7fffffffffffffff
            # Build apk filename expected in repo/apk
            apk_filename = f'aniyomi-{lang_code}.{ext_name}-v{version_str}.apk'

            # Resolve icon: prefer existing repo icon, else try to extract from src resources
            icon_filename = f'{package_name}.png'

            extension = {
                'name': f'Aniyomi: {gradle_info["name"]}',
                'pkg': package_name,
                'package': package_name,
                'apk': f'apk/{apk_filename}',
                'icon': f'icon/{icon_filename}',
                'lang': get_language_name(lang_code),
                'code': gradle_info['version_code'],
                'version': version_str,
                'nsfw': gradle_info['nsfw'],
                'sources': [
                    {
                        'name': gradle_info['name'],
                        'lang': get_language_name(lang_code),
                        'id': id_hash,
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

    # Ensure repo/icon and repo/apk directories exist
    repo_icon_dir = script_path / 'repo' / 'icon'
    repo_apk_dir = script_path / 'repo' / 'apk'
    repo_icon_dir.mkdir(parents=True, exist_ok=True)
    repo_apk_dir.mkdir(parents=True, exist_ok=True)

    # Try to copy icons from source folders if present
    print("🔍 Ensuring icons are available in repo/icon/...")
    for lang_folder in (script_path / 'src').iterdir():
        if not lang_folder.is_dir():
            continue
        for ext_folder in lang_folder.iterdir():
            if not ext_folder.is_dir():
                continue
            lang_code = lang_folder.name
            ext_name = ext_folder.name
            package_name = f'eu.kanade.tachiyomi.animeextension.{lang_code}.{ext_name}'
            icon_target = repo_icon_dir / f"{package_name}.png"
            # If icon already exists in repo/icon, skip
            if icon_target.exists():
                continue
            # Look for common launcher icons inside src extension
            possible_icons = list(ext_folder.glob('**/ic_launcher*.png')) + list(ext_folder.glob('**/icon.png'))
            if possible_icons:
                try:
                    src_icon = possible_icons[0]
                    print(f"   → Copying icon for {package_name} from {src_icon}")
                    with open(src_icon, 'rb') as sf, open(icon_target, 'wb') as tf:
                        tf.write(sf.read())
                except Exception as e:
                    print(f"   ⚠️  Failed to copy icon for {package_name}: {e}")
    
    # Extract just the extensions array (Aniyomi format)
    extensions_only = index['extensions']
    
<<<<<<< HEAD
    # Convert relative apk/icon paths to full raw GitHub URLs pointing to branch 'repo'
    raw_base = 'https://raw.githubusercontent.com/Diogo-Pereira-Ribeiro/Depo/repo/'
=======
    # Convert relative apk/icon paths to full raw GitHub URLs
    # APKs will be published to branch 'repo' by CI; icons we keep in 'main' for immediate availability
    raw_base_repo = 'https://raw.githubusercontent.com/Diogo-Pereira-Ribeiro/Depo/repo/'
    raw_base_main = 'https://raw.githubusercontent.com/Diogo-Pereira-Ribeiro/Depo/main/'
>>>>>>> c61379e (fix(icons): serve icons from main branch and add icons to repo)
    for ext in extensions_only:
        if 'apk' in ext and ext['apk']:
            # If already a full URL, keep it
            if not ext['apk'].startswith('http'):
<<<<<<< HEAD
                ext['apk'] = raw_base + ext['apk'].lstrip('/')
        if 'icon' in ext and ext['icon']:
            if not ext['icon'].startswith('http'):
                ext['icon'] = raw_base + ext['icon'].lstrip('/')
=======
                ext['apk'] = raw_base_repo + ext['apk'].lstrip('/')
        if 'icon' in ext and ext['icon']:
            if not ext['icon'].startswith('http'):
                # icons served from main/icon/ so they are immediately available
                ext['icon'] = raw_base_main + ext['icon'].lstrip('/')
>>>>>>> c61379e (fix(icons): serve icons from main branch and add icons to repo)

    # Write index.min.json (ARRAY FORMAT for Aniyomi)
    index_min_path = script_path / 'index.min.json'
    with open(index_min_path, 'w', encoding='utf-8') as f:
        json.dump(extensions_only, f, ensure_ascii=False, separators=(',', ':'))
    print(f"✅ Created {index_min_path} (array format)")
    
    # Write index.json (formatted ARRAY for Aniyomi)
    index_path = script_path / 'index.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(extensions_only, f, ensure_ascii=False, indent=2)
    print(f"✅ Created {index_path} (array format)")
    
    # Summary
    print(f"\n📊 Index Summary:")
    print(f"   Extensions: {len(index['extensions'])}")
    print(f"   Generated: {index['generated']}")
    print(f"\nExtensions:")
    for ext in index['extensions']:
        print(f"   - {ext['name']} ({ext['lang']})")

if __name__ == '__main__':
    main()
