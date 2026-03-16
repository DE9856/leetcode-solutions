/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     struct TreeNode *left;
 *     struct TreeNode *right;
 * };
 */

typedef struct TreeNode *node;
void inorder(node root, int *arr, int *returnSize){
    if(root == NULL)
        return;
    inorder(root->left, arr, returnSize);
    arr[*returnSize] = root->val;
    (*returnSize)++;
    inorder(root->right, arr, returnSize);
}

int* inorderTraversal(struct TreeNode* root, int* returnSize) {
    node temp = root;
    int *arr = malloc(100 * sizeof(int));
    *returnSize = 0;
    inorder(temp, arr, returnSize);
    return arr;
}
