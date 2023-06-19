# Name: Megan Grant
# OSU Email: granmega@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/17/23
# Description: A hash map implementation using separate chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        :param hash: represents the key hashed by the function
        :param index: represents the correct index for the hash map
        returns nothing
        """

        if self._size != 0:
            load_factor = self.table_load()
            if load_factor >= 1:
                self.resize_table(self._capacity * 2)
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index].length() == 0:
            self._buckets[index].insert(key, value)
            self._size += 1
        else:
            if self._buckets[index].contains(key):
                self._buckets[index].remove(key)
                self._buckets[index].insert(key, value)
            else:
                self._buckets[index].insert(key, value)
                self._size += 1

    def empty_buckets(self) -> int:
        """
        Counts the number of empty buckets in the hash map
        :param count: represents the count of the number of empty buckets
        returns count
        """
        count = 0
        for num in range(self._capacity):
            if self._buckets[num].length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        Calculates the load factor of the hash map
        :param load_factor: represents the load factor of the hash map
        returns the load factor
        """
        load_factor = self._size / self._capacity
        return load_factor

    def clear(self) -> None:
        """
        Clears the hash map of all elements
        :param cap: represents the beginning capacity of the hash map
        returns nothing
        """
        cap = self._capacity
        self._buckets = DynamicArray()
        self._capacity = cap
        self._size = 0
        for num in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash map and redistributes the key-value pairs accordingly
        :param old_cap: represents the original capacity
        :param old_hash: represents the orignial hash map array
        returns nothing
        """
        if new_capacity < 1:
            return
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        old_cap = self._capacity
        old_hash = self._buckets
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0
        for num in range(self._capacity):
            self._buckets.append(LinkedList())
        for num in range(old_cap):
            for node in old_hash[num]:
                self.put(node.key, node.value)

    def get(self, key: str):
        """
        Gets the value for the given key in a hash map
        :param answer: represents the node of the given key
        returns the value if there is one or else returns None
        """
        for num in range(self._capacity):
            answer = self._buckets[num].contains(key)
            if answer is not None:
                return answer.value
        return

    def contains_key(self, key: str) -> bool:
        """
        Checks to see if the hashmap contains the given key
        :param answer: represents the node of the given key
        returns True if the key is in the hash map and False otherwise
        """
        for num in range(self._capacity):
            answer = self._buckets[num].contains(key)
            if answer is not None:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its value from the hash map
        :param hash: represents the key run through the given hash function
        :param index: represents the correct index of the given key
        :param result: represents the result of the LL remove function (True if successful)
        returns nothing
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        result = self._buckets[index].remove(key)
        if result is True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Provides a dynamic array of tuples holding a hash map's key value pairs
        :param new_array: represents the new array to add the tuples to
        :param tuple: represents a tuple of a new key value pair from the hash map
        returns the new dynamic array
        """
        new_array = DynamicArray()
        for num in range(self._capacity):
            for node in self._buckets[num]:
                tuple = (node.key, node.value)
                new_array.append(tuple)
        return new_array


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Finds the mode of the given dynamic array
    :param map: represents an instance of the hash map class
    :param largest: represents an integer value of the frequency of the mode
    :param value: represents the marker of the frequency, passed as the value in the key value pair
    :param new_array: represents an array with the hash map's key value pairs stored in tuples
    :param tuple: represents an individual tuple in the new_array
    :param number: represents the frequency stored in the tuple
    :param final_array: represents the array of values that are modes
    returns a tuple that stores the final_array and the frequency (largest)
    """

    map = HashMap()
    largest = 0
    # stores the values and keeps track of their frequency
    for num in range(da.length()):
        if map.contains_key(da[num]):
            value = map.get(da[num])
            map.put(da[num], value + 1)
        else:
            map.put(da[num], 1)
    new_array = map.get_keys_and_values()
    # finds the frequency
    for num in range(new_array.length()):
        tuple = new_array[num]
        number = tuple[1]
        if number > largest:
            largest = number
    final_array = DynamicArray()
    # appends any modes to the dynamic array
    for num in range(new_array.length()):
        tuple = new_array[num]
        if tuple[1] == largest:
            final_array.append(tuple[0])
    final_tuple = (final_array, largest)
    return final_tuple

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
