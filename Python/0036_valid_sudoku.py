class Solution(object):
    def isValidSudoku(self, board):
        """
        :type board: List[List[str]]
        :rtype: bool
        """
        rows = [set() for _ in range(9)]
        columns = [set() for _ in range(9)]
        sbox = [set() for _ in range(9)]
        for i in range(9):
            for j in range(9):
                if board[i][j]=='.':
                    continue
                num = board[i][j]
                sbox1 = (i//3)*3 + (j//3)
                if num in rows[i]:
                    return False
                if num in columns[j]:
                    return False
                if num in sbox[sbox1]:
                    return False
                rows[i].add(num)
                columns[j].add(num)
                sbox[sbox1].add(num)
        return True
        
