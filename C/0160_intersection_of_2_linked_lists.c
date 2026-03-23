/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     struct ListNode *next;
 * };
 */
typedef struct ListNode *node;
struct ListNode *getIntersectionNode(struct ListNode *headA, struct ListNode *headB) {
    if(headA==NULL || headB==NULL)
        return NULL;
    node a = headA;
    node b = headB;
    while(a!=b){
        if(a==NULL)
            a = headB;
        else
            a = a->next;
            
        if(b==NULL)
            b = headA;
        else
            b = b->next;
    }

    return b;
}
