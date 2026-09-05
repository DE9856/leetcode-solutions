class Solution(object):
    def trap(self, height):
        water=0
        stack = []
        for i in range(len(height)):
            while stack and height[i]>height[stack[-1]]:
                bottom = stack.pop()
                if not stack:
                    break
                left = stack[-1]
                width = i-left-1
                h = min(height[left],height[i])-height[bottom]
                water+=width*h
            stack.append(i)
        return water
        
        
