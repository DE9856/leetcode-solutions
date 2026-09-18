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
struct ListNode* partition(struct ListNode* head, int x) {
    node smallhead = create();
    node bighead = create();
    node s = smallhead;
    node l = bighead;
    node temp = head;
    while(temp!=NULL){
        if(temp->val < x){
            s->next = temp;
            s = s->next;
        }
        else{
            l->next = temp;
            l = l->next;
        }
        temp = temp->next;
    }
    l->next = NULL;
    s->next = bighead->next;
    return smallhead->next;
}
