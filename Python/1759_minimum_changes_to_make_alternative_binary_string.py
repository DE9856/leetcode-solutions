class Solution(object):
    def minOperations(self, s):
        change0 = 0
        change1 = 0
        for i in range(len(s)):
            expectedstarting0 = '0' if i%2==0 else '1'
            expectedstarting1 = '1' if i%2==0 else '0'
            if s[i]!=expectedstarting0:
                change0+=1
            if s[i]!=expectedstarting1:
                change1+=1

        return change0 if change0<change1 else change1
