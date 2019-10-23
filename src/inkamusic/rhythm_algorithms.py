# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file contains the rhythm algorithmic functions

"""
import math
import copy
import inkamusic.const as const
from inkamusic.const import PROP_INDX, PROP_USEPART, PROP_INTRO_BRIDGE_END, NO_REPEAT
from inkamusic.const import PROP_FROM_BAR, CRB
from inkamusic.const import RHYTHM_BEAT_INDX, RHYTHM_PAT_INDX
from inkamusic.const import ACC_UNDEFINED, RY_POS, RY_ACC, RY_LEV, RY_LEN
from inkamusic.const import RM_REPEAT, RM_HARMONY_TRACK, RM_SOLO_PATTERN
from inkamusic.const import RM_TRACK_RHYTHM, RM_VARI_TRACK_RHYTHM
from inkamusic.const import FIRST_BAR_OF_PART, BEAT_RHYTHM

import inkamusic.trackinfo_util as tu
from inkamusic.basic_rhythms import RHY_PATTERN_INDX, BLOCK_ACC

import inkamusic.music_parameter as mp


def get_rhythm_from_bars_and_beats(beat_indx, start_from_bar, comp_data_2):
    """start_from_bar is the global bar number (1 = first bar of composition)
       beat_indx is counted from there.
       All rhythm positions are relative to first bar entry in
       which they appear, so they need to be shifted"""

    def shift_rhythm(rhythm, bars_to_shift):
        shifted = copy.deepcopy(rhythm)
        for pos in shifted:
            pos[0] += (bars_to_shift * comp_data_2['num_of_beats'] * const.TICKSRES)
        return shifted

    len_bars_and_beats = len(comp_data_2['bars_and_beats'])
    indx = 0
    active = 0
    while indx < len_bars_and_beats:
        if comp_data_2['bars_and_beats'][indx][0] == FIRST_BAR_OF_PART:
            current_first_bar_is = comp_data_2['bars_and_beats'][indx][1]

            if current_first_bar_is == start_from_bar:
                active = 1
                beat_counter = 0

        if active == 1:
            if comp_data_2['bars_and_beats'][indx][0] == BEAT_RHYTHM:
                if beat_counter == beat_indx:
                    one_beat_rhythm = copy.deepcopy(shift_rhythm(comp_data_2['bars_and_beats'][indx][2],
                                                                 current_first_bar_is - start_from_bar))

                    break
                beat_counter += 1
        indx += 1

    return one_beat_rhythm


def create_combined_rhythm(selected_rhythm):
    """combines all parts of the selected rhythm
    This will be the starting point for further subdivisions"""
    all_pos = []
    for rhythm_part in range(1, len(selected_rhythm)):
        for pos in range(len(selected_rhythm[rhythm_part][RHY_PATTERN_INDX])):
            if selected_rhythm[rhythm_part][RHY_PATTERN_INDX][pos][RY_ACC] != BLOCK_ACC:
                all_pos.append(selected_rhythm[rhythm_part][RHY_PATTERN_INDX][pos][RY_POS])
    all_pos = list(set(all_pos))
    all_pos.sort()
    num_pos = len(all_pos)
    assert num_pos > 1, "Selected Rhythm is not usable"

    combined_rhythm = []
    num_beats = selected_rhythm[0]
    for i in range(num_pos):
        if i != num_pos - 1:
            combined_rhythm.append([all_pos[i], 0, 0, all_pos[i + 1] - all_pos[i]])
        else:
            combined_rhythm.append([all_pos[i], 0, 0, all_pos[0] - all_pos[num_pos - 1] + num_beats * const.TICKSRES])

    return combined_rhythm


def exists_pos(pos, rhythm):
    """checks if position is used in rhythm"""
    for i in rhythm:
        if pos == i[0]:
            return True
    return False


def max_acc_of_pos(position, selected_rhythm):
    """finds max intensity of a position over all rhythm parts"""
    acc = ACC_UNDEFINED
    for rhythm_part in range(1, len(selected_rhythm)):
        for pos in range(len(selected_rhythm[rhythm_part][RHY_PATTERN_INDX])):
            if selected_rhythm[rhythm_part][RHY_PATTERN_INDX][pos][RY_POS] == position:
                if acc < selected_rhythm[rhythm_part][RHY_PATTERN_INDX][pos][RY_ACC]:
                    acc = selected_rhythm[rhythm_part][RHY_PATTERN_INDX][pos][RY_ACC]
    return acc


def strip_blocked(selected_rhythm):
    """removes BLOCK_ACC entries from selected rhythm, after global rhythm has
       been created"""
    for rhythm_part in range(1, len(selected_rhythm)):
        pos = len(selected_rhythm[rhythm_part][RHY_PATTERN_INDX])-1
        while pos >= 0:
            if selected_rhythm[rhythm_part][RHY_PATTERN_INDX][pos][RY_ACC] == BLOCK_ACC:
                del selected_rhythm[rhythm_part][RHY_PATTERN_INDX][pos]
            pos -= 1
    return selected_rhythm


def check_rhythm(selected_rhythm, combined_rhythm):
    """checks if selected rhythm is compatible with combined_rhythm"""

    all_pos_found = True
    min_acc = 999

    # example for selected_rhythm
    # [4,
    #   [0, [[0, 4], [720, 3], [1440, 3], [2160, 3]]],
    #   [5, [[0, 4], [360, 1], [720, 3], [1080, 1], [1440, 3], [1800, 1], [2160, 3], [2520, 1]]]
    # ]

    for sub_rhythm in range(1, len(selected_rhythm)):

        for indx in range(len(selected_rhythm[sub_rhythm][RHY_PATTERN_INDX])):
            pos = selected_rhythm[sub_rhythm][RHY_PATTERN_INDX][indx][RY_POS]
            style_acc = selected_rhythm[sub_rhythm][RHY_PATTERN_INDX][indx][RY_ACC]
            if style_acc != BLOCK_ACC:
                if min_acc > style_acc:
                    min_acc = style_acc
            pos_found = exists_pos(pos, combined_rhythm)

            if (not pos_found and style_acc != BLOCK_ACC) or (pos_found and style_acc == BLOCK_ACC):
                all_pos_found = False
                break
        if not all_pos_found:
            break
    if all_pos_found:
        assert min_acc >= 0, "Something is wrong with min_acc"
        # change accents of selected rhythm if necessary
        # min acc should at least be 2 to use accent 1 for
        # extra positions in global rhythm which are
        # not used in selected rhythm
        if min_acc < 2:
            add_acc = 2 - min_acc
        else:
            add_acc = 0
        indx = len(combined_rhythm) - 1
        while indx >= 0:
            acc = max_acc_of_pos(combined_rhythm[indx][RY_POS], selected_rhythm)
            if acc == ACC_UNDEFINED:
                combined_rhythm[indx][RY_ACC] = 1
            else:
                combined_rhythm[indx][RY_ACC] = acc + add_acc
            indx -= 1

    return all_pos_found


def subdivide_rhythm(combined_rhythm, rnd_type, min_split_length):
    """subdivides rhythm into next level
       min_split_length is the minimum length which must remain AFTER a subdivision
       see menu_entries.SPEED_LIST for an example"""

    def getfirst(item):
        return item[0]

    def split_position(level, length, split, position):
        for j, ry_entry in enumerate(combined_rhythm):
            if ry_entry[RY_POS] == position[RY_POS]:
                del combined_rhythm[j]
                break
        for j in range(split):
            ins = [position[RY_POS] + length * j, 0, level + 1, length]
            combined_rhythm.append(ins)
            combined_rhythm.sort(key=getfirst)

    new_level_added = True
    level = 0
    # example for split steps of rhythm entries [position, (unused), level, length]
    # level 0: [[0, 0, 0, 720],
    #           [720, 0, 0, 720],
    #           [1440, 0, 0, 720],
    #           [2160, 0, 0, 720]]
    # level 1: [[0, 0, 1, 360], [360, 0, 1, 360],
    #           [720, 0, 1, 360], [1080, 0, 1, 360],
    #           [1440, 0, 0, 720],
    #           [2160, 0, 1, 360], [2520, 0, 1, 360]]
    # level 2: [[0, 0, 2, 180], [180, 0, 2, 180], [360, 0, 1, 360],
    #           [720, 0, 2, 180], [900, 0, 2, 180], [1080, 0, 2, 180], [1260, 0, 2, 180],
    #           [1440, 0, 0, 720],
    #           [2160, 0, 2, 180], [2340, 0, 2, 180], [2520, 0, 1, 360]]
    # level 3: [[0, 0, 3, 90], [90, 0, 3, 90], [180, 0, 3, 90], [270, 0, 3, 90], [360, 0, 1, 360],
    #           [720, 0, 3, 90], [810, 0, 3, 90], [900, 0, 2, 180], [1080, 0, 3, 90], [1170, 0, 3, 90],
    #                                                                               [1260, 0, 3, 90], [1350, 0, 3, 90],
    #           [1440, 0, 0, 720],
    #           [2160, 0, 2, 180], [2340, 0, 2, 180], [2520, 0, 1, 360]]

    while new_level_added:  # level = current level, level + 1 will be constructed
        new_level_added = False
        original_ry = copy.deepcopy(combined_rhythm)
        for position in original_ry:
            if position[RY_LEV] == level:
                split = rnd_type[const.RNDM_BASE_RHYTHM].rndm_choice(mp.RHYTHM_SUBDIVISION)
                length = (position[RY_LEN] // split)
                if length >= min_split_length and position[RY_LEN] % split == 0:
                    split_position(level, length, split, position)
                    new_level_added = True

        level += 1


def create_global_rhythm(selected_rhythm, num_of_beats, min_split_length, rnd_type):
    """creates the main rhythm for the composition"""

    max_try_count = 1000
    ry_try_count = 0

    selected_rhythm_reached = False

    while not selected_rhythm_reached:

        ry_try_count += 1
        assert ry_try_count < max_try_count, "Selected rhythm can not be used"

        # initialize combined_rhythm. Combined_rhythm will be subdivided to create rhythm
        combined_rhythm = create_combined_rhythm(selected_rhythm)
        subdivide_rhythm(combined_rhythm, rnd_type, min_split_length)

        all_pos_found = check_rhythm(selected_rhythm, combined_rhythm)

        if all_pos_found:
            global_rhythm = [num_of_beats, []]
            for i in combined_rhythm:
                global_rhythm[1].append([i[RY_POS], i[RY_ACC]])
            selected_rhythm_reached = True
            selected_rhythm_stripped = strip_blocked(copy.deepcopy(selected_rhythm))
    if const.DEBUG_OUTPUT:
        print(' ')
        print('global rhythm is', global_rhythm)
    return global_rhythm, selected_rhythm_stripped


def calc_rhythm_speed(track_rhythm, beats_per_minute):
    """ calculates the number of tones played in 1 second, averaged over 1 bar """

    pat = track_rhythm[RHYTHM_PAT_INDX]

    total_time_per_bar_in_sec = 60 * track_rhythm[RHYTHM_BEAT_INDX] / beats_per_minute
    num_tones_per_bar = len(pat)
    speed = num_tones_per_bar / total_time_per_bar_in_sec  # tones per second
    return round(speed, 1)


def check_max_tones_per_s(track_rhythm, max_tones_per_s, bpm):
    """ checks if rhythm is too fast for instrument
        const.TICKSRES is the number of MIDI units for one beat
        bpm is number of beats per minute
        => time for 1 beat = 60s / bpm
        => time for 1 MIDI unit =  60s / (bpm * const.TICKSRES) =: midi_unit_in_sec
        rhythm positions are defined in MIDI units
    """

    midi_unit_in_sec = 60 / (bpm * const.TICKSRES)

    time_remove = False
    rhy = track_rhythm[RHYTHM_PAT_INDX]

    for i in range(len(rhy)):
        first = i
        if i == len(rhy) - 1:
            second = 0
        else:
            second = i + 1
        time_diff = rhy[second][0] - rhy[first][0]
        if time_diff <= 0:
            time_diff += track_rhythm[RHYTHM_BEAT_INDX] * const.TICKSRES

        abs_time = time_diff * midi_unit_in_sec  # in seconds
        tones_per_s = 1 / abs_time

        if tones_per_s > max_tones_per_s:

            time_remove = True
            critical_time_diff = time_diff
            break

    if time_remove:
        return False, critical_time_diff

    return True, 0


def remove_one(track_rhythm, intensity_dependency_val, crit_time_diff, rndm_2):
    """removes one position from rhythm, with probability depending on intensity"""

    def dist2nearest_neighbour(i, num, pat):
        if num <= 1:
            return crit_time_diff+1  # do nothing
        if i == num - 1:
            dist1 = pat[i][0] - pat[i - 1][0]
            dist2 = pat[0][0] - pat[i][0] + numbeats * const.TICKSRES
            return min(dist1, dist2)
        if i == 0:
            dist1 = numbeats * const.TICKSRES - (pat[num - 1][0] - pat[0][0])
            dist2 = pat[i + 1][0] - pat[i][0]
            return min(dist1, dist2)

        dist1 = pat[i][0] - pat[i - 1][0]
        dist2 = pat[i + 1][0] - pat[i][0]
        return min(dist1, dist2)

    def calc_p_sum(pat):
        """calculates a weighted sum for intensity dependent removal probability"""

        num = len(pat)
        # example pat: [[0, 5], [360, 2], [720, 4], [1080, 2], [1440, 4], [1800, 2], [2160, 4]]

        intens_weighted_sum = 0.0

        for i in range(num):
            intens = get_intensity(i, num, pat)
            # intensities for example: 5 2 4 2 4 2 4

            inverse_weight = math.pow(intensity_dependency_val, intens)
            # inverse weights for example: 243, 9, 81, 9, 81, 9, 81 (intensity_dependency_val is 3)

            intens_weighted_sum += 100.0 / inverse_weight  # 100 only to get nice numbers

        return intens_weighted_sum

    def get_intensity(i, num, pat):
        # decrease remove prob (by increasing intensity) for low intensity position near end of bar
        # (up beat for better rhythmic flow)
        if i == num - 1:
            intens = pat[i][1]
            if intens < 2:
                intens += 1.0
        else:
            intens = pat[i][1]

        if crit_time_diff > 0:  # increase remove prob for positions too near to each other
            if dist2nearest_neighbour(i, num, pat) <= crit_time_diff:
                intens -= 2.0

        return intens

    def remove_selected(pat, choose_random):
        """removes the selected entry"""
        num = len(pat)
        intens_weighted_sum = 0.0

        for i in range(num):
            intens = get_intensity(i, num, pat)
            inverse_weight = math.pow(intensity_dependency_val, intens)
            intens_weighted_sum += 100.0 / inverse_weight  # 100 only to get nice numbers
            if intens_weighted_sum >= choose_random:
                del pat[i]
                break

    num = len(track_rhythm[RHYTHM_PAT_INDX])
    numbeats = track_rhythm[RHYTHM_BEAT_INDX]
    assert num > 0, "num == 0"

    intens_weighted_sum = calc_p_sum(track_rhythm[RHYTHM_PAT_INDX])

    choose_random = rndm_2[const.RNDM_MELO_RHYTHM].rndm_random() * intens_weighted_sum
    remove_selected(track_rhythm[RHYTHM_PAT_INDX], choose_random)


def set_connection_types(track_info, track_rhythm, actual_num_of_tones, rndm_2):
    """sets the connection type of a created rhythm"""

    # get track info about connection type
    track_info_connect = tu.get_track_connect_info(track_info)

    num = len(track_rhythm[RHYTHM_PAT_INDX])
    assert num == actual_num_of_tones, "Should not happen, num != actual_num_of_tones"

    for i in range(actual_num_of_tones):
        if track_info_connect[0] in [const.AUTODAMP_PERC, const.AUTODAMP_MELO]:
            connection_type = const.CONNECT_AUTODAMP
        else:
            ct_rndm = rndm_2[const.RNDM_MELO_RHYTHM].rndm_int(1, 100)
            if ct_rndm <= track_info_connect[0]:
                connection_type = const.CONNECT_LEGATO
            elif ct_rndm <= track_info_connect[0] + track_info_connect[1]:
                connection_type = const.CONNECT_STANDARD
            else:
                connection_type = const.CONNECT_STACCATO
        track_rhythm[RHYTHM_PAT_INDX][i].append(connection_type)

    return track_rhythm


def get_intensity_dependency_val(track_info, rndm_2):
    """ choose intensity_dependency_val for specific instrument type
        low (lowest = 1) intensity_dependency_val => position to remove is less dependent on intensity/accent
        high (for example 50) intensity_dependency_val => position to remove is more dependent on intensity/accent
        (with low intensity removed first) """

    # find type of instrument
    melody_instrument = tu.is_melody_instrument(track_info)
    instrument_type = tu.get_instrument_type(track_info)
    instrument_type_2 = tu.get_instrument_type_2(track_info)

    if not melody_instrument:  # percussion
        if instrument_type_2 in [const.P_BASS, const.P_ACCENT]:
            intensity_dependency_val_list = mp.INTENSITY_DEPENCY_VAL_HEAVY_PERC
        else:
            intensity_dependency_val_list = mp.INTENSITY_DEPENCY_VAL_LIGHT_PERC
    else:  # melody instrument
        if instrument_type in [const.T_SOLO]:
            intensity_dependency_val_list = mp.INTENSITY_DEPENCY_VAL_SOLO
        elif instrument_type in [const.T_BASS]:
            intensity_dependency_val_list = mp.INTENSITY_DEPENCY_VAL_BASS
        elif instrument_type in [const.T_CHOR, const.T_HMNY]:
            intensity_dependency_val_list = mp.INTENSITY_DEPENCY_VAL_CHORUS_HARMONY

    intensity_dependency_val = rndm_2[const.RNDM_MELO_RHYTHM].rndm_choice(intensity_dependency_val_list)

    return intensity_dependency_val


def correct_tones_per_sec(track_rhythm, track_info, bpm, rndm_2):
    """removes tones from rhythm until max and average number of tones per sec criterion is met"""

    max_tones_per_sec = tu.get_max_tones_per_sec(track_info)

    # max_tones_per_sec_ok will be False if the time difference is too small between adjacent positions, at least once
    max_tones_per_sec_ok, crit_time_diff = check_max_tones_per_s(track_rhythm, max_tones_per_sec, bpm)

    avg_tones_per_sec = calc_rhythm_speed(track_rhythm, bpm)

    # avg_tones_per_sec_ok will be False if the time difference is too small between adjacent positions, on average
    # over all positions of a bar
    avg_tones_per_sec_ok = avg_tones_per_sec < 0.8 * max_tones_per_sec
    while not max_tones_per_sec_ok or not avg_tones_per_sec_ok:

        intens_dependency = 50

        remove_one(track_rhythm, intens_dependency, crit_time_diff, rndm_2)

        max_tones_per_sec_ok, crit_time_diff = check_max_tones_per_s(track_rhythm, max_tones_per_sec, bpm)
        avg_tones_per_sec = calc_rhythm_speed(track_rhythm, bpm)
        avg_tones_per_sec_ok = avg_tones_per_sec < mp.AVG_TONES_PER_SEC_PERCENT / 100.0 * max_tones_per_sec


def create_track_rhythm(track_info, global_rhythm, bpm, selected_speed, rndm_2):
    """creates individual rhythms for each track, based on global rhythm"""

    def weight_array(num):
        return [1/(i + mp.TONE_DENSITY) for i in range(1, num+1)]

    def number_of_tones_array(num):
        return [i for i in range(1, num+1)]

    track_rhythm = copy.deepcopy(global_rhythm)

    correct_tones_per_sec(track_rhythm, track_info, bpm, rndm_2)

    actual_num_of_tones = len(track_rhythm[RHYTHM_PAT_INDX])
    num_of_beats = track_rhythm[RHYTHM_BEAT_INDX]
    smallest_possible_distance = selected_speed[1]  # see menu_entries.SPEED_LIST for details

    assert actual_num_of_tones >= 1, "actual_num_of_tones < 1"
    if tu.is_solo_instrument(track_info):  # average speed of solo instrument should be fast enough
        average_speed_ok = False
        while not average_speed_ok:

            use_num_of_tones = rndm_2[const.RNDM_MELO_RHYTHM].rndm_choice(number_of_tones_array(actual_num_of_tones),
                                                                          weight_array(actual_num_of_tones))
            if use_num_of_tones == actual_num_of_tones:
                average_speed_ok = True
            else:
                average_speed_ok = (num_of_beats * const.TICKSRES / use_num_of_tones) <= mp.MIN_SPEED_FACTOR * \
                             smallest_possible_distance
    else:
        use_num_of_tones = rndm_2[const.RNDM_MELO_RHYTHM].rndm_choice(number_of_tones_array(actual_num_of_tones),
                                                                      weight_array(actual_num_of_tones))

    intensity_dependency_val = get_intensity_dependency_val(track_info, rndm_2)

    while actual_num_of_tones > use_num_of_tones:

        remove_one(track_rhythm, intensity_dependency_val, 0, rndm_2)

        actual_num_of_tones -= 1

    track_rhythm = set_connection_types(track_info, track_rhythm, actual_num_of_tones, rndm_2)
    return track_rhythm


def rhythm2intro(rhythm, rndm_2):
    """starts rhythm at random position under the condition
       that there exist stronger intensities before that position"""

    def has_stronger_intens_to_left(pat, posindx):
        found_stronger_or_equal = False
        for i in range(posindx):
            if pat[i][1] >= pat[posindx][1]:
                found_stronger_or_equal = True
                break
        return found_stronger_or_equal

    new_rhythm = copy.deepcopy(rhythm)
    pat = new_rhythm[RHYTHM_PAT_INDX]

    # count valid start positions
    count = 0
    for i in range(len(pat)):
        if has_stronger_intens_to_left(pat, i):
            count += 1
    if count == 0:
        pat = []
    else:

        choose = rndm_2[const.RNDM_BASE_RHYTHM].rndm_int(1, count)
        count = 0
        for i in range(len(pat)):
            if has_stronger_intens_to_left(pat, i):
                count += 1
                if count == choose:
                    for _ in range(i):
                        del pat[0]
                    break

    return new_rhythm


def rhythm2end(rhythm, rndm_2):
    """ends rhythm at random position under the condition
       that there don't exist stronger intensities after that position"""

    def has_stronger_intens_to_right(pat, posindx):
        found_stronger = False
        for i in range(posindx + 1, len(pat)):
            if pat[i][1] > pat[posindx][1]:
                found_stronger = True
                break
        return found_stronger

    new_rhythm = copy.deepcopy(rhythm)
    pat = new_rhythm[RHYTHM_PAT_INDX]

    # count valid end positions
    count = 0
    for i in range(len(pat)):
        if not has_stronger_intens_to_right(pat, i):
            count += 1
    if count == 0:
        pat = []
    else:
        choose = rndm_2[const.RNDM_BASE_RHYTHM].rndm_int(1, count)
        count = 0
        for i in range(len(pat)):
            if not has_stronger_intens_to_right(pat, i):
                count += 1
                if count == choose:
                    length = len(pat)
                    for _ in range(i + 1, length):
                        del pat[-1]
                    break
    return new_rhythm


