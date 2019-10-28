# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file contains all menu entries used in the web interface or, for now, as parameters to the webutilities
generate function
"""

from inkamusic.const import TICKSRES
from inkamusic.const import NOTE_C, NOTE_CIS, NOTE_D, NOTE_DIS  # noqa: F401 # pylint: disable=unused-import
from inkamusic.const import NOTE_E, NOTE_F, NOTE_FIS  # noqa: F401 # pylint: disable=unused-import
from inkamusic.const import NOTE_G, NOTE_GIS, NOTE_A, NOTE_BFLAT, NOTE_B  # noqa: F401 # pylint: disable=unused-import
from inkamusic.const import HARMONY_PREFER_MAJOR_VAR, HARMONY_PREFER_MINOR_VAR, HARMONY_ANY, HARMONY_AVOID_MAJMIN
from inkamusic.const import HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR
from inkamusic.const import T_SOLO, T_CHOR, T_HMNY, T_BASS, R_HIGH  # noqa: F401 # pylint: disable=unused-import
from inkamusic.const import R_MEDI, R_LOW, R_BASS, R_FULL  # noqa: F401 # pylint: disable=unused-import

INSTRUMENTATION_LIST = [
    ['Piano + Bass',
     [
         ['Grand Piano', T_SOLO, R_MEDI],
         ['Grand Piano', T_SOLO, R_HIGH],
         ['Grand Piano', T_CHOR, R_MEDI],
         ['Grand Piano', T_HMNY, R_MEDI],
         ['Fingered Bass', T_BASS, R_BASS],
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
    ['Marimba + Bass',
     [
         ['Marimba', T_SOLO, R_MEDI],
         ['Marimba', T_SOLO, R_HIGH],
         ['Marimba', T_CHOR, R_MEDI],
         ['Nylon String Guitar', T_HMNY, R_MEDI],
         ['Fingered Bass', T_BASS, R_BASS],
      ],
     ],
    ['Sax + Bass',
     [
         ['Tenor Sax', T_SOLO, R_MEDI],
         ['Tenor Sax', T_SOLO, R_FULL],
         ['Bright Grand Piano', T_CHOR, R_MEDI],
         ['Nylon String Guitar', T_HMNY, R_MEDI],
         ['Fingered Bass', T_BASS, R_BASS],
      ],
     ],
    [],  # separator line
    ['Synth 1',
     [
         ['Saw Wave', T_SOLO, R_MEDI],
         ['Warm Pad', T_SOLO, R_HIGH],
         ['Synth Strings 2', T_HMNY, R_MEDI],
         ['Synth Bass 2', T_BASS, R_BASS],
      ],
     ],
    ['Synth 2',
     [
         ['Synth Brass 2', T_SOLO, R_MEDI],
         ['Square Lead', T_SOLO, R_HIGH],
         ['5th Sawtooth Wave', T_CHOR, R_MEDI],
         ['Polysynth', T_CHOR, R_MEDI],
         ['Synth Bass 3', T_BASS, R_BASS],
      ],
     ],
    [],  # separator line
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
    [],  # separator line
    ['Random instrumentation', [[0]]],

    #     ['Electric Guitars + Bass', [[206, 25], [205, 12], [774, 12],  [261, 25]]],
    #     [],  # separator line
    #     ['Sine', [[698, 40], [697, 40], [695, 40], [702, 40]]],
    #     ['Polysynth', [[563, 40], [560, 40], [561, 40]]],

    ]

"""an instrumentation list entry defines the specific instruments, their register and role in an instrumentation

possible roles are

- T_BASS bass instrument
- T_CHOR chorus instrument
- T_SOLO solo instrument
- T_HMNY harmony instrument (generates chords)
- T_PERC percussion instrument

possible registers are

- R_BASS bass
- R_LOW low
- R_MEDI medium
- R_HIGH high
- R_FULL full instrument range

