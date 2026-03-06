class Solution(object):
    def searchRange(self, nums, target):
        l1 = [-1,-1]
        left = 0
        right=len(nums)-1
        start=-1
      
        while(left<=right):
            mid = (left+right)//2
            if target==nums[mid]:
                start = mid
                break
            elif target<nums[mid]:
                right = mid-1
            else:
                left = mid+1
              
        if start!=-1:
            left=right=start
            while(left-1>=0 and nums[left-1]==target):
                left-=1
            while(right+1<len(nums) and nums[right+1]==target):
                right+=1
            l1[0] = left
            l1[1] = right
          
        return l1

        
        
