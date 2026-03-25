class Solution(object):
    def lengthOfLongestSubstring(self, s):
        lastseen = {}
        maxlength = 0
        left = 0

        for right in range(len(s)):
            if s[right] in lastseen and lastseen[s[right]] >=left:
                left = lastseen[s[right]]+1
            lastseen[s[right]] = right
            x = right-left+1
            maxlength = x if x>maxlength else maxlength
        
        return maxlength
        
        
