class Solution(object):
    def numberOfSets(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """
        MOD = 10**9+7
        a = n+k-1
        b = 2*k
        ans = 1
        for i in range(1,b+1):
            ans = ans * (a - b + i) % MOD
            ans = ans * pow(i, MOD - 2, MOD) % MOD
        return ans
        
        
