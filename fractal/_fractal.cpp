#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <complex>
#include "numpy/ndarraytypes.h"

typedef struct Range2Di {
    int x1;
    int y1;
    int x2;
    int y2;
} Range2Di;

typedef struct Range2Df {
    float x1;
    float y1;
    float x2;
    float y2;
} Range2Df;

static int convert_range2df(PyObject *obj, Range2Df *addr) {
    if (!PyObject_HasAttrString(obj, "x1")) {
        PyErr_SetString(PyExc_AttributeError, "missing attribute 'x1'");
        return 0;
    }
    if (!PyObject_HasAttrString(obj, "x2")) {
        PyErr_SetString(PyExc_AttributeError, "missing attribute 'x2'");
        return 0;
    }
    if (!PyObject_HasAttrString(obj, "y1")) {
        PyErr_SetString(PyExc_AttributeError, "missing attribute 'y1'");
        return 0;
    }
    if (!PyObject_HasAttrString(obj, "y2")) {
        PyErr_SetString(PyExc_AttributeError, "missing attribute 'y2'");
        return 0;
    }
    addr->x1 = (float) PyFloat_AsDouble(PyObject_GetAttrString(obj, "x1"));
    addr->x2 = (float) PyFloat_AsDouble(PyObject_GetAttrString(obj, "x2"));
    addr->y1 = (float) PyFloat_AsDouble(PyObject_GetAttrString(obj, "y1"));
    addr->y2 = (float) PyFloat_AsDouble(PyObject_GetAttrString(obj, "y2"));

    return 1;
}

static int convert_range2di(PyObject *obj, Range2Di *addr) {
    if (!PyObject_HasAttrString(obj, "x1")) {
        PyErr_SetString(PyExc_AttributeError, "missing attribute 'x1'");
        return 0;
    }
    if (!PyObject_HasAttrString(obj, "x2")) {
        PyErr_SetString(PyExc_AttributeError, "missing attribute 'x2'");
        return 0;
    }
    if (!PyObject_HasAttrString(obj, "y1")) {
        PyErr_SetString(PyExc_AttributeError, "missing attribute 'y1'");
        return 0;
    }
    if (!PyObject_HasAttrString(obj, "y2")) {
        PyErr_SetString(PyExc_AttributeError, "missing attribute 'y2'");
        return 0;
    }
    addr->x1 = (int) PyLong_AsLong(PyObject_GetAttrString(obj, "x1"));
    addr->x2 = (int) PyLong_AsLong(PyObject_GetAttrString(obj, "x2"));
    addr->y1 = (int) PyLong_AsLong(PyObject_GetAttrString(obj, "y1"));
    addr->y2 = (int) PyLong_AsLong(PyObject_GetAttrString(obj, "y2"));

    return 1;
}

// Module method definitions
static PyObject *create_fractal(PyObject *self, PyObject *args) {
    Range2Di pix;
    Range2Df frac;
    int max_iterations;
    PyObject *obj;

    if (!PyArg_ParseTuple(args, "O&O&iO",
                          convert_range2di, &pix,
                          convert_range2df, &frac,
                          &max_iterations,
                          &obj)) {
        return NULL;
    }


    PyArray_FROM_OTF
    double x_scale = (frac.x2 - frac.x1) / ((double) pix.x2 - pix.x1);
    double y_scale = (frac.y2 - frac.y1) / ((double) pix.y2 - pix.y1);

    for (int y = pix.y1; y <= pix.y2; y++) {
        for (int x = pix.x1; x <= pix.x2; x++) {
            std::complex<double> c(x * x_scale * frac.x1, y * y_scale + frac.y1);
            std::complex<double> z(0, 0);

            int n = 0;
            while (abs(z) < 2 && n < max_iterations) {
                z = (z * z) + c;
                n++;
            }

//            fractal.append(n)
        }

    }



    //return fractal
    printf("(x, y) = (%d, %d)\n", pix.x1, pix.y1);
    printf("(x, y) = (%d, %d)\n", pix.x2, pix.y2);

    printf("(x, y) = (%f, %f)\n", frac.x1, frac.y1);
    printf("(x, y) = (%f, %f)\n", frac.x2, frac.y2);

    Py_RETURN_NONE;
}

// Method definition object for this extension, these argumens mean:
// ml_name: The name of the method
// ml_meth: Function pointer to the method implementation
// ml_flags: Flags indicating special features of this method, such as
//          accepting arguments, accepting keyword arguments, being a
//          class method, or being a static method of a class.
// ml_doc:  Contents of this method's docstring
static PyMethodDef fractal_methods[] = {
        {"create_fractal", create_fractal, METH_VARARGS,
                "Calculate a Julia fractal given a range"},
        {NULL, NULL, 0, NULL}
};

// Module definition
// The arguments of this structure tell Python what to call your extension,
// what it's methods are and where to look for it's method definitions
static struct PyModuleDef fractal_definition = {
        PyModuleDef_HEAD_INIT,
        "_fractal",
        "A Python module that caculates a fractal from C code.",
        -1,
        fractal_methods
};

// Module initialization
// Python calls this function when importing your extension. It is important
// that this function is named PyInit_[[your_module_name]] exactly, and matches
// the name keyword argument in setup.py's setup() call.
PyMODINIT_FUNC PyInit__fractal(void) {
    Py_Initialize();
    return PyModule_Create(&fractal_definition);
}