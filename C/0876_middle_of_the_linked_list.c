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
    newnode-> val = 0;
    newnode->next = NULL;
    return newnode;
}
struct ListNode* middleNode(struct ListNode* head) {
    node temp = head;
    int count = 0;
    while(temp!=NULL){
        count++;
        temp = temp->next;
    }
    int mid = count/2;
    temp = head;
    for(int i=0;i<mid;i++)
        temp = temp->next;

    return temp;

}
