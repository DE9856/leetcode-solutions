class Solution(object):
    def firstUniqChar(self, s):
        hashmap = {}

        for ch in s:
            hashmap[ch] = hashmap.get(ch,0)+1

        for i,ch in enumerate(s):
            if hashmap[ch]==1:
                return i
        return -1
        
