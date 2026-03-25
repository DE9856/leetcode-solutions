class Solution(object):
    def maxVowels(self, s, k):
        count = 0
        for i in range(k):
            if s[i] in "aeiou":
                count += 1
        
        maxcount = count
        for i in range(k, len(s)):
            if s[i] in "aeiou":
                count += 1
            if s[i-k] in "aeiou":
                count -= 1
            
            maxcount = count if count>maxcount else maxcount
        
        return maxcount
            
        
        
