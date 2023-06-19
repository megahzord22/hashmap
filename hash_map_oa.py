# Name: Megan Grant
# OSU Email: granmega@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/17/23
# Description: A hash map implementation using open addressing

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the given key/value pair in the hashmap.
        :param load_factor: represents the load factor of the hash map
        :param initial: represents the correct index for the hash map
        :param original: represents a constant of the initial index
        :param j: represents the integer for quadratic probing
        returns nothing
        """
        hash = HashEntry(key, value)
        if self._size != 0:
            load_factor = self.table_load()
            if load_factor >= .5:
                self.resize_table(self._capacity * 2)
        initial = self._hash_function(hash.key) % self._capacity
        j = 1
        if self._buckets[initial] is None:
            self._buckets[initial] = HashEntry(key, value)
            self._size += 1
            return
        if self._buckets[initial] is not None:
            original = initial
            while self._buckets[initial] is not None:
                if self._buckets[initial].key == key:
                    if self._buckets[initial].is_tombstone:
                        self._buckets[initial]._is_tombsone = False
                        self._size += 1
                    else:
                        self._buckets[initial].value = value
                    break
                initial = (original + (j**2)) % self._capacity
                j += 1
            if self._buckets[initial] is not None:
                if self._buckets[initial].is_tombstone is True:
                    self._buckets[initial] = HashEntry(key, value)
                    return
            if self._buckets[initial] is None:
                self._buckets[initial] = HashEntry(key, value)
                self._size += 1
                return
            if self._buckets[initial].is_tombstone:
                self._buckets[initial].value = value
                self._size += 1
                return

    def table_load(self) -> float:
        """
        Calculates the load factor of the hash map
        :param load_factor: represents the load factor of the hash map
        returns the load factor
        """
        load_factor = self._size / self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Provides the number of empty buckets in the hash map
        returns the number of empty buckets
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table with the given capacity
        :param old_cap: represents the capacity before resize
        :param old_hash: represents the hash table before resize
        returns nothing
        """

        if new_capacity < self._size:
            return
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        old_cap = self._capacity
        old_hash = self._buckets
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        for num in range(self._capacity):
            self._buckets.append(None)
        self._size = 0
        for num in range(old_cap):
            if old_hash[num] is not None and old_hash[num].is_tombstone is False:
                self.put(old_hash[num].key, old_hash[num].value)

    def get(self, key: str) -> object:
        """
        Gets the value for the given key in a hash map
        :param hash: represents the current index in the table
        :param original: represents a constant of the first index
        :param j: represents a variable utilized to move quadratic probing forward
        returns the value if there is one or else returns None
        """
        hash = self._hash_function(key) % self._capacity
        if self._buckets[hash] is not None:
            if self._buckets[hash].key == key:
                if self._buckets[hash].is_tombstone:
                    return
                else:
                    return self._buckets[hash].value
            else:
                original = hash
                j = 1
                while self._buckets[hash] is not None and self._buckets[hash].key != key:
                    hash = (original + (j ** 2)) % self._capacity
                    j += 1
                if self._buckets[hash] is not None:
                    if self._buckets[hash].key == key:
                        if self._buckets[hash].is_tombstone:
                            return
                        else:
                            return self._buckets[hash].value
                return

    def contains_key(self, key: str) -> bool:
        """
        Finds out if the imputed key exists in the hashmpa
        returns True if the key is found and False if not
        """
        if self._size == 0:
            return False
        for num in range(self._capacity):
            if self._buckets[num] is not None:
                if self._buckets[num].key == key:
                    return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes a key from the hashtable
        :param hash: represents the current index
        :param original: represents a constant for the first index
        :param j: represents the variable used to create quadratic probing
        returns nothing
        """

        hash = self._hash_function(key) % self._capacity
        if self._buckets[hash] is not None:
            if self._buckets[hash].key == key:
                if self._buckets[hash].is_tombstone:
                    return
                else:
                    self._buckets[hash].is_tombstone = True
                    self._size -= 1
                    return
            else:
                original = hash
                j = 1
                while self._buckets[hash] is not None and self._buckets[hash].key != key:
                    hash = (original + (j ** 2)) % self._capacity
                    j += 1
                if self._buckets[hash] is not None:
                    if self._buckets[hash].key == key:
                        if self._buckets[hash].is_tombstone:
                            return
                        else:
                            self._buckets[hash].is_tombstone = True
                            self._size -= 1
                            return
                return

    def clear(self) -> None:
        """
        Clears the hash map of all values
        :param cap: represents the beginning capacity of the hash map
        returns nothing
        """

        cap = self._capacity
        self._buckets = DynamicArray()
        for num in range(cap):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Provides an array of tuples of the key-value pairs in the given hash map
        :param new_array: represents the new array containing the tuples
        :param tuple: represents a singular tuple with a given key-value pair
        returns the new_array of key-value pairs
        """
        new_array = DynamicArray()
        for num in range(self._capacity):
            if self._buckets[num] is not None:
                if self._buckets[num].is_tombstone is False:
                    tuple = (self._buckets[num].key, self._buckets[num].value)
                    new_array.append(tuple)
        return new_array

    def __iter__(self):
        """
        Get the index in the hash map
        returns self
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Get the value at the index in the hash map and move forward one
        :param value: represents the value at the index
        returns the value
        """
        try:
            if self._index <= self._capacity - 1:
                while self._buckets[self._index] is None or self._buckets[self._index].is_tombstone:
                    self._index = self._index + 1
                value = self._buckets[self._index]
                self._index = self._index + 1
                return value
        except DynamicArrayException:
            raise StopIteration


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
