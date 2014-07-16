/*
Writing a Python wrapper for the C quadtree code 
*/

#include <Python.h>
#include <numpy/arrayobject.h>
#include "Quadtree.h"

static char module_docstring[] = 
    "Python interface for C implementation of a Quadtree";

static char new_quadtree_docstring[] =
    "Initilizing the quadtree in C given boundaries.";

static char insert_source_docstring[] =
    "Insert source objects into the tree, organizing by x and y position.";

static char nearest_source_docstring[] =
    "Given a point, find the nearest source.";

static PyObject *Quadtree_new_quadtree(PyObject *self, PyObject *args);
static PyObject *Quadtree_insert_source(PyObject *self, PyObject *args);
static PyObject *Quadtree_nearest_source(PyObject *self, PyObject *args);

/* Need to do this for all functions? */
static PyMethodDef module_methods[] = {
    {"new_quadtree", Quadtree_new_quadtree, METH_VARARGS, new_quadtree_docstring},
    {"insert_source", Quadtree_insert_source, METH_VARARGS, insert_source_docstring},
    {"nearest_source", Quadtree_nearest_source, METH_VARARGS, nearest_source_docstring},
    {NULL, NULL, 0, NULL}
};

/* Need to do this just for Quadtree/or all functions? */
PyMODINIT_FUNC init_Quadtree(void) {
    PyObject *m = Py_InitModule3("_Quadtree", module_methods, module_docstring);
    
    if (m == NULL)
        return;

    /* Load 'numpy' functionality. */
    import_array();
}

static PyObject *Quadtree_new_quadtree(PyObject *self, PyObject *args) {
    double xmin, ymin, xmax, ymax;
    
    if (!PyArg_ParseTuple(args, "dddd", &xmin, &ymin, &xmax, &ymax))
        return NULL;

    node_t *tree = new_quadtree(xmin, ymin, xmax, ymax);
    
    /* Return a PyObject to Python */
    return Py_BuildValue("O", tree);
}

static PyObject *Quadtree_insert_source(PyObject *self, PyObject *args) {
    PyObject *node_obj, *source_obj;

    if (!PyArg_ParseTuple(args, "OO", &node_obj, &source_obj))
        return NULL;

    PyObject *node_array = PyArray_FROM_OTF(node_obj, NPY_DOUBLE, NPY_IN_ARRAY);
    PyObject *source_array = PyArray_FROM_OTF(source_obj, NPY_DOUBLE, NPY_IN_ARRAY);

    if (node_array == NULL || source_array == NULL) {
        Py_XDECREF(node_array);
        Py_XDECREF(source_array);
    }

    node_t *node = (node_t*)PyArray_DATA(node_array);
    source_t *source = (source_t*)PyArray_DATA(source_array);

    // Don't know if this is right.
    insert_source(node, source);

    /* Clean up. Something wrong with the implicit declaration? */
    Py_DECREF(node_array);
    Py_DECREF(source_array);

    // Don't know if this is right.
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject *Quadtree_nearest_source(PyObject *self, PyObject *args) {
    double x, y;
    PyObject *tree_obj;

    if (!PyArg_ParseTuple(args, "Odd", &tree_obj, &x, &y))
        return NULL;

    PyObject *tree_array = PyArray_FROM_OTF(tree_obj, NPY_DOUBLE, NPY_IN_ARRAY);

    if (tree_array == NULL) {
        Py_XDECREF(tree_array);
    }
    
    node_t *tree = (node_t*)PyArray_DATA(tree_array);
    
    source_t *source = nearest_source(tree, x, y);
    
    Py_DECREF(tree_array);

    return Py_BuildValue("O", source);
}
