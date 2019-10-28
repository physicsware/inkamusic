# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2019  Udo Wollschläger

"""
# pylint  --rcfile = rcudo file
import os
import cherrypy

import inkamusic.const as const
from inkamusic.const import SUB_INDX
import inkamusic.trackinfo_util as tu
import inkamusic.basic_scales as basic_scales
import inkamusic.harmonies as harmonies
import inkamusic.structures as structures
import inkamusic.bar_distribution as bar_distribution
import inkamusic.algorithms as algorithms
import inkamusic.music_parameter as mp
import inkamusic.midiutil as midiutil
import inkamusic.rhythm_algorithms as rhythm_algorithms


def find_first_dissonance(pos, pos_current_tone, tones, current_tone):
    """finds first dissonance for current track"""
    position = 0
    dissonance_delta = -1
    while position < len(pos):
        if pos[position] > pos_current_tone:
            for z_1 in current_tone:
                for z_2 in tones[position]:
                    if (z_1 - z_2) % 12 in [1, 11]:  # dissonance
                        dissonance_delta = pos[position] - pos_current_tone

        if dissonance_delta != -1:
            break
        else:
            position += 1
    return dissonance_delta


def set_midi_on_off(t_chord, midi_params, c_3):
    """creates note on and off events for a tone or chord"""
    num_of_tones = len(t_chord)
    intensity_reduce = (mp.VOLUME_REDUCE_CHORD_TONES / 2) * (num_of_tones - 1)
    delta_shift = 0
    for indx, tone in enumerate(t_chord):

        in1 = int((c_3['intensities'][midi_params['index']] * (100 - intensity_reduce)) / 100 + 0.5)

        if indx == 0:
            midiutil.note_on_event(midi_params['current_track'],
                                   tick=midi_params['ticks'], channel=midi_params['current_channel'],
                                   pitch=tone, velocity=in1)
#
        else:
            delta = min(mp.CHORD_SPREAD, midi_params['exact_midi_tone_length'] // 6)
            midiutil.note_on_event(midi_params['current_track'], tick=delta, channel=midi_params['current_channel'],
                                   pitch=tone, velocity=in1)
            delta_shift += delta

    for indx, tone in enumerate(t_chord):
        if indx == 0:
            midiutil.note_off_event(midi_params['current_track'],
                                    tick=midi_params['exact_midi_tone_length']-delta_shift,
                                    channel=midi_params['current_channel'], pitch=tone)
        else:
            midiutil.note_off_event(midi_params['current_track'], tick=0,
                                    channel=midi_params['current_channel'], pitch=tone)


class InkaAlgorithmicMusic():
    """ This is the Inka_Algorithmic_Music application main class.
    """

    def __init__(self, **inka_data):

        self.inka_data = inka_data
        self.inka_data_2 = {'number_of_tracks': -1,  # will be set to total number of tracks
                            'track_info': [],  # will contain information about each track
                            'composed_track': [],  # will contain the composed tracks
                            'harmony_track': None,  # contains the harmony track
                            'basic_scales': basic_scales.BasicScale(),  # create a BasicScale class object
                            'num_of_beats': -1,
                            'length_in_seconds': -1,
                            'bpm': -1,
                            'num_of_bars': -1,
                            'global_rhythm': -1,
                            'selected_rhythm': -1,
                            'composition_struct': [],
                            'bar_struct': -1,
                            'bar_distribution': -1,
                            }
        self.inka_data_3 = {'harmony_class': harmonies.HarmonyBasics(self.inka_data_2['basic_scales']),
                            'current_track_midi_id': [],
                            'num_composed_bars': -1,
                            'tones': [],
                            'positions': [],
                            'intensities': [],
                            'connection_types': [],
                            'staccato_length_in_ticks': -1,
                            'min_tone_separation_in_ticks': -1,
                            }

    def calc_num_of_bars(self):
        """calculates number of bars"""
        c_2 = self.inka_data_2

        bars = int(((c_2['bpm'] * c_2['length_in_seconds'] / 60.0) / c_2['num_of_beats']) + 0.5)

        assert bars > 0, "bars wrong"
        return bars

        # end calc_num_of_bars

    def get_pan_value(self, track, is_melody_instrument):
        """sets pan value for a track"""
        if is_melody_instrument:
            pan = [32, 96, 48, 80, 64, 16, 112]  # was  [48, 80, 56, 72, 64, 40, 88]
            modi_pan = pan[track % len(pan)] + self.inka_data['rndm_2'][const.RNDM_INSTRU].rndm_int(-2, 2)
        else:
            modi_pan = 64

        return modi_pan

    def adapt_tone_length(self, pos_current_tone, pos_next_tone, end_pos_limit, check_connect_type):
        """tries to adapt tone length using rules for different connection types"""
        c_3 = self.inka_data_3

        adapted_tone_length = const.NO_USABLE_TONE_LENGTH

        if check_connect_type == const.CONNECT_STANDARD:

            # rule:  pos_current_tone + tone_length + tone_separation = pos_next_tone
            # and:  tone_separation >= c_3['min_tone_separation_in_ticks']

            tone_length = min(end_pos_limit - pos_current_tone,
                              pos_next_tone - pos_current_tone - c_3['min_tone_separation_in_ticks'])
            if tone_length >= 2 * c_3['staccato_length_in_ticks']:
                adapted_tone_length = tone_length

        elif check_connect_type == const.CONNECT_LEGATO:

            # rule:  pos_current_tone + tone_length = pos_next_tone

            if end_pos_limit >= pos_next_tone:
                adapted_tone_length = pos_next_tone - pos_current_tone

        elif check_connect_type == const.CONNECT_AUTODAMP:

            adapted_tone_length = min(pos_next_tone - pos_current_tone, end_pos_limit - pos_current_tone)

        elif check_connect_type == const.CONNECT_STACCATO:
            # rule:  pos_current_tone + staccato_tone_length + tone_separation = pos_next_tone
            # and:  tone_separation >= c_3['min_tone_separation_in_ticks']

            tone_length = min(end_pos_limit - pos_current_tone,
                              pos_next_tone - pos_current_tone - c_3['min_tone_separation_in_ticks'])
            if tone_length >= c_3['staccato_length_in_ticks']:
                adapted_tone_length = c_3['staccato_length_in_ticks']

        return adapted_tone_length

    def calculate_tone_length(self, connection_type, pos_current_tone, pos_next_tone, end_pos_limit):
        """calculates the tone length"""

        # start calculate_tone_length
        c_2 = self.inka_data_2
        c_3 = self.inka_data_3

        adapted_length = const.NO_USABLE_TONE_LENGTH

        found_usable_tone_length = False
        index = 0

        while not found_usable_tone_length:
            if index % 3 == 0:
                try_connection_type = connection_type
                minimum_tone_length_factor = 1.0 - index // 3 * 0.1
            elif index % 3 == 1:
                assert connection_type != const.CONNECT_AUTODAMP, "should always work on first try"
                if connection_type == const.CONNECT_STANDARD:
                    try_connection_type = const.CONNECT_LEGATO
                else:
                    try_connection_type = const.CONNECT_STANDARD
                minimum_tone_length_factor = 1.0 - index // 3 * 0.1
            elif index % 3 == 2:
                if connection_type == const.CONNECT_STACCATO:
                    try_connection_type = const.CONNECT_LEGATO
                else:
                    try_connection_type = const.CONNECT_STACCATO
                minimum_tone_length_factor = 1.0 - index // 3 * 0.1

            c_3['staccato_length_in_ticks'] = int(const.TICKSRES * c_2['bpm'] *
                                                  mp.STACC_LEN_IN_S / 60 * minimum_tone_length_factor + 0.5)
            c_3['min_tone_separation_in_ticks'] = int(const.TICKSRES * c_2['bpm'] *
                                                      mp.TONE_SEPARATION_IN_S / 60 * minimum_tone_length_factor + 0.5)

            adapted_length = self.adapt_tone_length(pos_current_tone, pos_next_tone, end_pos_limit, try_connection_type)
            if adapted_length == const.NO_USABLE_TONE_LENGTH:
                index += 1
            else:
                found_usable_tone_length = True
                assert adapted_length % 1 == 0

        return adapted_length

        # end calculate_tone_length

    def find_dissonance_delta(self, current_track_id, pos_current_tone, current_tone):
        """Finds distance to nearest dissonant tone in all other tracks"""

        c_2 = self.inka_data_2

        min_dissonance_delta = -1  # not yet set

        for track in range(len(c_2['track_info'])):
            track_midi_id = tu.get_instrument_midi(c_2['track_info'][track])
            perc = (track_midi_id[1] < 0)

            if not perc and track != current_track_id:

                tones = c_2['composed_track'][track].gettones()
                pos = c_2['composed_track'][track].getpositions()

                # find pos of first tone with pos > pos_current_tone which is dissonant to current_tone
                dissonance_delta = find_first_dissonance(pos, pos_current_tone, tones, current_tone)
                if dissonance_delta != -1:
                    if min_dissonance_delta == -1 or dissonance_delta < min_dissonance_delta:
                        min_dissonance_delta = dissonance_delta

        if min_dissonance_delta == -1:  # no dissonat tone found
            min_dissonance_delta = 100 * const.TICKSRES  # use very big value instead
        return min_dissonance_delta

    # end find_dissonance_delta

    def get_tone_length_and_connection_type(self, indx, track_id, is_percussion):

        """This functions calculates the exact tone length,
        avoiding dissonances or tones too short or pauses"""
        c_3 = self.inka_data_3

        pos_current_tone = c_3['positions'][indx]
        if len(c_3['tones']) - 1 == indx:  # last tone
            pos_next_tone = pos_current_tone + (mp.LAST_TONE_LENGTH * const.TICKSRES * self.inka_data_2['bpm']) // 60
        else:
            pos_next_tone = c_3['positions'][indx + 1]

        connection_type = c_3['connection_types'][indx]
        if connection_type == const.CONNECT_AUTODAMP:
            auto_damp_time_in_ticks = (mp.AUTO_DAMP_TIME * const.TICKSRES * self.inka_data_2['bpm']) // 60

        if is_percussion:
            dissonance_limit = pos_next_tone  # no dissonance for percussion instruments
        else:
            delta_to_first_dissonant_tone = self.find_dissonance_delta(track_id, pos_current_tone, c_3['tones'][indx])

            # if distance to next dissonant tone is greater than auto_damp_time_in_ticks,
            # enlarge delta_to_first_dissonant_tone even more
            # this ensures that auto_damp instruments are not unnecessarily switched off
            if connection_type == const.CONNECT_AUTODAMP and delta_to_first_dissonant_tone > auto_damp_time_in_ticks:
                delta_to_first_dissonant_tone = max(4 * auto_damp_time_in_ticks, delta_to_first_dissonant_tone)

            dissonance_limit = pos_current_tone + delta_to_first_dissonant_tone

        # limit tone length

        if connection_type == const.CONNECT_AUTODAMP:
            end_pos_limit = min(pos_current_tone + 4 * const.TICKSRES, dissonance_limit)
        else:
            if (pos_next_tone - pos_current_tone) < mp.TONE_LENGTH_PARAM[3] * const.TICKSRES:
                # if next tone is not too far away, this tone defines the end of the previous tone
                tone_ends = pos_next_tone
            else:
                quarter_notes = self.inka_data['rndm_2'][const.RNDM_MELO_RHYTHM].rndm_gauss_limit(mp.TONE_LENGTH_PARAM)
                tone_ends = pos_current_tone + quarter_notes * const.TICKSRES

            end_pos_limit = int(min(tone_ends, dissonance_limit) + 0.5)

        return self.calculate_tone_length(connection_type, pos_current_tone, pos_next_tone, end_pos_limit)

    def create_melody_midi(self, current_track, current_channel, track_id):

        """create midi data for melody instrument"""

        c_3 = self.inka_data_3

        midiutil.control_change_event(current_track,
                                      channel=current_channel,
                                      control=const.MIDI_BANK_SELECT,
                                      value=c_3['current_track_midi_id'][0])

        midiutil.program_change_event(current_track,
                                      channel=current_channel,
                                      data=c_3['current_track_midi_id'][1])

        index = 0
        exact_midi_tone_length = -1  # not set yet

        midi_params = {'current_track': current_track,
                       'current_channel': current_channel,
                       'ticks': 0,
                       'index': 0,
                       'exact_midi_tone_length': exact_midi_tone_length,
                       }

        for t_chord in c_3['tones']:

            if index == 0:
                ticks = c_3['positions'][index]
            else:
                ticks = c_3['positions'][index] - c_3['positions'][index - 1] - exact_midi_tone_length

            exact_midi_tone_length = self.get_tone_length_and_connection_type(index, track_id, is_percussion=False)

            assert exact_midi_tone_length > 0, "Something is wrong with exact_midi_tone_length"

            if t_chord:  # one or more tones
                midi_params['ticks'] = ticks
                midi_params['index'] = index
                midi_params['exact_midi_tone_length'] = exact_midi_tone_length

                set_midi_on_off(t_chord, midi_params, c_3)

            else:  # no tone, len(t_chord) == 0

                midiutil.note_on_event(current_track, tick=ticks, channel=current_channel, pitch=60, velocity=0)

                midiutil.note_off_event(current_track, tick=exact_midi_tone_length, channel=current_channel, pitch=60)

            index += 1
        if index > 0:

            midiutil.note_on_event(current_track, tick=0, channel=current_channel, pitch=60, velocity=0)
            midiutil.note_off_event(current_track,
                                    tick=(const.END_PAUSE_IN_S * const.TICKSRES * self.inka_data_2['bpm']) // 60,
                                    channel=current_channel,
                                    pitch=60)

    # end create_melody_midi

    def create_percussion_midi(self, current_track, perc_instrument_type, track_id):
        """create midi data for percussion instrument"""

        c_3 = self.inka_data_3

        midiutil.control_change_event(current_track,
                                      channel=9,
                                      control=const.MIDI_BANK_SELECT,
                                      value=0)

        midiutil.program_change_event(current_track,
                                      channel=9,
                                      data=0)

        exact_midi_tone_length = -1  # not set yet

        for index, _ in enumerate(c_3['tones']):

            if index == 0:
                ticks = c_3['positions'][index]
            else:
                ticks = c_3['positions'][index] - c_3['positions'][index - 1] - exact_midi_tone_length

            velocity = int(c_3['intensities'][index] + 0.5)

            midiutil.note_on_event(current_track, tick=ticks, channel=9, pitch=perc_instrument_type, velocity=velocity)

            exact_midi_tone_length = self.get_tone_length_and_connection_type(index, track_id, is_percussion=True)
            assert exact_midi_tone_length >= 0, "Something is wrong with exact_midi_tone_length"

            midiutil.note_off_event(current_track, tick=exact_midi_tone_length, channel=9, pitch=perc_instrument_type)
            index += 1

    # end create_percussion_midi

    def create_midi(self):
        """creates midi data for all tracks"""

        c_2 = self.inka_data_2
        c_3 = self.inka_data_3

        midi_pattern = []

        current_channel = 0

        for track_id in range(len(c_2['track_info'])):

            current_track = []

            c_3['current_track_midi_id'] = tu.get_instrument_midi(c_2['track_info'][track_id])
            if c_3['current_track_midi_id'][1] >= 0:  # melody instrument
                is_melody_instrument = True
                active_channel = current_channel
            else:
                is_melody_instrument = False
                active_channel = 9
                perc_instrument_type = -(c_3['current_track_midi_id'][1])

            midi_pattern.append(current_track)

            c_3['tones'] = c_2['composed_track'][track_id].gettones()
            c_3['positions'] = c_2['composed_track'][track_id].getpositions()
            c_3['intensities'] = c_2['composed_track'][track_id].getintensities()
            c_3['connection_types'] = c_2['composed_track'][track_id].getconnection_types()

            midiutil.set_tempo_event(current_track, bpm=c_2['bpm'])
            midiutil.time_signature_event(current_track, numerator=c_2['num_of_beats'], denominator=4)

            # pan reverb chorus volume
            pan = self.get_pan_value(track_id, is_melody_instrument)

            midiutil.control_change_event(current_track, channel=active_channel, control=const.MIDI_PAN, value=pan)

            midiutil.control_change_event(current_track, channel=active_channel, control=const.MIDI_BALANCE,
                                          value=mp.MIDI_BALANCE)
            midiutil.control_change_event(current_track, channel=active_channel, control=const.MIDI_REVERB,
                                          value=mp.MIDI_REVERB_VAL)
            midiutil.control_change_event(current_track, channel=active_channel, control=const.MIDI_CHORUS,
                                          value=mp.MIDI_CHORUS_VAL)
            midiutil.control_change_event(current_track, channel=active_channel, control=const.MIDI_CHANNEL_VOLUME,
                                          value=mp.MIDI_CHANNEL_VOLUME_VAL)

            if is_melody_instrument:

                self.create_melody_midi(current_track, current_channel, track_id)
                current_channel += 1
                if current_channel == 9:
                    current_channel += 1  # 9 reserved for percussion

            else:  # percussion instrument

                self.create_percussion_midi(current_track, perc_instrument_type, track_id)

            midiutil.end_of_track_event(current_track)

        package_dir = os.path.dirname(const.__file__) + "/"
        midifilename = package_dir + const.MID_DIR + self.inka_data['random_file_name'] + '.mid'

        midiutil.write_midifile(midifilename, midi_pattern)

    # end create_midi

    def create_track(self, track):
        """ Main function called for each instrument track.
            generates tone positions, height values, intensities and connection_types

        """

        # start create_track

        c_2 = self.inka_data_2
        c_3 = self.inka_data_3

        if track == const.HARMONY_TRACK:
            c_2['harmony_track'] = algorithms.InkaAlgorithms(composition_struct=c_2['composition_struct'],
                                                             num_composed_bars=c_3['num_composed_bars'],
                                                             track_id=const.HARMONY_TRACK,
                                                             track_info=[],
                                                             rndm_2=self.inka_data['rndm_2'])
            c_2['harmony_track'].set_scale(self.inka_data['menu_options'].get_selected_scale())
            c_2['harmony_track'].set_harmony_class(c_3['harmony_class'])
            c_2['harmony_track'].set_bar_distribution(c_2['bar_distribution'])
            c_2['harmony_track'].start_createmelody([], c_2['bpm'], c_2['selected_speed'], c_2['global_rhythm'])
        else:
            c_2['composed_track'].append(algorithms.InkaAlgorithms(composition_struct=c_2['composition_struct'],
                                                                   num_composed_bars=c_3['num_composed_bars'],
                                                                   track_id=track,
                                                                   track_info=c_2['track_info'][track],
                                                                   rndm_2=self.inka_data['rndm_2']))

            assert c_2['harmony_track'] is not None, "harmony track is  missing"

            c_2['composed_track'][track].set_scale(self.inka_data['menu_options'].get_selected_scale())
            c_2['composed_track'][track].set_harmony_class(c_3['harmony_class'])
            c_2['composed_track'][track].set_basicscale_class(c_2['basic_scales'])
            c_2['composed_track'][track].set_bar_distribution(c_2['bar_distribution'])

            c_2['composed_track'][track].start_createmelody(c_2['harmony_track'],
                                                            c_2['bpm'],
                                                            c_2['selected_speed'],
                                                            c_2['global_rhythm'])

    def create_composition(self):
        """ This function generates a composition """

        c_2 = self.inka_data_2
        c_3 = self.inka_data_3

        try:
            # to do: is this line correct? is it necessary?
            cherrypy.session.release_lock()

        except AttributeError:
            pass

        # get num of beats (per bar) for selected rhythm
        c_2['num_of_beats'] = self.inka_data['menu_options'].get_num_of_beats()

        # get length of composition in seconds
        c_2['length_in_seconds'] = self.inka_data['menu_options'].get_selected_length()

        # calculate slightly corrected bpm to ensure number of bars is multiple of 4 AND length
        # of composition is as set in web interface
        c_2['bpm'] = self.inka_data['menu_options'].get_corrected_bpm(c_2['num_of_beats'], c_2['length_in_seconds'])
        if const.DEBUG_OUTPUT:
            print('bpm is', c_2['bpm'])

        c_2['num_of_bars'] = self.calc_num_of_bars()

        c_2['selected_speed'] = self.inka_data['menu_options'].get_selected_speed()

        # replace any wildcard harmonies in scale
        self.inka_data['menu_options'].replace_wildcard_harmonies_in_scale(c_3['harmony_class'],
                                                                           self.inka_data['rndm_2'])

        # set other values, which depend on num_of_bars
        self.inka_data['menu_options'].set_intro_ending_bridge_melody_length(self.inka_data['rndm_2'],
                                                                             c_2['num_of_bars'])

        # create a global rhythm for the composition, based on the selected rhythm
        speed = self.inka_data['menu_options'].get_selected_speed()  # speed[1] is MIN_SPLIT_LENGTH
        c_2['global_rhythm'], c_2['selected_rhythm'] = \
            rhythm_algorithms.create_global_rhythm(self.inka_data['menu_options'].get_selected_rhythm_definition(),
                                                   c_2['num_of_beats'],
                                                   speed[1],
                                                   self.inka_data['rndm_2'])

        # prepare all tracks of the composition, based on instruments and rhythm selected
        c_2['number_of_tracks'] = tu.prepare_track_info(c_2['track_info'],
                                                        self.inka_data['menu_options'],
                                                        c_2['selected_rhythm'],
                                                        self.inka_data['rndm_2'])

        # now create the main structure of the composition, as a hierarchical object
        composition_struct_object = structures.CompositionStructure(num_of_bars=c_2['num_of_bars'],
                                                                    number_of_tracks=c_2['number_of_tracks'],
                                                                    track_info=c_2['track_info'],
                                                                    menu_options=self.inka_data['menu_options'],
                                                                    rndm_2=self.inka_data['rndm_2'])
        c_2['composition_struct'], c_3['num_composed_bars'] = composition_struct_object.create_composition_structure()

        # create a flat (non-hierarchical) version of the composition structure

        # start with level 1, level 0 never contains created bars
        c_2['bar_struct'] = composition_struct_object.create_bar_structure(c_2['composition_struct'][SUB_INDX], 1)

        # for debugging purposes
        # composition_struct_object.show_bar_struct()

        # calculate how often a specific bar is used within the composition
        # The data structure bar_distribution will later contain additional information about
        # each bar

        bar_distribution_object = bar_distribution.BarDistribution(self.inka_data, c_2)
        c_2['bar_distribution'] = bar_distribution_object.create_bar_distribution(c_2['bar_struct'])
        # self.show_bar_distribution()

        bar_distribution_object.set_bar_harmony_type()
        bar_distribution_object.set_paused_bars()

        # create track rhythms for all non-percussion tracks

        for track in c_2['track_info']:
            if tu.is_melody_instrument(track):
                tr_rhythm = rhythm_algorithms.create_track_rhythm(track, c_2['global_rhythm'], c_2['bpm'],
                                                                  c_2['selected_speed'],
                                                                  self.inka_data['rndm_2'])
                tu.set_track_rhythm(track, tr_rhythm)

        tu.show_track_info(c_2['track_info'])

        # create a harmony track first, used by all other instrument tracks
        self.create_track(const.HARMONY_TRACK)

        # now create all instrument tracks
        for track in range(len(c_2['track_info'])):
            self.create_track(track)

        self.create_midi()
