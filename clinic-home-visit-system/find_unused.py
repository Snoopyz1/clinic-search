import os
import re

def get_all_files(directory, extensions):
    all_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                all_files.append(os.path.join(root, file))
    return all_files

def find_unused_vue_js(frontend_dir):
    src_dir = os.path.join(frontend_dir, "src")
    vue_js_files = get_all_files(src_dir, [".vue", ".js"])
    
    # Read all contents to search for imports
    all_contents = ""
    for f in vue_js_files:
        try:
            with open(f, "r", encoding="utf-8") as file:
                all_contents += file.read() + "\n"
        except:
            pass
            
    try:
        with open(os.path.join(frontend_dir, "index.html"), "r", encoding="utf-8") as file:
            all_contents += file.read() + "\n"
    except:
        pass

    unused_files = []
    for f in vue_js_files:
        filename = os.path.basename(f)
        basename, _ = os.path.splitext(filename)
        
        # main.js is entry point
        if filename == "main.js":
            continue
            
        # check if filename or basename is in all_contents
        # This is a basic heuristic, can produce false positives/negatives, but good for starting.
        # We look for the exact filename like "Component.vue" or just "Component"
        
        # A more precise way: check if there's any import containing the basename
        # e.g., import X from './Component.vue' or import X from './Component'
        
        pattern1 = f"/{filename}"
        pattern2 = f"/{basename}'"
        pattern3 = f"/{basename}\""
        pattern4 = f"name: '{basename}'"
        pattern5 = f"name: \"{basename}\""
        
        if (pattern1 not in all_contents and 
            pattern2 not in all_contents and 
            pattern3 not in all_contents and
            filename not in all_contents):
            
            # Additional check: routes might use dynamic imports
            # like `component: () => import('../views/AboutView.vue')`
            if basename not in all_contents:
                unused_files.append(f)
            else:
                # Need regex to confirm if the basename is an import
                if not re.search(r"import\s+.*" + re.escape(basename) + r"|import\(.*" + re.escape(basename), all_contents):
                    # Also check for component registration
                    if not re.search(re.escape(basename), all_contents):
                        unused_files.append(f)

    return unused_files

def find_unused_py(services_dir):
    py_files = get_all_files(services_dir, [".py"])
    
    all_contents = ""
    for f in py_files:
        try:
            with open(f, "r", encoding="utf-8") as file:
                all_contents += file.read() + "\n"
        except:
            pass

    unused_files = []
    for f in py_files:
        filename = os.path.basename(f)
        basename, _ = os.path.splitext(filename)
        
        if basename in ["main", "__init__", "models", "schemas", "database", "config"]:
            continue
            
        # Very rough heuristic: if the basename is not mentioned anywhere in other files
        if not re.search(r"import\s+.*\b" + re.escape(basename) + r"\b|from\s+.*\b" + re.escape(basename) + r"\b", all_contents):
            # Maybe it's a router that is imported by main?
            # Let's check if the basename is used anywhere
            content_without_current_file = all_contents.replace(open(f, "r", encoding="utf-8").read(), "")
            if basename not in content_without_current_file:
                unused_files.append(f)

    return unused_files

frontend_unused = find_unused_vue_js(r"d:\PTIT\Python\Clinic-Search\clinic-home-visit-system\frontend")
services_unused = find_unused_py(r"d:\PTIT\Python\Clinic-Search\clinic-home-visit-system\services")

print("--- UNUSED FRONTEND FILES ---")
for f in frontend_unused:
    print(f)

print("\n--- UNUSED BACKEND FILES (Potential) ---")
for f in services_unused:
    print(f)
