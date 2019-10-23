# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file contains utility functions

"""
import random
import math
import inkamusic.const as const
from inkamusic.const import SUB_INDX, PROP_INDX, LEN_INDX, CR, CR2, CRB, CR_INTRO, CR_ENDING
from inkamusic.const import PROP_USEPART, PROP_INTRO_BRIDGE_END, PROP_FROM_BAR, PROP_TO_BAR, PROP_ACTUAL_BAR
import inkamusic.music_parameter as mp


class Rndm():
    """
    Implements standard random functions independently (i. e. with separate seed values)
    for the following parts:

    Structure
    Scale
    Harmony
    Instrumentation
    Rhythm
    Melody

    """
    def __init__(self, seed):
        random.seed(a=seed)
        self.rndm_state = random.getstate()

    def rndm_int(self, lower, upper):
        """
        replaces standard randint function
        """
        random.setstate(self.rndm_state)
        random_value = random.randint(lower, upper)
        self.rndm_state = random.getstate()
        return random_value

    def rndm_choice(self, seq, weights=None):
        """
        replaces standard choice function
        """
        random.setstate(self.rndm_state)
        random_value = random.choices(seq, weights)
        self.rndm_state = random.getstate()
        return random_value[0]

    def rndm_uniform(self, lower, upper):
        """
        replaces standard uniform function
        """
        random.setstate(self.rndm_state)
        random_value = random.uniform(lower, upper)
        self.rndm_state = random.getstate()
        return random_value

    def rndm_random(self):
        """
        replaces standard random function
        """
        random.setstate(self.rndm_state)
        random_value = random.random()
        self.rndm_state = random.getstate()
        return random_value

    def rndm_gauss_limit(self, param):
        """
        replaces standard gauss function and allows to define upper and lower limits
        param is [mean, delta, lower, upper]
        """
        random.setstate(self.rndm_state)
        if param[2] == param[3]:
            lower = param[2]
            condition = True
        elif param[1] == 0:
            lower = param[0]
            condition = True
        else:
            condition = False
        while not condition:
            lower = random.gauss(param[0], param[1])
            if param[2] <= lower <= param[3]:
                condition = True
        self.rndm_state = random.getstate()
        return lower


def show_composition_structure(comp_struct, level):
    """prints composition structure for debugging purposes """

    def format_props(props):
        txt = ''
        if props:
            if props[PROP_USEPART] == -1:
                txt += 'Creates '
                if props[PROP_INTRO_BRIDGE_END] == CR:
                    txt += 'CR'
                elif props[PROP_INTRO_BRIDGE_END] == CR2:
                    txt += 'CR2'
                elif props[PROP_INTRO_BRIDGE_END] == CRB:
                    txt += 'CRB'
                elif props[PROP_INTRO_BRIDGE_END] == CR_INTRO:
                    txt += 'CR_INTRO'
                elif props[PROP_INTRO_BRIDGE_END] == CR_ENDING:
                    txt += 'CR_ENDING'
                else:
                    assert False
            else:
                txt += 'Repeats part '
                txt += repr(props[PROP_USEPART])
                txt += ' from bar ' + repr(props[PROP_FROM_BAR])
                txt += ' to bar ' + repr(props[PROP_TO_BAR])
            txt += ', '
            txt += 'actual bar number is '
            txt += repr(props[PROP_ACTUAL_BAR])
#             txt += ', '
#             txt += 'starts level '
#             txt += repr(props[PROP_START])
#             txt += ', '
#             txt += 'ends level '
#             txt += repr(props[PROP_END])
            return txt
        return ''

    if const.DEBUG_OUTPUT:
        txt = ''
        for _ in range(level):
            txt += '   '
        print('')
        print('')
        print(txt, 'Level', level)
        if level == 0:
            print(txt, 'Length', comp_struct[LEN_INDX])
            if comp_struct[SUB_INDX] == []:
                pass
            else:
                level += 1
                show_composition_structure(comp_struct[SUB_INDX], level)
                level -= 1
        else:

            for i, comp_struct_entry in enumerate(comp_struct):
                print('')
                print(txt, 'Part', i)

                if comp_struct_entry[SUB_INDX] == []:
                    print(txt, 'Length', comp_struct_entry[LEN_INDX], ' ', format_props(comp_struct_entry[PROP_INDX]))
                else:
                    print(txt, 'Length', comp_struct_entry[LEN_INDX])
                    level += 1
                    show_composition_structure(comp_struct_entry[SUB_INDX], level)
                    level -= 1


def get_up_down_equal_characteristics(rndm_local):
    """selects up, down or equal and tone group length"""

    up_down_equal_probs = rndm_local.rndm_choice(mp.UP_DOWN_EQUAL_PROBS)
    if up_down_equal_probs == 0:  # only equal tones
        tone_group_length = int(rndm_local.rndm_gauss_limit(mp.TONE_GROUP_LENGTH_EQUAL) + 0.5)
    else:
        tone_group_length = int(rndm_local.rndm_gauss_limit(mp.TONE_GROUP_LENGTH_UP_DOWN) + 0.5)
    return tone_group_length, up_down_equal_probs


def get_jump_points(tone_abs_height, prev_tone):
    """calculates the jump height between tone and previous tone"""

    assert len(prev_tone[0]) >= 0, "prev_tone should be array"

    if prev_tone[0] == []:
        return 10
    smallest_jump_height = 999
    for tone in prev_tone[0]:
        jump_height = abs(tone - tone_abs_height)
        if jump_height < smallest_jump_height:
            smallest_jump_height = jump_height
    if smallest_jump_height >= len(mp.POINTS_JUMP_HEIGHT):
        jump_points = 0
    else:
        jump_points = mp.POINTS_JUMP_HEIGHT[smallest_jump_height]

    return jump_points


def get_second_last_tone_diff(tone_abs_height, previous_tones):
    """calculates the difference to the second last tone"""

    assert len(previous_tones[0]) >= 0, "prev_tone should be array"

    if previous_tones[0] == []:
        return 10
    if previous_tones[1] == []:
        return 10
    if len(previous_tones[1]) > 1:
        return 10  # don't use for chords
    tone = previous_tones[1][0]
    jump_height = abs(tone - tone_abs_height)

    if jump_height >= len(mp.POINTS_SECOND_LAST_TONE):
        second_last_tone_points = 10
    else:
        second_last_tone_points = mp.POINTS_SECOND_LAST_TONE[jump_height]

    return second_last_tone_points


def get_up_down_equal_points(tone_abs_height, prev_tone, c_3):
    """checks if up, down or equal setting is met"""

    assert len(prev_tone[0]) >= 0, "prev_tone should be array"

    if prev_tone[0] == []:
        return 10
    compare_tone = max(prev_tone[0])  # compare against highest tone

    delta = tone_abs_height - compare_tone
    if delta == 0:
        up_down_equal_type = 0
    else:
        up_down_equal_type = (delta) / abs(delta)

    if up_down_equal_type == c_3['up_down_equal_probs']:
        up_down_equal_points = 10
    else:
        if abs(delta) <= 4:
            up_down_equal_points = 0.1  # if original up / down / equal is not possible, jump away
        else:
            up_down_equal_points = 2

    return up_down_equal_points


def get_cont_in_scale_points(tone_abs_height, prev_tone, c_3):
    """checks whether tone continues within the scale (up or down)"""

    assert len(prev_tone[0]) >= 0, "prev_tone should be array"

    if prev_tone[0] == []:  # no previous tone
        return 1

    if len(prev_tone[0]) > 1:  # not applicable to chords
        return 10

    previous_tone_abs = prev_tone[0][0]

    previous_tone_rel = previous_tone_abs % 12

    assert c_3['basic_scale'][previous_tone_rel] == 1  # should always be in basic scale

    # find next tone in scale
    index = 1
    while index <= 12:
        if c_3['basic_scale'][(previous_tone_rel + index) % 12] == 1:
            next_tone_in_scale = (previous_tone_rel + index) % 12
            break
        index += 1

    if tone_abs_height % 12 == next_tone_in_scale:
        return 10

    # find prev tone in scale
    index = 1
    while index <= 12:
        if c_3['basic_scale'][(previous_tone_rel - index) % 12] == 1:
            prev_tone_in_scale = (previous_tone_rel - index) % 12
            break
        index += 1

    if tone_abs_height % 12 == prev_tone_in_scale:
        return 10

    return 0.1


def get_cont_in_harmony_points(tone_abs_height, prev_tone, c_3):
    """checks whether tone continues within the current harmony (up or down)"""

    assert len(prev_tone[0]) >= 0, "prev_tone should be array"

    if prev_tone[0] == []:  # no previous tone
        return 10

    if len(prev_tone[0]) > 1:  # not applicable to chords
        return 10

    previous_tone_abs = prev_tone[0][0]

    previous_tone_rel = previous_tone_abs % 12
    # example of c_3['current_beat_harmony_rule'] [[9, [6, 10, 1], 1]]

    harmony = c_3['current_beat_harmony_rule'][0][1]
    if previous_tone_rel not in harmony:  # prev tone was not in harmony
        return 10

    # find previous_tone_rel in harmony
    for index, tone in enumerate(harmony):
        if tone == previous_tone_rel:
            start_index = index
            break

    # find next tone in harmony rule
    next_tone_in_harmony = harmony[(start_index + 1) % len(harmony)]
    if tone_abs_height % 12 == next_tone_in_harmony:
        return 10

    # find prev tone in harmony rule
    prev_tone_in_harmony = harmony[(start_index - 1) % len(harmony)]
    if tone_abs_height % 12 == prev_tone_in_harmony:
        return 10

    return 0.1


def get_distance_points(tone_abs_height, instrument_type, c_3):
    """calculates the harmonic distances of a tone against the already used tones and against the current harmony"""

    tone_rel_height = tone_abs_height % 12

    # test against used_tones

    used_tones_distance = c_3['disharmony_to_used_tones'][tone_rel_height]
    if (used_tones_distance == const.NOT_IN_SCALE or used_tones_distance >= const.DISHARMONIC_LIMIT):
        return 0, 0  # never use this tone

    points = mp.POINTS_USED_TONES_DISTANCE
    used_dist_points = points[used_tones_distance]

    assert 0 <= used_dist_points <= 10, "Think again"

    # test against harmony_rule

    harmonic_distance = c_3['disharmony_to_harmony_rule'][tone_rel_height]
    assert harmonic_distance != const.NOT_IN_SCALE, " should  never happen"

    if instrument_type in [const.T_SOLO]:
        if harmonic_distance >= const.DISHARMONIC_LIMIT:
            harmony_dist_points = mp.POINTS_DISSONANT_DISTANCE_SOLO
        else:
            points = mp.POINTS_HARMONIC_DISTANCE_SOLO
            harmony_dist_points = points[harmonic_distance]
    else:
        if harmonic_distance >= const.DISHARMONIC_LIMIT:
            return 0, 0  # never use this tone

        points = mp.POINTS_HARMONIC_DISTANCE_NON_SOLO
        harmony_dist_points = points[harmonic_distance]

    assert 0 <= harmony_dist_points <= 10, "Think again"

    return used_dist_points, harmony_dist_points


def check_tone(tone_abs_height, instrument_type, target_tone, previous_tones, c_3):
    """evaluates a tone"""

    def apply_weight(weight, points):
        """weight 0 gives 1.0, weight 1 gives points"""
        return weight * (points - 1.0) + 1.0

    used_dist_points, harmony_dist_points = get_distance_points(tone_abs_height, instrument_type, c_3)

    # anchor tone, slightly prefer anchor tone, anchor_tone is c_3['scale'][const.SCALE_NOTE_INDX]
    if c_3['scale'][const.SCALE_NOTE_INDX] == tone_abs_height % 12:
        anchor_points = mp.ANCHOR_POINTS
    else:
        anchor_points = mp.NO_ANCHOR_POINTS

    assert 0 <= anchor_points <= 10

    # jump height
    jump_points = get_jump_points(tone_abs_height, previous_tones)
    assert 0 <= jump_points <= 10

    # second last tone
    second_last_tone_points = get_second_last_tone_diff(tone_abs_height, previous_tones)
    assert 0 <= second_last_tone_points <= 10

    # local up down equal state
    # up_down_equal_points = get_up_down_equal_points(tone_abs_height, previous_tones, c_3)

    # continues in scale
    cont_in_scale_points = get_cont_in_scale_points(tone_abs_height, previous_tones, c_3)

    assert 0 <= cont_in_scale_points <= 10

    # continues in harmony
    cont_in_harmony_points = get_cont_in_harmony_points(tone_abs_height, previous_tones, c_3)
    assert 0 <= cont_in_harmony_points <= 10

    # target tone
    if abs(tone_abs_height - target_tone) >= len(mp.POINTS_TARGET_TONE):
        target_points = 0
    else:
        target_points = mp.POINTS_TARGET_TONE[abs(tone_abs_height - target_tone)]
    assert 0 <= target_points <= 10

    final_points = (apply_weight(mp.W_USED_DIST[instrument_type], used_dist_points) *
                    apply_weight(mp.W_HARMONY_DIST[instrument_type], harmony_dist_points) *
                    apply_weight(mp.W_ANCHOR[instrument_type], anchor_points) *
                    apply_weight(mp.W_JUMP[instrument_type], jump_points) *
                    apply_weight(mp.W_CONT_IN_SCALE[instrument_type], cont_in_scale_points) *
                    apply_weight(mp.W_CONT_IN_HARMONY[instrument_type], cont_in_harmony_points) *
                    apply_weight(mp.W_SECOND_LAST_TONE[instrument_type], second_last_tone_points) *
                    apply_weight(mp.W_TARGET[instrument_type], target_points))

    if 0 in [used_dist_points,
             harmony_dist_points,
             anchor_points,
             jump_points,
             cont_in_scale_points,
             cont_in_harmony_points,
             target_points]:  # up_down_equal_points removed
        final_points = 0
    return [tone_abs_height, final_points]


def sin_special(x_val):
    """this function differs from sine in that it generates more values in the range around 0 instead
    of extreme values near +1 and -1."""
    pi_val = math.pi

    # map to interval 0 ... 2 * pi
    while x_val > 2 * pi_val:
        x_val -= 2 * pi_val
    while x_val < 0:
        x_val += 2 * pi_val

    if x_val > pi_val:
        factor = -1
        x_val -= pi_val
    else:
        factor = 1
    if x_val <= pi_val / 2:
        return factor * (4 / pi_val * x_val - math.sin(x_val))

    return factor * (-4 / pi_val * x_val - math.sin(x_val) + 4.0)
