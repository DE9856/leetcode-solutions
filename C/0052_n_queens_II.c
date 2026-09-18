int board[20], n,count;

int place(int row, int col){
    for(int i =0;i<row;i++){
        if(board[i]==col || abs(board[i]-col)==abs(i-row))
            return 0;
    }
    return 1;
}

void queen(int row){
    for(int col = 0;col<n;col++){
        if(place(row,col)){
            board[row] = col;
            if(row==n-1)
                count++;
            else
                queen(row+1);
        }
    }
}
int totalNQueens(int N) {
    n = N;
    count = 0;
    queen(0);
    return count;
}
