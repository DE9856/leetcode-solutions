class Solution(object):
    def totalNumbers(self, digits):
        count = 0
        for num in range(100,1000):
            if num%2!=0:
                continue
            a = num//100
            b = (num//10)%10
            c = num%10
            temp = digits[:]
            if a in temp:
                temp.remove(a)
            else:
                continue
            if b in temp:
                temp.remove(b)
            else:
                continue
            if c in temp:
                temp.remove(c)
            else:
                continue
            count+=1
        return count
        
