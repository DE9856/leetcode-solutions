class Solution(object):
    def characterReplacement(self, s, k):
        count = {}
        left = 0
        maxfrequency = 0
        result = 0

        for right in range(len(s)):
            count[s[right]] = count.get(s[right],0)+1
            maxfrequency = count[s[right]] if count[s[right]]>maxfrequency else maxfrequency
            while(right-left+1) - maxfrequency > k:
                count[s[left]]-=1
                left+=1
            x = right-left+1
            result = x if x>result else result
        return result
        
