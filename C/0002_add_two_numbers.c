/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
typedef struct ListNode *node;
node create(int val){
    node newnode = (node)malloc(sizeof(struct ListNode));
    newnode-> val = val;
    newnode->next = NULL;
    return newnode;
}
struct ListNode* addTwoNumbers(struct ListNode* l1, struct ListNode* l2) {
    node head3 = NULL;
    node temp = NULL;
    int carry = 0;

    while(l1!=NULL || l2!=NULL || carry!=0){
        int sum = carry;
        if(l1!=NULL){
            sum+=l1->val;
            l1 = l1->next;
        }
        if(l2!=NULL){
            sum+=l2->val;
            l2 = l2->next;
        }
        carry = sum/10;
        node newnode = create(sum%10);

        if(head3==NULL){
            head3 = newnode;
            temp = newnode;
        }
        else{
            temp->next = newnode;
            temp = temp->next;
        }
    }
    return head3;
    
}
