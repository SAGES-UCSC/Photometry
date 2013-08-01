/* ------- INCLUDES ------- */

#include <stdio.h>
#include <stdlib.h>
#include "quadtree.h"
#include "list.h"

/* ------- PROTOTYPES ------- */

list_t *associate(list_t *list1, node_t *tree2, node_t *tree3); 
void write_list(list_t *list);
node_t *fill_quadtree(char *name);
list_t *fill_list(char *name);


/* ------- GLOBALS ------- */

int debug = 0;


/*  ------- FUNCTIONS ------- */

int main(int argc, char **argv) {
    int i;
    double x, y;
    source_t *s;
	
	list_t *list1, *matchlist;
	node_t *quadtree2, *quadtree3;
	char *name1, *name2, *name3;

    /* Simple error handling */
    if (argc != 4) {
        printf("Need three input catalogs.\n");
        printf("Please see the readme file for instructions.\n");
        exit(EXIT_FAILURE);
    }

	name1 = argv[1];
	name2 = argv[2];
	name3 = argv[3];

	// Read in the source extractor results and sort into the tree
	list1 = fill_list(name1);
	quadtree2 = fill_quadtree(name2);
	quadtree3 = fill_quadtree(name3);

	// Make list of common elements
	matchlist = associate(list1, quadtree2, quadtree3);	

	// Write out the matched list
	write_list(matchlist);

    return EXIT_SUCCESS;
}

/* Write a list to file */
void write_list(list_t *list) {
    source_t *source;
    FILE *out;
    out = fopen("MatchedCatalog.txt", "w+");

    fprintf(out, "%6s %14s %14s %14s %18s %18s %14s %14s\n", "Source", "Magnitude 1", "Error", 
            "Size", "X_pos", "Y_pos","Magnitude 2", "Magnitude 3");
    while ((source = pop(list))) {
        fprintf(out, "%6d %14.4f %14.4f %14.4f %18.4f %18.4f %14.4f %14.4f\n", source->num, source->mag, 
                        source->mag_err, source->size, source->x, source->y,
                        source->match2->mag, source->match3->mag);

    }
    fclose(out);
}

/* Traverse the list, pop the sources off the tree and compare to the points in 
the tree. Add any matched points to the matchlist */
list_t *associate(list_t *list1, node_t *tree2, node_t *tree3) {
    source_t *match2, *match3, *target;
    list_t *matchlist = new_list();
    
    while ((target = pop(list1))) {
        match2 = nearest_source(tree2, target->x, target->y);
        if (match2 != NULL && norm(match2->x, match2->y, target->x, target->y) <= MAXDIST) {
            match3 = nearest_source(tree3, target->x, target->y);
            if (match3 != NULL && norm(match3->x, match3->y, target->x, target->y) <= MAXDIST) {
                target->match2 = match2;
                target->match3 = match3;
                push(matchlist, target);
                continue;
            }
        }
        free_source(target);
    }
    return matchlist;
}

node_t *fill_quadtree(char *name) {
    FILE *in;
    int num;
    float mag, mag_err;
    float size;
    float x, y;
    int flag;

    // Eventually want to fill in the dimension of the tree from 
    // the header
    node_t *quadtree = new_quadtree(0, 0, 11000, 10000);
    in = fopen(name, "r");
    
    // Fill the quadtree from the input file
    while (!feof(in)) {
        fscanf(in, "%d %f %f %f %f %f %d", &num, &mag, &mag_err, &size, &x, &y, &flag);
        if (mag != 99.0)
            insert_source(quadtree, new_source(num, mag, mag_err, size, x, y, flag));
    }
    fclose(in);
    return quadtree;
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