def rhythm2double(rhythm, rndm_2):
    """duplicates rhythm of first beat randomly to other beats"""

    def first_position_of_beat(beat):
        return const.TICKSRES * beat

    def last_position_of_beat(beat):
        return const.TICKSRES * (beat + 1) - 1

    def pat_replace(pat, beat1, beat2):
        """replace positions of beat2 with positions of beat1
           first beat of a bar is 0"""
        assert beat2 > beat1, "beat2 must be > beat1"

        # first remove beat2
        pat_len = len(pat)
        for j in range(pat_len - 1, -1, -1):
            if pat[j][0] >= first_position_of_beat(beat2) \
                                  and pat[j][0] <= last_position_of_beat(beat2):
                del pat[j]

        # now duplicate beat1 as beat2
        # find index before which to insert
        insert_index = len(pat)
        for j, pat_entry in enumerate(pat):
            if pat_entry[0] > last_position_of_beat(beat2):
                insert_index = j
                break

        pat_len = len(pat)
        for j in range(pat_len):
            if pat[j][0] >= first_position_of_beat(beat1) \
                                    and pat[j][0] <= last_position_of_beat(beat1):
                ptx = copy.copy(pat[j])
                # shift to beat2 position
                ptx[0] += (const.TICKSRES * beat2 - const.TICKSRES * beat1)
                pat.insert(insert_index, ptx)
                insert_index += 1

    new_rhythm = copy.deepcopy(rhythm)
    pat = new_rhythm[RHYTHM_PAT_INDX]
    numbeats = new_rhythm[RHYTHM_BEAT_INDX]

    for i in range(1, numbeats):
        prob = rndm_2[const.RNDM_BASE_RHYTHM].rndm_int(1, 100)
        if mp.RHYTHM_DOUBLE_PROB > prob:
            pat_replace(pat, 0, i)  # replace beat i with beat 0
    return new_rhythm


