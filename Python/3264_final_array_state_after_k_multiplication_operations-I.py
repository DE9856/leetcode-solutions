class Solution(object):
    def getFinalState(self, nums, k, multiplier):
        for i in range(k):
            minvalue = min(nums)
            indexvalue = nums.index(minvalue)
            nums[indexvalue]*=multiplier
        return nums
        
