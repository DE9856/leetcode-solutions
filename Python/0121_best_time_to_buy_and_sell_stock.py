class Solution(object):
    def maxProfit(self, prices):
        min1 = prices[0]
        profit = 0
        for price in prices:
            if price < min1:
                min1 = price
            profit1 = price - min1
            if profit1 > profit:
                profit = profit1
        return profit 
