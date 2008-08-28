/* -*- mode: C; c-basic-offset: 4 -*- */
#ifndef __PYGNOMEVFSBONOBO_H_
#define __PYGNOMEVFSBONOBO_H_

#include <pygnomevfs.h>


G_BEGIN_DECLS


struct _PyGnomeVFSBonobo_Functions {
    PyObject * (*mime_component_action_new) (GnomeVFSMimeAction *action);
};

#define pygnomevfs_bonobo_mime_component_action_new (_PyGnomeVFSBonobo_API->mime_component_action_new)


#if defined(NO_IMPORT) || defined(NO_IMPORT_PYGNOMEVFSBONOBO)
extern struct _PyGnomeVFSBonobo_Functions *_PyGnomeVFSBonobo_API;
#else
struct _PyGnomeVFSBonobo_Functions *_PyGnomeVFSBonobo_API;
#endif

static inline PyObject *
pygnome_vfs_bonobo_init(void)
{
    PyObject *module = PyImport_ImportModule("gnomevfs.gnomevfsbonobo");
    if (module != NULL) {
        PyObject *mdict = PyModule_GetDict(module);
        PyObject *cobject = PyDict_GetItemString(mdict, "_PyGnomeVFSBonobo_API");
        if (PyCObject_Check(cobject))
            _PyGnomeVFSBonobo_API = (struct _PyGnomeVFSBonobo_Functions *)PyCObject_AsVoidPtr(cobject);
        else {
	    Py_FatalError("could not find _PyGnomeVFSBonobo_API object");
        }
    } else {
        Py_FatalError("could not import gnomevfs.gnomevfsbonobo");
    }
    return module;
}

G_END_DECLS

#endif /* __PYGNOMEVFSBONOBO_H_ */
