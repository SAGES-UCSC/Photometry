/* 
Author: Alexa Villaume
Date: July 29th, 2013
Routines needed to build quadtree
*/

#include <stdio.h>
#include <stdlib.h>
#include <quadtree.h>

/* Remove source from a list. */
source_t *pop(list_t *list) {
    source_t *source = list->first;
    if (source != NULL) {
        list->first = list->first->next;
        list->length -= 1;
    }
    return source;
}

/* Add a source to a list */
void push(list_t *list, source_t *source) {
    source->next = list->first;
    list->first = source;
    list->length += 1;
}

/* Create an empty node apart from it's boundaries. At some point 
need to fill with rowdata */ 
node_t *new_node(double xmin, double ymin, double xmax, double ymax) {
    node_t *node = malloc(sizeof(node_t));
    node->box.xmin = xmin;
    node->box.ymin = ymin;
    node->box.xmax = xmax;
    node->box.ymax = ymax;
    node->xmid = (xmin + xmax)/2;
    node->ymid = (ymin + ymax)/2;
    node->q1 = node->q2 = node->q3 = node->q4 = NULL;   
    node->contents.first = NULL;
    node->contents.length = 0;
    return node;
}

void insert_source(node_t *node, source_t *source) {
    node_t *quadrant;
    
    // Check if the MAX has been reached
    if (node->contents.length == MAX)
        subdivide(node);    

    // A node in the tree will be filled with either content or sub
    // quadrants. Check to see whether subquads exist.
    if (node->q1 != NULL) {

        if (source->x >= node->xmid) {
            if (source->y >= node->ymid)
                quadrant = node->q1;
            else
                quadrant = node->q4;
        } else {
            if (source->y >= node->ymid)
                quadrant = node->q2;
            else
                quadrant = node->q3;
        }
        insert_source(quadrant, source);

    } else {    
        // If no subquads exist add source to the list in contents element 
        // Use push() to prepend the source on the list.
        push(&node->contents, source);
    }
}

list_t *new_list(void) {
    list_t *list = malloc(sizeof(list_t));
	list->first = NULL;
	list->length = 0;

	return list;
}

list_t *fill_list(char *name) {
    FILE *in;
    int num;
    float mag, mag_err;
    float size;
    float x, y;
    int flag;
    list_t *list;

	list = new_list();
    in = fopen(name, "r");
    
    // Fill the list from the input file
    while (!feof(in)) {
        fscanf(in, "%d %f %f %f %f %f %d", &num, &mag, &mag_err, &size, &x, &y, &flag);
        if (mag != 99.0)
            push(list, new_source(num, mag, mag_err, size, x, y, flag));
    }
    fclose(in);
    return list;
}


void subdivide(node_t *node) {
    source_t *source;

    // Divide up the node
    node->q1 = new_node(node->xmid, node->ymid, node->box.xmax, node->box.ymax);
    node->q2 = new_node(node->box.xmin, node->ymid, node->xmid, node->box.ymax);
    node->q3 = new_node(node->box.xmin, node->box.ymin, node->xmid, node->ymid);
    node->q4 = new_node(node->xmid, node->box.ymin, node->box.xmax, node->ymid);

    while ((source = pop(&node->contents)))
        insert_source(node, source);
}
