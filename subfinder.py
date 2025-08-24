#!/usr/bin/env python3
"""
Subdomain Finder - simple, fast, and extensible.

Usage:
  python subfinder.py -d example.com -w wordlists/subdomains_small.txt
  python subfinder.py -d example.com -w subs.txt -t 50 --timeout 3 --show-ips -o results.json

Author: orhan pala
License: MIT
"""
import argparse
import concurrent.futures
import json
import socket
import time
from typing import List, Dict, Optional

import requests
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except Exception:
    pass

__version__ = "0.1.0"


def read_wordlist(path: str) -> List[str]:
    subs = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            s = line.strip().lower()
            if not s:
                continue
            # allow only safe chars for sub labels
            ok = all(c.isalnum() or c in "-_" for c in s)
            if ok:
                subs.append(s.replace("_", "-"))
    # remove duplicates preserving order
    seen = set()
    unique = []
    for s in subs:
        if s not in seen:
            unique.append(s)
            seen.add(s)
    return unique


def resolve_dns(host: str, timeout: float) -> List[str]:
    # socket timeout global
    old_to = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        _, _, ips = socket.gethostbyname_ex(host)
        return ips or []
    except socket.gaierror:
        return []
    except Exception:
        return []
    finally:
        socket.setdefaulttimeout(old_to)


def http_probe(host: str, timeout: float) -> List[Dict[str, Optional[str]]]:
    session = requests.Session()
    session.headers.update({
        "User-Agent": f"SubFinder/{__version__} (+https://github.com/yourname/SubdomainFinder)"
    })
    results = []
    for scheme in ("http", "https"):
        url = f"{scheme}://{host}"
        try:
            r = session.get(url, timeout=timeout, allow_redirects=True, verify=False)
            results.append({
                "scheme": scheme,
                "status": r.status_code,
                "final_url": r.url
            })
        except requests.RequestException:
            results.append({
                "scheme": scheme,
                "status": None,
                "final_url": None
            })
    return results


def check_one(sub: str, domain: str, do_dns: bool, do_http: bool, timeout: float, show_ips: bool, verbose: int):
    host = f"{sub}.{domain}"
    found = False
    item: Dict[str, object] = {"host": host}
    ips: List[str] = []

    if do_dns:
        ips = resolve_dns(host, timeout)
        if ips:
            item["dns"] = True
            if show_ips:
                item["ips"] = ips
            found = True
        else:
            item["dns"] = False

    if do_http:
        http_info = http_probe(host, timeout)
        item["http"] = http_info
        # consider HTTP "alive" if any scheme returns a status code
        if any(h.get("status") and int(h["status"]) < 400 for h in http_info):
            found = True

    if found:
        if verbose:
            print(f"[+] {host} {' '.join(ips) if (show_ips and ips) else ''}".strip())
        return item
    else:
        if verbose >= 2:
            print(f"[-] {host}")
        return None


def save_output(results: List[Dict[str, object]], output: str):
    if output.endswith(".json"):
        with open(output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
    else:
        with open(output, "w", encoding="utf-8") as f:
            for r in results:
                f.write(f"{r['host']}\n")


def parse_args():
    p = argparse.ArgumentParser(
        description="Simple Subdomain Finder (DNS + optional HTTP probe)",
        epilog="Use only on targets you own or have permission to test."
    )
    p.add_argument("-d", "--domain", required=True, help="Target domain, e.g., example.com")
    p.add_argument("-w", "--wordlist", required=True, help="Path to subdomain wordlist file")
    p.add_argument("-t", "--threads", type=int, default=32, help="Number of worker threads (default: 32)")
    p.add_argument("--timeout", type=float, default=3.0, help="Timeout for DNS/HTTP in seconds (default: 3)")
    p.add_argument("--skip-dns", action="store_true", help="Skip DNS resolution")
    p.add_argument("--skip-http", action="store_true", help="Skip HTTP probing")
    p.add_argument("--show-ips", action="store_true", help="Show resolved IPs in output (printed/JSON)")
    p.add_argument("-o", "--output", help="Save results to file (.json or .txt)")
    p.add_argument("-v", "--verbose", action="count", default=1, help="-v to print hits, -vv to print misses too")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p.parse_args()


def main():
    args = parse_args()
    if args.skip_dns and args.skip_http:
        print("At least one of DNS or HTTP probing must be enabled.")
        return 2

    subs = read_wordlist(args.wordlist)
    if not subs:
        print("No subdomains loaded from wordlist.")
        return 2

    domain = args.domain.strip().strip(".")
    started = time.time()

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(
            check_one, s, domain, not args.skip_dns, not args.skip_http, args.timeout, args.show_ips, args.verbose
        ) for s in subs]
        for fut in concurrent.futures.as_completed(futures):
            item = fut.result()
            if item:
                results.append(item)

    # sort alphabetically
    results.sort(key=lambda x: x["host"])

    print(f"\nDone. Found {len(results)} subdomains in {time.time() - started:.1f}s.")

    if args.output:
        save_output(results, args.output)
        print(f"Saved results to: {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
