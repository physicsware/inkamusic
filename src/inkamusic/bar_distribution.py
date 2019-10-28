# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file creates the bar distribution

"""
import random
import inkamusic.const as const

from inkamusic.const import BAR_GROUP
from inkamusic.const import USED_HOW_OFTEN, CREATE_TYPE_IDENTIFIER, GROUP_IDENTIFIER, PLAYED_IN_TRACK
import inkamusic.music_parameter as mp
import inkamusic.trackinfo_util as tu
import inkamusic.settings as settings


class BarDistribution():
    """keeps information about each bar of a composition"""

    def __init__(self, inka_data, c_2):  # num_of_bars, num_of_tracks, track_info, menu_options, rndm_2):
        self.c_2 = c_2
        self.inka_data = inka_data
        self.bar_distribution = []

    def show_bar_distribution(self):
        """prints bar distribution for debugging purposes"""
        if const.DEBUG_OUTPUT:
            print(' ')
            for i in range(1, len(self.bar_distribution)):  # bar numbers start at 1, index 0 not used
                if self.bar_distribution[i][USED_HOW_OFTEN] == 0:  # bar is a repeated bar
                    print('bar', i, ' (not created)')
                else:
                    print('bar', i, ' is used', self.bar_distribution[i][USED_HOW_OFTEN],
                          'times, bar is part of group starting at bar', self.bar_distribution[i][1])
                    print('       harmony type is', self.bar_distribution[i][const.HARMONY_IDENTIFIER])
                    print('       create type is', self.bar_distribution[i][CREATE_TYPE_IDENTIFIER])

    def create_bar_distribution(self, bar_struct):
        """ This functions counts for each created (i. e. not repeated) bar, how often this
        bar is used within the composition. Also the group in which the bar is first used is stored.
        This data structure will be extended with pause and harmony information
        in set_paused_bars and set_bar_harmony_type

        """
        const.ORIGINAL_BAR_NUM_INDX = 3
        bar_distri = [[0, 0, 0]]  # index 0 not used

        for _ in range(1, self.c_2['num_of_bars'] + 1):
            bar_distri.append([0, 0, 0])

        for bar_struct_entry in bar_struct:
            if bar_struct_entry[0] == BAR_GROUP:
                currentgroup = bar_struct_entry[1]
            else:
                barnum = bar_struct_entry[const.ORIGINAL_BAR_NUM_INDX]
                bar_distri[barnum][USED_HOW_OFTEN] += 1
                if bar_distri[barnum][GROUP_IDENTIFIER] == 0:  # group undefined
                    bar_distri[barnum][GROUP_IDENTIFIER] = currentgroup
                if bar_distri[barnum][CREATE_TYPE_IDENTIFIER] == 0:
                    bar_distri[barnum][CREATE_TYPE_IDENTIFIER] = bar_struct_entry[const.CREATE_TYPE_INDX]

        self.bar_distribution = bar_distri

        return self.bar_distribution

    def set_non_special_bars_harmony_types(self, harmony_list, num_of_bars_to_reach, num_of_bars_currently_assigned):
        """sets the harmony type for all normal bars, i. e. not the first, last and second-last bar"""
        for bar_num in range(2, self.c_2['num_of_bars'] - 1):

            num_used = self.bar_distribution[bar_num][USED_HOW_OFTEN]
            found = []
            if num_used != 0:
                # check if one or more harmony types need exactly this number of bars
                for i in range(len(harmony_list)):
                    if abs(num_of_bars_to_reach[i] - num_of_bars_currently_assigned[i] - num_used) < 1:
                        found.append(i)
                if found != []:
                    choose = self.inka_data['rndm_2'][const.RNDM_MELO_RHYTHM].rndm_choice(found)
                    num_of_bars_currently_assigned[choose] += num_used
                    self.set_harmony_type(bar_num, harmony_list[choose])
                else:
                    best_harmony_delta = -999
                    best_harmony = -1
                    for i in range(len(harmony_list)):
                        reach_minus_assigned = num_of_bars_to_reach[i] - \
                                               num_of_bars_currently_assigned[i] - num_used
                        if reach_minus_assigned > 0:
                            found.append(i)
                        elif reach_minus_assigned > best_harmony_delta:
                            best_harmony_delta = reach_minus_assigned
                            best_harmony = i
                    if found == []:
                        found.append(best_harmony)
                    choose = self.inka_data['rndm_2'][const.RNDM_MELO_RHYTHM].rndm_choice(found)
                    num_of_bars_currently_assigned[choose] += num_used
                    self.set_harmony_type(bar_num, harmony_list[choose])

    def set_harmony_type(self, bar_num, harmony_type):
        """sets the harmony type for a specific bar"""
        maxindex = len(self.bar_distribution[bar_num]) - 1
        if maxindex < const.SCALE_HARMONY_TYPES_INDX:
            self.bar_distribution[bar_num].append(harmony_type)
        else:
            self.bar_distribution[bar_num][const.SCALE_HARMONY_TYPES_INDX] = harmony_type

    def set_bar_harmony_type(self):
        """sets the harmony type for each bar"""

        scale = self.inka_data['menu_options'].get_selected_scale()

        # get list of harmony types used with this scale
        harmony_list = scale[const.SCALE_HARMONY_TYPES_INDX]

        # calculate exact number of bars to be used for each harmony type (in general no integer)

        num_of_bars_to_reach = []  # for each harmony_type in harmony_list
        num_of_bars_currently_assigned = []  # for each harmony_type in harmony_list

        p_reduce = mp.HARMONY_FREQUENCY_DECREASE

        factor = 1.0
        sum_factor = 0.0

        # calculate sum of all weight factors
        for i in range(len(harmony_list)):
            sum_factor += factor
            factor = factor / p_reduce

        factor = 1.0

        for i in range(len(scale[const.SCALE_HARMONY_TYPES_INDX])):
            num_of_bars_to_reach.append(self.c_2['num_of_bars'] * factor / sum_factor)
            factor = factor / p_reduce

        for i in range(len(harmony_list)):
            num_of_bars_currently_assigned.append(0)

        # use first harmony entry for first, last and second last bar
        self.set_harmony_type(1, harmony_list[0])
        num_of_bars_currently_assigned[0] += self.bar_distribution[1][USED_HOW_OFTEN]
        if self.c_2['num_of_bars'] > 1:
            self.set_harmony_type(self.c_2['num_of_bars'], harmony_list[0])
            num_of_bars_currently_assigned[0] += self.bar_distribution[self.c_2['num_of_bars']][USED_HOW_OFTEN]
        if self.c_2['num_of_bars'] > 2:
            self.set_harmony_type(self.c_2['num_of_bars'] - 1, harmony_list[0])
            num_of_bars_currently_assigned[0] += self.bar_distribution[self.c_2['num_of_bars'] - 1][USED_HOW_OFTEN]

        if self.c_2['num_of_bars'] > 3:
            self.set_non_special_bars_harmony_types(harmony_list, num_of_bars_to_reach, num_of_bars_currently_assigned)
        if const.DEBUG_OUTPUT:
            print(' ')
            for i, entry in enumerate(harmony_list):
                print('harmony id', entry, 'is used in', num_of_bars_currently_assigned[i], 'bars')
        self.show_bar_distribution()

    def init_play_state(self, track):
        """resets the play state for all bars for one  or all tracks"""
        if track == -1:  # all tracks
            first = 0
            last = self.c_2['number_of_tracks']
        else:
            first = track
            last = track + 1
        for track_num in range(first, last):
            for bar_num in range(1, self.c_2['num_of_bars'] + 1):
                if self.bar_distribution[bar_num][USED_HOW_OFTEN] != 0:  # not for repeated bars
                    maxindex = len(self.bar_distribution[bar_num]) - 1
                    if maxindex < (PLAYED_IN_TRACK + track_num):
                        self.bar_distribution[bar_num].append(1)
                    else:
                        self.bar_distribution[bar_num][(PLAYED_IN_TRACK + track_num)] = 1

    def check_non_pause_in_other_tracks(self, current_index_in_all_tracks, choose_bar, all_tracks):
        """checks if bar is not paused in another track"""
        for i in range(current_index_in_all_tracks):
            if self.bar_distribution[choose_bar][(PLAYED_IN_TRACK + all_tracks[i])] == 1:
                # not paused in this track
                return True
        return False

    def do_list_type_pause(self, pause, track):
        """sets pauses in tracks depending on instruments distribution catalogs"""
        special_cr = pause[track]
        for current_cr_type in special_cr:
            # count number of bars
            cr_type_bars = 0
            for bar_num in range(1, self.c_2['num_of_bars'] + 1):
                cr_type = self.bar_distribution[bar_num][CREATE_TYPE_IDENTIFIER]
                if cr_type == current_cr_type:  # no pause
                    cr_type_bars += 1
            # choose number of bars to pause even if cr type is correct
            cr_type_bars_to_pause = mp.PERC_CR_BARS_PAUSES * cr_type_bars // 100

            for bar_num in range(1, self.c_2['num_of_bars'] + 1):
                if self.bar_distribution[bar_num][USED_HOW_OFTEN] != 0:  # not for repeated bars
                    cr_type = self.bar_distribution[bar_num][CREATE_TYPE_IDENTIFIER]
                    if cr_type == current_cr_type:  # no pause
                        if cr_type_bars_to_pause > 0 and \
                          self.inka_data['rndm_2'][const.RNDM_MELO_RHYTHM].rndm_int(1, 100) < mp.PERC_CR_BARS_PAUSES:
                            cr_type_bars_to_pause -= 1
                            self.bar_distribution[bar_num][(PLAYED_IN_TRACK + track)] = 0
                        else:
                            self.bar_distribution[bar_num][(PLAYED_IN_TRACK + track)] = 1
                    elif cr_type not in special_cr:
                        self.bar_distribution[bar_num][(PLAYED_IN_TRACK + track)] = 0

    def do_percent_type_pause(self, pause, track, all_tracks, current_index_in_all_tracks):
        """sets random pauses in tracks depending on pause setting for track and
           depending on pauses of the same bar in other tracks"""
        # - 2, because last 2 bars are never paused
        min_number_of_paused_bars = max(int(pause[track] * (self.c_2['num_of_bars'] - 2) + 0.5) - 1, 0)
        max_number_of_paused_bars = min(int(pause[track] * (self.c_2['num_of_bars'] - 2) + 0.5) + 1,
                                        self.c_2['num_of_bars'])
        actual_number_of_paused_bars = 0

        num_of_paused_bars_ok = max_number_of_paused_bars == 1

        counter = 0
        counter2 = 0
        while not num_of_paused_bars_ok:
            # - 2: never  pause last 2 bars
            choose_bar = self.inka_data['rndm_2'][const.RNDM_MELO_RHYTHM].rndm_int(1,
                                                                                   self.c_2['num_of_bars'] - 2)
            if self.bar_distribution[choose_bar][USED_HOW_OFTEN] == 0:  # repeated bar, don't use
                continue
            elif self.bar_distribution[choose_bar][(PLAYED_IN_TRACK + track)] == 1:  # not yet paused
                non_pause_found = self.check_non_pause_in_other_tracks(current_index_in_all_tracks,
                                                                       choose_bar,
                                                                       all_tracks)
                if non_pause_found or counter2 > 4 * self.c_2['num_of_bars']:
                    add = self.bar_distribution[choose_bar][USED_HOW_OFTEN]
                    if actual_number_of_paused_bars + add >= min_number_of_paused_bars and  \
                       actual_number_of_paused_bars + add <= max_number_of_paused_bars:
                        actual_number_of_paused_bars += add
                        self.bar_distribution[choose_bar][(PLAYED_IN_TRACK + track)] = 0
                        num_of_paused_bars_ok = True
                    elif actual_number_of_paused_bars + add < min_number_of_paused_bars:
                        actual_number_of_paused_bars += add
                        self.bar_distribution[choose_bar][(PLAYED_IN_TRACK + track)] = 0

            counter += 1
            counter2 += 1
            if counter % (5 * self.c_2['num_of_bars']) == 0:
                actual_number_of_paused_bars = 0
                self.init_play_state(track)
                counter2 = 0

    def set_pause_for_all_tracks(self, all_tracks, pause):
        """sets random pauses in tracks depending on pause setting for track and
           depending on pauses of the same bar in other tracks"""
        current_index_in_all_tracks = 0
        for track in all_tracks:
            if isinstance(pause[track], list):
                self.do_list_type_pause(pause, track)

            else:
                self.do_percent_type_pause(pause, track, all_tracks, current_index_in_all_tracks)

            current_index_in_all_tracks += 1

    def check_for_silent_bars(self, count_silent):
        """checks if any bar is silent or if to many bars play percussion only"""

        silent_bars_found = False
        silent_bars = 0
        only_perc = 0

        for bar_num in range(1, self.c_2['num_of_bars'] + 1):
            if self.bar_distribution[bar_num][USED_HOW_OFTEN] != 0:  # no repeat
                playsum = 0
                non_perc_playsum = 0
                for j in range(PLAYED_IN_TRACK, PLAYED_IN_TRACK + self.c_2['number_of_tracks']):

                    playsum += self.bar_distribution[bar_num][j]
                    if tu.is_melody_instrument(self.c_2['track_info'][j - PLAYED_IN_TRACK]):
                        non_perc_playsum += self.bar_distribution[bar_num][j]

                if playsum == 0:
                    silent_bars += 1
                if non_perc_playsum == 0:
                    only_perc += 1
        if silent_bars > 0 or only_perc > mp.MAX_PERCUSSION_ONLY_BARS:
            if count_silent > 5:
                silent_bars_found = False
                print(' *** SILENTBAR CONDITION')
            else:
                silent_bars_found = True

        return silent_bars_found

    def set_paused_bars(self):
        """sets the pause status for each bar within each track"""

        pause = []
        max_non_percussion_track = -1
        perc_track_found = False
        for track in range(self.c_2['number_of_tracks']):
            track_info = self.c_2['track_info'][track]
            if tu.is_melody_instrument(track_info):
                assert not perc_track_found, "perc tracks only after non-perc tracks allowed"
                if track > max_non_percussion_track:
                    max_non_percussion_track = track
                track_pause = tu.get_track_pause(track_info)
                if track_pause == -1:
                    pause.append(settings.get_pause_probability(tu.get_instrument_type(track_info),
                                                                tu.get_instrument_type_2(track_info),
                                                                self.inka_data['rndm_2']))
                else:
                    pause.append(track_pause)
            else:
                perc_track_found = True
                pause.append(settings.get_pause_probability(tu.get_instrument_type(track_info),
                                                            tu.get_instrument_type_2(track_info),
                                                            self.inka_data['rndm_2']))

        assert max_non_percussion_track != -1, "At least one non-percussion track needed"

        silent_bars_found = True

        count_silent = 0

        while silent_bars_found:
            count_silent += 1
            assert count_silent < 100, "problem with pause distribution"

            self.init_play_state(-1)  # initialise for all tracks

            non_perc_tracks = list(range(0, max_non_percussion_track + 1))
            random.shuffle(non_perc_tracks)

            # all_tracks will contain a list of all tracks, with non-percussion tracks shuffled
            all_tracks = [] + non_perc_tracks
            for track in range(max_non_percussion_track + 1, self.c_2['number_of_tracks']):
                all_tracks.append(track)

            self.set_pause_for_all_tracks(all_tracks, pause)

            silent_bars_found = self.check_for_silent_bars(count_silent)
