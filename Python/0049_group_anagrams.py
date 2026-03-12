class Solution(object):
    def groupAnagrams(self, strs):
        d1 = {}
        for stri in strs:
            key = "".join(sorted(stri))
            if key not in d1:
                d1[key] = []
            d1[key].append(stri)
        return d1.values()
        
