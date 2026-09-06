/**
 * Definition for a Node.
 * struct Node {
 *     int val;
 *     struct Node *next;
 *     struct Node *random;
 * };
 */
typedef struct Node *node;

node create(int val) {
    node newnode = (node)malloc(sizeof(struct Node));
    newnode->val = val;
    newnode->next = NULL;
    newnode->random = NULL;
    return newnode;
}

struct Node* copyRandomList(struct Node* head) {
    if (head == NULL)
        return NULL;

    node curr = head;

    while (curr != NULL) {
        node newnode = create(curr->val);
        newnode->next = curr->next;
        curr->next = newnode;
        curr = newnode->next;
    }
    curr = head;
    while (curr != NULL) {
        if (curr->random != NULL)
            curr->next->random = curr->random->next;

        curr = curr->next->next;
    }
    curr = head;
    node newhead = head->next;
    while (curr != NULL) {
        node copy = curr->next;
        curr->next = copy->next;
        if (copy->next != NULL)
            copy->next = copy->next->next;

        curr = curr->next;
    }
    return newhead;
}