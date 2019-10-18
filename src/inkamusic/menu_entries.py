# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file contains all menu entries
"""

from inkamusic.const import TICKSRES
from inkamusic.const import NOTE_C, NOTE_CIS, NOTE_D, NOTE_DIS, NOTE_E, NOTE_F  # pylint: disable=unused-import
from inkamusic.const import NOTE_FIS, NOTE_G, NOTE_GIS, NOTE_A, NOTE_BFLAT, NOTE_B  # pylint: disable=unused-import
from inkamusic.const import HARMONY_PREFER_MAJOR_VAR, HARMONY_PREFER_MINOR_VAR, HARMONY_ANY, HARMONY_AVOID_MAJMIN
from inkamusic.const import HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR
from inkamusic.const import T_SOLO, T_CHOR, T_HMNY, T_BASS, R_HIGH, R_MEDI, R_LOW, R_BASS, R_FULL  # pylint: disable=unused-import


INSTRUMENTATION_LIST = [
    ['Random instrumentation', [[0]]],
    ['Random bass only', [[1]]],
    ['Random harmony instrument only', [[2]]],
    ['Random solo instrument only', [[3]]],
    ['Random double solo', [[4]]],
    [],  # separator line

    ['Piano + Bass',
     [
         ['Grand Piano', T_SOLO, R_MEDI],
         ['Grand Piano', T_SOLO, R_HIGH],
         ['Grand Piano', T_CHOR, R_MEDI],
         ['Grand Piano', T_HMNY, R_MEDI],
         ['Fingered Bass', T_BASS, R_BASS],
         ],
     ],
    ['Marimba + Bass',
     [
         ['Marimba', T_SOLO, R_MEDI],
         ['Marimba', T_SOLO, R_HIGH],
         ['Marimba', T_CHOR, R_MEDI],
         ['Nylon String Guitar', T_HMNY, R_MEDI],
         ['Fingered Bass', T_BASS, R_BASS],
      ],
     ],
    ['Strings',
     [
         ['Strings', T_SOLO, R_MEDI],
         ['Strings', T_SOLO, R_MEDI],
         ['Strings', T_CHOR, R_MEDI],
         ['Strings', T_CHOR, R_MEDI],
         ['Contrabass', T_BASS, R_BASS],
      ],
     ],

    ['Brass',
     [
         ['Trumpet', T_SOLO, R_FULL],
         ['Trumpet', T_SOLO, R_MEDI],
         ['Trumpet', T_HMNY, R_MEDI],
         ['Tuba', T_BASS, R_BASS],
      ],
     ],

    ['Classical Guitars + Bass',
     [
         ['Nylon String Guitar', T_SOLO, R_MEDI],
         ['Nylon String Guitar', T_SOLO, R_FULL],
         ['Nylon String Guitar', T_CHOR, R_MEDI],
         ['Nylon String Guitar', T_HMNY, R_MEDI],
         ['Acoustic Bass', T_BASS, R_BASS],
      ],
     ],
    #     ['Electric Guitars + Bass', [[206, 25], [205, 12], [774, 12],  [261, 25]]],
    #     [],  # separator line
    #     ['Sine', [[698, 40], [697, 40], [695, 40], [702, 40]]],
    #     ['Polysynth', [[563, 40], [560, 40], [561, 40]]],

    ]

LENGTH_MIN = [
    ['0 min', 0],
    ['1 min', 1],
    ['2 min', 2],
    ['3 min', 3],
    ['4 min', 4],
    ['5 min', 5],
    ['6 min', 6],
    ['7 min', 7],
    ['8 min', 8],
    ]

LENGTH_SEC = [
    ['0 s', 0],
    ['5 s', 5],
    ['10 s', 10],
    ['15 s', 15],
    ['20 s', 20],
    ['25 s', 25],
    ['30 s', 30],
    ['35 s', 35],
    ['40 s', 40],
    ['45 s', 45],
    ['50 s', 50],
    ['55 s', 55],
    ]

""" a scale is defined by:

     - title,
     - number of tones,
     - index of basic_scale as defined in basic_scales
       (example: the same basic_scale (7, 65) is used for c major, c minor, d major, ...)
     - index of first tone (0 - 11) within basic_scale, this defines the start position within the scale
       (example: if this is set to 0 for scale (7, 65) a major scale is fixed, so c major and d major are still
                 possible, but not c minor)
     - interpretation ( = absolute height) of first tone, i.e. c, cis, d, dis, ...
       (if set to c in the example above the scale is now fixed as c major)
     - 1, 2, or 3 harmony IDs as defined in harmonies,
       first ID defines main harmony, 2nd and 3rd (if defined) are used less often
     - the first harmony must be buildable with the first tone as starting point
       for example, if c-major is defined as described above, the first harmony can not
       be minor (which is not buildable over c)
    """
SCALES_LIST = [
    ['C maj', [7, 65, 0, NOTE_C, [HARMONY_PREFER_MAJOR]]],
    ['C maj maj7', [7, 65, 0, NOTE_C, [HARMONY_PREFER_MAJOR, 43]]],
    ['C maj min', [7, 65, 0, NOTE_C, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    ['D maj min', [7, 65, 0, NOTE_D, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    ['F maj min', [7, 65, 0, NOTE_F, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    ['G maj min', [7, 65, 0, NOTE_G, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    ['A maj min', [7, 65, 0, NOTE_A, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    [],  # separator line
    ['A min maj (harmonic)', [7, 55, 4, NOTE_A, [HARMONY_PREFER_MINOR, HARMONY_PREFER_MAJOR]]],
    ['A min maj (natural)', [7, 65, 9, NOTE_A, [HARMONY_PREFER_MINOR, HARMONY_PREFER_MAJOR]]],
    ['A min maj (melodic)', [7, 64, 9, NOTE_A, [HARMONY_PREFER_MINOR, HARMONY_PREFER_MAJOR_VAR, HARMONY_ANY]]],
    ['A min min7', [7, 65, 9, NOTE_A, [HARMONY_PREFER_MINOR, 48]]],
    [],  # separator line
    ['C-minor blues', [6, 63, 5, NOTE_C, [HARMONY_PREFER_MINOR_VAR, HARMONY_PREFER_MAJOR_VAR, HARMONY_ANY]]],
    [],  # separator line
    ['C-min Pentatonic', [5, 58, 5, NOTE_C, [HARMONY_PREFER_MINOR, HARMONY_PREFER_MAJOR]]],
    ['C-maj Pentatonic', [5, 58, 8, NOTE_C, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    ['Japanese Pentatonic', [5, 38, 11, NOTE_C, [HARMONY_PREFER_MAJOR_VAR, HARMONY_PREFER_MINOR_VAR, HARMONY_ANY]]],
    ['Chinese Pentatonic', [5, 43, 0, NOTE_C, [HARMONY_AVOID_MAJMIN, HARMONY_PREFER_MAJOR_VAR]]],
    ['Byzantine', [7, 54, 11, NOTE_C, [HARMONY_PREFER_MINOR_VAR, HARMONY_ANY, HARMONY_ANY]]],
    [],  # separator line
    ['6 tone maj', [6, 70, 3, NOTE_C, [HARMONY_PREFER_MAJOR]]],
    ['6 tone maj min', [6, 70, 3, NOTE_C, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    ['5 tone maj min', [5, 51, 0, NOTE_C, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    ['5 tone min maj', [5, 32, 4, NOTE_C, [HARMONY_PREFER_MINOR, HARMONY_PREFER_MAJOR]]],
    [],  # separator line
    ['Chromatic', [12, 0, 0, NOTE_A, [HARMONY_PREFER_MINOR, HARMONY_PREFER_MAJOR]]],
]

PERCUSSION_LIST = [
    # add or don't add percussion to melody instruments
    ['Add percussion', True],
    ["Don't add percussion", False],
]

RHYTHM_LIST = [
    # rhythm details are defined in basic_rhythms
    # id is index in list of all basic rhythms
    ['4/4 variation', 0, 60, 160],
    ['4/4 + 8th', 1, 60, 160],
    ['4/4 + 8th +16th', 2, 60, 160],
    ['4/4 + triplets', 9, 60, 160],
    ['4/4 swing', 12, 60, 160],
    [],  # separator line
    ['3/4 variation', 3, 60, 160],
    ['3/4 + 8th', 4, 60, 160],
    ['3/4 + 8th +16th', 5, 60, 160],
    ['3/4 + triplets', 10, 60, 160],
    ['3/4 swing', 13, 60, 160],
    [],  # separator line
    ['2/4 variation', 6, 60, 160],
    ['2/4 + 8th', 7, 60, 160],
    ['2/4 + 8th +16th', 8, 60, 160],
    ['2/4 + triplets', 11, 60, 160],
    ['2/4 swing', 14, 60, 160],
    [],  # separator line
    ['Mozambique', 15, 90, 130],
    ['Rock', 16, 80, 150],
    ['Jazz Ride', 17, 80, 180],
    ['Merengue', 18, 100, 140],
    ['Soca', 35, 102, 138],
    ['Reggae', 19, 60, 160],#bpm from here
    ['Viennese Waltz', 20, 60, 160],
    ['Tango', 21, 60, 160],
    ['Cha cha', 22, 60, 160],
    ['Calypso', 23, 60, 160],
    ['Hip Hop', 24, 60, 160],
    ['Fast Hip Hop', 25, 60, 160],
    ['Techno', 26, 60, 160],
    ['House', 27, 60, 160],
    ['Syrto', 28, 60, 160],
    ['Guaguanco', 29, 60, 160],
    ['Polka', 30, 60, 160],
    ['Blues Shuffle', 31, 60, 160],
    ['Mambo', 32, 60, 160],
    ['Waltz', 33, 60, 160],
    ['Train Beat', 34, 60, 160],

]

SPEED_LIST = [
    # speed restricts possible bpm (beats per minute)
    # value (lower and upper limit)
    # and restricts also possible subdivisions
    # example: TICKRES (a quarter note) // 2 defines the smallest possible distance of to notes to be an eighth
    # example: TICKRES (a quarter note) // 8 defines the smallest possible distance of to notes to be an 32th
    #['very low speed', [45, 60], TICKSRES // 1],
    ['lower speed', 0, TICKSRES // 2],
    ['normal speed', 1, TICKSRES // 3],
    ['higher speed', 2, TICKSRES // 6],
    #['very high speed', [150, 165], TICKSRES // 8],
]

SMALLEST_PART_LENGTH_OPTIONS = [1, 2, 3, 4, 5]
INTRO_LENGTH_OPTIONS = [1, 2, 4, 6, 8, 10, 12, 16]
ENDING_LENGTH_OPTIONS = [2, 4, 6, 8, 10, 12, 16]
BRIDGE_LENGTH_OPTIONS = [10, 11, 12, 13, 14]  # this is NOT the number of bars but a divisor

# probability for legato, standard, staccato
# each track will be assigned one of these tuples
# instruments which can not play continuous sounds (for example piano, guitar, percussion)
# always use the first entry [100, 0, 0]

RHYTHM_CONNECT_PROBABILITIES = [
    [100, 0, 0],
    [80, 20, 0],
    [60, 40, 0],
    [50, 50, 0],
    [40, 60, 0],
    [20, 80, 0],
    [0, 100, 0],
    [80, 0, 20],
    [70, 10, 20],
    [50, 30, 20],
    [40, 40, 20],
    [30, 50, 20],
    [10, 70, 20],
    [0, 80, 20],
    ]
