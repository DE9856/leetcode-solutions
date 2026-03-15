class Solution(object):
    def lengthOfLastWord(self, s):
        strarr = s.split()
        stri = strarr[len(strarr)-1]
        return len(stri)
