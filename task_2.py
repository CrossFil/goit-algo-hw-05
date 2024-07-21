def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            upper_bound = arr[mid]
            return (iterations, upper_bound)
        elif arr[mid] < target:
            low = mid + 1
        else:
            upper_bound = arr[mid]
            high = mid - 1
    
    if upper_bound is None and low < len(arr):
        upper_bound = arr[low]
    
    return (iterations, upper_bound)

# Example usage:
arr = [0.1, 0.5, 1.1, 1.5, 2.2, 2.8, 3.3]
target = 1.6
result = binary_search(arr, target)
print(result)  # Output example: (3, 2.2)
