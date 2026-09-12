class Solution(object):
    def sortColors(self, nums):
        """
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        def partition(arr,low,high):
            pivot = arr[low]
            i = low+1
            j = high
            while(1):
                while(i<=high and arr[i]<=pivot):
                    i+=1
                while(j>low and arr[j]>=pivot):
                    j-=1
                if(i>=j):
                    break
                arr[i],arr[j] = arr[j],arr[i]
            arr[j],arr[low] = arr[low],arr[j]
            return j
        def quick(arr,low,high):
            if(low<high):
                p = partition(arr,low,high)
                quick(arr,low,p-1)
                quick(arr,p+1,high)

        quick(nums,0,len(nums)-1)
        return nums





#or

 class Solution(object):
    def sortColors(self, nums):
        """
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        left = 0
        right = len(nums)-1
        i=0
        while i<=right:
            if nums[i]==0:
                nums[i], nums[left] = nums[left],nums[i]
                left+=1
                i+=1
            elif nums[i]==2:
                nums[i], nums[right] = nums[right],nums[i]
                right -=1
            else:
                i+=1

        
