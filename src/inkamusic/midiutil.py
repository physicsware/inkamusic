# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file contains MIDI file functions

"""

import math
from struct import pack
import inkamusic.const as const

STATUSMSG_INDX = 0
LEN_INDX = 1
TICK_INDX = 2
CHANNEL_INDX = 3
META_COMMAND = 4
DATA_INDX = 5


def end_of_track_event(current_track):
    """appends an end of track event"""
    current_track.append([0xFF, 0, 1, 0, 0x2F])


def program_change_event(current_track, channel, data):
    """appends a program change of track event"""

    current_track.append([0xC0, 1, 0, channel, 0, data])


def note_on_event(current_track, tick, channel, pitch, velocity):
    """appends a note on event"""

    current_track.append([0x90, 2, tick, channel, 0, pitch, velocity])


def note_off_event(current_track, tick, channel, pitch):
    """appends a note off event"""
    current_track.append([0x80, 2, tick, channel, 0, pitch, 0])


def control_change_event(current_track, channel, control, value):
    """appends a control change event"""
    current_track.append([0xB0, 2, 0, channel, 0, control, value])


def sys_ex_message_gm2(current_track):
    """appends a sys_ex message"""
    current_track.append([0xF0, 4, 0, 0, 0, 126, 127, 9, 3])


def set_tempo_event(current_track, bpm):
    """appends a tempo event"""
    val = int(float(6e7) / bpm)
    data = [(val >> (16 - (8 * x)) & 0xFF) for x in range(3)]
    current_track.append([0xFF, 3, 0, 0, 0x51, data[0], data[1], data[2]])


def time_signature_event(current_track, numerator, denominator):
    """appends a time signature event"""
    current_track.append([0xFF, 4, 0, 0, 0x58, numerator, int(math.log(denominator, 2)), 0, 0])


def encode_track_header(trklen):
    """encodes the track header"""
    return bytes('MTrk', 'UTF-8') + pack(">L", trklen)


def encode_midi_event(event, running_status):
    """encodes a midi event"""
    ret = bytes()
    ret += write_varlen(event[TICK_INDX])

    data = []
    if event[LEN_INDX] > 0:
        for i in range(event[LEN_INDX]):
            data.append(event[DATA_INDX + i])

    if event[STATUSMSG_INDX] in [0xFF]:  # meta events
        ret += bytes([event[STATUSMSG_INDX], event[META_COMMAND]])
        ret += write_varlen(event[LEN_INDX])
        ret += bytes(data)
    elif event[STATUSMSG_INDX] in [0xF0]:  # Sysex events
        ret += bytes([0xF0])
        ret += write_varlen(event[LEN_INDX] + 1)
        ret += bytes(data)
        ret += bytes([0xF7])
    else:
        if not running_status or running_status[STATUSMSG_INDX] != event[STATUSMSG_INDX] or \
          running_status[CHANNEL_INDX] != event[CHANNEL_INDX]:
            running_status = event
            ret += bytes([(event[STATUSMSG_INDX] | event[CHANNEL_INDX])])
        ret += bytes(data)

    return ret, running_status


def write_track(midifile, track):
    """writes the track into the midi file"""
    buf = bytes()
    running_status = None
    for event in track:
        encoded, running_status = encode_midi_event(event, running_status)
        buf += encoded

    bufbyte = encode_track_header(len(buf)) + buf
    midifile.write(bufbyte)


def write_file_header(midifile, pattern):
    """writes the file header"""
    # First four bytes are MIDI header
    packdata = pack(">LHHH", 6,
                    1,
                    len(pattern),
                    const.TICKSRES)
    midifile.write(bytes('MThd', 'UTF-8') + packdata)


def write_midifile(midifile, pattern):
    """writes the midi file"""
    midifile = open(midifile, 'wb')
    write_file_header(midifile, pattern)
    for track in pattern:
        write_track(midifile, track)


def write_varlen(value):
    """converts value to variable length structure"""
    chr1 = bytes(0)
    chr2 = bytes(0)
    chr3 = bytes(0)
    chr4 = bytes(0)
    chr1 = bytes([value & 0x7F])
    value >>= 7
    if value:
        chr2 = bytes([(value & 0x7F) | 0x80])
        value >>= 7
        if value:
            chr3 = bytes([(value & 0x7F) | 0x80])
            value >>= 7
            if value:
                chr4 = bytes([(value & 0x7F) | 0x80])
                res = chr4 + chr3 + chr2 + chr1
            else:
                res = chr3 + chr2 + chr1
        else:
            res = chr2 + chr1
    else:
        res = chr1
    return res
