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
struct ListNode* mergeTwoLists(struct ListNode* head1, struct ListNode* head2) {
    node head3 = NULL;
    node temp = NULL;
    while(head1!=NULL && head2!=NULL){
        node newnode;
        if(head1->val <= head2->val){
            newnode = create(head1->val);
            head1 = head1->next;
        }
        else{
            newnode = create(head2->val);
            head2 = head2->next;
        }
        if(head3==NULL){
            head3 = newnode;
            temp = newnode;
        }
        else{
            temp->next = newnode;
            temp = newnode;
        }
    }

    while(head1!=NULL){
        node newnode = create(head1->val);
        if(head3==NULL){
            head3 = newnode;
            temp = newnode;
        }
        else{
            temp->next = newnode;
            temp = newnode;
        }
        head1 = head1->next;
    }

    while(head2!=NULL){
        node newnode = create(head2->val);
        if(head3==NULL){
            head3 = newnode;
            temp = newnode;
        }
        else{
            temp->next = newnode;
            temp = newnode;
        }
        head2 = head2->next;
    }

    return head3;
    
}
