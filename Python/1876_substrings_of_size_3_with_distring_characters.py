class Solution(object):
    def countGoodSubstrings(self, s):
        goodcount = 0
        for i in range(len(s)-2):
            if len(set(s[i:i+3]))==3:
                goodcount+=1
        return goodcount
