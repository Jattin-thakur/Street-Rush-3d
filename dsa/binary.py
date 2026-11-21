def binary_search(arr, target):
    left, right=0, len(arr) - 1
    while left <= right:
        mid = left + (right - left) // 2
n = int(input("Enter number of elements: "))
arr = []

print("Enter elements in sorted order:")
for _ in range(n):
    arr.append(int(input()))

target = int(input("Enter target element: "))

result = binary_search(arr, target)

if result != -1:
    print(f"Element found at index {result}")
else:
    print("-1")