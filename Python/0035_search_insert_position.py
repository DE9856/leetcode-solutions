class Solution(object):
    def searchInsert(self, l1, key):
        left=0
        right=len(l1)-1
        while(left<=right):
            mid = int((left+right)/2)
            if l1[mid]==key:
                return mid
            if l1[mid]>key:
                right = mid-1
            if l1[mid]<key:
                left = mid+1
        return left
        
