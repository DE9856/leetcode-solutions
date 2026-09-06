/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
typedef struct ListNode *node;

void reorderList(struct ListNode* head) {
    if(head==NULL || head->next==NULL)
        return;
    node slow = head;
    node fast = head;
    while(fast->next!=NULL && fast->next->next!=NULL){
        slow = slow->next;
        fast= fast->next->next;
    }

    node curr = slow->next;
    slow->next=NULL;
    node prev = NULL;
    while(curr!=NULL){
        node next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    node first = head;
    node second = prev;

    while(second!=NULL){
        node temp1 = first->next;
        node temp2 = second->next;
        first->next = second;
        second->next = temp1;
        first = temp1;
        second = temp2;
    }
}
