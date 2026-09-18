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
    newnode->val =0;
    return newnode;
}

node merge(node a, node b){
    node temp = create();
    node current = temp;
    while(a!=NULL && b!=NULL){
        if(a->val <= b->val){
            current->next = a;
            a = a->next;
        }
        else{
            current->next = b;
            b = b->next;
        }
        current = current->next;
    }
    if(a!=NULL)
        current->next = a;
    else
        current->next = b;
    
    temp = temp->next;
    return temp;
}

struct ListNode* mergeKLists(struct ListNode** lists, int listsSize) {
    node sol = NULL;
    for(int i=0;i<listsSize; i++)
        sol = merge(sol, lists[i]);
    return sol;
}
