"""
hash_table.py — Custom Hash Table built from scratch

HASHING CONCEPTS COVERED:
  1. Hash Functions
  2. Collision Handling (Chaining)
  3. Load Factor & Rehashing
  4. Dynamic Resizing
  5. Key-Value Storage
"""


class Node:
    """A single node in the linked list (used for chaining)."""
    def __init__(self, key, value=True):
        self.key = key
        self.value = value
        self.next = None  # Pointer to the next node (for collision chaining)


class HashTable:
    """
    A hash table that uses SEPARATE CHAINING to resolve collisions.

    Internal structure:
      - self.buckets: A fixed-size list of "slots" (each slot is a linked list head)
      - self.size:    Current number of key-value pairs stored
      - self.capacity:Current number of buckets/slots

    LOAD FACTOR = size / capacity
      - When load factor > 0.7, we REHASH (double the capacity)
      - This keeps operations O(1) average time
    """

    INITIAL_CAPACITY = 8   # Start small so you can see rehashing happen
    LOAD_FACTOR_LIMIT = 0.7

    def __init__(self):
        self.capacity = self.INITIAL_CAPACITY
        self.size = 0
        self.buckets = [None] * self.capacity   # Array of linked-list heads
        self.collision_count = 0                # Track collisions for learning
        self.rehash_count = 0                   # Track how many times we rehashed

    # ------------------------------------------------------------------ #
    #  HASH FUNCTION — THE HEART OF HASHING                               #
    # ------------------------------------------------------------------ #
    def _hash(self, key: str) -> int:
        """
        Polynomial Rolling Hash Function.

        Formula:
            hash = sum( char_code[i] * PRIME^i ) mod capacity

        Why a prime number (31)?
          - Primes distribute values more uniformly across buckets
          - Reduces clustering (many keys landing in same bucket)

        Why mod capacity?
          - Keeps the index within [0, capacity-1]
        """
        PRIME = 31
        hash_value = 0
        for i, char in enumerate(key):
            hash_value += ord(char) * (PRIME ** i)
        return hash_value % self.capacity

    # ------------------------------------------------------------------ #
    #  SECONDARY HASH FUNCTION (for Double Hashing demo)                  #
    # ------------------------------------------------------------------ #
    def _hash2(self, key: str) -> int:
        """
        A second, independent hash function.
        Used to show the concept of double hashing.
        (We use chaining in this table, but showing both approaches)
        """
        PRIME = 37
        hash_value = 0
        for char in key:
            hash_value = (hash_value * PRIME + ord(char))
        return hash_value % self.capacity

    # ------------------------------------------------------------------ #
    #  INSERT                                                              #
    # ------------------------------------------------------------------ #
    def insert(self, key: str, value=True):
        """
        Insert a key into the hash table.

        Steps:
          1. Compute bucket index via hash function
          2. If bucket is empty → create new node there
          3. If bucket is occupied → COLLISION!
             Walk the linked list:
             - If key already exists → update value
             - If end of list → append new node (chaining)
          4. After insert, check load factor → rehash if needed
        """
        index = self._hash(key)
        node = self.buckets[index]

        if node is None:
            # Empty bucket — no collision
            self.buckets[index] = Node(key, value)
            self.size += 1
        else:
            # COLLISION — walk the chain
            self.collision_count += 1
            while node:
                if node.key == key:
                    node.value = value   # Update existing key
                    return
                if node.next is None:
                    node.next = Node(key, value)  # Append to chain
                    self.size += 1
                    return
                node = node.next

        # Check if rehashing is needed
        if self.load_factor() > self.LOAD_FACTOR_LIMIT:
            self._rehash()

    # ------------------------------------------------------------------ #
    #  SEARCH / LOOKUP                                                     #
    # ------------------------------------------------------------------ #
    def search(self, key: str):
        """
        Look up a key.

        Returns the value if found, None if not found.
        Average time complexity: O(1)
        Worst case (all keys in one bucket): O(n)
        """
        index = self._hash(key)
        node = self.buckets[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def __contains__(self, key: str) -> bool:
        """Allows: 'hello' in hash_table"""
        return self.search(key) is not None

    # ------------------------------------------------------------------ #
    #  DELETE                                                              #
    # ------------------------------------------------------------------ #
    def delete(self, key: str) -> bool:
        """
        Remove a key from the table.
        Must carefully re-link the chain after removing a node.
        """
        index = self._hash(key)
        node = self.buckets[index]
        prev = None

        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next   # Skip over deleted node
                else:
                    self.buckets[index] = node.next  # Was the head
                self.size -= 1
                return True
            prev = node
            node = node.next
        return False

    # ------------------------------------------------------------------ #
    #  LOAD FACTOR                                                         #
    # ------------------------------------------------------------------ #
    def load_factor(self) -> float:
        """
        Load Factor = size / capacity

        - Low (< 0.5): Lots of empty buckets — wastes memory
        - High (> 0.7): Too many collisions — slows performance
        - Sweet spot: 0.5 – 0.7
        """
        return self.size / self.capacity

    # ------------------------------------------------------------------ #
    #  REHASHING                                                           #
    # ------------------------------------------------------------------ #
    def _rehash(self):
        """
        When load factor exceeds the limit, REHASH:
          1. Double the capacity
          2. Create a new, larger bucket array
          3. Re-insert ALL existing keys (new hash indices!)

        Why re-insert? Because hash(key) % new_capacity ≠ hash(key) % old_capacity
        """
        old_buckets = self.buckets
        self.capacity *= 2          # Double the size
        self.buckets = [None] * self.capacity
        self.size = 0               # Will be re-counted during re-insertion
        self.rehash_count += 1

        for bucket in old_buckets:
            node = bucket
            while node:
                self.insert(node.key, node.value)
                node = node.next

    # ------------------------------------------------------------------ #
    #  UTILITY                                                             #
    # ------------------------------------------------------------------ #
    def get_stats(self) -> dict:
        """Return internal stats — useful for learning and debugging."""
        chain_lengths = []
        for bucket in self.buckets:
            length = 0
            node = bucket
            while node:
                length += 1
                node = node.next
            chain_lengths.append(length)

        non_empty = [l for l in chain_lengths if l > 0]
        return {
            "size": self.size,
            "capacity": self.capacity,
            "load_factor": round(self.load_factor(), 3),
            "collisions_total": self.collision_count,
            "rehash_count": self.rehash_count,
            "max_chain_length": max(chain_lengths) if chain_lengths else 0,
            "avg_chain_length": round(sum(non_empty) / len(non_empty), 2) if non_empty else 0,
            "empty_buckets": chain_lengths.count(0),
        }

    def __len__(self):
        return self.size

    def __repr__(self):
        return f"HashTable(size={self.size}, capacity={self.capacity}, load={self.load_factor():.2f})"
