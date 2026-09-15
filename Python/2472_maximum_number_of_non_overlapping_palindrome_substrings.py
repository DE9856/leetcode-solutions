class Solution(object):
    def maxPalindromes(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        n = len(s)
        dp = [0] * (n + 1)
        def isPalindrome(l, r):
            while l < r:
                if s[l] != s[r]:
                    return False
                l += 1
                r -= 1
            return True
        for i in range(k, n + 1):
            dp[i] = dp[i - 1]
            if isPalindrome(i - k, i - 1):
                dp[i] = max(dp[i], dp[i - k] + 1)
            if i - k - 1 >= 0 and isPalindrome(i - k - 1, i - 1):
                dp[i] = max(dp[i], dp[i - k - 1] + 1)

        return dp[n]