def last_bar_rhythm(beat_in_current_bar, current_bar_num, comp_data, comp_data_2):
    """create new rhythm up to first accent of track_rhythm
       find first rhythm position which has equal or lower acc than previous position.
       Delete all positions starting with this position"""

    one_beat_rhythm = []

    pat = tu.get_track_rhythm(comp_data['track_info'])[RHYTHM_PAT_INDX]
    acc_found = -1

    del_from_pos = len(pat)
    for i, pat_entry in enumerate(pat):
        assert pat_entry[1] > 0, "Something is wrong with acc"
        if pat_entry[1] <= acc_found:
            del_from_pos = i
            break
        else:
            acc_found = pat_entry[1]

    one_beat_rhythm = []
    # CHECK    if slice_num_in_current_bar==0: weggelassen, richtig ????
    for i in range(del_from_pos):
        if pos_in_beat(pat[i], beat_in_current_bar):

            connection_type = conn_type(pat[i], comp_data)
            one_beat_rhythm.append([shift_to_bar(pat[i], current_bar_num, comp_data_2),
                                    pat[i][1], connection_type])

    return one_beat_rhythm


def first_bar_rhythm(beat_in_current_bar, current_bar_num, comp_data, comp_data_2):
    """create new rhythm starting with upbeat"""

    pat = tu.get_track_rhythm(comp_data['track_info'])[RHYTHM_PAT_INDX]
    one_beat_rhythm = []
    if len(pat) <= 1:  # don't use 1 pos rhythm for first bar
        pass
    else:
        low_acc = 999  # find lowest acc in pat
        last_low_pos = -1
        for i, pat_entry in enumerate(pat):
            if pat_entry[1] <= low_acc:
                low_acc = pat_entry[1]
                last_low_pos = i

        assert last_low_pos != -1, "last_low_pos wrong"

        # choose last low_acc position as start position
        start_from = last_low_pos

        for i in range(start_from, len(pat)):
            if pos_in_beat(pat[i], beat_in_current_bar):
                connection_type = conn_type(pat[i], comp_data)
                one_beat_rhythm.append([shift_to_bar(pat[i], current_bar_num, comp_data_2),
                                        pat[i][1], connection_type])
    return one_beat_rhythm


