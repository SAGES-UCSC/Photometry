/* 
Author: Alexa Villaume
Data: July 29th, 2013
All the types required to make a quadtree 
*/


/* source_t is filled with the information that defines the sources */
typedef struct source_t {
    struct source_t *next, *prev;
    int num;
    double mag, mag_err;
    double size;
    double x, y;
    int flag;
    struct source_t *match2, *match3;
} source_t;

/* Lists are found in leaf nodes */
typedef struct {
    source_t *first;
    int length;
} list_t;

/* Nodes are what make up the tree. A node will either have
pointers to children are a linked list of source_t types */
typedef struct node_t {
    box_t box;
    double xmid, ymid;
    struct node_t *q1, *q2, *q3, *q4;
    list_t contents;
} node_t;

void push(list_t *list, source_t *source);
source_t *pop(list_t *list);
node_t *new_node(double xmin, double ymin, double xmax, double ymax);
void insert_source(node_t *node, source_t *source);
list_t *new_list(void);
list_t *fill_list(char *name);
void subdivide(node_t *node);

