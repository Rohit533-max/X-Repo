"""
spell_checker.py — Main Spell Checker Engine

HASHING CONCEPTS USED HERE:
  1. Hash Table  → Fast O(1) dictionary lookups
  2. Bloom Filter → Space-efficient pre-filtering
  3. Hashing for suggestions → Edit distance with hashing

This is the brain that connects everything together.
"""

import re
import os
from hash_table import HashTable
from bloom_filter import BloomFilter


# ------------------------------------------------------------------ #
#  BUILT-IN WORD LIST (so the project works with no external files)   #
# ------------------------------------------------------------------ #
BUILTIN_WORDS = """
hello world spell check spelling checker correct incorrect suggest
suggestion dictionary word words text paragraph sentence error errors
python programming language code function method class variable type
a able about above accept accident account achieve across act action
active actually add address advance after again age ago agree air all
allow almost alone along already also always among amount and another
answer any anything appear apply approach area around ask attack available
away back bad balance ball basic become before begin behind believe best
better between big both break bring build business but call can care carry
catch cause change character check child choice choose class clear close
come common complete condition consider continue control copy correct cost
could country create culture current cut dark deal decide deep define
describe design develop difference different difficult direction discover
discuss distance do does down drive during each early easy economic effect
eight either else empty end energy enjoy enough enter environment equal
establish even every examine example exist experience explain face fact fall
family far fast feel few figure finally find five for force foreign form
forward found four free from front full future game general get give go
good government great ground group grow half hand happen hard have hear
heart heavy help high him his history hold home hope hour human hundred
idea imagine important include increase indicate individual information
inside instead interest into its just keep kind know land language large
last late lead learn less letter life light like list little live local long
look lose main make man matter mean meet method might mind model modern more
morning most move much must need never new next night nor note nothing notice
now number occur office only open order other out own page part past pay
people perhaps person place plan play point political poor position power
practice present problem produce program provide pull push put raise reach
real reason receive recent remain report require result return right rise
role run school science second seem send sense serve several short show
simple since situation size slow small social society some sort sound space
speak special specific stand start state stay step study subject such suggest
sure take talk ten than that the their them there they thing think though
three through time today together too top toward town trade traditional
true turn two type under understand until upon use usually value very view
visit voice want war was water way we well what where which while who will
with within without work world write year yes yet you young your
the quick brown fox jumps over lazy dog
able about above accord account accurate achieve across add address
admit adult advance affect afford afford after agenda agree ahead aim
airport also although always among analyze animal annual another answer
any apart appear approach area argue around arrange arrive article
artist ask aspect assess assist assume assure attach attend attitude
attract authority available avoid aware away background balance base
basis become before begin behavior benefit better beyond big bill both
break budget build but buy calculate call calm campaign can capable
care carry case cause certain change charge check choice choose claim
clear client close coach collect color comfort comment commit common
compare complete concern condition confirm conflict connect consider
contact contain content contribute control core correct cost create
crisis critical culture daily data deal decide decision define demand
depend design despite detail develop difference difficult direct discuss
distribute divide document down draw drive early ease education effort
eight either else emotion enable encourage engage ensure entire equal
error establish evaluate every evidence examine explain explore fall
family feature feel find focus follow force forward free full function
future goal government grow guide handle health help human impact improve
include increase indicate individual install instead integrate involve
issue keep knowledge late lead learn level likely limit listen live local
maintain manage market measure meet method mind model monitor need
network offer open operate option order organize other outcome own
outside perform personal plan position practice prepare present problem
process produce program project provide quality question raise reach
reason reduce relate rely require respond result review role run safe
scale secure serve several show simple since small social solve some
specific standard start state step stop strategy structure study
subject support system take task team test time together track train
understand user value vision work write
""".split()

# Deduplicate
BUILTIN_WORDS = list(set(w.strip().lower() for w in BUILTIN_WORDS if w.strip()))


