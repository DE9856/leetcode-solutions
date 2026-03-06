/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
typedef struct ListNode *node;
struct ListNode* removeNthFromEnd(struct ListNode* head, int n) {
    node prev = NULL, temp = head, next = NULL;
    while(temp!=NULL){
        next = temp->next;
        temp->next = prev;
        prev = temp;
        temp = next;
    }
    node newhead = prev;
    
    if(n==1)
        newhead = newhead->next;
    else{
        node before = NULL;
        node temp = newhead;
        for(int i=0;i<n-1;i++){
            before = temp;
            temp = temp->next;
        }
        before->next = temp->next;
    }

    prev = NULL;
    temp = newhead;
    next = NULL;
    while(temp!=NULL){
        next = temp->next;
        temp->next = prev;
        prev = temp;
        temp = next;
    }
    return prev;    
}
