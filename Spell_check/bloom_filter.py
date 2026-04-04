"""
bloom_filter.py — Probabilistic Hashing with Bloom Filters

HASHING CONCEPT:
  A Bloom Filter uses MULTIPLE hash functions to test set membership.
  It can tell you:
    - "Definitely NOT in the dictionary" (100% accurate)
    - "PROBABLY in the dictionary" (small chance of false positive)

  It NEVER gives false negatives.
  Space-efficient: stores bits, not actual words.

Use case in spell checker:
  Fast pre-check before doing full dictionary lookup.
  If Bloom Filter says NO → skip the expensive lookup entirely.
"""

import math


class BloomFilter:
    """
    Bloom Filter using k independent hash functions.

    Internal structure:
      - self.bit_array: A list of 0s and 1s (the bit vector)
      - self.size:      Number of bits
      - self.k:         Number of hash functions

    INSERT: Set bits at all k hash positions to 1
    SEARCH: Check if ALL k positions are 1
            → If any is 0, the element is DEFINITELY NOT present
            → If all are 1, it is PROBABLY present
    """

    def __init__(self, expected_items: int = 100_000, false_positive_rate: float = 0.01):
        """
        Automatically calculate optimal size and number of hash functions.

        Formulas (from probability theory):
          m = -(n * ln(p)) / (ln(2)^2)
          k = (m / n) * ln(2)

        Where:
          n = expected number of items
          p = desired false positive rate
          m = number of bits
          k = number of hash functions
        """
        self.expected_items = expected_items
        self.false_positive_rate = false_positive_rate

        # Optimal bit array size
        self.size = self._optimal_size(expected_items, false_positive_rate)
        # Optimal number of hash functions
        self.k = self._optimal_k(self.size, expected_items)

        self.bit_array = [0] * self.size
        self.items_added = 0

    @staticmethod
    def _optimal_size(n: int, p: float) -> int:
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @staticmethod
    def _optimal_k(m: int, n: int) -> int:
        k = (m / n) * math.log(2)
        return max(1, int(k))

    # ------------------------------------------------------------------ #
    #  MULTIPLE HASH FUNCTIONS via seeding                                #
    # ------------------------------------------------------------------ #
    def _hashes(self, item: str):
        """
        Generate k different hash values for one item.

        Technique: Use two base hash functions (h1, h2) and combine them:
            hash_i(x) = (h1(x) + i * h2(x)) mod m

        This is called "double hashing" and gives k independent functions
        without writing k separate functions.
        """
        # Base hash 1 — FNV-1a variant
        h1 = 0
        FNV_PRIME = 16777619
        FNV_OFFSET = 2166136261
        for char in item:
            h1 ^= ord(char)
            h1 = (h1 * FNV_PRIME) & 0xFFFFFFFF

        # Base hash 2 — djb2 variant
        h2 = 5381
        for char in item:
            h2 = ((h2 << 5) + h2) + ord(char)
        h2 = h2 & 0xFFFFFFFF

        # Generate k hashes using double-hashing formula
        for i in range(self.k):
            yield (h1 + i * h2) % self.size

    # ------------------------------------------------------------------ #
    #  INSERT                                                              #
    # ------------------------------------------------------------------ #
    def add(self, item: str):
        """Set all k bit positions to 1."""
        for index in self._hashes(item):
            self.bit_array[index] = 1
        self.items_added += 1

    # ------------------------------------------------------------------ #
    #  SEARCH                                                              #
    # ------------------------------------------------------------------ #
    def might_contain(self, item: str) -> bool:
        """
        Returns True if item MIGHT be in the set.
        Returns False if item is DEFINITELY NOT in the set.
        """
        return all(self.bit_array[index] == 1 for index in self._hashes(item))

    def estimated_false_positive_rate(self) -> float:
        """
        Estimate the current false positive rate based on how full the filter is.
        """
        if self.items_added == 0:
            return 0.0
        bits_set = sum(self.bit_array)
        ratio = bits_set / self.size
        return (1 - math.exp(-self.k * self.items_added / self.size)) ** self.k

    def get_stats(self) -> dict:
        bits_set = sum(self.bit_array)
        return {
            "bit_array_size": self.size,
            "hash_functions_k": self.k,
            "bits_set": bits_set,
            "fill_ratio": round(bits_set / self.size, 3),
            "items_added": self.items_added,
            "est_false_positive_rate": round(self.estimated_false_positive_rate(), 5),
            "memory_bytes": self.size // 8,
        }

    def __repr__(self):
        return (f"BloomFilter(size={self.size} bits, k={self.k} hashes, "
                f"items={self.items_added}, fp≈{self.false_positive_rate})")