def do_track_rhythm(rule, beat_in_current_bar, current_bar_num, comp_data, comp_data_2):
    """create new rhythm based on variation track rhythm or original track rhythm"""

    if rule == RM_VARI_TRACK_RHYTHM:
        pat = comp_data_2['vari_track_rhythm'][RHYTHM_PAT_INDX]
    else:
        pat = tu.get_track_rhythm(comp_data['track_info'])[RHYTHM_PAT_INDX]

    one_beat_rhythm = []
    for pat_entry in pat:
        if pos_in_beat(pat_entry, beat_in_current_bar):
            connection_type = conn_type(pat_entry, comp_data)
            one_beat_rhythm.append([shift_to_bar(pat_entry, current_bar_num, comp_data_2),
                                    pat_entry[1], connection_type])

    return one_beat_rhythm


def pos_in_beat(pat_entry, beat):
    """checks if a given position is within a specific beat"""
    return (pat_entry[0] >= beat * const.TICKSRES) and (pat_entry[0] < (beat + 1) * const.TICKSRES)


def conn_type(pat_entry, comp_data):
    """returns connection type of a pat entry"""
    is_percussion_instrument = not tu.is_melody_instrument(comp_data['track_info'])
    if is_percussion_instrument:
        connection_type = const.CONNECT_AUTODAMP
    else:
        connection_type = pat_entry[2]
    return connection_type


