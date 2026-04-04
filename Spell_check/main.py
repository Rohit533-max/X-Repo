"""
main.py — Command-Line Spell Checker

Run this file to use the spell checker interactively.
Usage:
    python main.py
    python main.py --file myessay.txt
    python main.py --demo
    python main.py --stats.
"""

import sys
import argparse
import os
from spell_checker import SpellChecker


# ─────────────────────────────── COLORS ──────────────────────────────── #
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def banner():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════╗
║       🔍  HASH-POWERED SPELL CHECKER  🔍          ║
║   Hash Tables • Bloom Filters • Edit Distance     ║
╚══════════════════════════════════════════════════╝{RESET}
""")

def print_section(title: str):
    print(f"\n{BLUE}{BOLD}━━━━━ {title} ━━━━━{RESET}")


# ─────────────────────────────── MODES ───────────────────────────────── #

def interactive_mode(checker: SpellChecker):
    """Word-by-word interactive mode."""
    print_section("INTERACTIVE MODE")
    print("Type a word to check it. Commands: :quit, :stats, :add <word>")
    print()
    while True:
        try:
            user_input = input(f"{BOLD}Enter word: {RESET}").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input == ":quit":
            break
        if user_input == ":stats":
            show_stats(checker)
            continue
        if user_input.startswith(":add "):
            word = user_input[5:].strip()
            checker.add_word(word)
            print(f"  {GREEN}✓ Added '{word}' to dictionary{RESET}")
            continue

        if checker.is_correct(user_input):
            print(f"  {GREEN}✓ '{user_input}' — Correctly spelled{RESET}")
        else:
            suggestions = checker.suggest(user_input)
            print(f"  {RED}✗ '{user_input}' — Misspelled!{RESET}")
            if suggestions:
                print(f"  {YELLOW}Suggestions: {', '.join(suggestions)}{RESET}")
            else:
                print(f"  {YELLOW}No suggestions found.{RESET}")


def text_mode(checker: SpellChecker):
    """Check a full paragraph of text."""
    print_section("TEXT CHECK MODE")
    print("Paste your text below. Press Enter twice when done.\n")
    lines = []
    try:
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
    except (EOFError, KeyboardInterrupt):
        pass

    text = "\n".join(lines)
    if not text.strip():
        print("No text entered.")
        return

    results = checker.check_text(text)
    print(f"\n{BOLD}Results:{RESET}")
    print(f"  Total words : {results['total_words']}")
    print(f"  {GREEN}Correct     : {len(results['correct'])}{RESET}")
    print(f"  {RED}Misspelled  : {len(results['misspelled'])}{RESET}")
    print(f"  Accuracy    : {results['accuracy']}%\n")

    if results["misspelled"]:
        print(f"{BOLD}Misspelled words & suggestions:{RESET}")
        for word, suggestions in results["misspelled_with_suggestions"].items():
            sugg = ", ".join(suggestions) if suggestions else "none"
            print(f"  {RED}✗ {word:<20}{RESET}→ {YELLOW}{sugg}{RESET}")


def file_mode(checker: SpellChecker, filepath: str):
    """Check spelling in a text file."""
    if not os.path.exists(filepath):
        print(f"{RED}Error: File '{filepath}' not found.{RESET}")
        return
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    print(f"\nChecking file: {BOLD}{filepath}{RESET}")
    results = checker.check_text(text)
    print(f"\n{BOLD}Results:{RESET}")
    print(f"  Total words : {results['total_words']}")
    print(f"  {GREEN}Correct     : {len(results['correct'])}{RESET}")
    print(f"  {RED}Misspelled  : {len(results['misspelled'])}{RESET}")
    print(f"  Accuracy    : {results['accuracy']}%\n")
    if results["misspelled"]:
        print(f"{BOLD}Misspelled words:{RESET}")
        for word, suggestions in results["misspelled_with_suggestions"].items():
            sugg = ", ".join(suggestions) if suggestions else "none"
            print(f"  {RED}✗ {word:<20}{RESET}→ {YELLOW}{sugg}{RESET}")


def demo_mode(checker: SpellChecker):
    """Demonstrate all hashing concepts with examples."""
    print_section("DEMO: HASH TABLE INTERNALS")
    test_words = ["hello", "world", "python", "hashing"]
    for w in test_words:
        idx = checker.dictionary._hash(w)
        print(f"  hash('{w}') = {idx}  →  bucket [{idx}]")

    print_section("DEMO: COLLISION DETECTION")
    print(f"  Collisions encountered during load: {checker.dictionary.collision_count}")
    print(f"  Rehash count (dynamic resizing):   {checker.dictionary.rehash_count}")
    print(f"  Current load factor:               {checker.dictionary.load_factor():.3f}")

    print_section("DEMO: BLOOM FILTER")
    bloom_stats = checker.bloom.get_stats()
    print(f"  Bit array size : {bloom_stats['bit_array_size']:,} bits = {bloom_stats['memory_bytes']:,} bytes")
    print(f"  Hash functions : {bloom_stats['hash_functions_k']}")
    print(f"  Fill ratio     : {bloom_stats['fill_ratio']:.1%}")

    test_cases = [("hello", True), ("pythn", False), ("speling", False), ("correct", True)]
    print(f"\n  {'Word':<15} {'Bloom says':<15} {'Hash Table says':<15} {'Result'}")
    print(f"  {'-'*60}")
    for word, _ in test_cases:
        bloom_ans = checker.bloom.might_contain(word)
        ht_ans = checker.dictionary.search(word) is not None
        result = GREEN + "✓ Correct" + RESET if ht_ans else RED + "✗ Wrong" + RESET
        print(f"  {word:<15} {'MAYBE' if bloom_ans else 'NO':<15} {'YES' if ht_ans else 'NO':<15} {result}")

    print_section("DEMO: SPELL SUGGESTIONS (Edit Distance)")
    misspelled = ["speling", "recieve", "freind", "langauge"]
    for word in misspelled:
        suggestions = checker.suggest(word)
        print(f"  '{word}' → {', '.join(suggestions) if suggestions else 'no suggestions'}")


def show_stats(checker: SpellChecker):
    """Display hash table and bloom filter statistics."""
    stats = checker.get_stats()
    ht = stats["hash_table"]
    bf = stats["bloom_filter"]

    print_section("HASH TABLE STATS")
    print(f"  Words stored    : {ht['size']:,}")
    print(f"  Buckets (slots) : {ht['capacity']}")
    print(f"  Load factor     : {ht['load_factor']} (ideal: 0.5–0.7)")
    print(f"  Total collisions: {ht['collisions_total']}")
    print(f"  Times rehashed  : {ht['rehash_count']}")
    print(f"  Max chain length: {ht['max_chain_length']}")
    print(f"  Empty buckets   : {ht['empty_buckets']}")

    print_section("BLOOM FILTER STATS")
    print(f"  Bit array size  : {bf['bit_array_size']:,} bits")
    print(f"  Memory used     : {bf['memory_bytes']:,} bytes")
    print(f"  Hash functions  : {bf['hash_functions_k']}")
    print(f"  Bits set to 1   : {bf['bits_set']:,}")
    print(f"  Fill ratio      : {bf['fill_ratio']:.1%}")
    print(f"  Est. FP rate    : {bf['est_false_positive_rate']:.5f}")


# ─────────────────────────────── MAIN ────────────────────────────────── #

def main():
    parser = argparse.ArgumentParser(
        description="Hash-Powered Spell Checker — Learn Hashing by Doing"
    )
    parser.add_argument("--file",  metavar="PATH", help="Check spelling in a text file")
    parser.add_argument("--demo",  action="store_true", help="Run concept demos")
    parser.add_argument("--stats", action="store_true", help="Show internal stats")
    parser.add_argument("--text",  action="store_true", help="Check a paragraph of text")
    parser.add_argument("--words", metavar="PATH", help="Load custom word list file")
    args = parser.parse_args()

    banner()
    print(f"Loading dictionary...", end=" ", flush=True)
    checker = SpellChecker()
    print(f"{GREEN}Done! ({len(checker.dictionary):,} words){RESET}")

    if args.words:
        n = checker.load_from_file(args.words)
        print(f"  Loaded {n} words from '{args.words}'")

    if args.demo:
        demo_mode(checker)
    elif args.stats:
        show_stats(checker)
    elif args.file:
        file_mode(checker, args.file)
    elif args.text:
        text_mode(checker)
    else:
        # Default: interactive word-by-word mode
        print("\nNo mode specified — entering interactive mode.")
        print("Try:  python main.py --demo   |   python main.py --text   |   python main.py --stats\n")
        interactive_mode(checker)


if __name__ == "__main__":
    main()
