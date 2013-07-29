#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <math.h>
#include <quadtree.h>
#include <quadtree.c>

/* ------- CONSTANTS ------- */

#define MAX  10
#define MAXDIST 10 // Arbitrary for now

/* ------- TYPES ------- */

typedef struct box_t {
    double xmin, ymin, xmax, ymax;
} box_t;


/* ------- PROTOTYPES ------- */

source_t *new_source(int num, double mag, double mag_err, double size, double x, double y, int flag);
int intersecting(box_t *box1, box_t *box2);
double norm2(double x1, double y1, double x2, double y2);
double norm(double x1, double y1, double x2, double y2);
source_t *nearest_source(node_t *node, double x, double y);
void nearer_source(node_t *node, double tx, double ty, box_t *interest, source_t **nearest, double *dist);
list_t *associate(list_t *list1, node_t *tree2, node_t *tree3); 
void print_node(node_t *node, int indent_count);
void print_source(source_t *s);
void free_source(source_t *source);
void write_list(list_t *list);

/* -------------------- GLOBALS ------------------- */
 int debug = 0;									

/*  ------- FUNCTIONS ------- */

source_t *new_source(int num, double mag, double mag_err, double size,
				 	 double x, double y, int flag) {
    source_t *source = malloc(sizeof(source_t));
    source->num = num;
	source->mag = mag;
	source->mag_err = mag_err;
	source->size = size;
    source->x = x;
    source->y = y;
	source->flag = flag; 
    return source;
}

int intersecting(box_t *b1, box_t *b2) {
    if ((b1->xmin >= b2->xmin && b1->xmin < b2->xmax) ||
        (b1->xmax >= b2->xmin && b1->xmax < b2->xmax) ||
        (b1->xmin <= b2->xmin && b1->xmax >= b2->xmax) ||
        (b1->xmin >= b2->xmin && b1->xmax <= b2->xmax)) {

        if ((b1->ymin >= b2->ymin && b1->ymin < b2->ymax) ||
            (b1->ymax >= b2->ymin && b1->ymax < b2->ymax) ||
            (b1->ymin <= b2->ymin && b1->ymax >= b2->ymax) ||
            (b1->ymin >= b2->ymin && b1->ymax <= b2->ymax)) {

            return 1;

        }
    }

    return 0;
}

double norm2(double x1, double y1, double x2, double y2) {
    double xd = x2 - x1;
    double yd = y2 - y1;
    return xd * xd + yd * yd;
}

double norm(double x1, double y1, double x2, double y2) {
	return sqrt(norm2(x1, y1, x2, y2));
}

void free_source(source_t *source) {
	free(source);
}

source_t *nearest_source(node_t *node, double x, double y) {
    source_t *nearest = NULL;
    box_t interest;
    double error;
    double dist;

    error = 2;
    interest.xmin = x - error;
    interest.ymin = y - error;
    interest.xmax = x + error;
    interest.ymax = y + error;

    if (debug) {
        printf("nearest_source: \n");
        printf("  x, y = %0.2f, %0.2f\n", x, y);
        printf("  interest = xmin %0.4f, ymin %0.4f, xmax %0.4f, ymax %0.4f\n", 
			    interest.xmin, interest.ymin, interest.xmax, interest.ymax);
    }

    dist = DBL_MAX;
    nearer_source(node, x, y, &interest, &nearest, &dist);

	return nearest;
}

/* Look for the nearest source to the target
node         -- Place that we're searching
target       -- source we're looking for
interest     -- the area of interest
nearest      -- the current nearest match
dist         -- distance to current nearest match */
void nearer_source(node_t *node, double tx, double ty, box_t *interest, source_t **nearest, double *dist) {
    source_t *s;
    double s_dist;

    if (debug) {
        printf("nearer_source: \n");
        printf("  xmin %0.4f, ymin %0.4f, xmax %0.4f, ymax %0.4f\n", 
			   node->box.xmin, node->box.ymin, node->box.xmax, node->box.ymax);
    }

    // Check if the node interesects with the area of interest
    if (intersecting(&node->box, interest)) {
        // If the node has no children run through the compares
        if (node->q1 == NULL) {
            if (debug)
                printf(" intersection with leaf\n");
            for (s = node->contents.first; s != NULL; s = s->next) {
                s_dist = norm2(s->x, s->y, tx, ty);
                if (debug)
                    printf("  comparing (%0.2f, %0.2f) dist %0.4f", s->x, s->y, s_dist);
                if (s_dist < *dist) {
                    *nearest = s;
                    *dist = s_dist;
                    if (debug)
                        printf("  -- new nearest");
                }
                if (debug)
                    printf("\n");
            }   
        } else {
            if (debug)
                printf(" intersection, checking children\n");
            // If the node has children, recurse through the
            // tree by calling nearer_source on each of the children
            nearer_source(node->q1, tx, ty, interest, nearest, dist);
            nearer_source(node->q2, tx, ty, interest, nearest, dist);
            nearer_source(node->q3, tx, ty, interest, nearest, dist);
            nearer_source(node->q4, tx, ty, interest, nearest, dist);
        }
    } else {
        if (debug)
            printf("  no intersection\n");
    }
}

/* Write a list to file */
void write_list(list_t *list) {
	source_t *source;
	FILE *out;
	out = fopen("MatchedCatalog.txt", "w+");

	fprintf(out, "%5s %20s %20s %20s %20s %20s %20s %25s", "Source", "Magnitude 1", "Error", 
			"Size", "X_pos", "Y_pos","Magnitude 2", "Magnitude 3");
	while ((source = pop(list))) {
		fprintf(out, "%5d %20f %20f %20f %20f %20f %20f %25f", source->num, source->mag, 
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
			} else 
				free_source(target);
		} else 
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
    node_t *quadtree = new_node(0, 0, 11000, 10000);
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

void print_node(node_t *node, int indent_count) {
    char indent[100];
    int i;
    source_t *source;

    for (i = 0; i < indent_count; ++i)
        indent[i] = ' ';
    indent[i] = '\0';
    
    printf("%sxmin %0.4f, ymin %0.4f, xmax %0.4f, ymax %0.4f\n", 
	indent, node->box.xmin, node->box.ymin, node->box.xmax, node->box.ymax);
    for (source = node->contents.first; source != NULL; source = source->next) {
        printf("%s", indent);
        print_source(source);
    }
    if (node->q1 != NULL) {
        printf("%sq1:\n", indent);
        print_node(node->q1, indent_count + 4);
        printf("%sq2:\n", indent);
        print_node(node->q2, indent_count + 4);
        printf("%sq3:\n", indent);
        print_node(node->q3, indent_count + 4);
        printf("%sq4:\n", indent);
        print_node(node->q4, indent_count + 4);
    }
}

void print_source(source_t *s) {
    printf("source num %d, (%0.2f, %0.2f)\n", s->num, s->x, s->y);
}

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

}


