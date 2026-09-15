class Solution(object):
    def isHappy(self, n):
        """
        :type n: int
        :rtype: bool
        """
        def square(n):
            total = 0
            while n>0:
                a = n%10
                total+= a*a
                n//=10
            return total
        slow = n
        fast = square(slow)
        while fast!=1 and slow!=fast:
            slow = square(slow)
            fast = square(square(fast))
        
        return fast==1

        
