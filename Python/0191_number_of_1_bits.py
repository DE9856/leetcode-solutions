class Solution(object):
    def hammingWeight(self, n):
        """
        :type n: int
        :rtype: int
        """
        binary = bin(n)
        sol = 0
        for ch in binary:
            if ch=='1':
                sol+=1
        return sol


#or

class Solution(object):
    def hammingWeight(self, n):
        """
        :type n: int
        :rtype: int
        """
        sol = 0
        while n:
            n = n & (n-1)
            sol+=1
        return sol
        
