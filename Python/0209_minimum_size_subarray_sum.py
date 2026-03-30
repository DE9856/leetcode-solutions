class Solution(object):
    def minSubArrayLen(self, target, nums):
        left = 0
        current = 0
        min_length = float('inf')

        for right in range(len(nums)):
            current+=nums[right]
            while current>=target:
                min_length = (right-left+1) if (right-left+1) < min_length else min_length
                current-=nums[left]
                left+=1
        return min_length if min_length != float('inf') else 0
        
