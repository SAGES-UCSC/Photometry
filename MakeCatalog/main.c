/* ====================================================================================

Author: Alexa Villaume
To Compile: gcc -a list.c quadtree.c main.c
To Execute: ./a.out <catalog1> <catalog2> <catalog2>
====================================================================================== */

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

int debug = 1;


/*  ------- FUNCTIONS ------- */

int main(int argc, char **argv) {
    printf("started program\n");
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
    //printf("filling list\n");
	//list1 = fill_list(name1);
    printf("filling first quadtree\n");
	quadtree2 = fill_quadtree(name2);
    printf("filling second quadtree\n");
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
    out = fopen("MatchedCatalog.txt", "w");

    while ((source = pop(list))) {
        fprintf(out, "%6d %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %14.4lf %6d %14.4lf %14.4lf %14.4lf %14.4lf\n", 
                source->number, source->flux_iso, source->fluxerr_iso, source->flux_aper,
                source->fluxerr_aper, source->x_image, source->y_image, source->alpha, 
                source->delta, source->mag_auto, source->magerr_auto, source->mag_best, 
                source->magerr_best, source->mag_aper, source->a_world, source->erra_world,
                source->b_world, source->errb_world, source->theta, source->errtheta, 
                source->isoarea_img, source->mu_max, source->flux_radius, source->flags,
                source->fwhm, source->elongation, source->match2->mag_aper, source->match3->mag_aper);
    }
    fclose(out);
}

/* Traverse the list, pop the sources off the tree and compare to the points in 
the tree. Add any matched points to the matchlist */
list_t *associate(list_t *list1, node_t *tree2, node_t *tree3) {
    source_t *match2, *match3, *target;
    list_t *matchlist = new_list();

int x = 0;    
    while ((target = pop(list1))) {
        match2 = nearest_source(tree2, target->alpha, target->delta);
        if (match2 != NULL && norm2(match2->alpha, match2->delta, target->alpha, target->delta) <= MAXDIST) {
            match3 = nearest_source(tree3, target->alpha, target->delta);
            if (match3 != NULL && norm2(match3->alpha, match3->delta, target->alpha, target->delta) <= MAXDIST) {
                target->match2 = match2;
                target->match3 = match3;
                push(matchlist, target);
                continue;
            }
        }
        free_source(target);
//	if (x % 10 == 0) printf("%d\n", x);
		x++;
    }
    return matchlist;
}

node_t *fill_quadtree(char *name) {
    FILE *in;

    double flux_iso, fluxerr_iso, flux_aper, fluxerr_aper;
	double mag_auto, magerr_auto, mag_best, magerr_best, mag_aper, magerr_aper;
    long double x_image, y_image, alpha, delta;
    double a_world, erra_world, b_world, errb_world;
    double theta, errtheta, isoarea_img, mu_max, flux_radius;
    int number, flags;
    double fwhm, elongation;

    // Eventually want to fill in the dimension of the tree from 
    // the header
    node_t *quadtree = new_quadtree(0, 0, 200, 20);
    in = fopen(name, "r");
    
    // Fill the quadtree from the input file
    while (!feof(in)) {
        fscanf(in, "%d %lf %lf %lf %lf %LG %LG %LG %LG %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %d %lf %lf", 
				&number, &flux_iso, &fluxerr_iso, &flux_aper, &fluxerr_aper, 
                &x_image, &y_image, &alpha, &delta, &mag_auto, &magerr_auto, &mag_best, &magerr_best,
                &mag_aper, &magerr_aper, &a_world, &erra_world, &b_world, &errb_world, &theta, &errtheta, 
                &isoarea_img, &mu_max, &flux_radius, &flags, &fwhm, &elongation );
        insert_source(quadtree, new_source(number, flux_iso, fluxerr_iso, flux_aper, fluxerr_aper, 
                        x_image, y_image, alpha, delta, mag_auto, magerr_auto, mag_best, magerr_best, mag_aper,
                        magerr_aper, a_world, erra_world, b_world, errb_world, theta, errtheta, isoarea_img, 
                        mu_max, flux_radius, flags, fwhm, elongation));
    }
    fclose(in);
    return quadtree;
}

list_t *fill_list(char *name) {
    FILE *in;
	FILE *out;
    
    int count;

    double flux_iso, fluxerr_iso, flux_aper, fluxerr_aper;
	double mag_auto, magerr_auto, mag_best, magerr_best, mag_aper, magerr_aper;
    long double x_image, y_image, alpha, delta;
    double a_world, erra_world, b_world, errb_world;
    double theta, errtheta, isoarea_img, mu_max, flux_radius;
    int number, flags;
    double fwhm, elongation;

    list_t *list;

    list = new_list();
    in = fopen(name, "r");
    
    // Fill the list from the input file
    while (!feof(in)) {
        fscanf(in, "%d %lf %lf %lf %lf %LG %LG %LG %LG %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %lf %d %lf %lf", 
				&number, &flux_iso, &fluxerr_iso, &flux_aper, &fluxerr_aper, 
                &x_image, &y_image, &alpha, &delta, &mag_auto, &magerr_auto, &mag_best, &magerr_best,
                &mag_aper, &magerr_aper, &a_world, &erra_world, &b_world, &errb_world, &theta, &errtheta, 
                &isoarea_img, &mu_max, &flux_radius, &flags, &fwhm, &elongation);
        push(list, new_source(number, flux_iso, fluxerr_iso, flux_aper, fluxerr_aper, x_image, y_image, 
                 alpha, delta, mag_auto, magerr_auto, mag_best, magerr_best, mag_aper, magerr_aper, a_world, 
                 erra_world, b_world, errb_world, theta, errtheta, isoarea_img, mu_max, flux_radius, flags,
                 fwhm, elongation));
    }

    fclose(in);
    return list;
}
