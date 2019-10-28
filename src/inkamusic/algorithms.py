# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file contains the main algorithmic functions

"""
import math
import copy
import inkamusic.trackinfo_util as tu
import inkamusic.const as const
from inkamusic.const import SUB_INDX, PROP_INDX, LEN_INDX, PROP_USEPART, NO_REPEAT
from inkamusic.const import PROP_FROM_BAR, PROP_ACTUAL_BAR, PROP_START, PROP_END
from inkamusic.const import RM_REPEAT
from inkamusic.const import FIRST_BAR_OF_PART, BEAT_RHYTHM, BEAT_MELODY

import inkamusic.music_parameter as mp
import inkamusic.rhythm_algorithms as rhythm_algorithms
import inkamusic.utilities as utilities


def show_bars_and_beats(txt, bars_beats):
    """prints bars and beats entries for debugging purposes"""
    if const.DEBUG_OUTPUT:
        print('Show bars_and_beats:  ', txt)
        for i in bars_beats:
            if i[0] == FIRST_BAR_OF_PART:
                print(' ')
                print('    Part starts with first bar number', i[1])
            elif i[0] == BEAT_RHYTHM:
                print('      rhythm for beat index', i[1])
                print('          ', i[2])
            elif i[0] == BEAT_MELODY:
                print('      melody for beat index', i[1])
                print('          rule', i[2])
                if not i[3]:
                    print('          melody entry is empty')
                else:
                    for j, melody_entry in enumerate(i[3]):
                        print('          melody entry', j, 'is', melody_entry)


def get_tone_from_envelope_val(envelope, instru_low, instru_high):
    """transforms envelope val (-1 ... +1) to tone height"""
    tone = ((instru_high - instru_low) * envelope + instru_high + instru_low) / 2
    tone = int(tone + 0.5)

    return tone


def get_last_tones_from_melody(melody, n_th_last_tone):
    """ gets nth last tone of current melody"""
    melody_len = len(melody)
    if melody_len < n_th_last_tone:
        return []

    return melody[melody_len - n_th_last_tone]


# def _change_up_down_equal(c_3, try_counter):
#     """selects different up down or equal setting if original setting was not possible"""
#     if try_counter > 0:
#         if try_counter == 1:
#             c_3['up_down_equal_probs'] = 1
#         elif try_counter == 2:
#             c_3['up_down_equal_probs'] = -1
#         else:
#             c_3['up_down_equal_probs'] = 0


class InkaAlgorithms():
    """This is the main algorithm class"""

    def __init__(self, **comp_data):

        self.comp_data = comp_data
        self.comp_data_2 = {'num_of_beats': -1,  # not yet defined
                            'num_of_first_bar': -1,  # not yet defined
                            'ends_level': -1,  # not yet defined
                            'starts_level': -1,  # not yet defined
                            'repeat_from_bar': -1,  # not yet defined
                            'num_bars_in_part': -1,  # not yet defined
                            'play_or_pause_indx': const.PLAYED_IN_TRACK + self.comp_data['track_id'],
                            'selected_solo_rhythm': -1,  # not yet defined
                            'vari_track_rhythm': -1,   # not yet defined
                            'global_rhythm': [],  # not yet defined
                            'bpm': -1,  # not yet defined
                            'tones': [],
                            'positions': [],
                            'bars_and_beats': [],
                            'connection_types': [],
                            'intensities': []
                            }
        self.comp_data_3 = {'scale': [],  # not yet defined
                            'harmony_class': None,  # not yet defined
                            'basicscale_class': None,  # not yet defined
                            'basic_scale': None,  # not yet defined
                            'bar_distribution': [],  # not yet defined  CHECK
                            'current_beat_harmony_rule': [],  # not yet defined
                            'disharmony_to_harmony_rule': [],  # not yet defined
                            'disharmony_to_used_tones': [],  # not yet defined
                            'up_down_equal_probs': -1,  # not yet defined
                            'melody': [],  # not yet defined CHECK
                            'inst_low': -1,  # not yet defined
                            'inst_high': -1,  # not yet defined
                            'is_percussion_instrument': -1,  # not yet defined
                            'is_solo_instrument': -1,  # not yet defined
                            'is_harmony_instrument': -1,  # not yet defined
                            'is_bass_instrument': -1,  # not yet defined
                            'created_bars_so_far': -1,  # not yet defined
                            'envelope_param_b': -1,  # not yet defined
                            'envelope_param_p': -1,  # not yet defined
                            'harmony_bars_and_beats': [],  # not yet defined
                            }

    def set_scale(self, scale):
        """ set scale of current composition"""
        self.comp_data_3['scale'] = scale

    def set_harmony_class(self, harmony_class):
        """ set instance of HarmonyBasics class"""
        self.comp_data_3['harmony_class'] = harmony_class

    def set_basicscale_class(self, basicscale_class):
        """ set instance of BasicScale class"""
        self.comp_data_3['basicscale_class'] = basicscale_class

    def set_bar_distribution(self, bar_distribution):
        """ sets bar distribution data of current composition"""
        self.comp_data_3['bar_distribution'] = bar_distribution

    def get_instrument_range(self):
        """sets instrument range"""

        low, high = tu.get_track_instrument_range(self.comp_data['track_info'])
        instru_range = high - low + 1
        assert instru_range >= mp.MIN_RANGE, "instru range too small"
        max_reduce_percent = mp.RANGE_REDUCTION
        max_reduce = int(max_reduce_percent * instru_range + 0.5)

        max_reduce = min(max_reduce, int((instru_range - mp.MIN_RANGE) / 2))

        reduce = self.comp_data['rndm_2'][const.RNDM_INSTRU].rndm_int(0, max_reduce)
        inst_low = low + reduce
        reduce = self.comp_data['rndm_2'][const.RNDM_INSTRU].rndm_int(0, max_reduce)
        inst_high = high - reduce
        assert inst_high - inst_low + 1 >= mp.MIN_RANGE

        return inst_low, inst_high

    def _get_envelope_param(self):
        """sets height envelope parameters"""
        num_of_bars_for_full_up_down \
            = int(self.comp_data['rndm_2'][const.RNDM_INSTRU].rndm_gauss_limit(mp.ENVELOPE_LENGTH))

        param_b = self.comp_data['num_composed_bars'] / num_of_bars_for_full_up_down
        # ending param defines how the piece ends (shifts by ending_param * pi/2)
        ending_param = self.comp_data['rndm_2'][const.RNDM_INSTRU].rndm_choice([0, 1, 2, 3])
        param_p = math.pi / 2 * (ending_param - 4 * param_b)

        return param_b, param_p

    def _get_previous_tones(self, tone_i):
        """ gets up to 2 previous tones if they are available"""
        c_3 = self.comp_data_3
        if tone_i > 1:
            first_previous_tone = get_last_tones_from_melody(c_3['melody'], 1)
            second_previous_tone = get_last_tones_from_melody(c_3['melody'], 2)

        elif tone_i > 0:
            first_previous_tone = get_last_tones_from_melody(c_3['melody'], 1)
            second_previous_tone = self._get_nth_last_tone_from_bars_and_beats(1)

        elif tone_i == 0:
            first_previous_tone = self._get_nth_last_tone_from_bars_and_beats(1)
            second_previous_tone = self._get_nth_last_tone_from_bars_and_beats(2)

        return [first_previous_tone, second_previous_tone]

    def _choose_new_harmony(self, anchor_harmony_needed, preset_harmo_type):
        """chooses a new harmony"""
        c_3 = self.comp_data_3

        melo_rule = self._get_last_harmony_from_bars_and_beats()

        if melo_rule != []:
            prev_harmony = melo_rule[0][1]  # example [2, 6, 9]
        else:
            prev_harmony = []

        if not anchor_harmony_needed:

            found_new_harmony = False
            count = 0

            while not found_new_harmony:
                count += 1
                harmony = c_3['harmony_class'].get_random_harmony_for_scale(c_3['scale'], preset_harmo_type,
                                                                            self.comp_data['rndm_2'])

                if melo_rule == []:
                    found_new_harmony = True
                else:
                    if (prev_harmony != harmony) or count > 100:
                        found_new_harmony = True
        else:  # anchor needed
            harmony, harmony_type \
             = c_3['harmony_class'].get_anchor_harmony_for_scale(c_3['scale'])
            assert harmony_type == preset_harmo_type

        one_beat_melody_rule = [[const.RM_HARMONY_TRACK_NEW_HARMO, harmony, preset_harmo_type]]
        # example for one_beat_melody_rule:  [[9, [4, 7, 11], 0]] ( 9 = constant for new harmony)

        one_beat_melody = []
        return one_beat_melody_rule, one_beat_melody

    def _get_tone_disharmony_values(self, beat_indx):
        """ calculates a value, which characterises the disharmony of a tone
            against a list of other tones.
            The distance between two tones is the shortest possible distance ignoring octaves.
            A distance of 0 is harmonic with a disharmony value of 0
            A distance of 1 is considered disharmonic with a disharmony value of 10
            A distance of 2 is harmonic with a disharmony value of 1
            Distance values >= 3 are considered harmonic with a disharmony value of 0
            """

        def find_tone_disharmony_value(tone, tone_list):
            """calculate the harmonic value of a tone added to a tone list
                possible values are 0, 1, 2 and >= const.DISHARMONIC_LIMIT
                The tone_list itself may contain disharmonic entries"""

            disharmony = 0

            for i in tone_list:
                distance = min((i - tone) % 12, (tone - i) % 12)
                if distance == 2:
                    disharmony += 1
                elif distance == 1:
                    disharmony += const.DISHARMONIC_LIMIT

            return disharmony

        c_3 = self.comp_data_3

        c_3['current_beat_harmony_rule'], used_tones \
            = self._get_harmony_from_bars_and_beats(beat_indx, self.comp_data_2['num_of_first_bar'])
        # example of c_3['current_beat_harmony_rule'] [[9, [6, 10, 1], 1]]
        # example of used_tones tbd
        # example of scale [7, 65, 0, 2, [1, 0, 2]] (SCALE_LEN, SCALE_COUNT, SCALE_START, SCALE_NOTE, harmonies)

        basic_scale = c_3['basicscale_class'].get_scale_by_index(c_3['scale'][const.SCALE_LEN_INDX],
                                                                 c_3['scale'][const.SCALE_COUNT_INDX],
                                                                 c_3['scale'][const.SCALE_START_INDX],
                                                                 c_3['scale'][const.SCALE_NOTE_INDX])

        c_3['basic_scale'] = basic_scale
        # example for basic_scale 7 65 with SCALE_START 0 (major pattern) and
        # SCALE_NOTE C (C-major): [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
        #                          c     d     e  f     g     a     b

        # example for basic_scale 7 65 with SCALE_START 0 (major pattern) and
        # SCALE_NOTE D (D-major): [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]

        # example for basic_scale 7 65 with SCALE_START 9 (minor pattern) and
        # SCALE_NOTE E (E-minor): [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
        #                          c     d     e    fis g     a     b

        assert c_3['current_beat_harmony_rule'] != [], "current_beat_harmony_rule can not be empty"

        # for each tone in scale: find disharmony to harmony_rule and disharmony to all used tones
        c_3['disharmony_to_harmony_rule'] = []
        c_3['disharmony_to_used_tones'] = []
        for tone in range(12):
            if basic_scale[tone] == 1:
                tone_disharmony = find_tone_disharmony_value(tone, c_3['current_beat_harmony_rule'][0][1])
                c_3['disharmony_to_harmony_rule'].append(tone_disharmony)
                c_3['disharmony_to_used_tones'].append(find_tone_disharmony_value(tone, used_tones))
            else:
                c_3['disharmony_to_harmony_rule'].append(const.NOT_IN_SCALE)
                c_3['disharmony_to_used_tones'].append(const.NOT_IN_SCALE)

    def _find_possible_tones(self, previous_tones, target_tone):
        """ finds all tones for an instrument track wich possibly could be used.
        For each usable tone an evaluation value is calculated"""

        c_3 = self.comp_data_3

        possible_tones = []

        instrument_type = tu.get_instrument_type(self.comp_data['track_info'])
        # const.T_SOLO, const.T_BASS, const.T_HMNY, const.T_CHOR, const.T_PERC
        assert instrument_type != const.T_PERC, "should never be perc instru"

        mp.MAX_TARGET_DEV = 9

        low_tone = target_tone - mp.MAX_TARGET_DEV
        high_tone = target_tone + mp.MAX_TARGET_DEV

        if low_tone < c_3['inst_low']:
            low_tone = c_3['inst_low']
            tones_available = high_tone - c_3['inst_low']
            if tones_available < 12:
                high_tone = c_3['inst_low'] + 12

        if high_tone > c_3['inst_high']:
            high_tone = c_3['inst_high']
            tones_available = c_3['inst_high'] - low_tone
            if tones_available < 12:
                low_tone = c_3['inst_high'] - 12

        for tone_abs_height in range(low_tone, high_tone + 1):
            result = utilities.check_tone(tone_abs_height, instrument_type, target_tone, previous_tones, c_3)
            # print('tone_abs_height, result',result[0],round(result[1],0))
            if result[1] > 0:  # final points
                possible_tones.append(result)

        return possible_tones

    def _decide_harmony_tones_only(self):
        """decides if solo, bass or chorus instrument uses only tones from current harmony"""
        c_3 = self.comp_data_3
        assert not c_3['is_harmony_instrument'] and not c_3['is_percussion_instrument']
        rnd_val = self.comp_data['rndm_2'][const.RNDM_MELO_RHYTHM].rndm_int(1, 100)
        if c_3['is_solo_instrument']:
            return rnd_val <= mp.SOLO_PLAYS_HARMONY_TONES_PROB
        if c_3['is_bass_instrument']:
            return rnd_val <= mp.BASS_PLAYS_HARMONY_TONES_PROB
        return rnd_val <= mp.CHORUS_PLAYS_HARMONY_TONES_PROB  # chorus instrument

    def _choose_tone(self, possible_tones):
        """selects randomly tone from possible tones weighted by evaluation points """
        num_tones = len(possible_tones)
        if num_tones == 0:
            return []

        population = [possible_tones[i][0] for i in range(0, num_tones)]
        weights = [possible_tones[i][1] for i in range(0, num_tones)]
        max_weight = max(weights)
        assert 0 <= mp.RATING_THRESHOLD <= 100
        for i, weight in enumerate(weights):
            if weight < max_weight:
                if weight < mp.RATING_THRESHOLD * max_weight / 100:
                    weights[i] = 0
        tone = self.comp_data['rndm_2'][const.RNDM_MELO_RHYTHM].rndm_choice(population,
                                                                            weights=weights)
        return [tone]

    def _do_harmony_instrument_tone(self, possible_tones):
        """selects tone (-group) for harmony instruments"""
        c_3 = self.comp_data_3
        # example of c_3['current_beat_harmony_rule'] [[9, [6, 10, 1], 1]]
        harmony_tones = c_3['current_beat_harmony_rule'][0][1]
        for i in range(len(possible_tones) - 1, -1, -1):
            if (possible_tones[i][0] % 12) not in harmony_tones:
                del possible_tones[i]

        selected_tone = []
        while possible_tones:
            add_tone = self._choose_tone(possible_tones)
            selected_tone = selected_tone + add_tone
            # remove this tone from all octaves
            for i in range(len(possible_tones) - 1, -1, -1):
                if (possible_tones[i][0] % 12) == add_tone[0] % 12:
                    del possible_tones[i]

        return selected_tone

    def _do_tone(self, possible_tones, ending_flags):
        """selects a tone for non-special cases"""
        c_3 = self.comp_data_3
        use_harmony_tones_only = self._decide_harmony_tones_only()

        # ending_flags[0] => True if last two bars
        if ending_flags[0] or use_harmony_tones_only:  # only harmonic tones are allowed
            # example of c_3['current_beat_harmony_rule'] [[9, [6, 10, 1], 1]]
            harmony_tones = c_3['current_beat_harmony_rule'][0][1]
            for i in range(len(possible_tones) - 1, -1, -1):
                if (possible_tones[i][0] % 12) not in harmony_tones:
                    del possible_tones[i]
        selected_tone = self._choose_tone(possible_tones)

        return selected_tone

    def _do_one_tone(self, beat_indx, tone_i, ending_flags, target_tone):
        """selects one tone within melody of current track"""

        # start do_one_tone
        # try to find previous tones
        previous_tones = self._get_previous_tones(tone_i)
        possible_tones = self._find_possible_tones(previous_tones, target_tone)
        # ex [[61, 8], [63, 8], [66, 8], [68, 8], [70, 8], [73, 8], [75, 8], [78, 8]]

        c_3 = self.comp_data_3

        if possible_tones == []:
            selected_tone = []
        else:
            # ending_flags[1] == True => last tone
            if ending_flags[1] and (c_3['is_solo_instrument'] or c_3['is_bass_instrument']):  # use  anchor
                anchor_tone = c_3['scale'][const.SCALE_NOTE_INDX]
                # print('anchor tone used in bar',self.comp_data_2['num_of_first_bar'] )
                for i in range(len(possible_tones) - 1, -1, -1):
                    if (possible_tones[i][0] % 12) != anchor_tone:
                        del possible_tones[i]

                selected_tone = self._choose_tone(possible_tones)

            elif c_3['is_harmony_instrument']:  # generates multiple tones
                selected_tone = self._do_harmony_instrument_tone(possible_tones)

            else:
                selected_tone = self._do_tone(possible_tones, ending_flags)

        c_3['melody'].append(selected_tone)

        self._add_as_used_tone_to_harmony_track(beat_indx, self.comp_data_2['num_of_first_bar'], selected_tone)

    def _do_melody(self, beat_indx, last_bar, nextto_last_bar):
        """creates the melody for one beat"""

        c_3 = self.comp_data_3

        c_3['melody'] = []  # melody of beat_index will be constructed in this array

        target_tone = get_tone_from_envelope_val(self._get_envelope_val(beat_indx), c_3['inst_low'], c_3['inst_high'])

        # up down equal characteristics
        if beat_indx == 0:
            tone_group_length, c_3['up_down_equal_probs'] \
             = utilities.get_up_down_equal_characteristics(self.comp_data['rndm_2'][const.RNDM_MELO_RHYTHM])
        else:
            _, melo_rule = self._get_melody_from_bars_and_beats(beat_indx - 1, self.comp_data_2['num_of_first_bar'])
            # example melo_rule = [[4, [25, 75, 0]]]
            tone_group_length = melo_rule[0][0]
            c_3['up_down_equal_probs'] = melo_rule[0][1]

        # get melody from previous beat, which is the last beat added to bars_and_beats
        last_used_tones = self._get_nth_last_tone_from_bars_and_beats(1)

        # add tones from previous beat to used_tones, will be used for following instruments, not for current
        # to avoid dissonances with long tones

        if last_used_tones:
            self._add_as_used_tone_to_harmony_track(beat_indx, self.comp_data_2['num_of_first_bar'],
                                                    last_used_tones)

        one_beat_rhythm = rhythm_algorithms.get_rhythm_from_bars_and_beats(beat_indx,
                                                                           self.comp_data_2['num_of_first_bar'],
                                                                           self.comp_data_2)

        # ex [[0, 5, 4], [360, 2, 4]]

        number_of_tones_in_beat = len(one_beat_rhythm)
        for tone_i in range(number_of_tones_in_beat):

            self._do_one_tone(beat_indx,
                              tone_i,
                              [last_bar or nextto_last_bar, last_bar and tone_i == number_of_tones_in_beat - 1],
                              target_tone)

        one_beat_melody = copy.deepcopy(c_3['melody'])

        tone_group_length -= number_of_tones_in_beat
        if tone_group_length <= 0:
            tone_group_length, c_3['up_down_equal_probs'] \
             = utilities.get_up_down_equal_characteristics(self.comp_data['rndm_2'][const.RNDM_MELO_RHYTHM])

        return [[tone_group_length, c_3['up_down_equal_probs']]], one_beat_melody

    def _get_melody_from_bars_and_beats(self, beat_indx, start_from_bar):
        """gets melody and melody rule for a beat defined by start_bar and beat_indx"""
        len_bars_and_beats = len(self.comp_data_2['bars_and_beats'])
        i = 0
        active = 0
        while i < len_bars_and_beats:
            if self.comp_data_2['bars_and_beats'][i][0] == FIRST_BAR_OF_PART:
                if self.comp_data_2['bars_and_beats'][i][1] == start_from_bar:
                    active = 1
                    beat_counter = 0

            if active == 1:
                if self.comp_data_2['bars_and_beats'][i][0] == BEAT_MELODY:
                    if beat_counter == beat_indx:
                        one_beat_melody = copy.deepcopy(self.comp_data_2['bars_and_beats'][i][3])
                        one_beat_melody_rule = copy.deepcopy(self.comp_data_2['bars_and_beats'][i][2])
                        break
                    beat_counter += 1
            i += 1
        return one_beat_melody, one_beat_melody_rule

    def _get_last_harmony_from_bars_and_beats(self):
        """returns the last used harmony"""

        len_bars_and_beats = len(self.comp_data_2['bars_and_beats'])
        i = len_bars_and_beats-1
        one_beat_melody_rule = []

        while i >= 0:
            if self.comp_data_2['bars_and_beats'][i][0] == BEAT_MELODY:

                one_beat_melody_rule = self.comp_data_2['bars_and_beats'][i][2]
                break

            i -= 1
        return one_beat_melody_rule

    def _get_nth_last_tone_from_bars_and_beats(self, n_from_end):
        """returns the n_from_end tone starting at the end of bars and beats
           A tone entry can be a tuple of more than one tone, if the beat contains more
           than one tone.
           The maximum number of beats this function searches backward from the end is n_from_end * 4"""

        len_bars_and_beats = len(self.comp_data_2['bars_and_beats'])
        i = len_bars_and_beats-1
        one_beat_melody = []
        find = n_from_end
        max_beats_backward = 0
        while i >= 0:
            if self.comp_data_2['bars_and_beats'][i][0] == BEAT_MELODY:
                max_beats_backward += 1
                num_of_tones_in_beat = len(self.comp_data_2['bars_and_beats'][i][3])
                if num_of_tones_in_beat >= find:
                    one_beat_melody = self.comp_data_2['bars_and_beats'][i][3][num_of_tones_in_beat - find]
                    break
                if max_beats_backward > n_from_end * 4:
                    break
                else:
                    find -= num_of_tones_in_beat
            i -= 1
        return one_beat_melody

    def _get_harmony_from_bars_and_beats(self, beat_indx, start_from_bar):
        """gets harmony rule and used tones for a beat defined by start_bar and beat_indx"""

        c_3 = self.comp_data_3

        one_beat_harmony_rule = []
        len_bars_and_beats = len(c_3['harmony_bars_and_beats'])
        i = 0
        active = 0
        while i < len_bars_and_beats:
            if c_3['harmony_bars_and_beats'][i][0] == FIRST_BAR_OF_PART:
                if c_3['harmony_bars_and_beats'][i][1] == start_from_bar:
                    active = 1
                    beat_counter = 0

            if active == 1:
                if c_3['harmony_bars_and_beats'][i][0] == BEAT_MELODY:
                    #  example for c_3['harmony_bars_and_beats'][i]
                    # [-5, 0, [[9, [4, 7, 11], 0]], []]
                    # [BEAT_MELODY, beat_indx, [harmony rule], used tones]
                    # [harmony rule] = [constant for new harmony, specific harmony, harmony type]

                    if beat_counter == beat_indx:
                        one_beat_harmony_rule = c_3['harmony_bars_and_beats'][i][2]
                        used_tones = c_3['harmony_bars_and_beats'][i][3]
                        break
                    beat_counter += 1
            i += 1
        return one_beat_harmony_rule, used_tones

    def _add_as_used_tone_to_harmony_track(self, beat_indx, start_from_bar, tone):
        """adds a tone as used tone to harmony entry"""
        # ex tone is [60, 64, 67]
        c_3 = self.comp_data_3
        len_bars_and_beats = len(c_3['harmony_bars_and_beats'])
        i = 0
        active = False
        while i < len_bars_and_beats:
            if c_3['harmony_bars_and_beats'][i][0] == FIRST_BAR_OF_PART:
                if c_3['harmony_bars_and_beats'][i][1] == start_from_bar:
                    active = True
                    beat_counter = 0

            if active and c_3['harmony_bars_and_beats'][i][0] == BEAT_MELODY:
                #  example for c_3['harmony_bars_and_beats'][i][0]
                # [-5, 0, [[9, [6, 10, 1], 1]], []]
                # [BEAT_MELODY, beat_indx, [harmony rule], used tones]

                if beat_counter == beat_indx:

                    for j in tone:
                        if j % 12 not in c_3['harmony_bars_and_beats'][i][3]:
                            c_3['harmony_bars_and_beats'][i][3].append(j % 12)
                    break
                beat_counter += 1
            i += 1

    def _get_envelope_val(self, beat_indx):
        """ returns value between -1 ... +1 indicating the height level to be used"""

        c_3 = self.comp_data_3

        # total number of composed beats in whole composition
        num_of_composed_beats = self.comp_data_2['num_of_beats'] * self.comp_data['num_composed_bars']

        current_composed_beat = c_3['created_bars_so_far'] * self.comp_data_2['num_of_beats'] + beat_indx

        relative_position = current_composed_beat / (num_of_composed_beats - 1)  # 0.0 ... 1.0
        relative_position = min(relative_position, 1.0)  # last bar may be created instead of repeated

        assert 0 <= relative_position <= 1.0, "rel pos wrong"

        envelope_val = utilities.sin_special(c_3['envelope_param_b'] * 2 * math.pi *
                                             relative_position + c_3['envelope_param_p'])

        return envelope_val

    def _melody_generator(self, beat_indx, melody_rule):
        """generates melody for one beat based on part type (normal, repeated, harmony) and bar position"""

        c_3 = self.comp_data_3

        current_bar_num = beat_indx // self.comp_data_2['num_of_beats']  # first bar = 0

        actual_global_bar_num = self.comp_data_2['num_of_first_bar'] + current_bar_num

        if self.comp_data['track_id'] != const.HARMONY_TRACK:
            c_3['inst_low'], c_3['inst_high'] = self.get_instrument_range()
            assert c_3['inst_high'] - c_3['inst_low'] + 1 >= mp.MIN_RANGE  # 1.5 octaves

        last_bar = self.comp_data_2['ends_level'] == 0 and \
            current_bar_num == self.comp_data_2['num_bars_in_part'] - 1

        nextto_last_bar = self.comp_data_2['ends_level'] == 0 and \
            current_bar_num == self.comp_data_2['num_bars_in_part'] - 2

        first_bar = self.comp_data_2['starts_level'] == 0 and current_bar_num == 0

        if (first_bar or last_bar or nextto_last_bar) and self.comp_data['track_id'] == const.HARMONY_TRACK:
            anchor_harmony_needed = True
            first_bar = False
            last_bar = False
            nextto_last_bar = False
            melody_rule = const.RM_HARMONY_TRACK_NEW_HARMO
        else:
            anchor_harmony_needed = False

        if self.comp_data['track_id'] != const.HARMONY_TRACK:
            self._get_tone_disharmony_values(beat_indx)

        one_beat_melody_rule = []
        one_beat_melody = []

        if melody_rule == const.RM_MELODY or last_bar or nextto_last_bar:

            one_beat_melody_rule, one_beat_melody = self._do_melody(beat_indx, last_bar, nextto_last_bar)

        elif melody_rule == RM_REPEAT:

            one_beat_melody, one_beat_melody_rule = \
              self._get_melody_from_bars_and_beats(beat_indx, self.comp_data_2['repeat_from_bar'])
            one_beat_melody_rule[0][0] = RM_REPEAT

        elif melody_rule == const.RM_HARMONY_TRACK_NEW_HARMO:
            one_beat_melody_rule, one_beat_melody = \
              self._choose_new_harmony(anchor_harmony_needed,
                                       c_3['bar_distribution'][actual_global_bar_num][const.HARMONY_IDENTIFIER])
            # example: one_beat_melody_rule = [[9, [4, 7, 11], 0]]
            #          c_3['bar_distribution'][actual_global_bar_num][const.HARMONY_IDENTIFIER] = 0

        elif melody_rule == const.RM_HARMONY_TRACK_LAST_HARMO:
            one_beat_melody, one_beat_melody_rule = \
              self._get_melody_from_bars_and_beats(beat_indx - 1, self.comp_data_2['num_of_first_bar'])

            # check if harmony type is still correct, otherwise choose new harmony
            if one_beat_melody_rule[0][2] != c_3['bar_distribution'][actual_global_bar_num][const.HARMONY_IDENTIFIER]:
                one_beat_melody_rule, one_beat_melody = \
                  self._choose_new_harmony(False,
                                           c_3['bar_distribution'][actual_global_bar_num][const.HARMONY_IDENTIFIER])
                one_beat_melody_rule[0][0] = const.RM_HARMONY_TRACK_NEW_HARMO
            else:
                one_beat_melody_rule[0][0] = const.RM_HARMONY_TRACK_LAST_HARMO

        return one_beat_melody_rule, one_beat_melody

    def _find_harmony_constant_beats(self, min_const_time, max_const_time):
        """finds number of beats for which a harmony remains constant"""

        min_const_beats = min_const_time * self.comp_data_2['bpm'] / 60.0
        max_const_beats = max_const_time * self.comp_data_2['bpm'] / 60.0

        gauss_mean = (min_const_time + max_const_time) / 2.0

        gauss_delta = (min_const_time + max_const_time) / 4.0
        rndm_local = self.comp_data['rndm_2'][const.RNDM_HARMO]

        # constant time in seconds
        harmony_constant_time = rndm_local.rndm_gauss_limit([gauss_mean, gauss_delta, min_const_time, max_const_time])

        harmony_constant_beats = max(int(harmony_constant_time * self.comp_data_2['bpm'] / 60.0 + 0.5), 1)

        ok_condition = False
        index = 0
        while not ok_condition:
            try_delta = [0, +1, -1, +2, +3, -2, -3, +4, +5, -4, -5, +6, +7, -6, -7][index]
            try_harmony_constant_beats = harmony_constant_beats + try_delta
            ok_condition = ((self.comp_data_2['num_of_beats'] % try_harmony_constant_beats) == 0
                            or (try_harmony_constant_beats % self.comp_data_2['num_of_beats']) == 0)
            ok_condition = (ok_condition and min_const_beats <= try_harmony_constant_beats <= max_const_beats)
            index += 1
        harmony_constant_beats = try_harmony_constant_beats

        return harmony_constant_beats

    def create_part_melody(self, c_strct):
        """selects the tone heights of a part for all rhythmic positions"""

        assert self.comp_data_2['num_bars_in_part'] > 0, "Something is wrong with num_bars_in_part"

        c_3 = self.comp_data_3

        # bridge_part = c_strct[PROP_INDX][PROP_INTRO_BRIDGE_END] == CRB why not used?
        rpt = c_strct[PROP_INDX][PROP_USEPART]
        if rpt != NO_REPEAT:
            self.comp_data_2['repeat_from_bar'] = c_strct[PROP_INDX][PROP_FROM_BAR]

        harmony_constant_beats = 0  # still undefined

        if self.comp_data['track_id'] == const.HARMONY_TRACK:
            c_3['is_percussion_instrument'] = False
            if rpt == NO_REPEAT:
                harmony_constant_beats = self._find_harmony_constant_beats(mp.HARMONY_MIN_CONST_TIME,
                                                                           mp.HARMONY_MAX_CONST_TIME)

                # harmony_type_constant_beats = self.find_harmony_constant_beats(8.0, 16.0)

        else:
            c_3['is_percussion_instrument'] = not tu.is_melody_instrument(self.comp_data['track_info'])
            c_3['is_solo_instrument'] = tu.is_solo_instrument(self.comp_data['track_info'])
            c_3['is_harmony_instrument'] = tu.is_harmony_instrument(self.comp_data['track_info'])
            c_3['is_bass_instrument'] = tu.is_bass_instrument(self.comp_data['track_info'])

        if not c_3['is_percussion_instrument']:
            self.loop_beats(rpt, harmony_constant_beats)

    def loop_beats(self, rpt, harmony_constant_beats):
        """ loops over all beats of current part"""
        # total number of beats in part
        num_of_beats_in_part = self.comp_data_2['num_of_beats'] * self.comp_data_2['num_bars_in_part']

        beat_indx = 0

        while beat_indx < num_of_beats_in_part:
            if rpt != NO_REPEAT:
                melody_rule = RM_REPEAT
            elif self.comp_data['track_id'] == const.HARMONY_TRACK:
                if beat_indx % harmony_constant_beats == 0:
                    melody_rule = const.RM_HARMONY_TRACK_NEW_HARMO
                else:
                    melody_rule = const.RM_HARMONY_TRACK_LAST_HARMO
            else:
                melody_rule = const.RM_MELODY

            one_beat_melody_rule, one_beat_melody = self._melody_generator(beat_indx, melody_rule)
            append_tuple = [BEAT_MELODY, beat_indx, one_beat_melody_rule, one_beat_melody]
            self.comp_data_2['bars_and_beats'].append(append_tuple)
            if self.comp_data['track_id'] == const.HARMONY_TRACK:
                assert one_beat_melody == [], "no melody for harmony track"
            for tones in one_beat_melody:
                self.comp_data_2['tones'].append(tones)

            beat_indx += 1

    def create_part(self, c_strct):
        """ Creates positions (rhythm), tone heights (melody) intensities and connection_types for one part.
            Loops through all beats of the part.
            In one loop the following functions are called:
            self.rhythm_generator
            self.melody_generator """

        c_3 = self.comp_data_3

        self.comp_data_2['num_of_first_bar'] = c_strct[PROP_INDX][PROP_ACTUAL_BAR]
        self.comp_data_2['ends_level'] = c_strct[PROP_INDX][PROP_END]
        self.comp_data_2['starts_level'] = c_strct[PROP_INDX][PROP_START]
        append_tuple = [FIRST_BAR_OF_PART, self.comp_data_2['num_of_first_bar']]

        self.comp_data_2['bars_and_beats'].append(append_tuple)

        self.comp_data_2['num_of_beats'] = self.comp_data_2['global_rhythm'][const.NUM_OF_BEATS_INDX]

        self.comp_data_2['num_bars_in_part'] = c_strct[LEN_INDX]
        # rhythm (position, connection type and intensity)
        pos_conn_intens = rhythm_algorithms.create_part_rhythm(c_strct,
                                                               self.comp_data,
                                                               self.comp_data_2,
                                                               c_3['bar_distribution'])
        # melody (tone heights)
        self.create_part_melody(c_strct)

        if c_strct[PROP_INDX][PROP_USEPART] == NO_REPEAT:
            c_3['created_bars_so_far'] += self.comp_data_2['num_bars_in_part']

        if self.comp_data['track_id'] != const.HARMONY_TRACK:

            self.humanize_positions(pos_conn_intens)

            # connection_types

            for i in pos_conn_intens:
                self.comp_data_2['connection_types'].append(i[2])

            # intensities
            max_intens = 5
            for i in pos_conn_intens:
                intensity = i[1]
                assert 0 <= intensity <= max_intens
                if tu.is_solo_instrument(self.comp_data['track_info']):
                    volume = int((intensity - 3) * (mp.SPREAD / max_intens) + mp.VOLUME_LEVEL_SOLO + 0.5)
                else:
                    volume = int((intensity - 3) * (mp.SPREAD / max_intens) + mp.VOLUME_LEVEL_NON_SOLO + 0.5)
                self.comp_data_2['intensities'].append(volume)

    def humanize_positions(self, pos_conn_intens):
        """humanizes all positions"""
        previous_position = 0
        assert self.comp_data_2['num_of_first_bar'] != 0, "num_of_first_bar is never 0"
        part_offset = (self.comp_data_2['num_of_first_bar']
                       - 1) * const.TICKSRES * self.comp_data_2['num_of_beats']

        humanize_max_in_ticks = (const.HUMANIZE_MAX_IN_MS * const.TICKSRES * self.comp_data_2['bpm']) / 60000
        gauss_delta = 2.0 / 3.0 * humanize_max_in_ticks
        for i in pos_conn_intens:
            humanize_in_ticks = int(self.comp_data['rndm_2'][const.RNDM_OTHER].rndm_gauss_limit(
                [0, gauss_delta, -humanize_max_in_ticks, humanize_max_in_ticks]))

            original_position = part_offset + i[0]
            test_position = original_position + humanize_in_ticks
            if test_position <= previous_position + humanize_max_in_ticks:
                test_position = original_position
            if test_position >= (part_offset + self.comp_data_2['num_bars_in_part'] *
                                 self.comp_data_2['num_of_beats'] * const.TICKSRES - humanize_max_in_ticks):
                test_position = original_position
            self.comp_data_2['positions'].append(test_position)
            previous_position = test_position

    def walk_structure(self, c_strct, level):
        """
        Walks along the part structure of the composition.
        A part may be a CREATE or REPEAT part, in which case self.create_part() is called.
        Or a part may be a substructure, in which case self.walk_structure is called recursively.
        """
        assert level > 0, "level should always be > 0 here"

        num_parts = len(c_strct)

        for part_no in range(0, num_parts):
            if c_strct[part_no][SUB_INDX] != []:  # part has sub structure

                level += 1
                self.walk_structure(c_strct[part_no][SUB_INDX], level)
                level -= 1

            else:  # create oder repeat part
                if const.DEBUG_OUTPUT:
                    print(' ')
                    for _ in range(level):
                        print('    ', end='')
                    print(' Now starts create_part (part', part_no, ')')
                self.create_part(c_strct[part_no])

    def createmelody(self):

        """
        This is the main algorithm for melody creation.
        Uses function self.walk_structure() to walk recursively along the structure of the piece.
        """
        c_3 = self.comp_data_3
        level = 1  # start on level 1 (level 0 never contains creatable parts)
        c_3['created_bars_so_far'] = 0  # number of bars which have been composed (created), not including repeated bars
        c_3['envelope_param_b'], c_3['envelope_param_p'] = self._get_envelope_param()

        self.walk_structure(self.comp_data['composition_struct'][SUB_INDX], level)

    def start_createmelody(self, harmony_track, bpm, selected_speed, global_rhythm):
        """
        Starts creating the melody (tone positions, heights, intensities and connection_types) for one instrument track
        calls self.createmelody(created)
        """
        c_3 = self.comp_data_3
        self.comp_data_2['bpm'] = bpm
        self.comp_data_2['global_rhythm'] = global_rhythm
        self.comp_data_2['selected_speed'] = selected_speed

        if harmony_track != []:
            c_3['harmony_bars_and_beats'] = harmony_track.get_bars_and_beats()
            if const.DEBUG_OUTPUT:
                print(' ')
                print('Now starts new track, ID =', self.comp_data['track_id'])
        else:
            c_3['harmony_bars_and_beats'] = []
            if const.DEBUG_OUTPUT:
                print(' ')
                print('Now starts harmony track')

        self.createmelody()

    def gettones(self):
        """returns melody tone heights"""
        return self.comp_data_2['tones']

    def getintensities(self):
        """returns intensities"""
        return self.comp_data_2['intensities']

    def get_bars_and_beats(self):
        """returns bars_and_beats data structure"""
        return self.comp_data_2['bars_and_beats']

    def getconnection_types(self):
        """returns connection types"""
        return self.comp_data_2['connection_types']

    def getpositions(self):
        """returns positions"""
        return self.comp_data_2['positions']