def shift_to_bar(pat_entry, bar_num, comp_data_2):
    """shifts a pat entry to another bar"""
    return pat_entry[0] + bar_num * const.TICKSRES * comp_data_2['num_of_beats']


def rhythm_generator(beat_indx, rhythm_rule, comp_data, comp_data_2, bar_distribution):
    """generates the rhythm for a beat"""

    beat_in_current_bar = beat_indx % comp_data_2['num_of_beats']
    current_bar_num = beat_indx // comp_data_2['num_of_beats']  # first bar = 0
    actual_global_bar_num = comp_data_2['num_of_first_bar'] + current_bar_num

    last_bar = comp_data_2['ends_level'] == 0 and current_bar_num == comp_data_2['num_bars_in_part'] - 1 \
        and comp_data['track_id'] != const.HARMONY_TRACK  # last bar

    first_bar = comp_data_2['starts_level'] == 0 and current_bar_num == 0 \
        and comp_data['track_id'] != const.HARMONY_TRACK  # first bar

    one_beat_rhythm = []
    use_pause = False

    if rhythm_rule in [RM_SOLO_PATTERN, RM_TRACK_RHYTHM, RM_VARI_TRACK_RHYTHM]:

        if bar_distribution[actual_global_bar_num][const.PLAYED_IN_TRACK + comp_data['track_id']] == 0:
            use_pause = True

    if use_pause:
        one_beat_rhythm = []

    elif last_bar:
        one_beat_rhythm = last_bar_rhythm(beat_in_current_bar, current_bar_num, comp_data, comp_data_2)

    elif rhythm_rule == RM_SOLO_PATTERN:

        pat = comp_data_2['selected_solo_rhythm'][RHYTHM_PAT_INDX]

        one_beat_rhythm = []

        for pat_entry in pat:
            if pos_in_beat(pat_entry, beat_in_current_bar):
                connection_type = conn_type(pat_entry, comp_data)
                one_beat_rhythm.append([shift_to_bar(pat_entry, current_bar_num, comp_data_2),
                                        pat_entry[1], connection_type])

    elif first_bar:
        one_beat_rhythm = first_bar_rhythm(beat_in_current_bar, current_bar_num, comp_data, comp_data_2)

    elif rhythm_rule in [RM_TRACK_RHYTHM, RM_VARI_TRACK_RHYTHM]:  # create new rhythm based on track_rhythm

        one_beat_rhythm = do_track_rhythm(rhythm_rule, beat_in_current_bar, current_bar_num, comp_data, comp_data_2)

    elif rhythm_rule == RM_HARMONY_TRACK:
        one_beat_rhythm = []
        one_beat_rhythm.append([beat_in_current_bar * const.TICKSRES +
                                current_bar_num * comp_data_2['num_of_beats'] * const.TICKSRES, 0, 0])

    elif rhythm_rule == RM_REPEAT:
        one_beat_rhythm = get_rhythm_from_bars_and_beats(beat_indx, comp_data_2['repeat_from_bar'], comp_data_2)

    return one_beat_rhythm


