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
struct ListNode* deleteDuplicates(struct ListNode* head) {
    if(head==NULL || head->next==NULL)
        return head;
    node temp = create();
    temp->next = head;
    node prev = temp;
    node curr = head;
    while(curr!=NULL){
        if(curr->next!=NULL && curr->val == curr->next->val){
            int value = curr->val;
            while(curr!=NULL && curr->val == value)
                curr = curr->next;
            prev->next = curr;
        }
        else{
            prev = curr;
            curr = curr->next;
        }
    }
    node sol = temp->next;
    free(temp);
    return sol;
}
