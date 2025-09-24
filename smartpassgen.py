#!/usr/bin/env python3
import argparse
import itertools
import string

# Base list of simple, lazy common passwords (no years by default)
COMMON_PASSWORDS = [
    "Summer", "Winter", "Spring", "Autumn", "Fall",
    "Password", "Welcome", "Admin", "Qwerty", "Letmein"
]

# Top 100 most common passwords from breach data
EXTRA_COMMON_PASSWORDS = [
    "123456", "123456789", "12345", "12345678", "1234567", "123123", "111111", "123321",
    "qwerty", "qwerty123", "1q2w3e4r", "abc123", "password1", "admin123", "letmein123",
    "welcome1", "welcome123", "iloveyou", "princess", "sunshine", "football", "baseball",
    "dragon", "monkey", "shadow", "superman", "batman", "trustno1", "passw0rd", "freedom",
    "starwars", "whatever", "qazwsx", "zaq12wsx", "qwertyuiop", "asdfghjkl", "1qaz2wsx",
    "pokemon", "696969", "buster", "jordan23", "harley", "ginger", "buster123", "samsung",
    "mustang", "hunter", "killer", "pepper", "secret", "cheese", "computer", "michelle",
    "daniel", "ashley", "buster1", "scooter", "maggie", "pepper123", "pass123", "hello123",
    "tigger", "charlie", "snoopy", "banana", "fuckyou", "michael", "jessica", "lovely",
    "cookie", "soccer", "hottie", "whatever123", "jordan", "matthew", "buster12", "pepper1",
    "samsung123", "dragon123", "freedom1", "qwerty2022", "monkey123",
    "ninja", "matrix", "george", "chocolate", "pepperoni", "hockey", "ginger123",
    "pokemon123", "iloveyou123", "princess123", "taylor", "phoenix", "babygirl"
]

# Mapping for leetspeak substitutions
LEET_MAP = {
    "a": ["4", "@"],
    "e": ["3"],
    "i": ["1", "!"],
    "o": ["0"],
    "s": ["5", "$"],
    "t": ["7"]
}

# Mask character sets
MASK_SETS = {
    "?u": string.ascii_uppercase,
    "?l": string.ascii_lowercase,
    "?d": string.digits,
    "?s": "!@#$%^&*"
}

def generate_leet_variations(password: str):
    """Generate leet-style variants for a given password."""
    chars = []
    for c in password:
        lower = c.lower()
        if lower in LEET_MAP:
            chars.append([c] + LEET_MAP[lower])
        else:
            chars.append([c])
    return set("".join(p) for p in itertools.product(*chars))

def generate_username_variations(username: str, year: str = None):
    """Generate password variations based on usernames."""
    username = username.strip()
    if not username:
        return set()

    variations = set()
    cases = {
        username.lower(),
        username.upper(),
        username.capitalize()
    }

    for base in cases:
        variations.add(base)
        variations.add(base + "1")
        variations.add(base + "123")
        variations.add(base + "!")
        variations.add(base + "@123")
        if year:
            variations.add(base + year)
            variations.add(base + "!" + year)
            variations.add(base + "@" + year)

    return variations

def generate_password_list(usernames, year=None, include_extra=False, leet=False):
    """Generate a comprehensive password list."""
    all_passwords = set(COMMON_PASSWORDS)

    if year:
        for pwd in COMMON_PASSWORDS:
            all_passwords.add(pwd + year)

    if include_extra:
        all_passwords.update(EXTRA_COMMON_PASSWORDS)
        if year:
            for pwd in EXTRA_COMMON_PASSWORDS:
                all_passwords.add(pwd + year)

    for username in usernames:
        all_passwords.update(generate_username_variations(username, year))

    if leet:
        leet_passwords = set()
        for pwd in all_passwords:
            leet_passwords.update(generate_leet_variations(pwd))
        all_passwords.update(leet_passwords)

    return sorted(all_passwords)

def generate_passwords_from_mask(mask: str):
    """
    Generate passwords based on a hashcat-style mask.
    Example: ?u?l?l?l?l2022!
    """
    parts = []
    i = 0
    while i < len(mask):
        if mask[i] == '?' and i + 1 < len(mask):
            token = mask[i:i+2]
            if token in MASK_SETS:
                parts.append(MASK_SETS[token])
                i += 2
                continue
        parts.append(mask[i])
        i += 1

    return ("".join(p) for p in itertools.product(*parts))

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate smart password lists for password spraying and brute forcing.\n\n"
            "MODES:\n"
            "  1. Username-based mode: Use -i <file> to create variations from usernames.\n"
            "  2. Common passwords mode: Includes seasonal and lazy defaults automatically.\n"
            "  3. Extra breached passwords: Use --extra to add top 100 leaked passwords.\n"
            "  4. Leetspeak mode: Use --leet to generate l33t-style variants.\n"
            "  5. Mask mode: Use --mask '<pattern>' to create custom structured passwords.\n\n"
            "MASK TOKENS:\n"
            "  ?u = Uppercase letter  (A-Z)\n"
            "  ?l = Lowercase letter  (a-z)\n"
            "  ?d = Digit             (0-9)\n"
            "  ?s = Special character (!@#$%%^&*)\n"
            "\nExample: --mask '?u?l?l?l?l2022!' generates passwords like 'James2022!'."
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument("-i", "--input", help="File containing usernames (one per line).")
    parser.add_argument("-o", "--output", help="Output file for generated passwords.")
    parser.add_argument("-y", "--year", help="Optional year to append to variations (e.g. 2022).")
    parser.add_argument("--extra", action="store_true", help="Include top 100 breached passwords.")
    parser.add_argument("--leet", action="store_true", help="Generate leet-style variants.")
    parser.add_argument("--mask", help="Custom hashcat-style mask, e.g. '?u?l?l?l?l2022!'")

    args = parser.parse_args()

    passwords = set()

    if args.input:
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                usernames = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[!] Input file '{args.input}' not found.")
            return
        passwords.update(generate_password_list(usernames, args.year, args.extra, args.leet))

    if args.mask:
        passwords.update(generate_passwords_from_mask(args.mask))

    if not passwords:
        print("[!] No passwords generated. Provide either --input or --mask.")
        return

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            for pwd in sorted(passwords):
                f.write(pwd + "\n")
        print(f"[+] Generated {len(passwords)} passwords and saved to '{args.output}'")
    else:
        for pwd in sorted(passwords):
            print(pwd)

if __name__ == "__main__":
    main()

