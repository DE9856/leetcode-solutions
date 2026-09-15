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
struct ListNode* rotateRight(struct ListNode* head, int k) {
    if(head==NULL || head->next==NULL || k==0)
        return head;
    node temp = head;
    int len = 1;
    while(temp->next!=NULL){
        temp=temp->next;
        len++;
    }
    k = k%len;
    if(k==0)
        return head;
    int steps = len-k-1;
    node split = head;
    for(int i=0;i<steps;i++)
        split = split->next;
    node newhead = split->next;
    split->next = NULL;
    temp ->next = head;
    return newhead;
}
