# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file contains all music generation parameter

"""
from inkamusic.const import RM_TRACK_RHYTHM, RM_VARI_TRACK_RHYTHM
from inkamusic.const import CR, CR2, CR_INTRO, CR_ENDING, CRB

# initial menu settings in web interface
# index starts with 0 for first menu item, separator lines are counted
# instrumentation, percussion, scales, rhythms, minutes, seconds, speed
MENU_INIT = [0, 0, 20, 22, 2, 2, 1]

# activate special settings in order to use Logic Pro with the MIDI files created by this app
LOGIC_PRO_MIDI_SETTINGS = True

# max number of bars in a composition with percussion only
MAX_PERCUSSION_ONLY_BARS = 3  # default 3

# staccato length in seconds
STACC_LEN_IN_S = 0.15  # default 0.15

# minimum tone separation in seconds (between two consecutive tones
# which are connected by type STANDARD, not LEGATO or STACCATO
TONE_SEPARATION_IN_S = 0.1

# volume reduce in % for chord tones played simultaneously by one instrument
VOLUME_REDUCE_CHORD_TONES = 4  # default 4

# the tones of a chord start at slightly different times. This constant gives the maximum amount in ticks of
# the difference
CHORD_SPREAD = 12  # default 20

# rhythm split values. These numbers are used to subdivide a rhythm
# 99 leads to no further subdivision.
# To change the probability of a subdivision, use the number more than once.
RHYTHM_SUBDIVISION = [2, 2, 2, 3, 99]  # default [2, 2, 2, 3, 99]

# choose intensity_dependency_val for specific instrument type
# low (lowest = 1) intensity_dependency_val => position to remove is less dependent on intensity/accent
# high (for example 50) intensity_dependency_val => position to remove is more dependent on intensity/accent
# (with low intensity removed first)

INTENSITY_DEPENCY_VAL_HEAVY_PERC = list(range(5, 7))  # default 8, 14
INTENSITY_DEPENCY_VAL_LIGHT_PERC = list(range(2, 5))  # default 3, 7

INTENSITY_DEPENCY_VAL_SOLO = [2, 3, 4]  # default 3, 5
INTENSITY_DEPENCY_VAL_BASS = [5, 6, 7]  # default 7, 9
INTENSITY_DEPENCY_VAL_CHORUS_HARMONY = [4, 5, 6]  # default 7, 9

# pause probabilities for different track types in %
# x % of all bars are paused for the track
PERC_PAUSE_PROB = [[17],  # P_STICK
                   [98, 99, 99, 99],  # P_ACCENT
                   [17],  # P_BASS
                   [17],  # P_HIGH
                   [17],  # P_LOW
                   [17],  # P_RIDE
                   [17],  # P_SNARE
                   ]
INSTRU_PAUSE_PROB = [[15],  # R_BASS
                     [15],  # R_LOW
                     [15],  # R_MEDI
                     [15],  # R_HIGH
                     [15],  # R_FULL
                     ]

# The frequency for each harmony type decreases by this factor for each position in the harmony list
# Example: for a 60 bar composition using a scale with harmony list [1, 0] (major and minor)
# there would be 40 major and 20 minor bars, when the factor is 2
HARMONY_FREQUENCY_DECREASE = 3.0

# up down or equal probabilities. For each tone group one of these settings will be used
# 1 up -1 down 0 equal
UP_DOWN_EQUAL_PROBS = [1, 1, -1, -1, 0]

# tone group length (gauss settings for up/down and for equal)
TONE_GROUP_LENGTH_UP_DOWN = [8, 3, 4, 16]
TONE_GROUP_LENGTH_EQUAL = [2, 2, 1, 6]

# MIDI Settings
MIDI_REVERB_VAL = 25  # default 25
MIDI_CHORUS_VAL = 25  # default 25
MIDI_CHANNEL_VOLUME_VAL = 64  # default 96
MIDI_BALANCE = 64  # default 64

# length of last tones of each track in seconds
LAST_TONE_LENGTH = 2  # default 2

# auto damp time, after this time (in seconds),
# no dissonance will be assumed to other tones
# This setting is used only for instruments with
# auto_damp style (like piano, guitar)
AUTO_DAMP_TIME = 1.5  # default 1.5

# tone length (gauss settings) in quarter beats = const.TICKSRES
# this tone length is used when the tone length can not be
# inferred from the position of the next tone when the next tone is too far away (> TONE_LENGTH_PARAM[3])
# or from the dissonance limit
TONE_LENGTH_PARAM = [1.5, 0.75, 1.0, 4.1]  # default [1.5, 0.75, 1.0, 4.1]

# probabilities in % for specific instrument types to play only tones
# of current harmony instead of using all possible tones
# if list of possible tones contains only non-harmony tones, no tone well be played
SOLO_PLAYS_HARMONY_TONES_PROB = 0  # default 25
BASS_PLAYS_HARMONY_TONES_PROB = 0  # default 90
CHORUS_PLAYS_HARMONY_TONES_PROB = 0  # default 90

# minimum range an instrument must be able to use
MIN_RANGE = 18  # default 18

# max deviation from current target tone
MAX_TARGET_DEV = 9  # default 9

# volume level and spread
VOLUME_LEVEL_SOLO = 80
VOLUME_LEVEL_NON_SOLO = 75
SPREAD = 20  # volume difference between strongest and weekest accent

# evaluation weights depending in instrument type [T_BASS, T_CHOR, T_SOLO, T_HMNY]

W_USED_DIST = [0.5, 0.5, 0.5, 0.5]  # harmony against  used tones by other instruments in the same or previous beat
W_HARMONY_DIST = [0.5, 0.5, 0.1, 0.5]  # harmony against harmony rule for current beat
W_ANCHOR = [0.1, 0.1, 0.1, 0.1]  # anchor tone used
W_JUMP = [0.3, 0.3, 0.3, 0.3]  # jump height against previous tone
W_CONT_IN_HARMONY = [0.5, 0.5, 0.5, 0.5]  # continues current harmony
W_CONT_IN_SCALE = [0.5, 0.7, 0.7, 0.5]  # continues scale
W_UP_DOWN_EQUAL = [0.0, 0.0, 0.0, 0.0]  # local up down equal setting was [0.5, 1.0, 1.0, 0.5]
W_SECOND_LAST_TONE = [0.5, 0.5, 0.8, 0.5]  # difference to second last tone
W_TARGET = [0.3, 0.3, 0.3, 0.3]  # target tone of envelope curve

# points must be within the range [0 ... 10]
# a point value of exactly 0 always removes a tone from the list of possible tones, even if the respective weight is
# also 0.
# for example: if W_HARMONY_DIST[T_SOLO] is 0 and POINTS_HARMONIC_DISTANCE_SOLO = [1, 1, 1, 1, 1, 1]
# the number of 2-tone distances is ignored in the evaluation
# but if POINTS_HARMONIC_DISTANCE_SOLO = [1, 0, 0, 0, 0, 0] tones which lead to 1 ore more 2 tone distances will not
# be used

# points for used_tones_distance (no 2-tone distance, 1, 2, 3, ... two-tone distances)
POINTS_USED_TONES_DISTANCE = [10, 1, 0.1, 0.01, 0]  # default [10, 8, 6, 4, 2]

# points for harmonic_distance (no 2-tone distance, 1, 2, 3, ... two-tone distances)
POINTS_HARMONIC_DISTANCE_SOLO = [10, 1, 0.1, 0.01, 0]  # default [10, 1, 0.1, 0.01, 0]
POINTS_HARMONIC_DISTANCE_NON_SOLO = [10, 1, 0.1, 0.01, 0]  # default [10, 1, 0.1, 0.01, 0]

# solo instruments may use tones which are dissonant to current harmony
POINTS_DISSONANT_DISTANCE_SOLO = 1

# points for jump height (0, 1, 2, ... half-tones)
POINTS_JUMP_HEIGHT = [1, 10, 10, 10, 10, 10, 10, 10, 10, 1, 0.05, 0.05]

# points for second last tone difference
POINTS_SECOND_LAST_TONE = [0.05]  # difference 0 should be avoided

# points for target tone
# 10 points as long as tone is within one octave around target_tone
POINTS_TARGET_TONE = [10, 8, 6, 4, 2, 1, 0.5, 0.3, 0.25, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1]

# points for anchor TONE
ANCHOR_POINTS = 10
NO_ANCHOR_POINTS = 2

# probability distribution normal or variational rhythm for non solo instruments
RHYTHM_NORM_OR_VARI_NON_SOLO = [RM_TRACK_RHYTHM, RM_TRACK_RHYTHM, RM_TRACK_RHYTHM, RM_TRACK_RHYTHM, RM_TRACK_RHYTHM,
                                RM_VARI_TRACK_RHYTHM]

# probability distribution normal or variational rhythm for solo instruments
RHYTHM_NORM_OR_VARI_SOLO = [RM_TRACK_RHYTHM, RM_TRACK_RHYTHM, RM_TRACK_RHYTHM, RM_TRACK_RHYTHM, RM_TRACK_RHYTHM,
                            RM_VARI_TRACK_RHYTHM]
# probability to duplicate the rhythm of the first beat to another beat when generating double solo rhythm
RHYTHM_DOUBLE_PROB = 60  # default 60

# probability distributions for using intro, ending or double solo rhythms (where possible to use)
# 0 index results in original rhythm, 1, 2, 3 and 4 gives intro, ending, doubled rhythm or paused rhythm
RHYTHM_DOUBLE_DISTRI = [0, 0, 3]
RHYTHM_INTRO_DISTRI = [0, 1, 1, 1, 1]
RHYTHM_ENDING_DISTRI = [0, 2, 2, 2, 2]

# min and max time in seconds for which a harmony remains constant
HARMONY_MIN_CONST_TIME = 1.5
HARMONY_MAX_CONST_TIME = 4

# constants for random instrumentation

# percentage of medium height solo instruments (instead of high)
RND_INSTRU_MEDIUM_SOLO = 25
# max and min pause for solo instrument (%)
RND_INSTRU_PAUSE_MIN_SOLO = 5
RND_INSTRU_PAUSE_MAX_SOLO = 30
# max and min pause for bass instrument (%)
RND_INSTRU_PAUSE_MIN_BASS = 5
RND_INSTRU_PAUSE_MAX_BASS = 30
# add harmony and chorus instrument (0 = add none, 1 = add harmony only, 2 = add chorus only, 3 = add both)
RND_INSTRU_HARMONY_CHORUS = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 0]
# max and min pause for chorus instrument (%)
RND_INSTRU_PAUSE_MIN_CHORUS = 5
RND_INSTRU_PAUSE_MAX_CHORUS = 30
# max and min pause for harmony instrument (%)
RND_INSTRU_PAUSE_MIN_HARMONY = 5
RND_INSTRU_PAUSE_MAX_HARMONY = 30

# tone selection: Use only tones that are rated with at least x% of the rating of the best tone.
# 100 % => only the best tone will be used
# 0 % => all tones will be used (but still weighted with rating points)
RATING_THRESHOLD = 10  # %

# the average number of tones within a bar can be changed with this parameter
# a value of 0 (the lowest value possible) prefers fewer tones (on average over many pieces)
# higher values (1, 2, 3, ...) lead to more tones. Values greater than 6 lead to barely noticeable changes.
TONE_DENSITY = 2  # default 2

# average number of tones per second (averaged over 1 bar) in percent of max possible number of tones per second
# for a specific instrument (as defined in general_midi_instruments)
AVG_TONES_PER_SEC_PERCENT = 85  # default 85 %

# for all rhythms the average tone distance is calculated
# for solo instruments this value must not be greater than the current speed distance time this factor
# a higher value for MIN_SPEED_FACTOR allows slower solo parts even when high speeds are selected
MIN_SPEED_FACTOR = 2.5  # default 2

# when a track (instrument) is played only for specific part types (for example CR or CR_ENDING), this value gives the
# percentage of bars from that part type, which are randomly paused.
PERC_CR_BARS_PAUSES = 15  # %

# structure catalogs
# rules for STRUCT_TYPES. STRUCT_TYPES are used to subdivide parts, with the exception
# of the top level part (the whole piece), which is subdivided by STRUCT_TOP_TYPES
# rule 1: must include at least one repetition (excludes [CR, CR] for example)
# rule 2: must include at least two different parts (excludes [CR, 0] for example)
# rule 3: total number of identical parts at beginning and end of structure must be <= 2
#         (excludes [CR, CR, 0, 0] for example)
# rule 4: total number of CR at beginning and end of structure must be <= 2
#         (excludes [CR, CR, 0, CR] for example)
# rule 5: no more than 2 consecutive CR
# rule 6: no more than 2 consecutive identical parts

STRUCT_TYPES = [
    [CR, CR, 0],
    [CR, CR, 1],
    [CR, 0, CR],
    [CR, CR, 0, 1],
    [CR, CR, 1, 0],
    [CR, 0, CR, 2],
    [CR, CR, 0, CR, 0],
    [CR, CR, 0, CR, 1],
    [CR, CR, 0, CR, 3],
    [CR, CR, 0, 0, 1],
    [CR, CR, 0, 1, 0],
    [CR, CR, 0, 1, 1],
    [CR, CR, 1, CR, 0],
    [CR, CR, 1, CR, 1],
    [CR, CR, 1, CR, 3],
    [CR, CR, 1, 0, 1],
    [CR, 0, CR, CR, 2],
    [CR, 0, CR, CR, 3],
    [CR, 0, CR, 0, CR],
    [CR, 0, CR, 0, 2],
    [CR, 0, CR, 2, CR],
    ]
# possible STRUCT_TOP_TYPES are CR CR2 CRB and repetitions (intro and ending will be added automatically)
# rule 1: CR has to be used at least twice (possibly as repetition)
# rule 1: must include at least one repetition
STRUCT_TOP_TYPES = [
    [CR, CR2, 0],
    [CR, CR2, 0, 1],
    [CR, CR2, CRB, 0, 1],
    [CR, CR2, 0, CRB, 1, 0],
    [CR, CR2, 0, 1, CRB, 0, 1],
    ]
# STRUCT_TOP_SHORT_TYPES are used if no standard structure is usable because the piece is too short
STRUCT_TOP_SHORT_TYPES = [[CR], []]

# instruments distribution catalogs

INSTRU_DISTRIBUTION = [
    # bass
    [
        [[CR, CR2, CR_INTRO, CR_ENDING], [CRB]],
        [[CR_INTRO, CRB], [CR, CR2, CR_ENDING]],
        [[CR_INTRO], [CR, CR2, CR_ENDING]],
    ],
    # chorus
    [
        [[CR, CR_INTRO, CR_ENDING], [CR2, CRB]],
        [[CR_INTRO, CRB, CR2], [CR, CR_ENDING]],
    ],
    # solo
    [
        [[CR, CR_INTRO, CR_ENDING], [CR2, CR_ENDING]],
        [[CR_INTRO, CR2], [CR, CR_ENDING]],
        [[CR_INTRO, CR, CR2], [CR2, CR_ENDING]],
        [[CR_INTRO, CR, CR2], [CR, CR2, CR_ENDING]],
    ],
    # harmony
    [
        [[CR, CR2, CR_INTRO, CR_ENDING], [CRB]],
        [[CR_INTRO, CRB], [CR, CR2, CR_ENDING]],
        [[CR_INTRO], [CR, CR2, CR_ENDING]],
    ],
    ]


# range reduction of instruments, max %
# to avoid using the full range every time
RANGE_REDUCTION = 0.05  # default 0.05

# used to calculate the random envelope length in bars (one full turn)
# these are gauss parameters (mean, delta, min, max)
ENVELOPE_LENGTH = [40, 10, 30, 50]  # default [40, 10, 30, 50]
