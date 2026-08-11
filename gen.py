# Usage: python3 gen.py <team_name.txt> <contest_id> <random_contest_token>
# <team_name.txt>: A text file, filled with team names, one name per line, where empty lines are filled with placeholder names. Must not contain duplicate names.
# <contest_id>: some digits (for example, 691856) which indicates the CF contest id (after creating mashup, it's available in the URL. For example, https://codeforces.com/gym/691856)
# <random_contest_token>: the seed that the RNG will use to generate random passwords. This seed must obviously be secret and be unique used for the contest.
# Running this program will write a list of domain users that can be copy-pasted to codeforces group (in the right Member management tab - click Domain users)


use_alphabet = False # If true, use A, B, ... instead of items
placeholder_items = [
    "Assembly",
    "Bash",
    "Basic",
    "C",
    "CPlusPlus",
    "CSharp",
    "Curl",
    "Fortran",
    "GDScript",
    "Go",
    "Haskell",
    "Java",
    "JavaScript",
    "Lisp",
    "Lua",
    "MATLAB",
    "OCaml",
    "Pascal",
    "Rust",
    "Smalltalk",
    "Swift",
]

import hashlib
import sys

def make_domain_user(team_name: str) -> str:
    username = team_name.strip().lower()
    while " " in username:
        username = username.replace(" ", "_")
    while "__" in username:
        username = username.replace("__", "_")
    username = username.strip("_")
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890_"
    is_all_good_ch = True
    filtered_name = ""
    for ch in username:
        if ch not in alphabet:
            is_all_good_ch = False
        else:
            filtered_name += ch
    while len(filtered_name) >= 1 and filtered_name[0] == '_':
        filtered_name = filtered_name[1:]
    while len(filtered_name) >= 1 and filtered_name[-1] == '_':
        filtered_name = filtered_name[:-1]
    while "__" in filtered_name:
        filtered_name = filtered_name.replace("__", "_")
    if len(filtered_name) >= 1:
        if is_all_good_ch and len(filtered_name) <= 5:
            return f"team_{filtered_name}"
        if is_all_good_ch and len(filtered_name) <= 30:
            return filtered_name
        if is_all_good_ch and len(filtered_name) > 30:
            # find first _ after 25 and cut off, or cut off at 38
            first_space = -1
            for i in range(25, len(filtered_name)):
                if filtered_name[i] == '_':
                    first_space = i
                    break
            if first_space == -1 or first_space > 38:
                return filtered_name[:38]
            else:
                return filtered_name[:first_space]
    print(f"Problematic team names: {team_name} to {filtered_name}", file=sys.stderr)
    if len(filtered_name) <= 5:
        return f"team_{filtered_name}"
    if len(filtered_name) <= 30:
        return filtered_name
    # find first _ after 25 and cut off, or cut off at 38
    first_space = -1
    for i in range(25, len(filtered_name)):
        if filtered_name[i] == '_':
            first_space = i
            break
    if first_space == -1 or first_space > 38:
        return filtered_name[:38]
    else:
        return filtered_name[:first_space]

def make_placeholder_name(index: int) -> str:
    if use_alphabet:
        alphabet = "abcdefghijkmnpqrstuvwxyz"
        alphabet = alphabet.upper()
        base_alpha = []
        if index == 0:
            base_alpha = [0]
        else:
            while index > 0:
                base_alpha.append(index % 26)
                index //= 26
        base_alpha = base_alpha[::-1]
        team_letters = "".join([alphabet[id] for id in base_alpha])
        return f"Team {team_letters}"
    else:
        assert(index < len(placeholder_items))
        return f"Team {placeholder_items[index]}"

def make_password(token: str, team_name: str) -> str:
    data = f"{token}\0{team_name}".encode("utf-8")
    digest = hashlib.sha256(data).digest()
    alphabet = "ABCDEFGHJKLMNPQRSTWXYZabcdefghijkmnpqrstwxyz123456789"
    password = ""
    for digit in range(8):
        block = hashlib.sha256(digest + digit.to_bytes(4, "big")).digest()
        for byte in block:
            password += alphabet[byte % len(alphabet)]
            break
    return password

def main() -> None:
    if len(sys.argv) != 4:
        print(
            "Usage: python3 gen.py "
            "<team_name.txt> <contest_id> <random_contest_token>",
            file=sys.stderr,
        )
        sys.exit(1)
    team_file = sys.argv[1]
    contest_id = sys.argv[2]
    token = sys.argv[3]
    try:
        with open(team_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as e:
        print(f"Error reading {team_file}: {e}", file=sys.stderr)
        sys.exit(1)
    processed_team_names = []
    placeholder_count = 0
    for line in lines:
        original_name = line.rstrip("\r\n")
        team_name = original_name.strip()
        if not team_name:
            team_name = make_placeholder_name(placeholder_count)
            placeholder_count += 1
        processed_team_names.append(team_name)
    if len(processed_team_names) > len(set(processed_team_names)):
        print("Team names are not unique!", file=sys.stderr)
        found_duplicate = False
        for i in range(len(processed_team_names)):
            for j in range(i):
                if processed_team_names[j] == processed_team_names[i]:
                    print(f"Duplicated: {processed_team_names[i]}", file=sys.stderr)
                    found_duplicate = True
                    break
            if found_duplicate:
                break
        sys.exit(1)
    processed_usernames = []
    for team_name in processed_team_names:
        username = make_domain_user(team_name)
        processed_usernames.append(username)
    if len(processed_usernames) > len(set(processed_usernames)):
        print("User names are not unique!", file=sys.stderr)
        found_duplicate = False
        for i in range(len(processed_usernames)):
            for j in range(i):
                if processed_usernames[j] == processed_usernames[i]:
                    print(f"Duplicated: {processed_usernames[i]}", file=sys.stderr)
                    found_duplicate = True
                    break
            if found_duplicate:
                break
        sys.exit(1)
    for (id, team_name) in enumerate(processed_team_names):
        username = processed_usernames[id]
        password = make_password(token, team_name)
        print(f"{contest_id} | {username} | {password} | {team_name}")

if __name__ == "__main__":
    main()