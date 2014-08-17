coubterm
========

Play your favourite coubs in terminal


Dependencies
------------

* python 2.7
* mplayer built with libcaca option

brew install mplayer --with-libcaca


Warning!!
---------
If you're going to build stuff manually note that in order to work with mplayer libcaca doesn't need to be build with imlib2. Although if you want to play with cacaview and jpg images imlib2 is required. If you're going to build with --without-x option then keep in mind 2 things:
* the latest stable imlib2 sources (1.4.6) has a [bug](http://git.enlightenment.org/legacy/imlib2.git/commit/?id=4f36e69934ebf520a3b677c344f4b0db6e2d1400)
* you have to pass CPPFLAGS=-DX_DISPLAY_MISSING to make


Usage
-----
./main.py  
get hot  
play 2vf1v
