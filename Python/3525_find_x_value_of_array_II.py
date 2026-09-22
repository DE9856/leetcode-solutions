class Solution(object):
    def resultArray(self, nums, k, queries):
        n = len(nums)

        size = 1
        while size < n:
            size *= 2

        tree = [(1, [0] * k) for _ in range(2 * size)]

        for i in range(n):
            v = nums[i] % k
            pref = [0] * k
            pref[v] = 1
            tree[size + i] = (v, pref)

        def merge(A, B):
            pa, prefa = A
            pb, prefb = B

            pref = prefa[:]

            for r in range(k):
                pref[(pa * r) % k] += prefb[r]

            return (pa * pb % k, pref)

        for i in range(size - 1, 0, -1):
            tree[i] = merge(tree[i * 2], tree[i * 2 + 1])

        def update(pos, val):
            pos += size

            v = val % k
            pref = [0] * k
            pref[v] = 1

            tree[pos] = (v, pref)
            pos //= 2

            while pos:
                tree[pos] = merge(tree[pos * 2], tree[pos * 2 + 1])
                pos //= 2

        def query(left):
            left += size
            right = size + n

            left_part = None
            right_part = None

            while left < right:
                if left & 1:
                    if left_part is None:
                        left_part = tree[left]
                    else:
                        left_part = merge(left_part, tree[left])
                    left += 1

                if right & 1:
                    right -= 1
                    if right_part is None:
                        right_part = tree[right]
                    else:
                        right_part = merge(tree[right], right_part)

                left //= 2
                right //= 2

            if left_part is None:
                return right_part

            if right_part is None:
                return left_part

            return merge(left_part, right_part)

        ans = []

        for index, value, start, x in queries:
            update(index, value)

            result = query(start)

            ans.append(result[1][x])

        return ans
