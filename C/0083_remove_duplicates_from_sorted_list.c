/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
typedef struct ListNode *node;
struct ListNode* deleteDuplicates(struct ListNode* head) {
    if(head==NULL) return NULL;
    node temp = head;
    while(temp->next !=NULL){
        if(temp->val == temp->next->val){
            node duplicate = temp->next;
            temp->next = duplicate->next;
            free(duplicate);
        }
        else
            temp = temp->next;
    }
    return head;
}
