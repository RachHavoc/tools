#!/usr/bin/env python3
import argparse
import os

LEET_MAP = {
    "a": "4",
    "e": "3",
    "i": "1",
    "o": "0",
    "s": "5",
    "t": "7"
}


def to_leet(word: str) -> str:
    """Convert a word into a leet-speak variant."""
    return "".join(LEET_MAP.get(c, c) for c in word)


def generate_usernames(first: str, last: str, leet: bool = False) -> set:
    """Generate realistic username combinations given a first and last name."""
    first = first.lower()
    last = last.lower()

    usernames = set()

    # Common corporate username formats
    usernames.add(first + "." + last)         # jane.doe
    usernames.add(first[0] + last)            # jdoe
    usernames.add(first[0] + "." + last)      # j.doe
    usernames.add(first + last[0])            # janed
    usernames.add(first + "_" + last)         # jane_doe
    usernames.add(first + last)               # janedoe
    usernames.add(last + first[0])            # doej
    usernames.add(first)                      # jane
    usernames.add(last)                       # doe

    # Numeric variants
    usernames.add(first[0] + last + "1")      # jdoe1
    usernames.add(first + "." + last + "99")  # jane.doe99
    usernames.add(first + last + "123")       # janedoe123

    # Add leet variants if enabled
    if leet:
        leet_usernames = {to_leet(u) for u in usernames}
        usernames.update(leet_usernames)

    return usernames


def generate_email_variants(first: str, last: str, domain: str, leet: bool = False) -> set:
    """Generate realistic corporate-style email addresses."""
    first = first.lower()
    last = last.lower()
    domain = domain.lower()

    emails = set()

    # Most common corporate email patterns
    emails.add(f"{first}.{last}@{domain}")     # jane.doe@example.com
    emails.add(f"{first[0]}{last}@{domain}")   # jdoe@example.com
    emails.add(f"{first[0]}.{last}@{domain}")  # j.doe@example.com
    emails.add(f"{first}{last[0]}@{domain}")   # janed@example.com
    emails.add(f"{first}{last}@{domain}")      # janedoe@example.com
    emails.add(f"{last}{first[0]}@{domain}")   # doej@example.com

    # Secondary formats
    emails.add(f"{first}@{domain}")            # jane@example.com
    emails.add(f"{last}@{domain}")             # doe@example.com

    # Numeric fallback patterns
    emails.add(f"{first}.{last}1@{domain}")    # jane.doe1@example.com
    emails.add(f"{first[0]}{last}99@{domain}") # jdoe99@example.com

    # Add leet variants if enabled
    if leet:
        leet_emails = set()
        for email in emails:
            local, domain_part = email.split("@")
            leet_emails.add(f"{to_leet(local)}@{domain_part}")
        emails.update(leet_emails)

    return emails


def process_file(input_file: str, output_file: str, leet: bool = False,
                 domain: str = None, verbose: bool = False) -> None:
    """Read names from input file, generate usernames/emails, and write to output file."""
    if not os.path.isfile(input_file):
        print(f"[-] Error: File '{input_file}' not found.")
        return

    all_usernames = set()
    total_lines = 0
    processed_lines = 0

    with open(input_file, "r", encoding="utf-8") as infile:
        for line in infile:
            total_lines += 1
            line = line.strip().replace("\r", "")
            if not line:
                continue

            parts = line.split()
            if len(parts) < 2:
                if verbose:
                    print(f"[!] Skipping invalid line {total_lines}: '{line}'")
                continue

            first, last = parts[0], parts[-1]  # Handles middle names

            # Generate usernames
            usernames = generate_usernames(first, last, leet=leet)
            all_usernames.update(usernames)

            if verbose:
                print(f"[+] {first} {last} -> {len(usernames)} usernames")

            # Generate email variants if a domain is provided
            if domain:
                emails = generate_email_variants(first, last, domain, leet=leet)
                all_usernames.update(emails)

                if verbose:
                    print(f"    ↳ Added {len(emails)} email variants for {first} {last}")

            processed_lines += 1

    if processed_lines == 0:
        print("[-] No valid names found in the input file.")
        return

    with open(output_file, "w", encoding="utf-8") as outfile:
        for username in sorted(all_usernames):
            outfile.write(username + "\n")

    print(f"[+] Processed {processed_lines}/{total_lines} lines")
    print(f"[+] Generated {len(all_usernames)} unique usernames in '{output_file}'.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate realistic usernames and optionally email addresses from a list of names."
    )
    parser.add_argument("input", help="Path to input file containing names (First Last).")
    parser.add_argument(
        "-o", "--output",
        default="usernames.lst",
        help="Output file to store generated usernames (default: usernames.lst)"
    )
    parser.add_argument(
        "--leet",
        action="store_true",
        help="Enable leet-speak variants (e.g., jane.doe -> j4n3.d03)"
    )
    parser.add_argument(
        "--domain",
        help="Optional domain to append and generate email-style usernames (e.g., example.com)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug output to show what's happening"
    )

    args = parser.parse_args()

    process_file(
        args.input,
        args.output,
        leet=args.leet,
        domain=args.domain,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()

