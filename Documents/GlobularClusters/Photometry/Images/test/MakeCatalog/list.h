/* 
Author: Alexa Villaume
Data: July 29th, 2013
All the types required to make a quadtree 
*/

#ifndef __LIST_H__
#define __LIST_H__

/* ------- TYPES ------- */

typedef struct list_links_t {
    struct list_links_t *next;
} list_links_t;

typedef struct {
    list_links_t *first;
    int length;
} list_t;


/* ------- GLOBALS ------- */

extern int debug;


/* ------- PROTOTYPES ------- */

list_t *new_list(void);
void init_list(list_t *list);
void free_list(list_t *list);
void push(list_t *list, void *elem);
void *pop(list_t *list);

#endif
