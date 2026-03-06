class Solution(object):
    def isAnagram(self, s, t):
        ss = sorted(s)
        ts = sorted(t)
        if ss==ts:
            return True
        else:
            return False
        
