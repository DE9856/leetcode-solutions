class Solution(object):
    def smallestIndex(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        for i in range(len(nums)):
            x = nums[i]
            s = 0
            while x > 0:
                s += x%10
                x //=10

            if s==i:
                return i
        return -1
        
