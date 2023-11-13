#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/workspace/py2_ws/src/wrs_algorithm21"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/workspace/py2_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/workspace/py2_ws/install/lib/python2.7/dist-packages:/workspace/py2_ws/build/wrs_algorithm/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/workspace/py2_ws/build/wrs_algorithm" \
    "/usr/bin/python2" \
    "/workspace/py2_ws/src/wrs_algorithm21/setup.py" \
    egg_info --egg-base /workspace/py2_ws/build/wrs_algorithm \
    build --build-base "/workspace/py2_ws/build/wrs_algorithm" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/workspace/py2_ws/install" --install-scripts="/workspace/py2_ws/install/bin"
