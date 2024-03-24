class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size

    def _hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash_function(key)
        if self.table[index] is None:
            self.table[index] = []
        self.table[index].append((key, value))

    def get(self, key):
        index = self._hash_function(key)
        if self.table[index] is not None:
            vals = []
            for stored_key, value in self.table[index]:
                if stored_key == key:
                    vals.append(value)
            return vals
        raise KeyError(f"Key '{key}' not found in the hash table.")

    def remove(self, key):
        index = self._hash_function(key)
        if self.table[index] is not None:
            for i, (stored_key, _) in enumerate(self.table[index]):
                if stored_key == key:
                    del self.table[index][i]
                    return
        raise KeyError(f"Key '{key}' not found in the hash table.")

    def display_table(self):
        for index, slot in enumerate(self.table):
            print(f"Index {index}: {slot}")

# Example usage:
hash_table = HashTable()

hash_table.insert("255_255_255", "A")
hash_table.insert("255_0_255", "B")
hash_table.insert("0_100_255","A")
hash_table.insert("0_255_0", "C")
hash_table.insert("255_255_255", "C")
hash_table.insert("255_255_255", "D")
# Display the full hash table
hash_table.display_table()

print(hash_table.get("255_255_255"))
