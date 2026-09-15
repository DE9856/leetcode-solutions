/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
typedef struct ListNode *node;
node create(){
    node newnode = (node)malloc(sizeof(struct ListNode));
    newnode->val = 0;
    newnode->next = NULL;
    return newnode;
}
struct ListNode* swapPairs(struct ListNode* head) {
    node temp = create();
    temp->next = head;
    node prev = temp;
    node first;
    node second;
    while(prev->next!=NULL && prev->next->next!=NULL){
        first = prev->next;
        second = first->next;
        first->next = second ->next;
        second->next = first;
        prev->next = second;
        prev = first;
    }
    node sol = temp->next;
    free(temp);
    return sol;
}
