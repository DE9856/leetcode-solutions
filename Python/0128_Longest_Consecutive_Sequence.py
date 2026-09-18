class Solution(object):
    def longestConsecutive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        nums = set(nums)
        sol = 0
        for num in nums:
            if num-1 not in nums:
                length = 1
                while num+length in nums:
                    length+=1
                sol = max(sol, length)
        return sol
        
