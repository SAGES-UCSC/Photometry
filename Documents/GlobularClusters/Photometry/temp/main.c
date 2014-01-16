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
node_t *new_node(double xmin, double ymin, double xmax, double ymax);


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

    fprintf(out, "# %16s %16s %16s %16s %16s %16s %16s %16s %16s %8s %16s %16s %16s\n", "Flux Aper", "G' Mag", "Mag Aper Error", "X_image", "Y_Image",
                "X_world", "Y_world", "Alpha", "Delta", "Ellipticity", "FWHM_Image", "FWHM_World", "Flags", "Class Star",
                "R' Mag", "I' Mag");
    while ((source = pop(list))) {
        fprintf(out, "%14.4f %14.4f %14.4f %14.4f %14.4f %14.4f %14.4f %14.4f %14.4f %14.4f %14.4f %14.4f %6d %14.4f %14.4f %14.4f\n",
                        source->flux_aper, source->mag_aper, source->magerr_aper,
                        source->x_image, source->y_image, source->x_world, source->y_world, source->alpha,
                        source->delta, source->ellipticity, source->fwhm_image, source->fwhm_world,
                        source->flags, source->class_star, source->match2->mag_aper, source->match3->mag_aper);

    }


    fclose(out);
}

/* Traverse the list, pop the sources off the tree and compare to the points in 
the tree. Add any matched points to the matchlist */
list_t *associate(list_t *list1, node_t *tree2, node_t *tree3) {
    source_t *match2, *match3, *target;
    list_t *matchlist = new_list();
    
    while ((target = pop(list1))) {
        match2 = nearest_source(tree2, target->x_world, target->y_world);
        if (match2 != NULL && norm(match2->x_world, match2->y_world, target->x_world, target->y_world) <= MAXDIST) {
            match3 = nearest_source(tree3, target->x_world, target->y_world);
//DEBUG
if (match3 != NULL) printf("hello\n"); 
           
			if (match3 != NULL && norm(match3->x_world, match3->y_world, target->x_world, target->y_world) <= MAXDIST) {
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
	float flux_aper, mag_aper, magerr_aper;
    float x_image, y_image, x_world, y_world;
    float alpha, delta;
    float ellipticity;
    float fwhm_image, fwhm_world;
    int flags;
    float class_star;
    // Eventually want to fill in the dimension of the tree from 
    // the header
    node_t *quadtree = new_node(0, 0, 11000, 10000);
    in = fopen(name, "r");

    // Fill the quadtree from the input file
    while (!feof(in)) {
        fscanf(in, "%f %f %f %f %f %f %f %f %f %f %f %f %d %f", &flux_aper, &mag_aper, &magerr_aper,
                    &x_image, &y_image, &x_world, &y_world, &alpha, &delta, &ellipticity, &fwhm_image,
                    &fwhm_world, &flags, &class_star);
        if (mag_aper != 99.0)
            insert_source(quadtree, new_source(flux_aper, mag_aper, magerr_aper, x_image, y_image, x_world, y_world,
                    alpha, delta, ellipticity, fwhm_image, fwhm_world, flags, class_star));
    }
    fclose(in);


    return quadtree;
}

list_t *fill_list(char *name) {
    FILE *in;
    float flux_aper, mag_aper, magerr_aper;
    float x_image, y_image, x_world, y_world;
    float alpha, delta;
    float ellipticity;
    float fwhm_image, fwhm_world;
    int flags;
    float class_star;
    list_t *list;
    list = new_list();
    in = fopen(name, "r");

    // Fill the list from the input file
    while (!feof(in)) {
        fscanf(in, "%f %f %f %f %f %f %f %f %f %f %f %f %d %f", &flux_aper, &mag_aper, &magerr_aper,
                    &x_image, &y_image, &x_world, &y_world, &alpha, &delta, &ellipticity, &fwhm_image,
                    &fwhm_world, &flags, &class_star);
        if (mag_aper != 99.0)
            push(list, new_source(flux_aper, mag_aper, magerr_aper, x_image, y_image, x_world, y_world,
                    alpha, delta, ellipticity, fwhm_image, fwhm_world, flags, class_star));
    }

    fclose(in);
    return list;
}
