# Username & Email Generator 🔐

A powerful Python tool for generating **realistic corporate-style usernames** and **email addresses** from a list of names.  
Built with **red teaming**, **password spraying**, and **O365/Azure AD enumeration** in mind.

---

## ✨ Features

- 🧩 **Multiple corporate-style username formats**
    - `jdoe`, `j.doe`, `janedoe`, `jane.doe`
- 📧 **Optional domain-aware email generation**
    - `jdoe@example.com`
    - `jane.doe@example.com`
- 🎭 **Leet-speak variants** (`--leet`)
    - `j4n3.d03`, `jdo3`, `d03j4n3`
- 🔍 **Verbose mode** (`--verbose`)  
    - See exactly what’s generated per user
- 🚀 **Red-team friendly**
    - Perfect for **password spraying** and **username enumeration**
- 🧹 **Automatic deduplication**
    - Never worry about duplicate usernames or emails

---

## 📦 Installation

Clone the repository and make the script executable:

```bash
git clone https://github.com/<your-username>/username-generator.git
cd username-generator
chmod +x generate_usernames.py
```

📄 Usage
python3 generate_usernames.py <input_file> [options]

Arguments
Flag	Description	Default
input	Path to input file containing names (First Last)	Required
-o	Output file for usernames/emails	usernames.lst
--leet	Enable leet-speak variants	Disabled
--domain	Generate domain-aware emails (e.g. --domain example.com)	None
--verbose	Show detailed debug info while generating usernames	Disabled


🧑‍💻 Examples
1. Basic Username Generation
python3 generate_usernames.py names.txt


Input (names.txt):

Jane Doe
John Smith


Output (usernames.lst):

jdoe
j.doe
janedoe
jane.doe
janed
doej
smithj
...


2. Domain-Aware Email Generation
python3 generate_usernames.py names.txt --domain corp.local


Output (usernames.lst):

jdoe
jane.doe
jdoe@corp.local
jane.doe@corp.local
j.doe@corp.local
...

3. Enable Leet-Speak Variants
python3 generate_usernames.py names.txt --leet


Output (usernames.lst):

jdoe
j4n3.d03
jan3d03
j.d03
d03j4n3
...

4. Combine Emails + Leet + Verbose
python3 generate_usernames.py names.txt --leet --domain example.com --verbose


Console Output:

[+] Jane Doe -> 12 usernames
    ↳ Added 10 email variants for Jane Doe
[+] John Smith -> 12 usernames
    ↳ Added 10 email variants for John Smith
[+] Processed 2/2 lines
[+] Generated 44 unique usernames in 'usernames.lst'

