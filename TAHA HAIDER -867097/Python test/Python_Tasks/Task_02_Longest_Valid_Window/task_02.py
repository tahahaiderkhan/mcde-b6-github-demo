# Task 02 | Longest Valid Window

def longest_unique_window(text):

    seen = {}
    start = 0

    longest = ""
    best_start = 0
    max_length = 0

    for i in range(len(text)):

        char = text[i]

        if char in seen and seen[char] >= start:
            start = seen[char] + 1

        seen[char] = i

        length = i - start + 1

        if length > max_length:
            max_length = length
            best_start = start
            longest = text[start:i+1]

    return longest, best_start, max_length


print(longest_unique_window("abcabcbb"))
print(longest_unique_window(""))
