class Solution(object):
    def singleNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        sol = 0
        for num in nums:
            sol ^= num
        return sol
