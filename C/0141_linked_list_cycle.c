/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
typedef struct ListNode *node;
node create(int data){
    node newnode = (node)malloc(sizeof(struct ListNode));
    newnode-> val = data;
    newnode->next = NULL;
    return newnode;
}
bool hasCycle(struct ListNode *head) {
    node dummy = create(5);
    node temp = head;
    while(temp!=NULL){
        if(temp->next==dummy)
            return true;
        node next1 = temp->next;
        temp->next = dummy;
        temp = next1;
    }
    return false;
}
