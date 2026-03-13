class Solution(object):
    def maxArea(self, height):
        left = 0
        right = len(height)-1
        max1 = 0
        current = 0
        while(left<right):
            current = (right-left)*min(height[left], height[right])
            if current > max1:
                max1 = current
            if height[left]<height[right]:
                left+=1
            else:
                right-=1   
        return max1

            
        
