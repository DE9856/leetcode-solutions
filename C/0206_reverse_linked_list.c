/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */

typedef struct ListNode *node;
struct ListNode* reverseList(struct ListNode* head) {
    node prev = NULL, temp = head, next = NULL;
    while(temp!=NULL){
        next = temp->next;
        temp->next = prev;
        prev = temp;
        temp = next;
    }
    return prev;
}
