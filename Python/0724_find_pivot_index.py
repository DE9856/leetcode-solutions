class Solution(object):
    def pivotIndex(self, nums):
        sum = 0
        for i in nums:
            sum+=i
        
        left = 0
        for i in range(len(nums)):
            right = sum - left - nums[i]
            if left==right:
                return i
            left+=nums[i]
        return -1
        
