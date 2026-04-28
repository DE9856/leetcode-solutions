class Solution(object):
    def reverseVowels(self, s):
        str1 = 'aAeEiIoOuU'
        i = 0
        j = len(s)-1
        s = list(s)
        while i<j:
            while i<j and s[i] not in str1:
                i+=1
            while i<j and s[j] not in str1:
                j-=1
            s[i],s[j] = s[j],s[i]
            i+=1
            j-=1
        return "".join(s)
