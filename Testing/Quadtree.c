/* 
Author: Alexa Villaume
Date: July 29th, 2013
Routines needed to build quadtree
Date August 22nd, 2013
Adding functions to calculate distance using RA and DEC values
*/

/* ------- INCLUDES ------- */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
//#include < double.h>
#include "quadtree.h"
#include "list.h"


/* ------- PROTOTYPES ------- */

node_t *new_node( double xmin,  double ymin,  double xmax,  double ymax);
static void nearer_source(node_t *tree, node_t *node,  double tx,  double ty, box_t *interest, source_t **nearest,  double *dist);
static void subdivide(node_t *node);


/* ------- FUNCTIONS ------- */

node_t *new_quadtree(double xmin, double ymin, double xmax, double ymax) {
    return new_node(xmin, ymin, xmax, ymax);
}

/* Create an empty node */ 
node_t *new_node( double xmin,  double ymin,  double xmax,  double ymax) {
    node_t *node = malloc(sizeof(node_t));
    node->box.xmin = xmin;
    node->box.ymin = ymin;
    node->box.xmax = xmax;
    node->box.ymax = ymax;
    node->xmid = (xmin + xmax)/2;
    node->ymid = (ymin + ymax)/2;
    node->q1 = node->q2 = node->q3 = node->q4 = NULL;
    init_list(&node->contents);
    return node;
}
source_t *new_source(int number, double flux_iso, double fluxerr_iso, double flux_aper,
                     double fluxerr_aper, double x_image, double y_image,
                     double alpha, double delta, double mag_auto, double magerr_auto,
                     double mag_best, double magerr_best, double mag_aper, double magerr_aper,
                     double a_world, double erra_world, double b_world, double errb_world,
                     double theta, double errtheta, double isoarea_img, double mu_max,
                     double flux_radius, int flags, double fwhm, double elongation, 
                     double vignet) {
    source_t *source = malloc(sizeof(source_t));
    source->number = number;
    source->flux_iso = flux_iso;
    source->fluxerr_iso = fluxerr_iso;
    source->flux_aper = flux_aper;
    source->fluxerr_aper = fluxerr_aper;
    source->x_image = x_image;
    source->y_image = y_image;
    source->alpha = alpha;
    source->delta = delta;
    source->mag_auto = mag_auto;
    source->magerr_auto = magerr_auto;
    source->mag_best = mag_best;
    source->magerr_best = magerr_best;
    source->mag_aper = mag_aper;
    source->magerr_aper = magerr_aper;
    source->a_world = a_world;
    source->erra_world  = erra_world;
    source->b_world = b_world;
    source->errb_world  = errb_world;
    source->theta = theta;
    source->errtheta = errtheta;
    source->isoarea_img = isoarea_img;
    source->mu_max = mu_max;
    source->flux_radius = flux_radius;
    source->flags = flags;
    source->fwhm = fwhm;
    source->elongation = elongation;
    source->vignet = vignet;
    return source;
}


void free_source(source_t *source) {
    free(source);
}

/* INSERT */

