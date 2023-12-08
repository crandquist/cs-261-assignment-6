# Name: Cat Randquist
# OSU Email: randquic@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/7/2023
# Description: Hash Map implementation using separate chaining


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
        Update the key / value pair in the hash map.
        """
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        hash_key = self._hash_function(key) % self._capacity
        chain_key = self._buckets.get_at_index(hash_key)

        # If the key in the hash map does not yet exist, then simply add the key to the corresponding bucket
        # and its value, which will be a linked list node.
        if chain_key.length() == 0:
            chain_key.insert(key, value)
            self._size += 1
        else:
            # iterate through the linked list and check if the same key exists. If it does then do nothing
            for item in chain_key:
                if item.key == key:
                    chain_key.remove(key)
                    chain_key.insert(key, value)
                    return
            chain_key.insert(key, value)
            self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        """

        # First, check if new_capacity is less than 1. If it is then do nothing
        if new_capacity < 1:
            return

        # A check for a new capacity with a prime number size
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # First, create a new Hashmap with the new capacity
        new_table = HashMap(new_capacity, self._hash_function)

        # this is to prevent next_prime from going to 3, when it should stay at 2 (since 2 is prime)
        if new_capacity == 2:
            new_table._capacity = 2

        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() > 0:
                # chain_key = self._buckets.get_at_index(i).__iter__()
                for item in self._buckets.get_at_index(i):
                    new_table.put(item.key, item.value)
                # for _ in range(self._buckets.get_at_index(i).length()):
                #     node = chain_key.__next__()
                #     new_table.put(node.key, node.value)

        # Reassigning new values to self
        self._buckets = new_table._buckets
        self._size = new_table._size
        self._capacity = new_table._capacity

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        # Calculate the load factor.
        load_factor = self._size / self._capacity
        return load_factor

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        # Initialize a counter for empty buckets.
        empty_buckets = 0

        # Iterate through the buckets and count the empty ones.
        index = 0
        while index < self._buckets.length():
            if self._buckets.get_at_index(index).length() == 0:
                empty_buckets += 1

            # Move to the next bucket.
            index += 1

        # Return the number of empty buckets.
        return empty_buckets

    def get(self, key: str):
        """
        Retrieves the value associated with the given key.
        """
        index = self._hash_function(key) % self._capacity
        current_bucket = self._buckets.get_at_index(index)

        # Check if key exists in the bucket.
        existing_node = current_bucket.contains(key)
        if existing_node:
            return existing_node.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Checks if a key exists in the hash map.
        """
        index = self._hash_function(key) % self._capacity
        current_bucket = self._buckets.get_at_index(index)

        # Check if key already exists in the bucket.
        existing_node = current_bucket.contains(key)
        if existing_node:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        Removes the key-value pair associated with the given key.
        """
        index = self._hash_function(key) % self._capacity
        current_bucket = self._buckets.get_at_index(index)

        # Find the node containing the key in the bucket.
        node = current_bucket.contains(key)

        # Remove the node if it exists and decrement the size.
        if node:
            current_bucket.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray containing tuples of keys and their values.
        """
        keys_and_values = DynamicArray()

        # Iterate through each bucket in the hash map.
        for i in range(self._buckets.length()):
            current_bucket = self._buckets.get_at_index(i)

            # Iterate through each node in the bucket.
            for node in current_bucket:
                keys_and_values.append((node.key, node.value))

        return keys_and_values

    def clear(self) -> None:
        """
        Clears the hash map by removing all elements.
        """
        # Create a new empty DynamicArray.
        self._buckets = DynamicArray()

        # Create new buckets with the default capacity.
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Return a tuple containing the mode DynamicArray and its frequency.
    """
    max_freq = 0
    mode_elements = DynamicArray()

    for i in range(da.length()):
        current_element = da.get_at_index(i)
        current_count = 0

        # Count occurrences of the current element in the array
        for j in range(da.length()):
            if da.get_at_index(j) == current_element:
                current_count += 1

        # Update the max frequency and mode_elements
        if current_count > max_freq:
            max_freq = current_count
            mode_elements = DynamicArray([current_element])
        elif current_count == max_freq and not any(
                current_element == mode_elements.get_at_index(k) for k in range(mode_elements.length())):
            mode_elements.append(current_element)

    return mode_elements, max_freq



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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
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