def set_selected_solo_rhythm(c_2, current_bar_num):
    """sets solo rhythm type depending on bar number and number of bars in current part"""
    if c_2['num_bars_in_part'] == 1:
        c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][c_2['double_select']]

    elif c_2['num_bars_in_part'] == 2:
        if current_bar_num == 0:
            c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][c_2['intro_select']]
        else:
            c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][c_2['end_select']]

    elif c_2['num_bars_in_part'] == 3:
        if current_bar_num == 0:
            c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][c_2['intro_select']]
        elif current_bar_num == c_2['num_bars_in_part'] - 1:
            c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][c_2['end_select']]
        else:
            c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][c_2['double_select']]

    elif c_2['num_bars_in_part'] >= 4:
        if current_bar_num == 0:
            c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][1]  # always use intro
        elif current_bar_num == c_2['num_bars_in_part'] - 1:
            c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][2]  # always use end

        else:
            c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][c_2['double_select']]
#         if current_bar_num == 0:
#             c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][1]  # always use intro
#         elif current_bar_num == c_2['num_bars_in_part'] - 2: # was - 1
#             c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][2]  # always use end
#         elif current_bar_num == c_2['num_bars_in_part'] - 1: #
#             c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][4]  # always use pause
#         else:
#             c_2['selected_solo_rhythm'] = c_2['solo_rhythm'][c_2['double_select']]


