# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file defines all composition structures

"""

import copy
import inkamusic.const as const
from inkamusic.const import SUB_INDX, PROP_INDX, LEN_INDX, PROP_USEPART, PROP_INTRO_BRIDGE_END, NO_REPEAT
from inkamusic.const import PROP_FROM_BAR, PROP_TO_BAR, PROP_ACTUAL_BAR, PROP_START, PROP_END
from inkamusic.const import CR, CR2, CR_INTRO, CR_ENDING, CRB
from inkamusic.const import BAR_GROUP, BAR_INFO, BAR_REPEATED, BAR_NOT_REPEATED
import inkamusic.utilities as utilities
import inkamusic.music_parameter as mp


def get_minimum_length(strc, min_len, melody_length):
    """ calculates minimum num of bars needed for struct """

    for k in strc:
        if k in [CR, CR2]:
            min_len += melody_length
        elif k == CRB:
            min_len += 1
        else:  # repeat
            if strc[k] in [CR, CR2]:
                min_len += melody_length
            else:
                min_len += 1
    return min_len


def get_random_struct_top(rndm_2, max_num_of_subdivisions):
    """returns randomly selected struct"""
    found = False
    while not found:

        strc = rndm_2[const.RNDM_STRUCTURE].rndm_choice(mp.STRUCT_TOP_TYPES)
        if len(strc) <= max_num_of_subdivisions:
            found = True
    return copy.deepcopy(strc)


def get_random_struct_top_short(rndm_2, max_num_of_subdivisions):
    """returns randomly selected struct"""
    found = False
    while not found:

        strc = rndm_2[const.RNDM_STRUCTURE].rndm_choice(mp.STRUCT_TOP_SHORT_TYPES)
        if len(strc) <= max_num_of_subdivisions:
            found = True
    return copy.deepcopy(strc)


def get_random_struct(rndm_2, max_num_of_subdivisions):
    """returns randomly selected struct"""
    found = False
    while not found:

        strc = rndm_2[const.RNDM_STRUCTURE].rndm_choice(mp.STRUCT_TYPES)
        if len(strc) <= max_num_of_subdivisions:
            found = True
    return copy.deepcopy(strc)


def init_part_data_structure(num_of_parts, sub, parent_level, upper_level_start,
                             upper_level_end):

    """ initialise data structure for each part
        if the adaption is not possible, the structure will be deleted again.
    """
    for i in range(0, num_of_parts):

        prelim_length = -1  # length is still undefined
        sub.append([prelim_length, [], []])

        for _ in range(0, const.NUM_OF_STRUCT_PROPERTIES):
            sub[i][PROP_INDX].append(0)
        sub[i][PROP_INDX][PROP_USEPART] = NO_REPEAT  # initialise to no repeat

        # the last part always ends the parent level but may also end an higher level
        # the highest level which is ended takes precedence
        if i == num_of_parts - 1:
            if upper_level_end != const.NO_LEVEL:
                sub[i][PROP_INDX][PROP_END] = upper_level_end
            else:
                sub[i][PROP_INDX][PROP_END] = parent_level
        else:
            sub[i][PROP_INDX][PROP_END] = const.NO_LEVEL

        # the first part always starts the parent level but may also start an higher level
        # the highest level which is started takes precedence
        if i == 0:
            if upper_level_start != const.NO_LEVEL:
                sub[i][PROP_INDX][PROP_START] = upper_level_start
            else:
                sub[i][PROP_INDX][PROP_START] = parent_level
        else:
            sub[i][PROP_INDX][PROP_START] = const.NO_LEVEL


def change_non_repeated_part(num_of_parts, sub, chindx, delta, parent_level):
    """applies length change for part which is not a repetition"""
    for i in range(0, num_of_parts):
        if i == chindx:
            sub[i][LEN_INDX] += delta
        elif sub[i][PROP_INDX][PROP_USEPART] == chindx:
            sub[i][LEN_INDX] += delta
        assert sub[i][LEN_INDX] >= 1, "should not happen"
        if sub[i][LEN_INDX] < 1:
            sub[i][LEN_INDX] = 1
        if parent_level == 0:
            # never reduce ending part to 1 bar
            if i == num_of_parts - 1 and sub[i][LEN_INDX] < 2:
                sub[i][LEN_INDX] = 2


def change_repeated_part(num_of_parts, sub, rpt, delta):
    """applies length change for part which is a repetition"""
    for i in range(0, num_of_parts):
        if i == rpt:
            sub[i][LEN_INDX] += delta
        elif sub[i][PROP_INDX][PROP_USEPART] == rpt:
            sub[i][LEN_INDX] += delta
        assert sub[i][LEN_INDX] >= 1, "should not happen"
        if sub[i][LEN_INDX] < 1:
            sub[i][LEN_INDX] = 1


class CompositionStructure():
    """Creates the structure of the composition, i. e. parts, repetitions, intro, ending and bridges"""

    def __init__(self, **kwargs):

        self.base_data = kwargs
        self.bar_struct = []
        self.smallest_part_length = None
        self.intro_length = None
        self.ending_length = None
        self.bridge_length = None

    def create_composition_structure(self):
        """creates recursively the structure of the composition, using catalog entries defined
        in module structures

        The top level (= level 0) serves as anchor and contains the total number of bars,
        a property array (which is unused for the top level) and an array of sub level structures.

        Example:
        top level (level 0): comp_struct = [num_of_bars, property array, sub level array]

        Level 1 divides the composition into n parts using 6 different part types:

        - Standard parts, which will contain composed music. A standard part will have
          approximately the length given by melody_length. If it were longer it would have been
          subdivided further.
        - Intro, Bridge and Ending parts, which are specialised versions of a standard part
        - Repeat parts, which are repetitions of earlier parts. Note that a repetition may
          be shifted in height at a later stage.
        - Sub structure parts, which serve as anchor for 1 or more parts on the next level.
          On levels greater than 1 the parts types Intro, Ending and Bridge are not used.

        Example (cont.):

        first sub level (in this example containing 2 parts)
          comp_struct[SUB_INDX][0] = [length of part 0, property array part 0, sub level array of part 0]
          comp_struct[SUB_INDX][1] = [length of part 1, property array part 1, sub level array of part 1]

        second sub level (in this example 1 part below part 1 of sub level 1)
          comp_struct[SUB_INDX][1][SUB_INDX][0] = [length of part 1, property array part 0,
                                          sub level array of part 0]

        """

        # initialise form array and prepare top level (= level 0)
        num_of_bars = self.base_data['num_of_bars']

        # this is level 0 (comp_struct[LEN_INDX], comp_struct[PROP_INDX], comp_struct[SUB_INDX])
        comp_struct = [num_of_bars, [], []]

        # get melody, intro, ending and bridge lengths (in bars)
        self.smallest_part_length = self.base_data['menu_options'].get_smallest_part_length()
        self.intro_length, self.ending_length = self.base_data['menu_options'].get_intro_ending_length()
        self.bridge_length = self.base_data['menu_options'].get_bridge_length()

        level = 0  # the level which will be subdivided, creating level 1 entries
        self.create_sub_level(sub=comp_struct[SUB_INDX],  # anchor for array of parts in next level
                              parent_level_part_length=comp_struct[LEN_INDX],  # length in bars of composition
                              parent_level=level,  # 0
                              upper_level_start=0,  # the top level part starts level 0
                              upper_level_end=0  # the top level part ends level 0
                              )

        composed = self.set_global_bar_numbers(comp_struct[SUB_INDX], 1)
        # shows structure for debugging purposes
        utilities.show_composition_structure(comp_struct, level)

        return comp_struct, composed

    def set_global_bar_numbers(self, composition_structure, bar_offset):
        """sets the global bar numbers starting with 1 for each part in the structure """

        num = len(composition_structure)
        new_offset = 0

        composed = 0

        for i in range(0, num):

            if composition_structure[i][SUB_INDX]:  # sub structure
                composed += self.set_global_bar_numbers(composition_structure[i][SUB_INDX], bar_offset + new_offset)

            elif composition_structure[i][PROP_INDX][PROP_USEPART] != NO_REPEAT:  # repeat
                rpt = composition_structure[i][PROP_INDX][PROP_USEPART]
                firstbar = bar_offset
                for j in range(0, rpt):
                    firstbar += composition_structure[j][LEN_INDX]
                lastbar = firstbar + composition_structure[rpt][LEN_INDX] - 1
                composition_structure[i][PROP_INDX][PROP_FROM_BAR] = firstbar
                composition_structure[i][PROP_INDX][PROP_TO_BAR] = lastbar

                actual_part = i
                firstbar = bar_offset
                for j in range(0, actual_part):
                    firstbar += composition_structure[j][LEN_INDX]
                composition_structure[i][PROP_INDX][PROP_ACTUAL_BAR] = firstbar

            else:
                composed += composition_structure[i][LEN_INDX]

                actual_part = i
                firstbar = bar_offset
                for j in range(0, actual_part):
                    firstbar += composition_structure[j][LEN_INDX]
                composition_structure[i][PROP_INDX][PROP_ACTUAL_BAR] = firstbar

            new_offset += composition_structure[i][LEN_INDX]
        return composed

    def set_preliminary_lengths(self, num_of_parts, sub):
        """sets initial length to parts, depending on part type"""
        for i in range(0, num_of_parts):
            rpt = sub[i][PROP_INDX][PROP_USEPART]
            if rpt == NO_REPEAT:
                if sub[i][PROP_INDX][PROP_INTRO_BRIDGE_END] == CR_INTRO:
                    prelim_length = self.intro_length
                    assert self.intro_length > 0, "intro length 0"
                elif sub[i][PROP_INDX][PROP_INTRO_BRIDGE_END] == CR_ENDING:
                    prelim_length = self.ending_length
                elif sub[i][PROP_INDX][PROP_INTRO_BRIDGE_END] == CRB:
                    prelim_length = self.bridge_length
                else:
                    prelim_length = self.smallest_part_length

                sub[i][LEN_INDX] = prelim_length
            else:  # repeat-part
                sub[i][LEN_INDX] = sub[rpt][LEN_INDX]

    def set_part_structs(self, num_of_parts, sub, form_struct, creating_level_one):
        """ sets the different types of parts and set the preliminary lengths based
        on the part types (normal part = smallest_part_length, for example)"""

        if self.intro_length == 0:  # don't create intro part
            add_intro = 0
        else:
            add_intro = 1

        for i in range(0, num_of_parts):
            assert sub[i][LEN_INDX] == -1, "Check this, this should never happen"
            if sub[i][LEN_INDX] == -1:  # still undefined
                sub[i][LEN_INDX] = 0
                if not creating_level_one:
                    struct_entry = form_struct[i]
                else:
                    if i == 0 and add_intro == 1:  # insert Intro part
                        struct_entry = CR_INTRO
                    elif i == num_of_parts-1:  # insert Ending part
                        struct_entry = CR_ENDING
                    else:
                        struct_entry = form_struct[i-1]
                        if struct_entry not in [CR, CR2, CRB]:  # i.e. a Repeat entry
                            struct_entry += add_intro  # shift +1 for added Intro part
                if struct_entry in [CR, CR2, CR_INTRO, CR_ENDING, CRB]:  # create part
                    sub[i][PROP_INDX][PROP_INTRO_BRIDGE_END] = struct_entry
                else:  # Repeat part
                    use_part = struct_entry
                    sub[i][PROP_INDX][PROP_USEPART] = use_part
                    assert sub[use_part][LEN_INDX] == 0, "Check this, this should never happen"

        self.set_preliminary_lengths(num_of_parts, sub)

    def change_intro_or_ending_length(self, intro, ending,
                                      actual_length, parent_level_part_length):
        """try first if changes in intro or ending length are sufficient to
           reach parent length"""

        def reduce_actual_length(intro, ending, actual_length):
            last_change_was_intro = False
            while actual_length != parent_level_part_length:
                if self.intro_length > 0 and (intro[LEN_INDX]) >= 3 and not last_change_was_intro:
                    intro[LEN_INDX] -= 1
                    actual_length -= 1
                    last_change_was_intro = True
                elif (ending[LEN_INDX]) >= 3:
                    ending[LEN_INDX] -= 1
                    actual_length -= 1
                    last_change_was_intro = False
                else:
                    last_change_was_intro = False

        def increase_actual_length(intro, ending, actual_length):
            last_change_was_intro = False
            while actual_length != parent_level_part_length:
                if self.intro_length > 0 and \
                  (self.smallest_part_length - intro[LEN_INDX]) > 0 and not last_change_was_intro:
                    intro[LEN_INDX] += 1
                    actual_length += 1
                    last_change_was_intro = True
                elif (self.smallest_part_length-ending[LEN_INDX]) > 0:
                    ending[LEN_INDX] += 1
                    actual_length += 1
                    last_change_was_intro = False
                else:
                    last_change_was_intro = False

        max_change_plus = 0
        max_change_minus = 0
        if self.intro_length > 0 and self.smallest_part_length-intro[LEN_INDX] > 0:
            max_change_plus += min((self.smallest_part_length - intro[LEN_INDX]), 3)
        if (self.smallest_part_length - ending[LEN_INDX]) > 0:
            max_change_plus += min((self.smallest_part_length - ending[LEN_INDX]), 3)
        if self.intro_length > 0 and intro[LEN_INDX] >= 3:
            max_change_minus += intro[LEN_INDX]-2
        if (ending[LEN_INDX]) >= 3:
            max_change_minus += ending[LEN_INDX]-2
        if actual_length > parent_level_part_length >= actual_length - max_change_minus:
            reduce_actual_length(intro, ending, actual_length)

            return True

        if actual_length < parent_level_part_length <= actual_length + max_change_plus:
            increase_actual_length(intro, ending, actual_length)

            return True

        return False  # not successful

    def change_proportional(self, num_of_parts, sub, parent_level, ratio):
        """ changes length of all parts (factor is 1 / ratio)"""

        if parent_level == 0:  # exclude intro and ending
            if self.intro_length > 0:
                dx_intro = 1
            else:
                dx_intro = 0
            dx_ending = 1
        else:
            dx_intro = 0
            dx_ending = 0

        for i in range(0 + dx_intro, num_of_parts - dx_ending):
            part_len = sub[i][LEN_INDX]
            if ratio < 1 or part_len >= ratio:
                new_len = int(part_len // ratio)
            else:
                new_len = part_len
            if sub[i][PROP_INDX][PROP_INTRO_BRIDGE_END] == CRB:  # bridge part
                pass
            elif sub[i][PROP_INDX][PROP_USEPART] != NO_REPEAT:  # repeat part
                rpt = sub[i][PROP_INDX][PROP_USEPART]
                if sub[rpt][PROP_INDX][PROP_INTRO_BRIDGE_END] == CRB:  # bridge repeated
                    pass
                else:  # normal part repeated
                    sub[i][LEN_INDX] = new_len
            else:  # normal part
                sub[i][LEN_INDX] = new_len

    def change_absolute(self, num_of_parts, sub, parent_level, ratio):
        """ changes length of one part by an absolute amount"""

        def find_valid_part():
            counter_2 = 0
            chindx = -1
            found_valid_part = False
            while not found_valid_part:
                counter_2 += 1
                if counter_2 > const.ADAPT_PARTS_MAX_TRIES or (num_of_parts == dx_intro + dx_ending):
                    break
                # exclude intro and ending
                chindx = self.base_data['rndm_2'][const.RNDM_STRUCTURE].rndm_int(dx_intro, num_of_parts - dx_ending - 1)

                rpt = sub[chindx][PROP_INDX][PROP_USEPART]
                counter_2_condition = counter_2 > const.ADAPT_PARTS_MAX_TRIES // 2
                if rpt != NO_REPEAT:
                    if sub[rpt][PROP_INDX][PROP_INTRO_BRIDGE_END] != CRB or counter_2_condition:
                        if delta == 1 or sub[rpt][LEN_INDX] > 1:
                            found_valid_part = True
                elif sub[chindx][PROP_INDX][PROP_INTRO_BRIDGE_END] != CRB or counter_2_condition:
                    if delta == 1 or sub[chindx][LEN_INDX] > 2:
                        found_valid_part = True
                    elif sub[chindx][LEN_INDX] == 2 and (parent_level != 0 or chindx != num_of_parts - 1):
                        found_valid_part = True

            return found_valid_part, chindx

        # start change_absolute

        if ratio < 1:  # actual_length is too short
            delta = 1
        else:
            delta = -1  # actual_length is too long

        dx_intro = 0
        if parent_level == 0 and self.intro_length > 0:
            dx_intro = 1

        dx_ending = 0
        if parent_level == 0:
            dx_ending = 1

        assert num_of_parts >= dx_intro + dx_ending

        found_valid_part, chindx = find_valid_part()

        if found_valid_part:
            rpt = sub[chindx][PROP_INDX][PROP_USEPART]
            if rpt != NO_REPEAT:  # change repeated part and all parts which refer to it
                change_repeated_part(num_of_parts, sub, rpt, delta)

            else:  # change part chindx and all parts which refer to it
                change_non_repeated_part(num_of_parts, sub, chindx, delta, parent_level)

    def adapt_parts(self, num_of_parts, sub, parent_level, parent_level_part_length):
        """After a structure has been selected, the part lengths are adapted to fit the overall
        number of bars in the upper level. This is not always possible, in which case another
        structure has to be used"""

        sum_of_lengths_ok = False
        counter = 0
        while not sum_of_lengths_ok and counter < const.ADAPT_PARTS_MAX_TRIES:
            counter += 1
            actual_length = 0
            for i in range(0, num_of_parts):
                actual_length += sub[i][LEN_INDX]

            if actual_length == parent_level_part_length:
                sum_of_lengths_ok = True
            else:
                if parent_level == 0:
                    if self.change_intro_or_ending_length(sub[0], sub[num_of_parts-1], actual_length,
                                                          parent_level_part_length):
                        actual_length = parent_level_part_length

                if actual_length == parent_level_part_length:
                    sum_of_lengths_ok = True
                else:

                    ratio = actual_length / parent_level_part_length
                    if ratio >= 2.0 or ratio <= 0.5:
                        # the ratio is big or small enough for a proportional change

                        self.change_proportional(num_of_parts, sub, parent_level, ratio)

                    else:
                        self.change_absolute(num_of_parts, sub, parent_level, ratio)

        return sum_of_lengths_ok  # if True: struct is usable, lengths are set, else no valid lengths were found

    def find_subdivision_structure(self, creating_level_one, max_num_of_subdivisions, level_data, cr_type):
        """find a possible subdivision """

        if creating_level_one:
            if max_num_of_subdivisions <= 2:
                form_struct = get_random_struct_top_short(self.base_data['rndm_2'], max_num_of_subdivisions)
            else:
                form_struct = get_random_struct_top(self.base_data['rndm_2'], max_num_of_subdivisions)

            if self.intro_length > 0:
                num_of_parts = len(form_struct) + 2  # 2 for intro and ending
            else:
                num_of_parts = len(form_struct) + 1  # 2 for ending
        else:
            form_struct = get_random_struct(self.base_data['rndm_2'], max_num_of_subdivisions)

            # replace CR types by current CR type
            for i, struct_type in enumerate(form_struct):
                if struct_type == CR:
                    form_struct[i] = cr_type

            num_of_parts = len(form_struct)

        del level_data['sub'][:]  # reset anchor
        init_part_data_structure(num_of_parts,
                                 level_data['sub'],
                                 level_data['parent_level'],
                                 level_data['upper_level_start'],
                                 level_data['upper_level_end'])
        self.set_part_structs(num_of_parts,
                              level_data['sub'],
                              form_struct,
                              creating_level_one)
        adapt_result = self.adapt_parts(num_of_parts,
                                        level_data['sub'],
                                        level_data['parent_level'],
                                        level_data['parent_level_part_length'])
        return adapt_result, num_of_parts

    def iterate_over_parts(self, num_of_parts, level_data):
        """iterate over all parts to create sublevels"""

        for part_no in range(0, num_of_parts):
            rpt = level_data['sub'][part_no][PROP_INDX][PROP_USEPART]
            if rpt == NO_REPEAT:
                cr_type = level_data['sub'][part_no][PROP_INDX][PROP_INTRO_BRIDGE_END]
                if part_no == 0:  # first part always starts a level
                    if level_data['upper_level_start'] != const.NO_LEVEL:  # part starts an upper level also
                        create_as_startpart_to_level = level_data['upper_level_start']
                    else:
                        create_as_startpart_to_level = level_data['parent_level']
                else:
                    create_as_startpart_to_level = const.NO_LEVEL

                if part_no == num_of_parts - 1:  # last part always ends a level
                    if level_data['upper_level_end'] != const.NO_LEVEL:  # part ends an upper level also
                        create_as_endpart_to_level = level_data['upper_level_end']
                    else:
                        create_as_endpart_to_level = level_data['parent_level']
                else:
                    create_as_endpart_to_level = const.NO_LEVEL

                level_data['parent_level'] += 1

                self.create_sub_level(sub=level_data['sub'][part_no][SUB_INDX],
                                      parent_level_part_length=level_data['sub'][part_no][LEN_INDX],
                                      parent_level=level_data['parent_level'],

                                      # the sub level part starts this upper level, if any
                                      upper_level_start=create_as_startpart_to_level,

                                      # the sub level part ends this upper level, if any
                                      upper_level_end=create_as_endpart_to_level,
                                      cr_type=cr_type)
                level_data['parent_level'] -= 1

    def create_sub_level(self, **level_data):

        """ This function is called recursively to subdivide a part for the next level
            Note that the parameter "parent_level" contains the level which is subdivided by this function,
            so the created parts will belong to "parent_level + 1" """

        creating_level_one = bool(level_data['parent_level'] == 0)
        # level 1 always includes ending and may contain intro and bridge parts
        if not creating_level_one:
            cr_type = level_data['cr_type']
        else:
            cr_type = 0

        if creating_level_one:
            # - 2 to account for possible intro or ending
            max_num_of_subdivisions = max((level_data['parent_level_part_length'] - 2) // self.smallest_part_length, 1)
            # divide again so that in general at least one level below the top level is possible
            max_num_of_subdivisions = max(max_num_of_subdivisions // min(self.smallest_part_length, 3), 1)
        else:

            max_num_of_subdivisions = max(level_data['parent_level_part_length'] // self.smallest_part_length, 1)

        # subdivision only if parent part is big enough and never for last (ending) part
        if creating_level_one or ((max_num_of_subdivisions > 2) and level_data['upper_level_end'] != 0):
            # try to find subdivision (with the exception of level 1 this subdivision will contain
            # at least 3 parts

            try_struct_counter = 0
            stop_condition = False

            while not stop_condition:
                try_struct_counter += 1
                if try_struct_counter > const.CREATE_SUB_LEVEL_MAX_TRIES:
                    assert not creating_level_one, "Level one should always be possible to create"
                    stop_condition = True
                    del level_data['sub'][:]  # give up and dont subdivide part
                    adapt_result = False
                else:
                    adapt_result, num_of_parts = self.find_subdivision_structure(creating_level_one,
                                                                                 max_num_of_subdivisions,
                                                                                 level_data,
                                                                                 cr_type)

                if not adapt_result:  # struct is not usable
                    # total length could not be reached exactly
                    # try another struct
                    pass

                else:  # struct is usable, iterate over all parts to create sublevels
                    self.iterate_over_parts(num_of_parts, level_data)

                    stop_condition = True

    def get_original_bar_num(self, global_bar_num):
        """finds global number of original (i. e. created) bar of a repetition bar"""

        max_bar_struct = len(self.bar_struct)
        i = 0
        active = 0
        while i < max_bar_struct:
            if self.bar_struct[i][0] == BAR_GROUP:
                start_bar_of_group = self.bar_struct[i][1]  # global number of first bar in group
                active = 1
                local_bar_indx = global_bar_num - start_bar_of_group
                # this local_bar_indx may or may not exist within the current group
                # if not, the bar will be found in a following group
            if active == 1 and self.bar_struct[i][0] == BAR_INFO and self.bar_struct[i][1] == local_bar_indx:
                return self.bar_struct[i][3]  # this is the original bar number
            i += 1
        return -1, -1

    def get_bar_info(self, use_type, bar_indx, num_of_first_bar, rpt_from_bar):
        """prepares information for the BAR_INFO data structure within the bar structure """

        type_and_first_bar_of_group = []
        original_bar_num = []

        if use_type == BAR_NOT_REPEATED:
            original_bar_num = num_of_first_bar + bar_indx
            type_and_first_bar_of_group.append(BAR_NOT_REPEATED)
            type_and_first_bar_of_group.append(num_of_first_bar)

        elif use_type == BAR_REPEATED:
            use_bar_num = bar_indx + rpt_from_bar
            original_bar_num = self.get_original_bar_num(use_bar_num)
            type_and_first_bar_of_group.append(BAR_REPEATED)
            type_and_first_bar_of_group.append(num_of_first_bar)

        return type_and_first_bar_of_group, original_bar_num

    def create_bar_group(self, comp_struct, part_id, rpt_from_bar):
        """ creates a new bar group, see create_bar_structure for details"""

        num_bars = comp_struct[part_id][LEN_INDX]

        num_of_first_bar = comp_struct[part_id][PROP_INDX][PROP_ACTUAL_BAR]
        cr_type = comp_struct[part_id][PROP_INDX][PROP_INTRO_BRIDGE_END]
        self.bar_struct.append([BAR_GROUP, num_of_first_bar, num_bars])

        bar_indx = 0
        while bar_indx < num_bars:

            if rpt_from_bar != NO_REPEAT:
                use_type = BAR_REPEATED
            else:
                use_type = BAR_NOT_REPEATED

            type_and_first_bar_of_group, original_bar_num = \
                self.get_bar_info(use_type, bar_indx, num_of_first_bar, rpt_from_bar)

            if type_and_first_bar_of_group != []:
                self.bar_struct.append([BAR_INFO, bar_indx, type_and_first_bar_of_group, original_bar_num, cr_type])
                bar_indx += 1

    def create_bar_structure(self, comp_struct, level):
        """This function serialises the hierarchical structure of the composition given by comp_struct.
           The resulting array self.bar_struct contains a start record for each group of bars
           ( bar_struct[i] = [BAR_GROUP, number of first bar in group, length of group]) and then the
           individual bars of the group
           (bar_struct[i + j] =
           [BAR_INFO,
           bar index within group,
           [BAR_REPEATED or BAR_NOT_REPEATED,
           number of first bar in group],
           original bar number, create_type])
           A bar group is identified by its first bar number.
        """

        num_parts = len(comp_struct)

        for part_no in range(0, num_parts):
            if comp_struct[part_no][SUB_INDX]:  # sub structure

                level += 1
                _ = self.create_bar_structure(comp_struct[part_no][SUB_INDX], level)
                level -= 1

            else:  # create or repeat part

                rpt = comp_struct[part_no][PROP_INDX][PROP_USEPART]

                if rpt != NO_REPEAT:
                    rpt_from_bar = comp_struct[part_no][PROP_INDX][PROP_FROM_BAR]

                else:
                    rpt_from_bar = NO_REPEAT

                self.create_bar_group(comp_struct, part_no, rpt_from_bar)
        if level == 1:
            return self.bar_struct
        return -1

    def show_bar_struct(self):
        """ shows bar_struct structure for debugging purposes"""
        if const.DEBUG_OUTPUT:
            print(' ')
            for i in range(len(self.bar_struct)):
                if self.bar_struct[i][0] == BAR_GROUP:
                    print(' ')
                    print('Now follows group of', self.bar_struct[i][2], 'bars, starting with global bar number',
                          self.bar_struct[i][1])
                else:
                    if self.bar_struct[i][2][0] == BAR_REPEATED:
                        txt = ': Repeat global bar'
                    else:
                        txt = ': Create global bar'
                    print('  group bar', self.bar_struct[i][1], txt, self.bar_struct[i][3])
