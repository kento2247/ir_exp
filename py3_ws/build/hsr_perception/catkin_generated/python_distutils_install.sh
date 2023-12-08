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

echo_and_run cd "/workspace/py3_ws/src/hsr_perception"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/workspace/py3_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/workspace/py3_ws/install/lib/python3/dist-packages:/workspace/py3_ws/build/hsr_perception/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/workspace/py3_ws/build/hsr_perception" \
    "/home/developer/.pyenv/versions/catkin_py3/bin/python3" \
    "/workspace/py3_ws/src/hsr_perception/setup.py" \
    egg_info --egg-base /workspace/py3_ws/build/hsr_perception \
    build --build-base "/workspace/py3_ws/build/hsr_perception" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/workspace/py3_ws/install" --install-scripts="/workspace/py3_ws/install/bin"
