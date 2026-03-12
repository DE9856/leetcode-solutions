class Solution(object):
    def minOperations(self, nums, k):
        sumvalue = sum(nums)
        return sumvalue%k
        
