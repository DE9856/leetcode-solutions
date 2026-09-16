class Solution(object):
    def canJump(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        max1 = 0
        for i in range(len(nums)):
            if i>max1:
                return False
            max1 = max(max1, i+nums[i])
        return True 
