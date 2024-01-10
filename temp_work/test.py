# def dfs_subset_sum(s, target, current_subset, index, seen):
#     print(f"Current Subset: {current_subset}, Current Index: {index}")
#
#     if sum(current_subset) == target:
#         print("Found subset:", current_subset)
#         return
#
#     seen.add(s[index])
#     for i in range(index, len(s)):
#         if s[i] in seen:
#             continue
#
#         # 包含当前元素
#         print(f"Including {s[i]}")
#         if i + 1 < len(s):
#             dfs_subset_sum(s, target, current_subset + [s[i]], i + 1, seen)
#
#         # 剪枝：如果已经找到子集和等于目标和，直接回溯
#         if sum(current_subset) >= target:
#             return
#
#         # 不包含当前元素
#         print(f"Not including {s[i]}")
#         if i + 1 < len(s):
#             dfs_subset_sum(s, target, current_subset + [s[i]], i + 1, seen)
#
#     seen.remove(s[index])
#     print(f"Backtrack from {index}")
#
#
# # 测试
# S = [7, 4, 6, 13, 20, 8]
# target_sum = 18
# seen = set()
# dfs_subset_sum(S, target_sum, [], 0, seen)

# def max_subarray_sum(nums):
#     if not nums:
#         return 0
#
#     max_sum = current_sum = nums[0]
#     start = end = temp_start = 0
#
#     for i in range(1, len(nums)):
#         if current_sum < 0:
#             current_sum = nums[i]
#             temp_start = i
#         else:
#             current_sum += nums[i]
#
#         if current_sum > max_sum:
#             max_sum = current_sum
#             start = temp_start
#             end = i
#
#     return max_sum, nums[start:end+1]
#
# # 示例
# nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
# max_sum, max_subarray = max_subarray_sum(nums)
# print("最大子数组和:", max_sum)
# print("最大子数组:", max_subarray)

def beautiful_array(N):
    if N == 1:
        return [1]
    # 构造奇数数组
    odds = beautiful_array((N + 1) // 2)
    # 构造偶数数组
    evens = beautiful_array(N // 2)
    # 合并奇数和偶数数组
    return [2 * x - 1 for x in odds] + [2 * x for x in evens]

# 示例
N = 4
result = beautiful_array(N)
print(result)