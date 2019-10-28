# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file defines all settings used to create a musical piece

"""

import copy
import inkamusic.const as const
from inkamusic.const import RNDM_STRUCTURE
import inkamusic.basic_rhythms as basic_rhythms
from inkamusic.general_midi_instruments import GM_INSTRUMENTS as gm
import inkamusic.menu_entries as me
import inkamusic.music_parameter as mp


def get_instrument_by_id(instru_id):
    """looks up instrument definition for given id"""

    num_of_instruments = len(gm)
    indx = 0
    while indx < num_of_instruments:
        if gm[indx][const.INSTRUMENT_ID_INDX] == instru_id:
            indx_2 = indx - 1
            while gm[indx][const.INSTRUMENT_TXT_INDX] == '':
                gm[indx][const.INSTRUMENT_TXT_INDX] = gm[indx_2][const.INSTRUMENT_TXT_INDX]
                gm[indx][const.INSTRUMENT_MIDI_INDX] = gm[indx_2][const.INSTRUMENT_MIDI_INDX]
                indx_2 -= 1

            return gm[indx]
        indx += 1
    assert False, "Instrument ID not found, "+repr(instru_id)


def get_instrument_type(instru_id):
    """returns instrument type (T_BASS, T_CHOR, T_SOLO, T_HMNY, T_PERC)"""

    instrument_type = get_instrument_by_id(instru_id)[const.INSTRUMENT_TYPE_INDX]
    return instrument_type


def get_instrument_by_property(instru_type, instru_type_2, rndm_2):
    """ selects instrument with specific properties randomly """

    block_for_logic_pro_list = [134, 142, 150, 158, 638, 639, 640, 641, 642, 643, 644]

    num_of_instruments = len(gm)
    indx = 0
    count = 0
    while indx < num_of_instruments:
        if gm[indx][const.INSTRUMENT_TYPE_INDX] == instru_type \
         and gm[indx][const.INSTRUMENT_TYPE_2_INDX] == instru_type_2:
            if not mp.LOGIC_PRO_MIDI_SETTINGS:
                count += 1
            elif gm[indx][const.INSTRUMENT_ID_INDX] not in block_for_logic_pro_list:
                count += 1

        indx += 1
    assert count > 0, "Instrument properties not found"

    use_instru = rndm_2[const.RNDM_INSTRU].rndm_int(1, count)
    indx = 0
    count = 0
    while indx < num_of_instruments:
        if gm[indx][const.INSTRUMENT_TYPE_INDX] == instru_type \
         and gm[indx][const.INSTRUMENT_TYPE_2_INDX] == instru_type_2:
            if not mp.LOGIC_PRO_MIDI_SETTINGS:
                count += 1
            elif gm[indx][const.INSTRUMENT_ID_INDX] not in block_for_logic_pro_list:
                count += 1
            if count == use_instru:
                return gm[indx]
        indx += 1


def get_instrument_by_name_and_property(name, instru_type, instru_type_2):
    """ selects instrument with specific properties """

    num_of_instruments = len(gm)
    indx = 0
    count = 0
    while indx < num_of_instruments:
        if gm[indx][const.INSTRUMENT_TYPE_INDX] == instru_type \
         and gm[indx][const.INSTRUMENT_TYPE_2_INDX] == instru_type_2:
            indx_2 = indx - 1
            while gm[indx][const.INSTRUMENT_TXT_INDX] == '':
                gm[indx][const.INSTRUMENT_TXT_INDX] = gm[indx_2][const.INSTRUMENT_TXT_INDX]
                gm[indx][const.INSTRUMENT_MIDI_INDX] = gm[indx_2][const.INSTRUMENT_MIDI_INDX]
                indx_2 -= 1
            if gm[indx][const.INSTRUMENT_TXT_INDX] == name:
                return gm[indx]

        indx += 1
    assert count > 0, "Instrument properties not found"


def get_length_min(txt=''):
    """ returns minutes options"""
    if txt == '':  # return all entries
        return me.LENGTH_MIN
    # return specific entry
    return [entry[1] for entry in me.LENGTH_MIN if entry and entry[0] == txt][0]


def get_length_sec(txt=''):
    """ returns seconds options"""
    if txt == '':  # return all entries
        return me.LENGTH_SEC
    # return specific entry
    return [entry[1] for entry in me.LENGTH_SEC if entry and entry[0] == txt][0]


def get_instrumentation(txt):
    """ returns list of ids for specific instrumentation"""
    return [entry[1] for entry in me.INSTRUMENTATION_LIST if len(entry) > 0 and entry[0] == txt][0]


def get_scale(txt):
    """ returns scale definition"""
    return [entry[1] for entry in me.SCALES_LIST if len(entry) > 0 and entry[0] == txt][0]


def get_scales_list():
    """ returns list of scales"""
    return me.SCALES_LIST


def get_percussion_list(txt=''):
    """ returns list of percussion options"""
    if txt == '':  # return all entries
        return me.PERCUSSION_LIST
    # return specific entry
    return [entry[1] for entry in me.PERCUSSION_LIST if len(entry) > 0 and entry[0] == txt][0]


def get_percussion(txt):
    """ returns percussion setting"""

    return [entry[1] for entry in me.PERCUSSION_LIST if len(entry) > 0 and entry[0] == txt][0]


def get_rhythm_list():
    """ returns list of all rhythms"""
    return me.RHYTHM_LIST


def get_rhythm(txt):
    """ returns id of specific basic rhythm"""

    return [entry[1] for entry in me.RHYTHM_LIST if len(entry) > 0 and entry[0] == txt][0]


def get_rhythm_bpm(txt):
    """ returns bpm range of specific basic rhythm"""

    return [(entry[2], entry[3]) for entry in me.RHYTHM_LIST if len(entry) > 0 and entry[0] == txt][0]


def get_speed(txt):
    """ returns bpm limits for specific speed"""
    return [(entry[1], entry[2]) for entry in me.SPEED_LIST if len(entry) > 0 and entry[0] == txt][0]


def get_speed_list():
    """ returns list of all speed options"""
    return me.SPEED_LIST


def get_pause_probability(instrument_type, instrument_type_2, rndm_2):
    """returns a random probability for the instrument type to pause for a full bar
       Used only for percussion instruments. melody instruments define pauses individually in
       instrumentation_list"""
    index = instrument_type_2

    if instrument_type == const.T_PERC:

        return rndm_2[const.RNDM_INSTRU].rndm_choice(mp.PERC_PAUSE_PROB[index]) / 100

    return rndm_2[const.RNDM_INSTRU].rndm_choice(mp.INSTRU_PAUSE_PROB[index]) / 100


class Settings():
    """ This class defines all possible settings and menu entries
    """

    def __init__(self):
        self.comp_data = {'selected_rhythm': None,
                          'bpm': None,
                          'selected_length': None,
                          'smallest_part_length': None,
                          'intro_length': None,
                          'ending_length': None,
                          'bridge_length': None,
                          'staccato_flag': None,
                          'selected_instrumentation': None,
                          'selected_scale': [],
                          'selected_percussion': None,
                          'selected_speed': None
                          }
        self.basic_rhythm_list = basic_rhythms.BasicRhythm()

    def reset(self):
        """ resets all settings"""
        self.comp_data = {'selected_rhythm': None,
                          'bpm': None,
                          'selected_length': None,
                          'smallest_part_length': None,
                          'intro_length': None,
                          'ending_length': None,
                          'bridge_length': None,
                          'staccato_flag': None,
                          'selected_instrumentation': None,
                          'selected_scale': None,
                          'selected_percussion': None,
                          'selected_speed': None
                          }

    def set_web_interface_selections(self, web_settings):
        """set all settings from web interface"""

        self.__set_selected_instrumentation(web_settings['sel_instrumentation'])
        self.__set_selected_scale(web_settings['sel_scales'])
        self.__set_selected_percussion(web_settings['sel_percussion'])
        self.__set_selected_rhythm(web_settings['sel_rhythms'])
        self.__set_selected_length(web_settings['sel_lengthmin'], web_settings['sel_lengthsec'])
        self.__set_selected_speed(web_settings['sel_speed'])

    def __set_selected_instrumentation(self, txt):
        """sets instrument id list of selected instrumentation"""
        self.comp_data['selected_instrumentation'] = get_instrumentation(txt)

    def get_selected_instrumentation(self):
        """returns id list of selected instrumentation"""
        assert self.comp_data['selected_instrumentation'] is not None, "Selected instrumentation was not set"
        return self.comp_data['selected_instrumentation']

    def __set_selected_scale(self, txt):
        """sets selected scale"""
        self.comp_data['selected_scale'] = copy.deepcopy(get_scale(txt))  # copy is used as wildcards are replaced later

    def get_selected_scale(self):
        """returns the currently selected scale"""
        return self.comp_data['selected_scale']

    def replace_wildcard_harmonies_in_scale(self, harmony_object, rndm_2):
        """replaces any wildcard harmony in scale definition"""

        # example for scale [7, 65, 0, 0, [HARMONY_PREFER_MAJOR_VAR, HARMONY_ANY]]
        already_used = []
        rc = rndm_2[const.RNDM_MELO_RHYTHM].rndm_choice
        for i, harmony_type in enumerate(self.comp_data['selected_scale'][const.SCALE_HARMONY_TYPES_INDX]):
            if harmony_type < 0:  # wildcard harmony
                if i == 0:  # first harmony must be buildable on first scale tone
                    use_type = rc(harmony_object.get_possible_harmony_type_for_scale(self.comp_data['selected_scale'],
                                                                                     harmony_type, True, already_used))
                else:
                    use_type = rc(harmony_object.get_possible_harmony_type_for_scale(self.comp_data['selected_scale'],
                                                                                     harmony_type, False, already_used))

                self.comp_data['selected_scale'][const.SCALE_HARMONY_TYPES_INDX][i] = use_type
                already_used.append(use_type)
            else:
                already_used.append(harmony_type)
        if const.DEBUG_OUTPUT:
            print(' ')
            for harmony_type in self.comp_data['selected_scale'][const.SCALE_HARMONY_TYPES_INDX]:

                print('harmony used is', harmony_object.get_harmony_steps_from_type(harmony_type))

    def __set_selected_percussion(self, txt):
        """sets selected percussion option"""
        self.comp_data['selected_percussion'] = get_percussion(txt)

    def get_selected_percussion(self):
        """returns percussion setting"""
        return self.comp_data['selected_percussion']

    def __set_selected_rhythm(self, txt):
        """sets id of rhythm selected in web interface"""
        self.comp_data['selected_rhythm'] = get_rhythm(txt)
        self.comp_data['selected_rhythm_bpm'] = get_rhythm_bpm(txt)

    def get_selected_rhythm(self):
        """returns id of selected rhythm"""
        assert self.comp_data['selected_rhythm'] is not None, "Selected rhythm was not set"
        return self.comp_data['selected_rhythm']

    def get_selected_rhythm_bpm(self):
        """returns bpm range of selected rhythm"""
        assert self.comp_data['selected_rhythm_bpm'] is not None, "Selected rhythm_bpm was not set"
        return self.comp_data['selected_rhythm_bpm']

    def get_num_of_beats(self):
        """returns num of beats per bar for selected rhythm"""
        r_id = self.get_selected_rhythm()

        rhythm = self.basic_rhythm_list.get_basic_rhythm_by_id(r_id)
        return rhythm[const.NUM_OF_BEATS_INDX]

    def get_selected_rhythm_definition(self):
        """returns basic definition for selected rhythm"""
        r_id = self.get_selected_rhythm()

        rhythm = self.basic_rhythm_list.get_basic_rhythm_by_id(r_id)
        return rhythm

    def __set_selected_length(self, txtmin, txtsec):
        """sets current length"""
        self.comp_data['selected_length'] = get_length_sec(txtsec) + 60 * get_length_min(txtmin)

        # correct special case 0
        if self.comp_data['selected_length'] == 0:
            self.comp_data['selected_length'] = 5

    def get_selected_length(self):
        """returns selected length in seconds"""
        assert self.comp_data['selected_length'] is not None, "Selected length was not set"
        return self.comp_data['selected_length']

    def __set_selected_speed(self, txt):
        """sets selected speed"""
        self.comp_data['selected_speed'] = get_speed(txt)

    def get_selected_speed(self):
        """returns bpm limits of selected speed"""
        assert self.comp_data['selected_speed'] is not None, "Selected speed was not set"
        return self.comp_data['selected_speed']

    # bpm (beats per minute) functions (not directly set in web interface)
    # pylint: disable=locally-disabled, unsubscriptable-object

    def set_selected_bpm(self, rndm_2):
        """sets bpm based on speed setting"""
        bpm_limits = self.get_selected_rhythm_bpm()
        bpm_range = bpm_limits[1] - bpm_limits[0]

        slow_fast = self.get_selected_speed()[0]

        low = int(bpm_limits[0] + slow_fast / 3 * bpm_range)
        high = int(bpm_limits[0] + (slow_fast + 1) / 3 * bpm_range)

        self.comp_data['bpm'] = rndm_2[const.RNDM_OTHER].rndm_int(low, high)

    def get_selected_bpm(self):
        """returns current bpm value"""
        assert self.comp_data['bpm'] is not None, "Selected bpm was not set"
        return self.comp_data['bpm']

    def get_corrected_bpm(self, beats, length_in_seconds):
        """Adjust self.comp_data['bpm'] slightly to ensure that the number of bars is
           exactly a multiple of num_of_bars_multiple
           AND the playing time is exactly as selected in the web interface."""

        # change bpm so that num of bars will be exact multiple of num_of_bars_multiple
        num_of_bars_multiple = 1  # default 1

        n_exact = ((self.comp_data['bpm'] * length_in_seconds / 60.0) / beats) / num_of_bars_multiple
        n_new = int(n_exact + 0.5)
        if n_new == 0:
            n_new = 1
        corr = (n_new * beats * num_of_bars_multiple * 60.0) / (self.comp_data['bpm'] * length_in_seconds)
        self.comp_data['bpm'] = int(corr * self.comp_data['bpm'] + 0.5)
        return self.comp_data['bpm']

    def set_intro_ending_bridge_melody_length(self, rndm_2, num_of_bars):
        """sets length of melody, intro, ending and bridge parts"""
        self.__set_smallest_part_length(rndm_2, num_of_bars)
        self.__set_intro_ending_length(rndm_2, num_of_bars, self.get_smallest_part_length())
        self.__set_bridge_length(rndm_2, num_of_bars)

        # also initializes staccato flag
        self.__set_staccato_flag(rndm_2)

    # smallest part length length
    def __set_smallest_part_length(self, rndm_2, num_of_bars):
        """Sets the smallest part length in bars. A part is subdivided (structured) if it is bigger than this number"""
        if self.comp_data['smallest_part_length'] is None:
            # the settings for num_of_bars 1 to 4 are special cases which would be used for extremely short pieces only
            if num_of_bars == 1:
                self.comp_data['smallest_part_length'] = 1  # ending 1 bar only
            elif num_of_bars == 2:
                self.comp_data['smallest_part_length'] = 2  # ending 2 bars only
            elif num_of_bars == 3:
                self.comp_data['smallest_part_length'] = 1  # intro 1 bar ending 2 bars
            elif num_of_bars == 4:
                self.comp_data['smallest_part_length'] = 2  # intro 2 bars ending 2 bars
            else:
                self.comp_data['smallest_part_length'] \
                 = rndm_2[RNDM_STRUCTURE].rndm_choice(me.SMALLEST_PART_LENGTH_OPTIONS)
                if self.comp_data['smallest_part_length'] + 2 > num_of_bars:
                    self.comp_data['smallest_part_length'] = num_of_bars - 2

        assert self.comp_data['smallest_part_length'] > 0, "Problem with smallest_part_length length"

    def get_smallest_part_length(self):
        """returns the smallest part length in bars"""
        assert self.comp_data['smallest_part_length'] is not None, "smallest_part length was not set"
        return self.comp_data['smallest_part_length']

    # intro and ending length (randomly chosen, could be included into web interface)
    def __set_intro_ending_length(self, rndm_2, num_of_bars, smallest_part_length):
        """sets the intro and ending length in bars"""
        if self.comp_data['intro_length'] is None:
            if num_of_bars <= 2:
                self.comp_data['intro_length'] = 0
                self.comp_data['ending_length'] = num_of_bars
            elif num_of_bars == 3:
                self.comp_data['intro_length'] = 1
                self.comp_data['ending_length'] = 2
            elif num_of_bars == 4:
                self.comp_data['intro_length'] = 2
                self.comp_data['ending_length'] = 2
            elif smallest_part_length + 2 == num_of_bars:
                self.comp_data['intro_length'] = 0
                self.comp_data['ending_length'] = 2
            else:
                self.comp_data['intro_length'] = num_of_bars
                self.comp_data['ending_length'] = num_of_bars
                while (smallest_part_length + self.comp_data['intro_length'] + self.comp_data['ending_length']
                       > num_of_bars):
                    self.comp_data['intro_length'] = rndm_2[RNDM_STRUCTURE].rndm_choice(me.INTRO_LENGTH_OPTIONS)
                    self.comp_data['ending_length'] = rndm_2[RNDM_STRUCTURE].rndm_choice(me.ENDING_LENGTH_OPTIONS)

    def get_intro_ending_length(self):
        """returns the intro_ending length in bars"""
        assert self.comp_data['intro_length'] is not None, "intro length was not set"
        assert self.comp_data['ending_length'] is not None, "ending length was not set"
        return self.comp_data['intro_length'], self.comp_data['ending_length']

    # bridge length (randomly chosen, could be included into web interface)
    def __set_bridge_length(self, rndm_2, num_of_bars):
        """sets the bridge length in bars"""
        if self.comp_data['bridge_length'] is None:
            self.comp_data['bridge_length'] \
             = num_of_bars // rndm_2[RNDM_STRUCTURE].rndm_choice(me.BRIDGE_LENGTH_OPTIONS)
            if self.comp_data['bridge_length'] < 1:
                self.comp_data['bridge_length'] = 1

    def get_bridge_length(self):
        """returns the bridge_length length in bars"""
        assert self.comp_data['bridge_length'] is not None, "bridge_length length was not set"
        return self.comp_data['bridge_length']

    # staccato allowed for composition (randomly chosen, could be included into web interface)
    def __set_staccato_flag(self, rndm_2):
        """sets the staccato flag,
           staccato rhythm connections are only allowed if this flag is True"""
        if self.comp_data['staccato_flag'] is None:
            self.comp_data['staccato_flag'] \
             = rndm_2[const.RNDM_MELO_RHYTHM].rndm_choice([True, False, False, False, False])

    def get_staccato_flag(self):
        """returns the staccato_flag"""
        assert self.comp_data['staccato_flag'] is not None, "staccato_flag was not set"
        return self.comp_data['staccato_flag']

    def get_rhythm_connect_tuple(self, rndm_2):
        """ returns a random tuple from rhythm connect probability list
            depending on staccato_flag"""
        assert self.comp_data['staccato_flag'] is not None, "staccato_flag not set "
        if self.comp_data['staccato_flag']:
            return rndm_2[const.RNDM_MELO_RHYTHM].rndm_choice(me.RHYTHM_CONNECT_PROBABILITIES)

        rhythm_connect_tuple = [0, 0, 100]
        while rhythm_connect_tuple[2] != 0:
            rhythm_connect_tuple = rndm_2[const.RNDM_MELO_RHYTHM].rndm_choice(me.RHYTHM_CONNECT_PROBABILITIES)
        return rhythm_connect_tuple
