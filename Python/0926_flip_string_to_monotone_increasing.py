class Solution(object):
    def minFlipsMonoIncr(self, s):
        ones = 0
        flips = 0
        for ch in s:
            if ch=='1':
                ones+=1
            else:
                flips = ones if ones < flips+1 else flips+1
        return flips
