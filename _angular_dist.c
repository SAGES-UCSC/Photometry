#include <Python.h>
#include "angular_dist.h"

static char module_docstring[] = 
    "This module provides an interface for computing the angular distance using C.";
static char angular_dist_docstring[] = 
    "Calculate the angular distance between two points";
static char angular_dist2_docstring[] = 
    "Calculate the square angular distance between two points. For efficiency.";

static PyObject *angular_dist_angular_dist(PyObject *self, PyObject *args);

static PyObject *angular_dist_angular_dist2(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
    {"angular_dist", angular_dist_angular_dist, METH_VARARGS, angular_dist_docstring},
    {"angular_dist2", angular_dist_angular_dist2, METH_VARARGS, angular_dist2_docstring},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_angular_dist(void) {
    PyObject *m = Py_InitModule3("_angular_dist", module_methods, module_docstring);
    if (m == NULL)
        return;
}

static PyObject *angular_dist_angular_dist(PyObject *self, PyObject *args) {
    double x1, y1, x2, y2;

    /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "ddOOO", &x1, &y1, &x2, &y2))
        return NULL;

    /* Call the external C function to compute the angular_dist. */
    double value = angular_dist(x1, y1, x2, y2);

    if (value < 0.0) {
        PyErr_SetString(PyExc_RuntimeError, 
                        "angular_dist returned an impossible value.");
    }
    PyObject *ret = Py_BuildValue("d", value);
    return ret;
}

static PyObject *angular_dist_angular_dist2(PyObject *self, PyObject *args) {
    double x1, y1, x2, y2;

    /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "ddOOO", &x1, &y1, &x2, &y2))
        return NULL;

    /* Call the external C function to compute the angular_dist. */
    double value = angular_dist2(x1, y1, x2, y2);

    if (value < 0.0) {
        PyErr_SetString(PyExc_RuntimeError, 
                        "angular_dist2 returned an impossible value.");
    }
    PyObject *ret = Py_BuildValue("d", value);
    return ret;
}
