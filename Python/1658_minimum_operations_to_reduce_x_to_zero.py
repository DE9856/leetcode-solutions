class Solution(object):
    def minOperations(self, nums, x):
        """
        :type nums: List[int]
        :type x: int
        :rtype: int
        """
        target = sum(nums) - x
        if target < 0:
            return -1
        left = 0
        current = 0
        longest = -1
        for right in range(len(nums)):
            current += nums[right]
            while current > target and left <= right:
                current -= nums[left]
                left += 1
            if current == target:
                longest = max(longest, right - left + 1)
        if longest == -1:
            return -1
        return len(nums) - longest
        
