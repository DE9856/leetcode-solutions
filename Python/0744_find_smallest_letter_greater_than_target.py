class Solution(object):
    def nextGreatestLetter(self, letters, target):
        for ch in letters:
            if ch > target:
                return ch
        return letters[0]
