import pexpect
import re

from threading import Thread
from time import sleep

class OMXPlayer(object):

    _VIDEOPROP_REXP = re.compile(r".*Video codec ([\w-]+) width (\d+) height (\d+) profile (\d+) fps ([\d.]+).*")
    _AUDIOPROP_REXP = re.compile(r"Audio codec (\w+) channels (\d+) samplerate (\d+) bitspersample (\d+).*")
    _STATUS_REXP = re.compile(r"V :\s*([\d.]+).*")
    _DONE_REXP = re.compile(r"have a nice day.*")
    _VOLUPDOWN_REXP = re.compile(r"Current Volume: (\d+.\d+)dB.*")

    _LAUNCH_CMD = '/usr/bin/omxplayer -s %s %s'
    _PAUSE_CMD = 'p'
    _TOGGLE_SUB_CMD = 's'
    _QUIT_CMD = 'q'
    _VOLUP_CMD = '+'
    _VOLDOWN_CMD = '-'
    _WINSIZE_CMD = " --win '%s %s %s %s' "  

    paused = False
    subtitles_visible = True
    volume = 0.0
    args = ""
    mediafile = ""
    

    def __init__(self, mediafile, args=None, start_playback=False):
        if not args:
            self.args = ""
        else:
            self.args = args

        self.mediafile = mediafile

        if start_playback:
            self.paused = not start_playback
            self.start()
            

    def start(self):
        cmd = self._LAUNCH_CMD % (self.mediafile, self.args)
        self._process = pexpect.spawn(cmd)

        self.video = dict()
        self.audio = dict()

        # Get video properties
        
        video_props = self._VIDEOPROP_REXP.match(self._process.readline().decode('utf-8')).groups()
        self.video['decoder'] = video_props[0]
        self.video['dimensions'] = tuple(int(x) for x in video_props[1:3])
        self.video['profile'] = int(video_props[3])
        self.video['fps'] = float(video_props[4])
        
        # Get audio properties
        
        audio_props = self._AUDIOPROP_REXP.match(self._process.readline().decode('utf-8')).groups()
        self.audio['decoder'] = audio_props[0]
        (self.audio['channels'], self.audio['rate'],
        self.audio['bps']) = [int(x) for x in audio_props[1:]]

        self._position_thread = Thread(target=self._get_position)
        self._position_thread.start()

    def _get_position(self):
        while True:
            index = self._process.expect([self._STATUS_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF,
                                            self._DONE_REXP])
            if index == 1: continue
            elif index in (2, 3): break
            else:
                self.position = float(self._process.match.group(1))
            sleep(0.05)

    def toggle_pause(self):
        if self._process.send(self._PAUSE_CMD):
            self.paused = not self.paused

    def vol_up(self):
            self._process.send(self._VOLUP_CMD)
            index = self._process.expect([self._VOLUPDOWN_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF])
            if index == 0:
                self.volume = float(self._process.match.group(1))
            

    def vol_down(self):
            self._process.send(self._VOLDOWN_CMD)
            index = self._process.expect([self._VOLUPDOWN_REXP,
                                            pexpect.TIMEOUT,
                                            pexpect.EOF])
            if index == 0:
                self.volume = float(self._process.match.group(1))
            

    def set_display_size(self, x, y, width, height):
        cmd = self._WINSIZE_CMD % (x, y, x+width, y+height)
        self.args = self.args + cmd
    
    #def toggle_subtitles(self):
    #    if self._process.send(self._TOGGLE_SUB_CMD):
    #        self.subtitles_visible = not self.subtitles_visible
            
    def stop(self):
        self._process.send(self._QUIT_CMD)
        self._process.terminate(force=True)

    def set_speed(self):
        raise NotImplementedError

    def set_audiochannel(self, channel_idx):
        raise NotImplementedError

    def set_subtitles(self, sub_idx):
        raise NotImplementedError

    def set_volume(self, volume):
        raise NotImplementedError

    def seek(self, minutes):
        raise NotImplementedError
