class Solution(object):
    def strStr(self, haystack, needle):
        i=0
        flag = 0
        for i in range(len(haystack)-len(needle)+1):
            if haystack[i::].startswith(needle):
                flag = 1
                break
        if flag==1:
            return i
        else:
            return -1

        
