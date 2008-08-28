/* -*- mode: C; c-basic-offset: 4 -*- */
#ifndef __PYGNOMEVFS_H_
#define __PYGNOMEVFS_H_

#include <Python.h>

#include <libgnomevfs/gnome-vfs-init.h>
#include <libgnomevfs/gnome-vfs-uri.h>
#include <libgnomevfs/gnome-vfs-file-info.h>
#include <libgnomevfs/gnome-vfs-directory.h>
#include <libgnomevfs/gnome-vfs-ops.h>
#include <libgnomevfs/gnome-vfs-mime-handlers.h>
#include <libgnomevfs/gnome-vfs-mime-utils.h>
#include <libgnomevfs/gnome-vfs-result.h>
#include <libgnomevfs/gnome-vfs-context.h>
#include <libgnomevfs/gnome-vfs-xfer.h>


G_BEGIN_DECLS

typedef struct {
    PyObject_HEAD
    GnomeVFSURI *uri;
} PyGnomeVFSURI;

typedef struct {
    PyObject_HEAD
    GnomeVFSFileInfo *finfo;
} PyGnomeVFSFileInfo;

typedef struct {
    PyObject_HEAD
    GnomeVFSContext *context;
} PyGnomeVFSContext;
    
#define pygnome_vfs_uri_get(v) (((PyGnomeVFSURI *)(v))->uri)
#define pygnome_vfs_uri_check(v) ((v)->ob_type == _PyGnomeVFS_API->uri_type)

#define pygnome_vfs_file_info_get(v) (((PyGnomeVFSFileInfo *)(v))->finfo)
#define pygnome_vfs_file_info_check(v) ((v)->ob_type == _PyGnomeVFS_API->file_info_type)

#define pygnome_vfs_context_get(v) (((PyGnomeVFSURI *)(v))->context)
#define pygnome_vfs_context_check(v) ((v)->ob_type == _PyGnomeVFS_API->context_type)

struct _PyGnomeVFS_Functions {
    GnomeVFSResult (* exception_check)(void);
    PyObject *(* uri_new)(GnomeVFSURI *uri);
    PyTypeObject *uri_type;
    PyObject *(* file_info_new)(GnomeVFSFileInfo *finfo);
    PyTypeObject *file_info_type;
    PyObject *(* context_new)(GnomeVFSContext *context);
    PyTypeObject *context_type;
};

#ifndef _INSIDE_PYGNOMEVFS_

#if defined(NO_IMPORT) || defined(NO_IMPORT_PYGNOMEVFS)
extern struct _PyGnomeVFS_Functions *_PyGnomeVFS_API;
#else
struct _PyGnomeVFS_Functions *_PyGnomeVFS_API;
#endif

#define pygnome_vfs_exception_check (_PyGnomeVFS_API->exception_check)
#define pygnome_vfs_uri_new         (_PyGnomeVFS_API->uri_new)
#define PyGnomeVFSURI_Type          (*_PyGnomeVFS_API->uri_type)
#define pygnome_vfs_file_info_new   (_PyGnomeVFS_API->file_info_new)
#define PyGnomeVFSFileInfo_Type     (*_PyGnomeVFS_API->file_info_type)
#define pygnome_vfs_context_new     (_PyGnomeVFS_API->context_new)
#define PyGnomeVFSContext_Type      (*_PyGnomeVFS_API->context_type)

static inline PyObject *
pygnomevfs_init(void)
{
    PyObject *module = PyImport_ImportModule("gnomevfs");
    if (module != NULL) {
        PyObject *mdict = PyModule_GetDict(module);
        PyObject *cobject = PyDict_GetItemString(mdict, "_PyGnomeVFS_API");
        if (PyCObject_Check(cobject))
            _PyGnomeVFS_API = (struct _PyGnomeVFS_Functions *)PyCObject_AsVoidPtr(cobject);
        else {
	    Py_FatalError("could not find _PyGnomeVFS_API object");
        }
    } else {
        Py_FatalError("could not import gnomevfs");
    }
    return module;
}

#define init_pygnomevfs() pygnomevfs_init();


#endif /* !_INSIDE_PYGNOMEVFS_ */


#define PYGVFS_CONTROL_MAGIC_IN 0xa346a943U
#define PYGVFS_CONTROL_MAGIC_OUT 0xb49535dcU

typedef struct {
    guint magic;
    PyObject *data;
} PyGVFSOperationData;

G_END_DECLS

#endif /* __PYGNOMEVFS_H_ */
