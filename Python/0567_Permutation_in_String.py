class Solution(object):
    def checkInclusion(self, s1, s2):
        if len(s1) > len(s2):
            return False
        
        for i in range(len(s2)-len(s1)+1):
            if sorted(s1) == sorted(s2[i:i+len(s1)]):
                return True
        return False
