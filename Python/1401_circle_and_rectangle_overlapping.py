class Solution(object):
    def checkOverlap(self, radius, xCenter, yCenter, x1, y1, x2, y2):
        """
        :type radius: int
        :type xCenter: int
        :type yCenter: int
        :type x1: int
        :type y1: int
        :type x2: int
        :type y2: int
        :rtype: bool
        """
        x = max(x1, min(xCenter,x2))
        y = max(y1, min(yCenter,y2))
        distance = (x-xCenter)**2 + (y-yCenter)**2
        return distance<=radius**2
        
