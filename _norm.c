#include <Python.h>
#include "norm.h"

static char module_docstring[] = 
    "This module provides an interface for computing the norm using C.";
static char norm_docstring[] = 
    "Calculate the norm between two points";
static char norm2_docstring[] = 
    "Calculate the square norm between two points. For efficiency.";

static PyObject *norm_norm(PyObject *self, PyObject *args);

static PyObject *norm_norm2(PyObject *self, PyObject *args);

static PyMethodDef module_methods[] = {
    {"norm", norm_norm, METH_VARARGS, norm_docstring},
    {"norm2", norm_norm2, METH_VARARGS, norm2_docstring},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init_norm(void) {
    PyObject *m = Py_InitModule3("_norm", module_methods, module_docstring);
    if (m == NULL)
        return;
}

static PyObject *norm_norm(PyObject *self, PyObject *args) {
    double x1, y1, x2, y2;

   /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "dddd", &x1, &y1, &x2, &y2))
        return NULL;

    /* Call the external C function to compute the norm. */
    double value = norm(x1, y1, x2, y2);

    if (value < 0.0) {
        PyErr_SetString(PyExc_RuntimeError, 
                        "Norm returned an impossible value.");
    }
    PyObject *ret = Py_BuildValue("d", value);
    return ret;
}

static PyObject *norm_norm2(PyObject *self, PyObject *args) {
    double x1, y1, x2, y2;

   /* Parse the input tuple */
    if (!PyArg_ParseTuple(args, "dddd", &x1, &y1, &x2, &y2))
        return NULL;

    /* Call the external C function to compute the norm. */
    double value = norm2(x1, y1, x2, y2);

    if (value < 0.0) {
        PyErr_SetString(PyExc_RuntimeError, 
                        "Norm2 returned an impossible value.");
    }
    PyObject *ret = Py_BuildValue("d", value);
    return ret;
}