def loop_beats(rhythm_rule, rpt, bar_distribution, comp_data, c_2):
    """loops over all beats of current part"""

    pos_conn_intens = []  # will contain tuples of position, length and intensity for part

    # total number of beats in part
    num_of_beats_in_part = c_2['num_of_beats'] * c_2['num_bars_in_part']

    beat_indx = 0
    while beat_indx < num_of_beats_in_part:

        if rpt != NO_REPEAT:  # ignore original rhythm rule, if any
            rhythm_rule = RM_REPEAT

        elif comp_data['track_id'] == const.HARMONY_TRACK:  # ignore original rhythm rule, if any
            rhythm_rule = RM_HARMONY_TRACK

        else:
            if rhythm_rule == RM_SOLO_PATTERN:

                current_bar_num = beat_indx // c_2['num_of_beats']

                set_selected_solo_rhythm(c_2, current_bar_num)

        one_beat_rhythm = rhythm_generator(beat_indx, rhythm_rule, comp_data, c_2, bar_distribution)

        c_2['bars_and_beats'].append([BEAT_RHYTHM, beat_indx, one_beat_rhythm])
        if comp_data['track_id'] != const.HARMONY_TRACK:
            is_percussion_instrument = not tu.is_melody_instrument(comp_data['track_info'])

            for i in one_beat_rhythm:
                pos_conn_intens.append(i)
                if is_percussion_instrument:
                    c_2['tones'].append(0)  # dummy, no tones heights for percussion instruments
        beat_indx += 1
    return pos_conn_intens


