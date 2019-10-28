# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file contains trackinfo utility functions

"""
import inkamusic.const as const
from inkamusic.const import TRACK_INFO_MELO_OR_PERC_INDX, TRACK_INFO_INSTRU_DEF_INDX
from inkamusic.const import TRACK_INFO_RHYTHM_INDX, TRACK_INFO_CONNECT_INDX, TRACK_INFO_INSTRU_PAUSE_INDX
import inkamusic.settings as settings
import inkamusic.music_parameter as mp


def show_track_info(track_info):
    """prints info about all tracks"""
    if const.DEBUG_OUTPUT:
        print(' ')
        print('Track info')
        print('----------')

        number_of_tracks = len(track_info)
        print(number_of_tracks, 'tracks')
        print(' ')
        for i in range(number_of_tracks):
            print(' ')
            print('Track', i)
            if track_info[i][TRACK_INFO_MELO_OR_PERC_INDX] == const.MELODY_INSTRUMENT:
                id_1 = track_info[i][TRACK_INFO_INSTRU_DEF_INDX][1]
                idtx = '(id = ' + repr(id_1) + ')'
                print('  melody instrument', track_info[i][TRACK_INFO_INSTRU_DEF_INDX][0], idtx, ', as ', end='')
                txt = ['Bass', 'Chorus', 'Solo', 'Harmony']
                print(txt[track_info[i][TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_TYPE_INDX]],
                      'instrument, playing in ', end='')
                txt = ['Bass', 'Low', 'Medium', 'High', 'Full']
                print(txt[track_info[i][TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_TYPE_2_INDX]], 'register')

            else:
                print('  percussion instrument', track_info[i][TRACK_INFO_INSTRU_DEF_INDX][0], ', as ', end='')
                txt = ['Stick', 'Accent', 'Bass', 'High', 'Low', 'Ride', 'Snare']
                print(txt[track_info[i][TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_TYPE_2_INDX]])
            print('  Speed:', track_info[i][TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_SPEED_INDX])
            print('  Pause:', track_info[i][TRACK_INFO_INSTRU_PAUSE_INDX])
            print('  Rhythm:', track_info[i][TRACK_INFO_RHYTHM_INDX])
            print('  Connect probs:', track_info[i][TRACK_INFO_CONNECT_INDX])
        print(' ')


def create_random_instrumentation(rnd_type, rndm_2):
    """creates a random instrumentation"""
    instru_list = []
    # example for instru_list to be created
    #          [['Grand Piano', 2, 2],  #  = ['Grand Piano', T_SOLO, R_MEDI],
    #          ['Grand Piano', 2, 3],
    #          ['Grand Piano', 1, 2],
    #          ['Grand Piano', 3, 2],
    #          ['Fingered Bass', 0, 0]]

    if rnd_type in [0, 3, 4]:  # random, random solo, random double solo
        # choose between high or medium
        val = rndm_2[const.RNDM_INSTRU].rndm_int(1, 100)
        if val > mp.RND_INSTRU_MEDIUM_SOLO:
            instrument = settings.get_instrument_by_property(const.T_SOLO, const.R_HIGH, rndm_2)
            if rnd_type in [4]:
                instrument2 = settings.get_instrument_by_property(const.T_SOLO, const.R_MEDI, rndm_2)
        else:
            instrument = settings.get_instrument_by_property(const.T_SOLO, const.R_MEDI, rndm_2)
            if rnd_type in [4]:
                instrument2 = settings.get_instrument_by_property(const.T_SOLO, const.R_HIGH, rndm_2)

        instru_list.append([instrument[0], instrument[3], instrument[4]])
        if rnd_type in [4]:
            instru_list.append([instrument2[0], instrument2[3], instrument2[4]])
    if rnd_type in [0, 1, 4]:  # random, random bass, random double solo
        # bass instrument

        instrument = settings.get_instrument_by_property(const.T_BASS, const.R_BASS, rndm_2)
        instru_list.append([instrument[0], instrument[3], instrument[4]])
    if rnd_type in [0, 2, 4]:  # random, random harmony, random double solo
        # decide about chorus and harmony instrument
        val = rndm_2[const.RNDM_INSTRU].rndm_choice(mp.RND_INSTRU_HARMONY_CHORUS)
        if val in [1, 3] or rnd_type in [2]:  # add harmony
            instrument = settings.get_instrument_by_property(const.T_HMNY, const.R_MEDI, rndm_2)
            instru_list.append([instrument[0], instrument[3], instrument[4]])
        if val in [2, 3] and rnd_type not in [2]:  # add chorus
            instrument = settings.get_instrument_by_property(const.T_CHOR, const.R_MEDI, rndm_2)
            instru_list.append([instrument[0], instrument[3], instrument[4]])

    return instru_list


def add_percussion(rhythm_definition, track_info, rndm_2):
    """adds percussion tracks when selected in web interface"""
    # Index 0 contains number of beats, index 1, 2, ... the individual tracks
    for rhy_indx in range(1, len(rhythm_definition)):
        track_info.append([])
        track_info[-1].append(const.PERCUSSION_INSTRUMENT)
        instrument = settings.get_instrument_by_property(const.T_PERC, rhythm_definition[rhy_indx][0], rndm_2)
        pause = -1  # not used for percussion, pauses are set in PAUSE_PROB
        track_info[-1].append(instrument)
        track_info[-1].append(pause)
        track_info[-1].append(rhythm_definition[rhy_indx])
        track_info[-1].append([const.AUTODAMP_PERC, 0, 0])


def prepare_track_info(track_info, menu_options, rhythm_definition, rndm_2):
    """ creates track info for each instrument used
        structure of track_info is as follows:

        for each track:
         track_info[track_no][TRACK_INFO_MELO_OR_PERC_INDX] = melody or percussion instrument
         track_info[track_no][TRACK_INFO_INSTRU_DEF_INDX] = instrument definition
         track_info[track_no][TRACK_INFO_RHYTHM_INDX] = track rhythm (track rhythm will be added here for percussion
         tracks and will be added later in create_track_rhythm for melody tracks)
         track_info[track_no][TRACK_INFO_CONNECT_INDX] = probability tuple for connection types
    """

    instrument_list = menu_options.get_selected_instrumentation()
    # example [['Grand Piano', 2, 2],  #  = ['Grand Piano', T_SOLO, R_MEDI],
    #          ['Grand Piano', 2, 3],
    #          ['Grand Piano', 1, 2],
    #          ['Grand Piano', 3, 2],
    #          ['Fingered Bass', 0, 0]]
    # or, example for random instrumentation
    # [[1]]  # Random bass only, instrument_list[0][0] == 1

    if len(instrument_list[0]) == 1:  # random instrumentation
        instrument_list = create_random_instrumentation(instrument_list[0][0], rndm_2)

    # step 1
    # add all instrument tracks to track_info, sorted by instrument type
    if const.DEBUG_OUTPUT:
        print(' ')
        print('instrument list is', instrument_list)
    for instru_type in [const.T_SOLO, const.T_BASS, const.T_HMNY, const.T_CHOR, const.T_PERC]:
        # count number of instruments with this type
        num_instru_current_type = 0
        for instru in instrument_list:
            instrument = settings.get_instrument_by_name_and_property(instru[0], instru[1], instru[2])
            if instrument[const.INSTRUMENT_TYPE_INDX] == instru_type:
                num_instru_current_type += 1
        count_instru_current_type = 0
        # select an catalog entry randomly
        if instru_type != const.T_PERC:
            cat_entries = rndm_2[const.RNDM_INSTRU].rndm_choice(mp.INSTRU_DISTRIBUTION[instru_type])
        for instru in instrument_list:
            instrument = settings.get_instrument_by_name_and_property(instru[0], instru[1], instru[2])

            if instrument[const.INSTRUMENT_TYPE_INDX] == instru_type:
                assert instru_type != const.T_PERC, "percussion can not be used as melody instrument"
                track_info.append([])
                track_info[-1].append(const.MELODY_INSTRUMENT)
                track_info[-1].append(instrument)
                if num_instru_current_type == 1:
                    pause = -1
                    track_info[-1].append(pause)
                else:

                    track_info[-1].append(cat_entries[count_instru_current_type])

                track_info[-1].append([])  # will be replaced by rhythm
                if instrument[const.INSTRUMENT_AUTODAMP_INDX] == 1:
                    track_info[-1].append([const.AUTODAMP_MELO, 0, 0])
                else:
                    track_info[-1].append(menu_options.get_rhythm_connect_tuple(rndm_2))
                count_instru_current_type += 1

    # step 2
    # if percussion is selected in web interface
    # add percussion tracks as defined by selected rhythm
    if menu_options.get_selected_percussion():  # add percussion
        add_percussion(rhythm_definition, track_info, rndm_2)

    number_of_tracks = len(track_info)

    return number_of_tracks


def is_melody_instrument(track):
    """ returns True if melody instrument"""
    return track[TRACK_INFO_MELO_OR_PERC_INDX] == const.MELODY_INSTRUMENT


def set_track_rhythm(track, tr_rhythm):
    """ sets rhythm for track"""
    track[TRACK_INFO_RHYTHM_INDX] = tr_rhythm


def get_track_rhythm(track):
    """ returns track rhythm"""
    return track[TRACK_INFO_RHYTHM_INDX]


def get_track_pause(track):
    """ returns pause setting for track, only used for melody instruments (set in prepare_track_info)
    for percussion instruments get_pause_probability is used"""
    return track[TRACK_INFO_INSTRU_PAUSE_INDX]


def get_max_tones_per_sec(track):
    """ returns max tones per second for a track based on instrument"""

    orig_max_per_sec = track[const.TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_SPEED_INDX]

    return orig_max_per_sec


def get_instrument_type_2(track):
    """ returns
    'Bass', 'Low', 'Medium', 'High', 'Full',
    'Stick', 'Accent', 'Bass', 'High', 'Low', 'Ride', 'Snare'"""
    return track[TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_TYPE_2_INDX]


def get_instrument_type(track):
    """ returns const.T_SOLO, const.T_BASS, const.T_HMNY, const.T_CHOR, const.T_PERC"""
    return track[TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_TYPE_INDX]


def get_instrument_midi(track):
    """ returns [8, 28], ..."""
    return track[TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_MIDI_INDX]


def get_track_connect_info(track):
    """returns connection type of track (LEGATO, ...) """
    return track[const.TRACK_INFO_CONNECT_INDX]


def is_solo_instrument(track):
    """ returns True if SOLO instrument"""
    return track[TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_TYPE_INDX] == const.T_SOLO


def is_harmony_instrument(track):
    """ returns True if harmony instrument (which creates chords instead of single tones"""
    return track[TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_TYPE_INDX] == const.T_HMNY


def is_bass_instrument(track):
    """ returns True if bass instrument"""
    return track[TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_TYPE_INDX] == const.T_BASS


def get_track_instrument_range(track):
    """ returns lowest and highest tone possible for instrument (within the current register)"""
    return track[const.TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_LOW_INDX],\
        track[const.TRACK_INFO_INSTRU_DEF_INDX][const.INSTRUMENT_HIGH_INDX]