"""

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


SCALES_LIST = [
    ['C (maj)', [7, 65, 0, NOTE_C, [HARMONY_PREFER_MAJOR]]],
    ['C (maj+maj7)', [7, 65, 0, NOTE_C, [HARMONY_PREFER_MAJOR, 43]]],
    ['C (maj+min)', [7, 65, 0, NOTE_C, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    ['F (maj+min)', [7, 65, 0, NOTE_F, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    ['A (maj+min)', [7, 65, 0, NOTE_A, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    [],  # separator line
    ['A harmonic (min maj)', [7, 55, 4, NOTE_A, [HARMONY_PREFER_MINOR, HARMONY_PREFER_MAJOR]]],
    ['A natural (min maj)', [7, 65, 9, NOTE_A, [HARMONY_PREFER_MINOR, HARMONY_PREFER_MAJOR]]],
    ['A melodic (min maj)', [7, 64, 9, NOTE_A, [HARMONY_PREFER_MINOR, HARMONY_PREFER_MAJOR_VAR, HARMONY_ANY]]],
    ['A (min min7)', [7, 65, 9, NOTE_A, [HARMONY_PREFER_MINOR, 48]]],
    [],  # separator line
    ['C (minor blues)', [6, 63, 5, NOTE_C, [HARMONY_PREFER_MINOR_VAR, HARMONY_PREFER_MAJOR_VAR, HARMONY_ANY]]],
    [],  # separator line
    ['C (minor Pentatonic)', [5, 58, 5, NOTE_C, [HARMONY_PREFER_MINOR, HARMONY_PREFER_MAJOR]]],
    ['C (major Pentatonic)', [5, 58, 8, NOTE_C, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    ['Japanese Pentatonic', [5, 38, 11, NOTE_C, [HARMONY_PREFER_MAJOR_VAR, HARMONY_PREFER_MINOR_VAR, HARMONY_ANY]]],
    ['Chinese Pentatonic', [5, 43, 0, NOTE_C, [HARMONY_AVOID_MAJMIN, HARMONY_PREFER_MAJOR_VAR]]],
    ['Byzantine', [7, 54, 11, NOTE_C, [HARMONY_PREFER_MINOR_VAR, HARMONY_ANY, HARMONY_ANY]]],
    [],  # separator line
    ['6 tone (maj)', [6, 70, 3, NOTE_C, [HARMONY_PREFER_MAJOR]]],
    ['6 tone (maj min)', [6, 70, 3, NOTE_C, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    ['5 tone (maj min)', [5, 51, 0, NOTE_C, [HARMONY_PREFER_MAJOR, HARMONY_PREFER_MINOR]]],
    ['5 tone (min maj)', [5, 32, 4, NOTE_C, [HARMONY_PREFER_MINOR, HARMONY_PREFER_MAJOR]]],
    [],  # separator line
    ['Chromatic', [12, 0, 0, NOTE_A, [HARMONY_PREFER_MINOR, HARMONY_PREFER_MAJOR]]],
]
""" a scale is defined by:

- title,
- number of tones,
- index of basic_scale as defined in basic_scales
  (example: the same basic_scale (7, 65) is used for c major, c minor, d major, ...)
- index of first tone (0 - 11) within basic_scale, this defines the start position within the scale
  (example: if this is set to 0 for scale (7, 65) a major scale is fixed, so c major and d major are still possible,
  but not c minor)
- interpretation ( = absolute height) of first tone, i.e. c, cis, d, dis, ...
  (if set to c in the example above the scale is now fixed as c major)
- 1, 2, or 3 harmony IDs as defined in harmonies,
  first ID defines main harmony, 2nd and 3rd (if defined) are used less often
- the first harmony must be buildable with the first tone as starting point
  for example, if c-major is defined as described above, the first harmony can not
  be minor (which is not buildable over c)

"""


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
    ['Reggae', 19, 100, 150],
    ['Viennese Waltz', 20, 140, 200],
    ['Tango', 21, 110, 136],
    ['Cha cha', 22, 95, 125],
    ['Calypso', 23, 80, 125],
    ['Hip Hop', 24, 60, 110],
    ['Fast Hip Hop', 25, 70, 86],
    ['Techno', 26, 100, 190],
    ['House', 27, 100, 190],
    ['Syrto', 28, 100, 160],
    ['Guaguanco', 29, 90, 110],
    ['Polka', 30, 90, 140],
    ['Blues Shuffle', 31, 80, 160],
    ['Mambo', 32, 85, 115],
    ['Waltz', 33, 75, 120],
    ['Train Beat', 34, 80, 160],

]

SPEED_LIST = [
    # speed restricts possible bpm (beats per minute) depending on selected rhythm
    # and restricts also possible subdivisions
    # example: TICKRES (a quarter note) // 2 defines the smallest possible distance of two notes to be an eighth
    # example: TICKRES (a quarter note) // 8 defines the smallest possible distance of two notes to be an 32th
    ['lower speed', 0, TICKSRES // 2],
    ['normal speed', 1, TICKSRES // 3],
    ['higher speed', 2, TICKSRES // 6],
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
