import os
import json
from collections import defaultdict

# Specify the main directory containing all folders
main_directory = "./lighthouse"

# Store relevant information in a list
audit_data_list = []

# Store relevant JavaScript library information and count in a dictionary
js_libraries_data_dict = defaultdict(lambda: {"count": 0, "versions": defaultdict(int)})

# Define the target audits
target_audits = [
    "is-on-https",
    "third-party-summary",
    "csp-xss",
    "js-libraries",
    "uses-http2",
    "uses-passive-event-listeners",
    "is-crawlable",
    "robots-txt",
    "meta-viewport",  # very important for mobile user!
    "content-width",  # mobile user
    "viewport",       # mobile user
    "link-name",
    "paste-preventing-inputs",
    "interactive",
    "unsized-images",
    "font-display",
    "redirects",
    "total-blocking-time",
    "max-potential-fid",
    "first-contentful-paint",
    "largest-contentful-paint",
    "first-meaningful-paint",
]

# Traverse all folders in the main directory
for folder_name in os.listdir(main_directory):
    folder_path = os.path.join(main_directory, folder_name)

    # Check if it's a folder
    if os.path.isdir(folder_path):
        # Traverse all files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                # Build the full file path
                file_path = os.path.join(folder_path, filename)

                # Parse the JSON report
                with open(file_path, 'r', encoding='utf-8') as file:
                    report = json.load(file)

                # Extract information for target audits
                for audit_name in target_audits:
                    audit_data = report.get("audits", {}).get(audit_name, {})
                    score = audit_data.get("score")
                    requested_url = report.get("requestedUrl")
                    final_displayed_url = report.get("finalDisplayedUrl")

                    # Extract information from the "js-libraries" section
                    js_libraries_data_audit = audit_data
                    if audit_name == "js-libraries" and js_libraries_data_audit:
                        js_libraries_name = js_libraries_data_audit.get("details", {}).get("items", [])
                        for library_info in js_libraries_name:
                            name = library_info.get("name")
                            version = library_info.get("version")

                            # Update count and versions in the dictionary
                            js_libraries_data_dict[name]["count"] += 1
                            js_libraries_data_dict[name]["versions"][version] += 1

                    # Analyze redirection information
                    is_redirect = requested_url != final_displayed_url
                    redirects_to_https = requested_url.startswith("http://") and final_displayed_url.startswith("https://")

                    # Add information to the list
                    audit_data_list.append({
                        "audit_name": audit_name,
                        "score": score,
                        "requested_url": requested_url,
                        "final_displayed_url": final_displayed_url,
                        "is_redirect": is_redirect,
                        "redirects_to_https": redirects_to_https
                    })

# Save audit data as JSON
with open("audit_data.json", "w", encoding="utf-8") as audit_file:
    json.dump(audit_data_list, audit_file, ensure_ascii=False, indent=2)

# Convert sets to lists in js_libraries_data_dict
js_libraries_data_dict_serializable = {}
for name, data in js_libraries_data_dict.items():
    js_libraries_data_dict_serializable[name] = {
        "count": data["count"],
        "versions": dict(data["versions"])  # Convert defaultdict to regular dict
    }

# Save js_libraries_data_dict as JSON
with open("js_libraries_data.json", "w", encoding="utf-8") as js_libraries_dict_file:
    json.dump(js_libraries_data_dict_serializable, js_libraries_dict_file, indent=2)

print(f"JavaScript libraries data dictionary saved to js_libraries_data.json")
