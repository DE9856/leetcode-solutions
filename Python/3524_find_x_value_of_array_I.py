class Solution(object):
    def resultArray(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        dp = [0]*k
        ans = [0]*k
        for num in nums:
            new = [0]*k
            new[num%k] +=1
            for r in range(k):
                new[(r*num)%k]+= dp[r]
            dp = new
            for r in range(k):
                ans[r] += dp[r]
        return ans
    
