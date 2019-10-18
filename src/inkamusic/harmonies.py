# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file contains all harmony related functions and definitions

"""

import inkamusic.const as const
from inkamusic.const import SCALE_HARMONY_TYPES_INDX, SCALE_LEN_INDX, SCALE_COUNT_INDX, SCALE_NOTE_INDX
from inkamusic.const import SCALE_START_INDX


def check_harmony(tone, harmony_steps, basic_scale):
    """checks if harmony is buildable on current tone with current scale"""
    harmony_ok = True
    for harmony_step in harmony_steps:
        next_tone = (tone+harmony_step) % 12
        if basic_scale[next_tone] == 1:
            tone += harmony_step
        else:
            harmony_ok = False
            break

    return harmony_ok


def harmony_type_check(harmony_type, loop_counter, harmony_steps, index, already_used):
    """checks if harmony is of selected harmony type. For the second and third call
       (used if no harmony was foun which can be used with the current scale) the check is less strict."""
    check_ok = True
    if loop_counter == 1:
        if harmony_type == const.HARMONY_PREFER_MAJOR and harmony_steps not in [[4, 3]]:
            check_ok = False
        elif harmony_type == const.HARMONY_PREFER_MINOR and harmony_steps not in [[3, 4]]:
            check_ok = False
        elif harmony_type == const.HARMONY_PREFER_MAJOR_VAR and harmony_steps not in [[4, 3], [2, 2, 3]]:
            check_ok = False
        elif harmony_type == const.HARMONY_PREFER_MINOR_VAR and harmony_steps not in [[3, 4], [3, 2, 2]]:
            check_ok = False
        elif harmony_type == const.HARMONY_AVOID_MAJMIN and harmony_steps in [[7], [4, 3], [2, 2, 3],
                                                                              [3, 4], [3, 2, 2]]:
            check_ok = False
        elif index in already_used:
            check_ok = False
    elif loop_counter == 2:
        if harmony_type in [const.HARMONY_PREFER_MAJOR,
                            const.HARMONY_PREFER_MINOR,
                            const.HARMONY_PREFER_MAJOR_VAR,
                            const.HARMONY_PREFER_MINOR_VAR] and harmony_steps not in [[7]]:
            check_ok = False
        elif index in already_used:
            check_ok = False
    return check_ok


class HarmonyBasics():
    """ Harmony related functions and definitions
    """

    def __init__(self, all_basic_scales):
        """ Defines all possible 3-tone harmonies according to these rules:
            - the numbers are the differences in half-tone steps between tones
            - distance 1 between tones is not allowed
            - sum has to be 12 (full octave)
            - sort order within a harmony is such that step 1 + step 2 is minimal
              i. e. [3, 4, 5] instead of [4, 5, 3]
            - To do: check if [5, 2, 5] and [2, 5, 5] are really different.
        """

        self.all_harmonies = [
            [2],  # 0
            [3],  # 1
            [4],  # 2
            [5],  # 3
            [6],  # 4
            [7],  # 5
            [8],  # 6
            [9],  # 7
            [10],  # 8
            [8, 2],  # 9
            [7, 3],  # 10
            [7, 2],  # 11
            [6, 4],  # 12
            [6, 3],  # 13
            [6, 2],  # 14
            [5, 5],  # 15
            [5, 4],  # 16
            [5, 3],  # 17
            [5, 2],  # 18
            [4, 6],  # 19
            [4, 5],  # 20
            [4, 4],  # 21
            [4, 3],  # 22
            [4, 2],  # 23
            [3, 7],  # 24
            [3, 6],  # 25
            [3, 5],  # 26
            [3, 4],  # 27
            [3, 3],  # 28
            [3, 2],  # 29
            [2, 8],  # 30
            [2, 7],  # 31
            [2, 6],  # 32
            [2, 5],  # 33
            [2, 4],  # 34
            [2, 3],  # 35
            [2, 2],  # 36
            [6, 2, 2],  # 37
            [5, 3, 2],  # 38
            [5, 2, 3],  # 39
            [5, 2, 2],  # 40
            [4, 4, 2],  # 41
            [4, 3, 3],  # 42
            [4, 3, 2],  # 43
            [4, 2, 4],  # 44
            [4, 2, 3],  # 45
            [4, 2, 2],  # 46
            [3, 5, 2],  # 47
            [3, 4, 3],  # 48
            [3, 4, 2],  # 49
            [3, 3, 4],  # 50
            [3, 3, 3],  # 51
            [3, 3, 2],  # 52
            [3, 2, 5],  # 53
            [3, 2, 4],  # 54
            [3, 2, 3],  # 55
            [3, 2, 2],  # 56
            [2, 6, 2],  # 57
            [2, 5, 3],  # 58
            [2, 5, 2],  # 59
            [2, 4, 4],  # 60
            [2, 4, 3],  # 61
            [2, 4, 2],  # 62
            [2, 3, 5],  # 63
            [2, 3, 4],  # 64
            [2, 3, 3],  # 65
            [2, 3, 2],  # 66
            [2, 2, 6],  # 67
            [2, 2, 5],  # 68
            [2, 2, 4],  # 69
            [2, 2, 3],  # 70
            [2, 2, 2],  # 71
            [4, 2, 2, 2],  # 72
            [3, 3, 2, 2],  # 73
            [3, 2, 3, 2],  # 74
            [3, 2, 2, 3],  # 75
            [3, 2, 2, 2],  # 76
            [2, 4, 2, 2],  # 77
            [2, 2, 4, 2],  # 78
            [2, 2, 2, 4],  # 79
            [2, 2, 2, 2],  # 80
            [2, 3, 3, 2],  # 81
            [2, 3, 2, 3],  # 82
            [2, 3, 2, 2],  # 83
            [2, 2, 3, 3],  # 84
            [2, 2, 3, 2],  # 85
            [2, 2, 2, 3],  # 86
            [2, 2, 2, 2, 2],  # 87

        ]

        self.all_basic_scales = all_basic_scales

    def get_all_harmonies(self):
        """ returns all harmony types"""
        return self.all_harmonies

    def get_harmony_steps_from_type(self, harmony_type):
        """ returns harmony steps for harmony type"""
        return self.all_harmonies[harmony_type]

    def get_possible_harmony_type_for_scale(self, selected_scale, harmony_type, first_harmony, already_used):
        """replaces wildcard harmony types such as  HARMONY_PREFER_MAJOR
           selects a random harmony type for a scale, using harmony_type and first_harmony flag
           avoids using already_used harmonies again
           example for selected_scale:
           [7, 65, 0, 0, [HARMONY_PREFER_MAJOR_VAR, HARMONY_ANY]]
           (SCALE_LEN, SCALE_COUNT, SCALE_START, SCALE_NOTE, harmonies) """

        basic_scale = self.all_basic_scales.get_scale_by_index(selected_scale[SCALE_LEN_INDX],
                                                               selected_scale[SCALE_COUNT_INDX],
                                                               selected_scale[SCALE_START_INDX],
                                                               selected_scale[SCALE_NOTE_INDX])

        # example for basic_scale 7 65 with SCALE_START 0 (major pattern) and
        # SCALE_NOTE C (C-major): [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
        #                          c     d     e  f     g     a     b

        # example for basic_scale 7 65 with SCALE_START 0 (major pattern) and
        # SCALE_NOTE D (D-major): [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]

        # example for basic_scale 7 65 with SCALE_START 9 (minor pattern) and
        # SCALE_NOTE E (E-minor): [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
        #                          c     d     e    fis g     a     b

        found_harmony_type = False
        loop_counter = 0

        while not found_harmony_type:
            loop_counter += 1
            assert loop_counter < 4

            found_harmonies = []
            for index, harmony_steps in enumerate(self.all_harmonies):
                if not harmony_type_check(harmony_type, loop_counter, harmony_steps, index, already_used):
                    continue

                assert len(harmony_steps) in [1, 2, 3, 4, 5]
                if first_harmony:
                    tone = selected_scale[SCALE_NOTE_INDX]
                    if basic_scale[tone] != 0:
                        if check_harmony(tone, harmony_steps, basic_scale) and index not in found_harmonies:

                            found_harmonies.append(index)
                            found_harmony_type = True
                else:
                    for tone in range(0, 12):
                        if basic_scale[tone] != 0 and \
                         check_harmony(tone, harmony_steps, basic_scale) and index not in found_harmonies:
                            found_harmonies.append(index)
                            found_harmony_type = True
        return found_harmonies

    def get_random_harmony_for_scale(self, selected_scale, harmony_type, rndm_2):
        """chooses a specific harmony from a scale for given harmony type
           example for selected_scale:
           [7, 65, 0, 2, [1, 0, 2]] (SCALE_LEN, SCALE_COUNT, SCALE_START, SCALE_NOTE, harmonies) """

        # example: selected_scale[SCALE_HARMONY_TYPES_INDX] = [1, 0 , 2]
        assert harmony_type in selected_scale[SCALE_HARMONY_TYPES_INDX]

        basic_scale = self.all_basic_scales.get_scale_by_index(selected_scale[SCALE_LEN_INDX],
                                                               selected_scale[SCALE_COUNT_INDX],
                                                               selected_scale[SCALE_START_INDX],
                                                               selected_scale[SCALE_NOTE_INDX])

        # example for basic_scale 7 65 with SCALE_START 0 (major pattern) and
        # SCALE_NOTE C (C-major): [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
        #                          c     d     e  f     g     a     b

        # example for basic_scale 7 65 with SCALE_START 0 (major pattern) and
        # SCALE_NOTE D (D-major): [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]

        # example for basic_scale 7 65 with SCALE_START 9 (minor pattern) and
        # SCALE_NOTE E (E-minor): [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
        #                          c     d     e    fis g     a     b

        found_harmonies = []

        harmony_steps = self.all_harmonies[harmony_type]
        # example: harmony_steps for harmony_type 1 (major): [4, 3, 5]

        assert len(harmony_steps) in [1, 2, 3, 4, 5]

        for tone in range(12):
            harmony = []
            if basic_scale[tone] != 0:
                harmony.append(tone)
                harmony_ok = True
                for harmony_step in harmony_steps:
                    next_tone = (tone+harmony_step) % 12
                    if basic_scale[next_tone] == 1:
                        harmony.append(next_tone)
                        tone += harmony_step
                    else:
                        harmony_ok = False
                        break
                if harmony_ok:
                    found_harmonies.append(harmony)

        num_harmonies = len(found_harmonies)
        assert num_harmonies > 0, "len of found_harmonies is 0"

        # example for found_harmonies for E-minor and harmony_type 0 (minor):
        #  [[4, 7, 11], [9, 0, 4], [11, 2, 6]]

        choose = rndm_2[const.RNDM_MELO_RHYTHM].rndm_choice(found_harmonies)

        return choose

    def get_anchor_harmony_for_scale(self, selected_scale):
        """chooses the anchor harmony of a scale
           example for selected_scale:
           [7, 65, 0, 2, [1, 0, 2]] (SCALE_LEN, SCALE_COUNT, SCALE_START, SCALE_NOTE, harmonies)"""

        harmony_types_in_scale = selected_scale[SCALE_HARMONY_TYPES_INDX]
        harmony_type = harmony_types_in_scale[0]  # use first only for anchor
        basic_scale = self.all_basic_scales.get_scale_by_index(selected_scale[SCALE_LEN_INDX],
                                                               selected_scale[SCALE_COUNT_INDX],
                                                               selected_scale[SCALE_START_INDX],
                                                               selected_scale[SCALE_NOTE_INDX])

        # example for basic_scale 7 65 with SCALE_START 0 (major pattern) and
        # SCALE_NOTE C (C-major): [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]
        #                          c     d     e  f     g     a     b

        # example for basic_scale 7 65 with SCALE_START 0 (major pattern) and
        # SCALE_NOTE D (D-major): [0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]

        # example for basic_scale 7 65 with SCALE_START 9 (minor pattern) and
        # SCALE_NOTE E (E-minor): [1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1]
        #                          c     d     e    fis g     a     b

        scale_start_position = selected_scale[SCALE_NOTE_INDX]
        found_harmonies = []

        harmony_steps = self.all_harmonies[harmony_type]
        # example: harmony_steps for harmony_type 1 (major): [4, 3, 5]

        harmony = []
        if basic_scale[scale_start_position] != 0:
            harmony.append(scale_start_position)
            harmony_ok = True
            for harmony_step in harmony_steps:
                next_tone = (scale_start_position+harmony_step) % 12
                if basic_scale[next_tone] == 1:
                    harmony.append(next_tone)
                    scale_start_position += harmony_step
                else:
                    harmony_ok = False
                    break
            if harmony_ok:
                found_harmonies.append([harmony, harmony_type])

        num_harmonies = len(found_harmonies)
        assert num_harmonies != 0, "anchor harmony is not constructable. Check SCALES_LIST entry."

        # example for E-minor: found_harmonies = [[[4, 7, 11], 0]]

        return found_harmonies[0][0], found_harmonies[0][1]  # returns specific harmony and type