void insert_source(node_t *node, source_t *source) {
    node_t *quadrant;
    // Check if the MAX has been reached
    if (node->contents.length == MAX)
        subdivide(node);    

    // A node in the tree will be filled with either content or sub
    // quadrants. Check to see whether subquads exist.
    if (node->q1 != NULL) {

        if (source->alpha >= node->xmid) {
            if (source->delta >= node->ymid)
                quadrant = node->q1;
            else
                quadrant = node->q4;
        } else {
            if (source->delta >= node->ymid)
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

static void subdivide(node_t *node) {
    source_t *source;

    // Divide up the node
    node->q1 = new_node(node->xmid, node->ymid, node->box.xmax, node->box.ymax);
    node->q2 = new_node(node->box.xmin, node->ymid, node->xmid, node->box.ymax);
    node->q3 = new_node(node->box.xmin, node->box.ymin, node->xmid, node->ymid);
    node->q4 = new_node(node->xmid, node->box.ymin, node->box.xmax, node->ymid);

    while ((source = pop(&node->contents)))
        insert_source(node, source);
}

/* SEARCH */

source_t *nearest_source(node_t *tree,   double x,   double y) {
    source_t *nearest = NULL;
      double dist;
    box_t interest;

    dist = dblmin(tree->box.xmax - tree->box.xmin, tree->box.ymax - tree->box.ymin) / 100.0;
    interest.xmin = x - dist;
    interest.ymin = y - dist;
    interest.xmax = x + dist;
    interest.ymax = y + dist;
    clip_box(&interest, &tree->box);
    dist = dist * dist;

    if (debug) {
        printf("nearest_source: \n");
        printf("  target (%0.2f, %0.2f)\n", x, y);
        printf("  interest (%0.4f, %0.4f) (%0.4f, %0.4f)\n", 
                interest.xmin, interest.ymin, interest.xmax, interest.ymax);
    }

    nearer_source(tree, tree, x, y, &interest, &nearest, &dist);

    if (debug)
        printf("\n");

    return nearest;
}

/* Look for the nearest source to the target
node         -- Place that we're searching
target       -- source we're looking for
interest     -- the area of interest
nearest      -- the current nearest match
dist         -- distance to current nearest match */
static void nearer_source(node_t *tree, node_t *node,   double tx,    double ty, box_t *interest, source_t **nearest,  double *dist) {
    source_t *s;
     double s_dist;

    if (debug) {
        printf("nearer_source: (%0.4f, %0.4f) (%0.4f, %0.4f)\n", 
               node->box.xmin, node->box.ymin, node->box.xmax, node->box.ymax);
    }

    // Check if the node interesects with the area of interest
    if (intersecting(&node->box, interest)) {
        // If the node has no children run through the compares
        if (node->q1 == NULL) {
            if (debug)
                printf("  intersection with leaf\n");
            for (s = (source_t *)node->contents.first; s != NULL; s = (source_t *)s->links.next) {
                s_dist = norm(s->alpha, s->delta, tx, ty);
                if (debug)
                    printf("  comparing (%0.2f, %0.2f) dist %0.4f", s->alpha, s->delta, s_dist);
                if (s_dist < *dist) {
                    *nearest = s;
                    *dist = s_dist;

                    s_dist = sqrt(s_dist);  // actual distance
                    interest->xmin = tx - s_dist;
                    interest->ymin = ty - s_dist;
                    interest->xmax = tx + s_dist;
                    interest->ymax = ty + s_dist;
                    clip_box(interest, &tree->box);

                    if (debug) {
                        printf("  -- new nearest: dist %0.4f box (%0.4f, %0.4f) (%0.4f, %0.4f)",
                            s_dist, interest->xmin, interest->ymin, interest->xmax, interest->ymax);
                    }
                }
                if (debug)
                    printf("\n");
            }   
        } else {
            if (debug)
                printf("  intersection, checking children\n");
            // If the node has children, recurse through the
            // tree by calling nearer_source on each of the children
            nearer_source(tree, node->q1, tx, ty, interest, nearest, dist);
            nearer_source(tree, node->q2, tx, ty, interest, nearest, dist);
            nearer_source(tree, node->q3, tx, ty, interest, nearest, dist);
            nearer_source(tree, node->q4, tx, ty, interest, nearest, dist);
        }
    } else {
        if (debug)
            printf("  no intersection\n");
    }
}


/* USEFUL GEOMETRY */

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


//long  double angular_dist(long double x1, long double y1, long double x2, long double y2) {
//	return angular_dist2(norm2(x1, y1, x2, y2));
//}

//long  double angular_dist2(long double x1, long double y1,long double x2, long double y2) {
	/* Simplified Law of Cosines
//	 gamma = ((RA1 - RA2)cos(DEC1))^2 + (DEC1 - DEC2)^2 */
//	long double a = ((x1-x2)*cos(y1))*((x1-x2)*cos(y1));
//	long double b = (y1-y2)*(y1-y2);
//	return a + b;	

	/* Law of Cosines */
//	double a = sin(y1)*sin(y2);
//	double b = cos(y1)*cos(y2)*cos(x2-x1);
//	return acos(a + b);
//}

double norm(double x1, double y1, double x2, double y2) {
    return sqrt(norm2(x1, y1, x2, y2));
}

double norm2(double x1, double y1, double x2, double y2) {
    double xd = x2 - x1;
    double yd = y2 - y1;
    return xd * xd + yd * yd;
}

double dblmax(double a, double b) {
    return a > b ? a : b;
}

double dblmin(double a, double b) {
    return a < b ? a : b;
}

void clip_box(box_t *b, box_t *bounds) {
    b->xmin = dblmax(b->xmin, bounds->xmin);
    b->ymin = dblmax(b->ymin, bounds->ymin);
    b->xmax = dblmin(b->xmax, bounds->xmax);
    b->ymax = dblmin(b->ymax, bounds->ymax);
}


/* DEBUG */

void print_node(node_t *node, int indent_count) {
    char indent[100];
    int i;
    source_t *source;

    for (i = 0; i < indent_count; ++i)
       indent[i] = ' ';
    indent[i] = '\0';
    
    printf("%sxmin %0.4f, ymin %0.4f, xmax %0.4f, ymax %0.4f\n",     indent, node->box.xmin, node->box.ymin, node->box.xmax, node->box.ymax);
    for (source = (source_t *)node->contents.first; source != NULL; source = (source_t *)source->links.next) {
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
    printf("Mag: %f, Source (%0.2f, %0.2f)\n", s->mag_aper, s->alpha, s->delta);
}
