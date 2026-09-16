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
    newnode->next = NULL;
    newnode->val = 0;
    return newnode;
}
struct ListNode* reverseKGroup(struct ListNode* head, int k) {
    node temp = head;
    int count = 0;

    while(temp!=NULL && count<k){
        temp = temp->next;
        count++;
    }
    if(count<k)
        return head;
    node prev = NULL;
    temp = head;
    for(int i=0;i<k;i++){
        node next = temp->next;
        temp->next = prev;
        prev = temp;
        temp = next;
    }
    head->next = reverseKGroup(temp,k);
    return prev;
}
