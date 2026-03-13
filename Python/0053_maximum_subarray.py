class Solution(object):
    def maxSubArray(self, nums):
        current = nums[0]
        maxsum = nums[0]

        for i in range(1,len(nums)):
            current = nums[i] if nums[i]>current+nums[i] else current+nums[i]
            maxsum = maxsum if maxsum>current else current

        return maxsum

        