def create_part_rhythm(c_strct, comp_data, comp_data_2, bar_distribution):
    """creates the rhythmic components of a part, i. e. position, length and intensity of tones.
       The tone height will be generated in function create_part_melody """

    c_2 = comp_data_2

    assert c_2['num_bars_in_part'] > 0, "Something is wrong with num_bars_in_part"

    rhythm_rule = -1  # still undefined
    bridge_part = c_strct[PROP_INDX][PROP_INTRO_BRIDGE_END] == CRB

    rpt = c_strct[PROP_INDX][PROP_USEPART]
    if rpt != NO_REPEAT:
        c_2['repeat_from_bar'] = c_strct[PROP_INDX][PROP_FROM_BAR]

    if rpt == NO_REPEAT and comp_data['track_id'] != const.HARMONY_TRACK:

        # prepare a variational rhythm

        c_2['vari_track_rhythm'] \
         = create_track_rhythm(comp_data['track_info'],
                               c_2['global_rhythm'],
                               c_2['bpm'],
                               c_2['selected_speed'],
                               comp_data['rndm_2'])

        if tu.is_solo_instrument(comp_data['track_info']):
            c_2['solo_rhythm'] = prepare_solo_rhythm(bridge_part, comp_data, c_2)
            rhythm_rule = RM_SOLO_PATTERN

            c_2['double_select'] = comp_data['rndm_2'][const.RNDM_MELO_RHYTHM].rndm_choice(mp.RHYTHM_DOUBLE_DISTRI)
            c_2['intro_select'] = comp_data['rndm_2'][const.RNDM_MELO_RHYTHM].rndm_choice(mp.RHYTHM_INTRO_DISTRI)
            c_2['end_select'] = comp_data['rndm_2'][const.RNDM_MELO_RHYTHM].rndm_choice(mp.RHYTHM_ENDING_DISTRI)

        elif bridge_part:
            rhythm_rule = RM_VARI_TRACK_RHYTHM

        else:
            rhythm_rule = \
              comp_data['rndm_2'][const.RNDM_MELO_RHYTHM].rndm_choice(mp.RHYTHM_NORM_OR_VARI_NON_SOLO)

    pos_conn_intens = loop_beats(rhythm_rule, rpt, bar_distribution, comp_data, c_2)
    return pos_conn_intens


def prepare_solo_rhythm(bridge_part, comp_data, comp_data_2):
    """prepares special rhythm variations used for solo instruments
       currently these are
       solo normal, solo intro, solo ending, solo double"""

    track_rhythm = tu.get_track_rhythm(comp_data['track_info'])
    vari_track_rhythm = comp_data_2['vari_track_rhythm']

    pause_rhythm = [track_rhythm[0], []]

    normal_or_vari = comp_data['rndm_2'][const.RNDM_MELO_RHYTHM].rndm_choice(mp.RHYTHM_NORM_OR_VARI_SOLO)
    if not bridge_part:
        if normal_or_vari == RM_VARI_TRACK_RHYTHM:
            rhythm_set = [vari_track_rhythm,
                          rhythm2intro(vari_track_rhythm, comp_data['rndm_2']),
                          rhythm2end(vari_track_rhythm, comp_data['rndm_2']),
                          rhythm2double(vari_track_rhythm, comp_data['rndm_2']),
                          pause_rhythm,
                          ]
        else:
            rhythm_set = [track_rhythm,
                          rhythm2intro(track_rhythm, comp_data['rndm_2']),
                          rhythm2end(track_rhythm, comp_data['rndm_2']),
                          rhythm2double(track_rhythm, comp_data['rndm_2']),
                          pause_rhythm,
                          ]
    else:  # always variational rhythms for bridge parts
        rhythm_set = [vari_track_rhythm,
                      rhythm2intro(vari_track_rhythm, comp_data['rndm_2']),
                      rhythm2end(vari_track_rhythm, comp_data['rndm_2']),
                      rhythm2double(vari_track_rhythm, comp_data['rndm_2']),
                      pause_rhythm,
                      ]
    return rhythm_set
