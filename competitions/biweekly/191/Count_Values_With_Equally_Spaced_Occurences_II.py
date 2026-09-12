class Solution(object):
    def countSpecialIntegers(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        dict = {}
        sol = 0
        for i in range(len(nums)):
            if nums[i] not in dict:
                dict[nums[i]] = [i]
            else:
                dict[nums[i]].append(i)

        for i in dict:
            if len(dict[i])>=3:
                positions = dict[i]
                validity = True
                spacing = positions[1]-positions[0]
                for j in range(2,len(positions)):
                    if positions[j] - positions[j-1]!=spacing:
                        validity = False
                        break
                if validity == True:
                     sol+=1
        return sol
