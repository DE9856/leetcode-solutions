class Solution(object):
    def palindrome(self,s,left,right):
        while left >=0 and right < len(s) and s[left]==s[right]:
            right+=1
            left-=1
        return s[left+1:right]
    def longestPalindrome(self, s):
        longest = ""
        for i in range(len(s)):
            str1 = self.palindrome(s,i,i)
            str2 = self.palindrome(s,i,i+1)

            if len(str1)>len(longest):
                longest = str1
            if len(str2)>len(longest):
                longest = str2

        return longest
        
