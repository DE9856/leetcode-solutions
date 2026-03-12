class Solution(object):
    def searchMatrix(self, matrix, target):
        flatlist = []
        for sublist in matrix:
            for item in sublist:
                flatlist.append(item)
        if target in flatlist:
            return True
        else:
            return False
        
