/*

Author: Alexa Villaume
Data: July 29th, 2013
All the types required to make a quadtree 
*/

#ifndef __QUADTREE_H__
#define __QUADTREE_H__

#include "list.h"

/* ------- CONSTANTS ------- */

#define MAX  10
//Kirsten uses half an arcsec for the matching
#define MAXDIST 0.000000014 

/* ------- TYPES ------- */

typedef struct {
    double xmin, ymin, xmax, ymax;
} box_t;

/* source_t is filled with rowdata and make up the linked lists */
typedef struct source_t {
	list_links_t links;
    struct source_t *next, *prev;
    int number; 
    double flux_iso, fluxerr_iso, flux_aper, fluxerr_aper;
    double x_image, y_image, alpha, delta;
    double mag_auto, magerr_auto, mag_best, magerr_best; 
    double mag_aper, magerr_aper, a_world, erra_world; 
    double b_world, errb_world, theta; 
    double errtheta, isoarea_img, mu_max, flux_radius; 
    int flags;
    double fwhm, elongation, vignet;
    struct source_t *match2, *match3;
} source_t;

/* Nodes are what make up the tree. A node will either have
pointers to children are a linked list of source_t types */
typedef struct node_t {
    box_t box;
    double xmid, ymid;
    struct node_t *q1, *q2, *q3, *q4;
    list_t contents;
} node_t;


/* ------- GLOBALS ------- */

extern int debug;


/* ------- PROTOYPES ------- */

/* making a tree */
node_t *new_quadtree(double xmin, double ymin, double xmax, double ymax);
source_t *new_source(int number, double flux_iso, double fluxerr_iso, double flux_aper, 
                     double fluxerr_aper, double x_image, double y_image, 
                     double alpha, double delta, double mag_auto, double magerr_auto,  
                     double mag_best, double magerr_best, double mag_aper, double magerr_aper,   
                     double a_world, double erra_world, double b_world, double errb_world,   
                     double theta, double errtheta, double isoarea_img, double mu_max,  
                     double flux_radius, int flags, double fwhm, double elongation, double vignet);

void insert_source(node_t *node, source_t *source);

void free_source(source_t *source);

/* searching */
source_t *nearest_source(node_t *quadtree, double x, double y);

/* useful geometry */
int intersecting(box_t *b1, box_t *b2);
double norm(double x1, double y1, double x2, double y2);
double norm2(double x1, double y1, double x2, double y2);
long double angular_dist(long double x1, long double y1, long double x2, long double y2);
long double angular_dist2(long double x1, long double y1, long double x2,long  double y2);
double dblmin(double a, double b);
double dblmax(double a, double b);
void clip_box(box_t *b, box_t *bounds);

/* for debugging */
void print_node(node_t *node, int indent_count);
void print_source(source_t *s);

#endif
