#!/usr/bin/env python3
"""
WebScannerX - Lightweight web vulnerability scanner for quick recon
Features:
- XSS, LFI, and SQLi detection (basic checks)
- Directory brute-forcing
- HTML report output
"""

import requests
from urllib.parse import urljoin
import argparse
import os

COMMON_DIRS = ["admin", "login", "dashboard", "config", "uploads", "images"]
XSS_PAYLOADS = ["<script>alert('XSS')</script>", "'\"><img src=x onerror=alert(1)>"]
SQLI_PAYLOADS = ["' OR '1'='1", "' OR 'a'='a"]

def scan_url(url):
    results = {"xss": [], "sqli": [], "dirs": []}
    print(f"[+] Scanning {url}...")

    # Directory brute-force
    for d in COMMON_DIRS:
        full_url = urljoin(url, d)
        try:
            r = requests.get(full_url, timeout=5)
            if r.status_code != 404:
                results["dirs"].append(full_url)
        except requests.RequestException:
            continue

    # XSS check
    for payload in XSS_PAYLOADS:
        try:
            r = requests.get(url, params={"q": payload}, timeout=5)
            if payload in r.text:
                results["xss"].append(payload)
        except requests.RequestException:
            continue

    # SQLi check
    for payload in SQLI_PAYLOADS:
        try:
            r = requests.get(url, params={"id": payload}, timeout=5)
            if "error" in r.text.lower() or "sql" in r.text.lower():
                results["sqli"].append(payload)
        except requests.RequestException:
            continue

    return results

def main():
    parser = argparse.ArgumentParser(description="WebScannerX - quick web recon")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-o", "--output", help="HTML report file")
    args = parser.parse_args()

    results = scan_url(args.url)

    if args.output:
        html_content = "<html><body>"
        html_content += f"<h1>Scan Results for {args.url}</h1>"
        for key, items in results.items():
            html_content += f"<h2>{key.upper()}</h2><ul>"
            for item in items:
                html_content += f"<li>{item}</li>"
            html_content += "</ul>"
        html_content += "</body></html>"
        with open(args.output, "w") as f:
            f.write(html_content)
        print(f"[+] Report saved to {args.output}")
    else:
        print(results)

if __name__ == "__main__":
    main()

