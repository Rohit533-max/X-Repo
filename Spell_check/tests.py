"""
tests.py — Test Suite for the Spell Checker

Run with:  python tests.py

Tests cover:
  - Hash Table operations (insert, search, delete, collision, rehash)
  - Bloom Filter (add, might_contain, false positive estimation)
  - Spell Checker (is_correct, suggest, check_text).
"""

import sys


def run_test(name: str, func):
    try:
        func()
        print(f"  \033[92m✓ PASS\033[0m  {name}")
        return True
    except AssertionError as e:
        print(f"  \033[91m✗ FAIL\033[0m  {name}: {e}")
        return False
    except Exception as e:
        print(f"  \033[91m✗ ERROR\033[0m {name}: {e}")
        return False


# ─────────────────── HASH TABLE TESTS ─────────────────── #

def test_hash_table():
    from hash_table import HashTable

    results = []

    def test_insert_search():
        ht = HashTable()
        ht.insert("hello")
        assert ht.search("hello") is not None, "Should find 'hello'"
        assert ht.search("world") is None, "Should not find 'world'"

    def test_contains():
        ht = HashTable()
        ht.insert("python")
        assert "python" in ht, "Should contain 'python'"
        assert "java" not in ht, "Should not contain 'java'"

    def test_delete():
        ht = HashTable()
        ht.insert("delete_me")
        assert ht.search("delete_me") is not None
        ht.delete("delete_me")
        assert ht.search("delete_me") is None, "Should be deleted"

    def test_collision_handling():
        ht = HashTable()
        # Insert many words — collisions will happen
        words = ["apple", "application", "apply", "apt", "apricot",
                 "ape", "apex", "apart", "appear", "appeal"]
        for w in words:
            ht.insert(w)
        for w in words:
            assert w in ht, f"'{w}' should be in table after collision"

    def test_load_factor():
        ht = HashTable()
        assert ht.load_factor() == 0.0, "Empty table load factor should be 0"

    def test_rehash():
        ht = HashTable()
        # Insert enough words to trigger at least one rehash
        import string
        words = [f"word{i}" for i in range(50)]
        for w in words:
            ht.insert(w)
        for w in words:
            assert w in ht, f"'{w}' should survive rehashing"
        assert ht.rehash_count >= 1, "Should have rehashed at least once"

    def test_update_existing():
        ht = HashTable()
        ht.insert("key", "value1")
        ht.insert("key", "value2")
        assert ht.search("key") == "value2", "Should update existing key"

    def test_len():
        ht = HashTable()
        for w in ["a", "b", "c", "d"]:
            ht.insert(w)
        assert len(ht) == 4

    print("\n\033[1mHash Table Tests:\033[0m")
    for name, fn in [
        ("Insert and Search", test_insert_search),
        ("__contains__ operator", test_contains),
        ("Delete", test_delete),
        ("Collision Handling (Chaining)", test_collision_handling),
        ("Load Factor Calculation", test_load_factor),
        ("Dynamic Rehashing", test_rehash),
        ("Update Existing Key", test_update_existing),
        ("__len__", test_len),
    ]:
        results.append(run_test(name, fn))
    return results


# ─────────────────── BLOOM FILTER TESTS ─────────────────── #

def test_bloom_filter():
    from bloom_filter import BloomFilter
    results = []

    def test_add_and_check():
        bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
        bf.add("hello")
        assert bf.might_contain("hello"), "'hello' should be found after add"

    def test_definite_negative():
        bf = BloomFilter(expected_items=1000)
        words = ["cat", "dog", "fish"]
        for w in words:
            bf.add(w)
        # A word never added should not be in the filter with high probability
        # (there's a tiny false positive chance, but with few items it's very low)
        assert not bf.might_contain("xyzzy123"), "Very unlikely word should not be found"

    def test_no_false_negatives():
        bf = BloomFilter(expected_items=1000)
        test_words = [f"word_{i}" for i in range(200)]
        for w in test_words:
            bf.add(w)
        for w in test_words:
            assert bf.might_contain(w), f"'{w}' should never give false negative"

    def test_stats():
        bf = BloomFilter(expected_items=1000, false_positive_rate=0.01)
        stats = bf.get_stats()
        assert "bit_array_size" in stats
        assert "hash_functions_k" in stats
        assert stats["hash_functions_k"] >= 1

    print("\n\033[1mBloom Filter Tests:\033[0m")
    for name, fn in [
        ("Add and might_contain", test_add_and_check),
        ("Definite negative (word never added)", test_definite_negative),
        ("No false negatives guarantee", test_no_false_negatives),
        ("Stats dictionary", test_stats),
    ]:
        results.append(run_test(name, fn))
    return results


# ─────────────────── SPELL CHECKER TESTS ─────────────────── #

def test_spell_checker():
    from spell_checker import SpellChecker
    results = []
    checker = SpellChecker()

    def test_correct_word():
        assert checker.is_correct("hello"), "'hello' should be correct"
        assert checker.is_correct("the"), "'the' should be correct"

    def test_wrong_word():
        assert not checker.is_correct("helo"), "'helo' should be wrong"
        assert not checker.is_correct("xyzzy"), "'xyzzy' should be wrong"

    def test_case_insensitive():
        assert checker.is_correct("Hello"), "Should handle uppercase"
        assert checker.is_correct("THE"), "Should handle all caps"

    def test_suggestions():
        sugg = checker.suggest("helo")
        assert len(sugg) > 0, "Should have suggestions for 'helo'"
        assert "hello" in sugg, "'hello' should be suggested for 'helo'"

    def test_add_custom_word():
        checker.add_word("pythonista")
        assert checker.is_correct("pythonista"), "Custom word should be found"

    def test_check_text():
        text = "I hav a problem with speling"
        result = checker.check_text(text)
        assert result["total_words"] == 6
        assert "speling" in result["misspelled"] or "hav" in result["misspelled"]

    def test_empty_string():
        assert checker.is_correct(""), "Empty string should be 'correct'"

    print("\n\033[1mSpell Checker Tests:\033[0m")
    for name, fn in [
        ("Correct word detection", test_correct_word),
        ("Misspelled word detection", test_wrong_word),
        ("Case insensitivity", test_case_insensitive),
        ("Suggestion generation", test_suggestions),
        ("Add custom word", test_add_custom_word),
        ("check_text method", test_check_text),
        ("Empty string edge case", test_empty_string),
    ]:
        results.append(run_test(name, fn))
    return results


# ─────────────────── MAIN ─────────────────── #

if __name__ == "__main__":
    print("\033[1m\033[96m" + "=" * 50)
    print("     SPELL CHECKER TEST SUITE")
    print("=" * 50 + "\033[0m")

    all_results = []
    all_results.extend(test_hash_table())
    all_results.extend(test_bloom_filter())
    all_results.extend(test_spell_checker())

    passed = sum(all_results)
    total = len(all_results)

    print(f"\n\033[1m{'=' * 50}")
    if passed == total:
        print(f"\033[92m  ALL {total} TESTS PASSED! ✓\033[0m")
    else:
        print(f"\033[91m  {passed}/{total} tests passed\033[0m")
    print("=" * 50 + "\033[0m\n")

    sys.exit(0 if passed == total else 1)
