pyomxplayer
===========
Python wrapper module around `OMXPlayer <https://github.com/huceke/omxplayer>`_
for the Raspberry Pi.

Unlike `other implementations <https://github.com/KenT2/pyomxplayer>`_, this
module does not rely on any external scripts and FIFOs, but uses the
`pexpect module <http://pypi.python.org/pypi/pexpect/2.4>`_ for communication
with the OMXPlayer process.

CPU overhead is rather low (~3% for the Python process on my development RPi)
and the object-oriented design makes it easy to re-use in other projects.

forked from jbaiter/pyomxplayer. Testet with omxplayer version 98982df.

Installation:
-------------
::

    git clone https://github.com/mortenfryd/pyomxplayer.git
    python pyomxplayer/setup.py install

Example:
--------
::

    >>> from pyomxplayer import OMXPlayer
    >>> from pprint import pprint
    >>> omx = OMXPlayer('/tmp/video.mp4',start_playback=False)
    >>> #set window size (x,y,width,height)
    >>> omx.set_display_size(0,0,1920,1080)
    >>> #finally start player
    >>> omx.start()
    >>> #pause
    >>> omx.toggle_pause()
    >>> #volume up
    >>> omx.vol_up()
    >>> #volume down
    >>> omx.vol_down()
    >>> #stop
    >>> omx.stop()
