class Solution(object):
    def solveNQueens(self, n):
        """
        :type n: int
        :rtype: List[List[str]]
        """
        board = [0] * n
        ans = []
        def place(row, col):
            for i in range(row):
                if board[i] == col or abs(board[i] - col) == abs(i - row):
                    return False
            return True
        def queen(row):
            for col in range(n):
                if place(row, col):
                    board[row] = col
                    if row == n - 1:
                        temp = []
                        for i in range(n):
                            s = ['.'] * n
                            s[board[i]] = 'Q'
                            temp.append(''.join(s))
                        ans.append(temp)
                    else:
                        queen(row + 1)
        queen(0)
        return ans
        
