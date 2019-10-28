# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file contains all pre_rhythm related functions and definitions

"""

from inkamusic.const import TICKSRES

from inkamusic.const import P_STICK, P_BASS, P_HIGH, P_LOW, P_RIDE, P_SNARE


# Position constants
# Every beat is subdivided in const.TICKSRES ticks, which is the smallest positioning unit.
# The first position in each rhythm pattern is 0. For example, a 4-beat pattern with one note
# exactly on each beat would use positionsBEAT_1, TICKSRES, 2 * TICKSRES and 3 * TICKSRES.
# Note that the actual speed is determined in combination with the beats per minute (bpm)
# setting defined for each piece.

BEAT_1 = 0
BEAT_2 = TICKSRES
BEAT_3 = 2 * TICKSRES
BEAT_4 = 3 * TICKSRES
HALF_BEAT = TICKSRES // 2
QUART_BEAT = TICKSRES // 4
EIGHTH_BEAT = TICKSRES // 8
THIRD_BEAT = TICKSRES // 3
SWING_BEAT = 2 * THIRD_BEAT
RHY_PATTERN_INDX = 1
RHY_STYLE_INDX = 0
BLOCK_ACC = 0


class BasicRhythm():
    """ BasicRhythm related functions and definitions
        Defines basic rhythm patterns
        A basic pattern consists in general of a length (in beats) and several sub patterns
        each associated with a specific sound type (for example Bass or Stick)
        Each sub pattern is defined by a list of positions and accent strength at that position
        An accent strength of 0 indicates a blocked position
        which will not be used in possible further subdivisions of a rhythm
    """

    def __init__(self):
        """ Defines catalog of basic rhythms
        """

        self.basic_rhythms_list = [

            # rhythm id 0, basic 4/4
            [4,
             [P_BASS, [[BEAT_1, 4], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 2], [BEAT_3, 2], [BEAT_4, 2], ],
              ],
             ],

            # rhythm id 1, basic 4/4 + 8th
            [4,
             [P_BASS, [[BEAT_1, 4], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3], [BEAT_3, 3], [BEAT_4, 3],
                        ],
              ],
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + HALF_BEAT, 1], [BEAT_2, 3], [BEAT_2 + HALF_BEAT, 1],
                       [BEAT_3, 3], [BEAT_3 + HALF_BEAT, 1], [BEAT_4, 3], [BEAT_4 + HALF_BEAT, 1],
                       ],
              ],
             ],

            # rhythm id 2, basic 4/4 + 8th + 16th
            [4,
             [P_BASS, [[BEAT_1, 4], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3], [BEAT_3, 3], [BEAT_4, 3],
                        ],
              ],
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + QUART_BEAT, 1], [BEAT_1 + HALF_BEAT, 2],
                       [BEAT_1 + HALF_BEAT + QUART_BEAT, 1],
                       [BEAT_2, 3], [BEAT_2 + QUART_BEAT, 1], [BEAT_2 + HALF_BEAT, 2],
                       [BEAT_2 + HALF_BEAT + QUART_BEAT, 1],
                       [BEAT_3, 3], [BEAT_3 + QUART_BEAT, 1], [BEAT_3 + HALF_BEAT, 2],
                       [BEAT_3 + HALF_BEAT + QUART_BEAT, 1],
                       [BEAT_4, 3], [BEAT_4 + QUART_BEAT, 1], [BEAT_4 + HALF_BEAT, 2],
                       [BEAT_4 + HALF_BEAT + QUART_BEAT, 1],
                       ],
              ],
             ],

            # rhythm id 3, basic 3/4
            [3,
             [P_BASS, [[BEAT_1, 4], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3], [BEAT_3, 3],
                        ],
              ],
             ],

            # rhythm id 4, basic 3/4 + 8th
            [3,
             [P_BASS, [[BEAT_1, 4], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3], [BEAT_3, 3],
                        ],
              ],
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + HALF_BEAT, 1], [BEAT_2, 3], [BEAT_2 + HALF_BEAT, 1],
                       [BEAT_3, 3], [BEAT_3 + HALF_BEAT, 1],
                       ],
              ],
             ],

            # rhythm id 5, basic 3/4 + 8th + 16th
            [3,
             [P_BASS, [[BEAT_1, 4], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3], [BEAT_3, 3],
                        ],
              ],
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + QUART_BEAT, 1], [BEAT_1 + HALF_BEAT, 2],
                       [BEAT_1 + HALF_BEAT + QUART_BEAT, 1],
                       [BEAT_2, 3], [BEAT_2 + QUART_BEAT, 1], [BEAT_2 + HALF_BEAT, 2],
                       [BEAT_2 + HALF_BEAT + QUART_BEAT, 1],
                       [BEAT_3, 3], [BEAT_3 + QUART_BEAT, 1], [BEAT_3 + HALF_BEAT, 2],
                       [BEAT_3 + HALF_BEAT + QUART_BEAT, 1],
                       ],
              ],
             ],

            # rhythm id 6, basic 2/4
            [2,
             [P_BASS, [[BEAT_1, 4], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3],
                        ],
              ],
             ],

            # rhythm id 7, basic 2/4 + 8th
            [2,
             [P_BASS, [[BEAT_1, 4], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3],
                        ],
              ],
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + HALF_BEAT, 1], [BEAT_2, 3], [BEAT_2 + HALF_BEAT, 1],
                       ],
              ],
             ],

            # rhythm id 8, basic 2/4 + 8th + 16th
            [2,
             [P_BASS, [[BEAT_1, 4], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3],
                        ],
              ],
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + QUART_BEAT, 1], [BEAT_1 + HALF_BEAT, 2],
                       [BEAT_1 + HALF_BEAT + QUART_BEAT, 1],
                       [BEAT_2, 3], [BEAT_2 + QUART_BEAT, 1], [BEAT_2 + HALF_BEAT, 2],
                       [BEAT_2 + HALF_BEAT + QUART_BEAT, 1],
                       ],
              ],
             ],

            # rhythm id 9, basic 4/4 triple (= 12/8)
            [4,
             [P_BASS, [[BEAT_1, 4], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3], [BEAT_3, 3], [BEAT_4, 3],
                        ],
              ],
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + THIRD_BEAT, 1], [BEAT_1 + SWING_BEAT, 1],
                       [BEAT_2, 3], [BEAT_2 + THIRD_BEAT, 1], [BEAT_2 + SWING_BEAT, 1],
                       [BEAT_3, 3], [BEAT_3 + THIRD_BEAT, 1], [BEAT_3 + SWING_BEAT, 1],
                       [BEAT_4, 3], [BEAT_4 + THIRD_BEAT, 1], [BEAT_4 + SWING_BEAT, 1],
                       ],
              ],
             ],

            # rhythm id 10, basic 3/4 triple (= 9/8)
            [3,
             [P_BASS, [[BEAT_1, 4], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3], [BEAT_3, 3],
                        ],
              ],
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + THIRD_BEAT, 1], [BEAT_1 + SWING_BEAT, 1],
                       [BEAT_2, 3], [BEAT_2 + THIRD_BEAT, 1], [BEAT_2 + SWING_BEAT, 1],
                       [BEAT_3, 3], [BEAT_3 + THIRD_BEAT, 1], [BEAT_3 + SWING_BEAT, 1],
                       ],
              ],
             ],

            # rhythm id 11, basic 2/4 triple (= 6/8)
            [2,
             [P_BASS, [[BEAT_1, 4], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3],
                        ],
              ],
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + THIRD_BEAT, 1], [BEAT_1 + SWING_BEAT, 1],
                       [BEAT_2, 3], [BEAT_2 + THIRD_BEAT, 1], [BEAT_2 + SWING_BEAT, 1],
                       ],
              ],
             ],

            # rhythm id 12, basic 4/4 swing
            [4,
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3], [BEAT_3, 3], [BEAT_4, 3],
                        ],
              ],
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + THIRD_BEAT, 0], [BEAT_1 + SWING_BEAT, 1],
                       [BEAT_2, 3], [BEAT_2 + THIRD_BEAT, 0], [BEAT_2 + SWING_BEAT, 1],
                       [BEAT_3, 3], [BEAT_3 + THIRD_BEAT, 0], [BEAT_3 + SWING_BEAT, 1],
                       [BEAT_4, 3], [BEAT_4 + THIRD_BEAT, 0], [BEAT_4 + SWING_BEAT, 1],
                       ],
              ],
             ],

            # rhythm id 13, basic 3/4 swing
            [3,
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3], [BEAT_3, 3],
                        ],
              ],
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + THIRD_BEAT, 0], [BEAT_1 + SWING_BEAT, 1],
                       [BEAT_2, 3], [BEAT_2 + THIRD_BEAT, 0], [BEAT_2 + SWING_BEAT, 1],
                       [BEAT_3, 3], [BEAT_3 + THIRD_BEAT, 0], [BEAT_3 + SWING_BEAT, 1],
                       ],
              ],
             ],

            # rhythm id 14, basic 2/4 swing
            [2,
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 3],
                        ],
              ],
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + THIRD_BEAT, 0], [BEAT_1 + SWING_BEAT, 1],
                       [BEAT_2, 3], [BEAT_2 + THIRD_BEAT, 0], [BEAT_2 + SWING_BEAT, 1],
                       ],
              ],
             ],

            # rhythm id 15 Mozambique
            [4,
             [P_RIDE, [[BEAT_1, 3], [BEAT_1 + HALF_BEAT, 2],
                       [BEAT_2, 2], [BEAT_2 + QUART_BEAT, 1], [BEAT_2 + HALF_BEAT + QUART_BEAT, 1],
                       [BEAT_3 + QUART_BEAT, 1], [BEAT_3 + HALF_BEAT, 1],
                       [BEAT_4, 2], [BEAT_4 + QUART_BEAT, 1], [BEAT_4 + HALF_BEAT + QUART_BEAT, 1],
                       ],
              ],
             [P_HIGH, [[BEAT_3 + HALF_BEAT + QUART_BEAT, 2], [BEAT_4 + HALF_BEAT, 2],
                       ],
              ],
             [P_SNARE, [[BEAT_2 + HALF_BEAT + QUART_BEAT, 2],
                        ],
              ],
             [P_BASS, [[BEAT_2, 2],
                       ],
              ],
             [P_STICK, [[BEAT_1, 3], [BEAT_2, 2], [BEAT_3, 2], [BEAT_4, 2],
                        ],
              ],
             ],

            # rhythm id 16 4/4 Rock
            [4,
             [P_SNARE, [[BEAT_2, 2], [BEAT_4, 2],
                        ],
              ],
             [P_BASS, [[BEAT_1, 3], [BEAT_3, 2],
                       ],
              ],
             [P_STICK, [[BEAT_1, 3], [BEAT_1 + HALF_BEAT, 1],
                        [BEAT_2, 2], [BEAT_2 + HALF_BEAT, 1],
                        [BEAT_3, 2], [BEAT_3 + HALF_BEAT, 1],
                        [BEAT_4, 2], [BEAT_4 + HALF_BEAT, 1],
                        ],
              ],
             ],

            # rhythm id 17 4/4 Jazz Ride
            [4,
             [P_RIDE, [[BEAT_1, 4], [BEAT_2, 3], [BEAT_2 + THIRD_BEAT, 0], [BEAT_2 + SWING_BEAT, 1],
                       [BEAT_3, 3], [BEAT_4, 3], [BEAT_4 + THIRD_BEAT, 0], [BEAT_4 + SWING_BEAT, 1], ],
              ],
             [P_STICK, [[BEAT_2, 3], [BEAT_4, 3], ],
              ],
             ],

            # rhythm id 18 Merengue
            [4,
             [P_BASS, [[BEAT_1, 3], [BEAT_2, 2], [BEAT_3, 2], [BEAT_4, 2],
                       ],
              ],
             [P_LOW, [[BEAT_1, 3],
                      [BEAT_4 + QUART_BEAT, 2], [BEAT_4 + HALF_BEAT, 2], [BEAT_4 + HALF_BEAT + QUART_BEAT, 2], ],
              ],
             [P_HIGH, [[BEAT_1, 3], [BEAT_2, 2], [BEAT_3, 2], [BEAT_4, 2], ],
              ],
             [P_STICK, [[BEAT_1 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_2, 2], [BEAT_2 + HALF_BEAT, 1], [BEAT_2 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_3, 2], [BEAT_3 + HALF_BEAT, 1], [BEAT_3 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_4, 2], ],
              ],
             ],

            # rhythm id 19 Reggae
            [4,
             [P_STICK, [[BEAT_1, 1], [BEAT_1 + THIRD_BEAT, 0], [SWING_BEAT, 1],
                        [BEAT_2, 2], [BEAT_2 + THIRD_BEAT, 0], [BEAT_2 + SWING_BEAT, 2],
                        [BEAT_3, 4], [BEAT_3 + THIRD_BEAT, 0], [BEAT_3 + SWING_BEAT, 1],
                        [BEAT_4, 2], [BEAT_4 + THIRD_BEAT, 0], [BEAT_4 + SWING_BEAT, 2], ],
              ],
             [P_BASS, [[BEAT_3, 4], ],
              ],
             ],

            # rhythm id 20 3/4 Viennese Waltz
            [3,
             [P_RIDE, [[BEAT_1, 3], [BEAT_2, 2], [BEAT_3, 2], ],
              ],
             [P_SNARE, [[SWING_BEAT, 1], [BEAT_3, 2], ],
              ],
             [P_BASS, [[BEAT_1, 3], ],
              ],
             [P_STICK, [[BEAT_3, 2], ],
              ],
             ],

            # rhythm id 21 Tango
            [4,
             [P_SNARE, [[BEAT_1, 3], [BEAT_2, 2], [BEAT_3, 2], [BEAT_4, 2],
                        [BEAT_4 + HALF_BEAT, 3], [BEAT_4 + HALF_BEAT + QUART_BEAT, 2], ],
              ],
             [P_BASS, [[BEAT_1, 3], [BEAT_2, 2], [BEAT_3, 2], [BEAT_4, 2], [BEAT_4 + HALF_BEAT, 3], ],
              ],
             [P_STICK, [[BEAT_1, 3], [BEAT_2, 2], [BEAT_3, 2], [BEAT_4, 2], ],
              ],
             ],

            # rhythm id 22 cha-cha
            [4,
             [P_RIDE, [[BEAT_1, 3], [BEAT_2, 2], [BEAT_3, 2], [BEAT_4, 2], ],
              ],
             [P_LOW, [[BEAT_4, 2], [BEAT_4 + HALF_BEAT, 2], ],
              ],
             [P_SNARE, [[BEAT_2, 2], ],
              ],
             [P_BASS, [[BEAT_2 + HALF_BEAT, 1], [BEAT_3, 2], ],
              ],
             [P_STICK, [[BEAT_1, 3], [BEAT_2, 2], [BEAT_3, 2], [BEAT_4, 2], ],
              ],
             ],

            # rhythm id 23 4/4 Calypso
            [4,
             [P_BASS, [[BEAT_1, 4], [BEAT_1 + HALF_BEAT + QUART_BEAT, 2],
                       [BEAT_3, 3], [BEAT_3 + HALF_BEAT + QUART_BEAT, 2], ],
              ],
             [P_RIDE, [[BEAT_1 + HALF_BEAT, 2],
                       [BEAT_2 + HALF_BEAT, 2],
                       [BEAT_3 + HALF_BEAT, 2],
                       [BEAT_4 + HALF_BEAT, 2], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_1 + QUART_BEAT, 1], [BEAT_1 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_2, 3], [BEAT_2 + QUART_BEAT, 1], [BEAT_2 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_3, 3], [BEAT_3 + QUART_BEAT, 1], [BEAT_3 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_4, 3], [BEAT_4 + QUART_BEAT, 1], [BEAT_4 + HALF_BEAT + QUART_BEAT, 1], ],
              ],
             ],

            # rhythm id 24 4/4 Hip Hop
            [4,
             [P_BASS, [[BEAT_1, 4], [BEAT_3 + HALF_BEAT, 3], ],
              ],
             [P_RIDE, [[BEAT_3 + HALF_BEAT, 3], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_1 + HALF_BEAT, 1], [BEAT_2, 2],
                        [BEAT_2 + HALF_BEAT, 1], [BEAT_3, 2], [BEAT_4, 2], [BEAT_4 + HALF_BEAT, 1], ],
              ],
             [P_SNARE, [[BEAT_2, 2], [BEAT_3 + QUART_BEAT, 1], [BEAT_4, 2], ],
              ],
             ],

            # rhythm id 25 4/4 Hip Hop fast
            [4,
             [P_BASS, [[BEAT_1, 4], [BEAT_2 + HALF_BEAT + QUART_BEAT, 1], [BEAT_3, 2], [BEAT_3 + HALF_BEAT, 2], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_1 + QUART_BEAT, 1], [BEAT_1 + HALF_BEAT, 1],
                        [BEAT_1 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_2, 3], [BEAT_2 + QUART_BEAT, 1], [BEAT_2 + HALF_BEAT, 1],
                        [BEAT_2 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_3, 2], [BEAT_3 + QUART_BEAT, 1], [BEAT_3 + HALF_BEAT, 1],
                        [BEAT_3 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_4, 3], [BEAT_4 + QUART_BEAT, 2], [BEAT_4 + QUART_BEAT + EIGHTH_BEAT, 2],
                        [BEAT_4 + HALF_BEAT, 3], [BEAT_4 + HALF_BEAT + EIGHTH_BEAT, 2],
                        [BEAT_4 + HALF_BEAT + QUART_BEAT, 2],
                        [BEAT_4 + HALF_BEAT + QUART_BEAT + EIGHTH_BEAT, 2], ],
              ],
             [P_SNARE, [[BEAT_2, 3], [BEAT_4, 3], ],
              ],
             ],

            # rhythm id 26 4/4 Techno
            [4,
             [P_BASS, [[BEAT_1, 4], [BEAT_2, 3], [BEAT_3, 3], [BEAT_4, 3], ],
              ],
             [P_STICK, [[BEAT_1 + HALF_BEAT, 2], [BEAT_2 + HALF_BEAT, 2],
                        [BEAT_3 + HALF_BEAT, 2], [BEAT_4 + HALF_BEAT, 2], ],
              ],
             [P_SNARE, [[BEAT_2, 3], [BEAT_4, 3], ],
              ],
             ],

            # rhythm id 27 4/4 House
            [4,
             [P_BASS, [[BEAT_1, 4], [BEAT_2, 3], [BEAT_3, 3], [BEAT_4, 3], ],
              ],
             [P_SNARE, [[BEAT_1 + HALF_BEAT, 2], [BEAT_2 + HALF_BEAT, 2], [BEAT_3 + HALF_BEAT, 2],
                        [BEAT_3 + HALF_BEAT + QUART_BEAT, 2], [BEAT_4 + HALF_BEAT, 2], ],
              ],
             [P_STICK, [[BEAT_1 + QUART_BEAT, 1], [BEAT_1 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_2 + QUART_BEAT, 1], [BEAT_2 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_3 + QUART_BEAT, 1], [BEAT_3 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_4 + QUART_BEAT, 1], [BEAT_4 + HALF_BEAT + QUART_BEAT, 1], ],
              ],
             ],

            # rhythm id 28  4/4 Syrto
            [4,
             [P_BASS, [[BEAT_1, 4], [BEAT_2 + HALF_BEAT, 3], [BEAT_3, 3], [BEAT_4 + HALF_BEAT, 3], ],
              ],
             [P_SNARE, [[BEAT_1 + HALF_BEAT + QUART_BEAT, 2], [BEAT_2 + HALF_BEAT, 2],
                        [BEAT_3 + HALF_BEAT + QUART_BEAT, 2], [BEAT_4 + HALF_BEAT, 2], ],
              ],
             [P_RIDE, [[BEAT_1, 2], [BEAT_1 + HALF_BEAT + QUART_BEAT, 1], [BEAT_2 + HALF_BEAT, 1],
                       [BEAT_3, 1], [BEAT_3 + HALF_BEAT + QUART_BEAT, 1], [BEAT_4, 1], [BEAT_4 + HALF_BEAT, 1], ],
              ],
             [P_STICK, [[BEAT_1 + HALF_BEAT + QUART_BEAT, 1], [BEAT_3 + HALF_BEAT + QUART_BEAT, 1], ],

              ],
             ],

            # rhythm id 29 Guaguanco
            [4,
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + HALF_BEAT, 3], [BEAT_1 + HALF_BEAT + QUART_BEAT, 2],
                       [BEAT_2 + QUART_BEAT, 2], [BEAT_2 + HALF_BEAT + QUART_BEAT, 2],
                       [BEAT_3, 3], [BEAT_3 + HALF_BEAT, 2],
                       [BEAT_4, 3], [BEAT_4 + QUART_BEAT, 2], [BEAT_4 + HALF_BEAT + QUART_BEAT, 2], ],
              ],
             [P_LOW, [[BEAT_2 + HALF_BEAT, 3], [BEAT_4 + HALF_BEAT, 3], ],
              ],
             [P_HIGH, [[BEAT_3, 3], [BEAT_3 + HALF_BEAT + QUART_BEAT, 2], ],
              ],
             [P_BASS, [[BEAT_1 + HALF_BEAT + QUART_BEAT, 3], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 2], [BEAT_3, 3], [BEAT_4, 2], ],
              ],
             ],

            # rhythm id 30 2/4 Polka
            [2,
             [P_STICK, [[BEAT_1, 4], [BEAT_1 + HALF_BEAT, 3], [BEAT_2, 2], [BEAT_2 + HALF_BEAT, 3], ],
              ],
             [P_BASS, [[BEAT_1, 4], [BEAT_2, 2], ],
              ],
             [P_SNARE, [[BEAT_1 + HALF_BEAT, 3], [BEAT_2 + HALF_BEAT, 3], ],
              ],
             ],

            # rhythm id 31  4/4 Blues shuffle
            [4,
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + THIRD_BEAT, BLOCK_ACC], [SWING_BEAT, 1],
                       [BEAT_2, 3], [BEAT_2 + THIRD_BEAT, BLOCK_ACC], [BEAT_2 + SWING_BEAT, 1],
                       [BEAT_3, 3], [BEAT_3 + THIRD_BEAT, BLOCK_ACC], [BEAT_3 + SWING_BEAT, 1],
                       [BEAT_4, 3], [BEAT_4 + THIRD_BEAT, BLOCK_ACC], [BEAT_4 + SWING_BEAT, 1], ],
              ],

             [P_SNARE, [[BEAT_2, 3], [BEAT_4, 3], ],
              ],
             [P_BASS, [[BEAT_1, 4], [BEAT_3, 3], ],
              ],
             ],

            # rhythm id 32 Mambo
            [4,
             [P_RIDE, [[BEAT_1, 4], [BEAT_1 + HALF_BEAT, 3],
                       [BEAT_2, 2], [BEAT_2 + QUART_BEAT, 2], [BEAT_2 + HALF_BEAT, 3],
                       [BEAT_2 + HALF_BEAT + QUART_BEAT, 3],
                       [BEAT_3 + QUART_BEAT, 2], [BEAT_3 + HALF_BEAT, 2], [BEAT_3 + HALF_BEAT + QUART_BEAT, 3],
                       [BEAT_4, 3], [BEAT_4 + HALF_BEAT, 2], [BEAT_4 + HALF_BEAT + QUART_BEAT, 2], ],
              ],
             [P_SNARE, [[BEAT_1 + HALF_BEAT, 3], ],
              ],
             [P_HIGH, [[BEAT_2 + HALF_BEAT, 3], [BEAT_2 + HALF_BEAT + QUART_BEAT, 3],
                       [BEAT_3 + HALF_BEAT + QUART_BEAT, 3],
                       [BEAT_4, 3], [BEAT_4 + HALF_BEAT, 2], [BEAT_4 + HALF_BEAT + QUART_BEAT, 2], ],
              ],
             [P_BASS, [[BEAT_1 + HALF_BEAT + QUART_BEAT, 2], [BEAT_3 + HALF_BEAT + QUART_BEAT, 3],
                       [BEAT_4 + HALF_BEAT, 2], ],
              ],
             [P_STICK, [[BEAT_1, 4], [BEAT_2, 2], [BEAT_3, 2], [BEAT_4, 3], ],
              ],
             ],

            # rhythm id 33 3/4 Waltz
            [3,
             [P_RIDE, [[BEAT_1, 3], [BEAT_2, 2], [BEAT_3, 2], ],
              ],
             [P_SNARE, [[BEAT_2, 2], [BEAT_3, 2], ],
              ],
             [P_BASS, [[BEAT_1, 3], ],
              ],
             [P_STICK, [[BEAT_2, 2], [BEAT_3, 2], ],
              ],
             ],

            # rhythm id 34 4/4 Train beat
            [4,
             [P_STICK, [[BEAT_1 + HALF_BEAT, 3],
                        [BEAT_2 + HALF_BEAT, 3],
                        [BEAT_3 + HALF_BEAT, 3],
                        [BEAT_4 + HALF_BEAT, 3], ],
              ],
             [P_SNARE, [[BEAT_1, 4], [BEAT_1 + QUART_BEAT, 2],
                        [BEAT_1 + HALF_BEAT, 3], [BEAT_1 + HALF_BEAT + QUART_BEAT, 2],
                        [BEAT_2, 3], [BEAT_2 + QUART_BEAT, 2], [BEAT_2 + HALF_BEAT, 3],
                        [BEAT_2 + HALF_BEAT + QUART_BEAT, 2],
                        [BEAT_3, 3], [BEAT_3 + QUART_BEAT, 3], [BEAT_3 + HALF_BEAT, 3],
                        [BEAT_3 + HALF_BEAT + QUART_BEAT, 2],
                        [BEAT_4, 3], [BEAT_4 + QUART_BEAT, 2], [BEAT_4 + HALF_BEAT, 3],
                        [BEAT_4 + HALF_BEAT + QUART_BEAT, 2], ],
              ],
             [P_BASS, [[BEAT_1, 4],
                       [BEAT_2, 3],
                       [BEAT_3, 3],
                       [BEAT_4, 3], ],

              ],
             ],

            # rhythm id 35  4/4 Soca
            [4,
             [P_STICK, [[BEAT_1, 4], [BEAT_1 + HALF_BEAT, 1],
                        [BEAT_2, 2], [BEAT_2 + HALF_BEAT, 3],
                        [BEAT_3, 2], [BEAT_3 + HALF_BEAT, 1],
                        [BEAT_4, 2], [BEAT_4 + HALF_BEAT, 3], ],
              ],
             [P_SNARE, [[BEAT_1 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_2 + HALF_BEAT, 3],
                        [BEAT_3 + HALF_BEAT + QUART_BEAT, 1],
                        [BEAT_4 + HALF_BEAT, 3], ],
              ],
             [P_BASS, [[BEAT_1, 4],
                       [BEAT_2, 2],
                       [BEAT_3, 2],
                       [BEAT_4, 2], ],
              ],
             ],
            ]  # self.basic_rhythms_list

    def get_basic_rhythms_list(self):
        """ returns list of all basic rhythms"""
        return self.basic_rhythms_list

    def get_basic_rhythm_by_id(self, r_id):
        """returns basic rhythm for given id"""
        assert 0 <= r_id < len(self.basic_rhythms_list), "rhythm ID out of range!"
        return self.basic_rhythms_list[r_id]
