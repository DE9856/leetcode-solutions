class Solution(object):
    def minSumOfLengths(self, arr, target):
        """
        :type arr: List[int]
        :type target: int
        :rtype: int
        """
        n = len(arr)
        INF = float('inf')

        best = [INF] * n
        left = 0
        total = 0
        ans = INF

        for right in range(n):
            total += arr[right]

            while total > target:
                total -= arr[left]
                left += 1

            if total == target:
                length = right - left + 1

                if left > 0 and best[left - 1] != INF:
                    ans = min(ans, length + best[left - 1])

                best[right] = length

            if right > 0:
                best[right] = min(best[right], best[right - 1])

        return -1 if ans == INF else ans
