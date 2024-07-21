import timeit

# Algorithm Implementations
def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0

    bad_char = [-1] * 256
    for i in range(m):
        bad_char[ord(pattern[i])] = i

    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        else:
            s += max(1, j - bad_char[ord(text[s + j])])
    
    return -1

def kmp_search(text, pattern):
    def compute_lps_array(pattern):
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1
        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    n = len(text)
    m = len(pattern)
    lps = compute_lps_array(pattern)

    i = 0
    j = 0
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            return i - j
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    
    return -1

def rabin_karp(text, pattern):
    d = 256
    q = 101
    m = len(pattern)
    n = len(text)
    p = 0
    t = 0
    h = 1

    for i in range(m-1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                return i

        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    
    return -1

# Measure execution time
def measure_time(algorithm, text, pattern):
    setup_code = f'from __main__ import {algorithm}, text, pattern'
    stmt = f'{algorithm}(text, pattern)'
    times = timeit.repeat(stmt, setup=setup_code, repeat=3, number=1000)
    return min(times)

# Load articles
def load_file(file_path, encoding='latin-1'):
    with open(file_path, 'r', encoding=encoding) as file:
        return file.read()

# Ensure file paths are correct
article1_path = 'article1.txt'
article2_path = 'article2.txt'

# Debugging print statements
print("Loading articles...")

try:
    article1 = load_file(article1_path)
    print(f"Loaded article1 ({len(article1)} characters).")
except Exception as e:
    print(f"Error loading article1: {e}")
    article1 = None

try:
    article2 = load_file(article2_path)
    print(f"Loaded article2 ({len(article2)} characters).")
except Exception as e:
    print(f"Error loading article2: {e}")
    article2 = None

if article1 and article2:
    # Substrings
    existing_substring = "example"
    non_existing_substring = "notpresent"

    text_samples = [article1, article2]
    patterns = [existing_substring, non_existing_substring]

    algorithms = ['boyer_moore', 'kmp_search', 'rabin_karp']

    results = []

    print("Starting performance tests...")

    for text in text_samples:
        for pattern in patterns:
            for algo in algorithms:
                print(f"Testing {algo} with pattern '{pattern}'...")
                time = measure_time(algo, text, pattern)
                results.append((text[:30], pattern, algo, time))
                print(f"{algo} with pattern '{pattern}' took {time:.6f} seconds.")

    # Display the results
    print("Results:")
    for result in results:
        print(f'Pattern: {result[1]} Algorithm: {result[2]} Time: {result[3]:.6f} seconds')
else:
    print("Could not load one or both articles. Exiting.")
