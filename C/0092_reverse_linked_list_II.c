/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
typedef  struct ListNode *node;
node create(){
    node newnode = (node)malloc(sizeof(struct ListNode));
    newnode->val = 0;
    newnode->next = NULL;
    return newnode;
}
struct ListNode* reverseBetween(struct ListNode* head, int left, int right) {
    node temp = create();
    temp->next = head;
    node prev = temp;
    for(int i=1;i<left;i++)
        prev = prev->next;
    node current = prev->next;
    for(int i=0;i<right-left;i++){
        node temp1 = current->next;
        current->next = temp1->next;
        temp1->next = prev->next;
        prev->next = temp1;
    }
    return temp->next;
}
