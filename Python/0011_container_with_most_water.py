class Solution(object):
    def maxArea(self, height):
        left = 0
        right = len(height)-1
        max1 = 0
        current = 0
        while(left<right):
            minvalue = height[left] if height[left]<height[right] else height[right]
            current = (right-left)*minvalue
            if current > max1:
                max1 = current
            if height[left]<height[right]:
                left+=1
            else:
                right-=1   
        return max1

            
        