# ------------------------------------------------------------------ #
#  SPELL CHECKER CLASS                                                #
# ------------------------------------------------------------------ #
class SpellChecker:
    """
    A spell checker powered by:
      - Custom Hash Table (dictionary storage)
      - Bloom Filter (fast pre-check)
      - Edit distance (suggestion generation)
    """

    def __init__(self):
        self.dictionary = HashTable()       # Primary storage: O(1) lookup
        self.bloom = BloomFilter(           # Probabilistic pre-filter
            expected_items=200_000,
            false_positive_rate=0.001
        )
        self.word_count = 0
        self._load_builtin_words()

    def _load_builtin_words(self):
        """Load the built-in word list."""
        for word in BUILTIN_WORDS:
            self.add_word(word)

    def load_from_file(self, filepath: str) -> int:
        """
        Load a word list file (one word per line, or space/newline separated).
        Returns number of words added.
        """
        if not os.path.exists(filepath):
            return 0
        count = 0
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                for word in line.strip().split():
                    clean = re.sub(r"[^a-z']", '', word.lower())
                    if clean:
                        self.add_word(clean)
                        count += 1
        return count

    def add_word(self, word: str):
        """
        Add a word to both the hash table AND the bloom filter.
        Both structures are updated for consistency.
        """
        word = word.lower().strip()
        if word:
            self.dictionary.insert(word)
            self.bloom.add(word)
            self.word_count += 1

    # ------------------------------------------------------------------ #
    #  SPELL CHECK — TWO-STAGE LOOKUP                                     #
    # ------------------------------------------------------------------ #
    def is_correct(self, word: str) -> bool:
        """
        Check if a word is spelled correctly.

        TWO-STAGE LOOKUP:
          Stage 1: Bloom Filter check (very fast, bit operations)
                   → If says NO → definitely misspelled (skip Stage 2)
                   → If says MAYBE → go to Stage 2

          Stage 2: Hash Table lookup (O(1) average)
                   → Definitive answer

        This two-stage approach is used in real-world systems.
        (e.g., Google Chrome's spell checker).
        """
        word = word.lower().strip()
        if not word:
            return True

        # Stage 1: Bloom filter pre-check
        if not self.bloom.might_contain(word):
            return False  # Definitely wrong — skip hash table entirely

        # Stage 2: Authoritative hash table lookup
        return self.dictionary.search(word) is not None

    def check_text(self, text: str) -> dict:
        """
        Check all words in a block of text.
        Returns a report with correct/incorrect words and their positions.
        """
        words = re.findall(r"[a-zA-Z']+", text)
        results = {
            "total_words": len(words),
            "correct": [],
            "misspelled": [],
            "misspelled_with_suggestions": {}
        }

        for word in words:
            clean = word.lower().strip("'")
            if self.is_correct(clean):
                results["correct"].append(word)
            else:
                results["misspelled"].append(word)
                results["misspelled_with_suggestions"][word] = self.suggest(clean)

        results["accuracy"] = (
            round(len(results["correct"]) / len(words) * 100, 1)
            if words else 100.0
        )
        return results

    # ------------------------------------------------------------------ #
    #  SUGGESTION ENGINE — EDIT DISTANCE + HASHING                       #
    # ------------------------------------------------------------------ #
    def suggest(self, word: str, max_suggestions: int = 5) -> list:
        """
        Generate spelling suggestions using edit operations.

        EDIT OPERATIONS (each creates a candidate):
          1. Deletion   — remove one character: "helo" → "hel", "heo", "elo", ...
          2. Transposition — swap adjacent chars: "helo" → "ehlo", "hleo", ...
          3. Replacement — replace one char: "helo" → "aelo", "belo", ...
          4. Insertion  — add one char: "helo" → "ahelo", "bhelo", ...

        Each candidate is looked up in the hash table (O(1) per lookup).
        This is Levenshtein distance-1 suggestion generation.

        HASHING CONNECTION:
          We generate ~54n candidates (where n = word length).
          Without hashing, checking each against the full dictionary
          would be O(n * dict_size). With hashing → O(n * 1) = O(n).
        """
        word = word.lower()
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        candidates = set()

        # Use a set (internally a hash set!) to avoid duplicate candidates
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]

        # 1. Deletions
        for L, R in splits:
            if R:
                candidates.add(L + R[1:])

        # 2. Transpositions
        for L, R in splits:
            if len(R) > 1:
                candidates.add(L + R[1] + R[0] + R[2:])

        # 3. Replacements
        for L, R in splits:
            if R:
                for c in alphabet:
                    candidates.add(L + c + R[1:])

        # 4. Insertions
        for L, R in splits:
            for c in alphabet:
                candidates.add(L + c + R)

        # Filter candidates: only keep real words (hash table lookups)
        suggestions = [c for c in candidates if self.is_correct(c)]

        # Sort by how similar they are to the original
        suggestions.sort(key=lambda s: self._edit_distance(word, s))
        return suggestions[:max_suggestions]

    @staticmethod
    def _edit_distance(s1: str, s2: str) -> int:
        """
        Classic dynamic programming edit distance (Levenshtein).
        Used to rank suggestions by similarity.
        O(m*n) time, O(m*n) space.
        """
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1): dp[i][0] = i
        for j in range(n + 1): dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        return dp[m][n]

    # ------------------------------------------------------------------ #
    #  STATS                                                              #
    # ------------------------------------------------------------------ #
    def get_stats(self) -> dict:
        return {
            "hash_table": self.dictionary.get_stats(),
            "bloom_filter": self.bloom.get_stats(),
            "words_in_dictionary": len(self.dictionary),
        }
