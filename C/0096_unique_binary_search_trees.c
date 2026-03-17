typedef int* arr;

int numTrees(int n) {
    arr dp = (int*)malloc((n + 1) * sizeof(int));

    dp[0] = 1;
    dp[1] = 1;

    for(int i = 2; i <= n; i++) {
        dp[i] = 0;

        for(int j = 1; j <= i; j++) {
            dp[i] += dp[j - 1] * dp[i - j];
        }
    }

    int result = dp[n];
    return result;
}
