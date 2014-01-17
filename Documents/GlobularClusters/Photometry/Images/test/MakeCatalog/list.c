/* 
Author: Alexa Villaume
Date: July 29th, 2013
Routines needed to build quadtree
*/

/* ------- INCLUDES ------- */

#include <stdio.h>
#include <stdlib.h>
#include "list.h"

/* ------- FUNCTIONS ------- */

/* Remove elem from a list. */
void *pop(list_t *list) {
    list_links_t *elem = list->first;
    if (elem != NULL) {
        list->first = list->first->next;
        list->length -= 1;
    }
    return elem;
}

/* Add a elem to a list */
void push(list_t *list, void *e) {
    list_links_t *elem = e;
    elem->next = list->first;
    list->first = elem;
    list->length += 1;
}

void init_list(list_t *list) {
    list->first = NULL;
    list->length = 0;    
}

list_t *new_list(void) {
    list_t *list = malloc(sizeof(list_t));
    init_list(list);
	return list;
}

void free_list(list_t *list) {
    free(list);
}
