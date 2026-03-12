class Solution(object):
    def findWordsContaining(self, words, x):
        l1 =[]
        for i in range(len(words)):
            if x in words[i]:
                l1.append(i)
        return l1

    
