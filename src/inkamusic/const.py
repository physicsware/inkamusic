# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2019  Udo Wollschläger

This file contains all global constants

"""


# set tu True for output of structural information of a piece
DEBUG_OUTPUT = False

# directories

STAT_DIR = 'public'  # public = static dir of cherrypy web server
MID_DIR = STAT_DIR+'/midi/'  # midi file sub directory
LOG_DIR = STAT_DIR+'/logs/'  # cherrypy error log sub directory

HTTP_PORT = 8080
HTTPS_PORT = 0  # 8443, 0 disables https support
HTTPS_KEY_FILE = 'privkey001.key'
HTTPS_INTERMEDIATE_FILE = 'intermedi.cer'
HTTPS_CERTIFICATE_FILE = 'inkaalgo.cer'

TICKSRES = 720  # MIDI resolution

# random classes
NUM_RNDM_CLASSES = 11

# max seed value allowed (used for seed and instrumentation ID)
MAX_SEED = 99999999

RNDM_INSTRU = 0
RNDM_SCALE = 1
RNDM_HARMO = 2
RNDM_MELO_RHYTHM = 3
RNDM_STRUCTURE = 4
RNDM_BASE_RHYTHM = 5
RNDM_SOLO_RHYTHM = 6
RNDM_PERC_RHYTHM = 7
RNDM_INSTRU_RHYTHM = 8
RNDM_HARMO_DISTRI = 9
RNDM_OTHER = 10

# composition structure constants
SUB_INDX = 2
PROP_INDX = 1
LEN_INDX = 0
NO_LEVEL = -1
NO_REPEAT = -1

# bar statistics constants
BAR_GROUP = 1  # this record type indicates the start of a group of bars
BAR_INFO = 7  # this record type is used for individual bars of a group
BAR_REPEATED = 2
BAR_NOT_REPEATED = 1

CR = -5  # indicates a part which is created (composed)
CR2 = -6  # indicates an alternative part which is created (composed)
CR_INTRO = -2
CR_ENDING = -3
CRB = -4  # indicates a bridge part which is created (composed)

NUM_OF_STRUCT_PROPERTIES = 7
PROP_USEPART = 0
PROP_INTRO_BRIDGE_END = 1
PROP_FROM_BAR = 2
PROP_TO_BAR = 3
PROP_ACTUAL_BAR = 4
PROP_START = 5
PROP_END = 6

# instrument usage type (role)
T_BASS = 0
T_CHOR = 1
T_SOLO = 2
T_HMNY = 3
T_PERC = 4

MELODY_INSTRUMENT = 0
PERCUSSION_INSTRUMENT = 1

# instrument register
R_BASS = 0
R_LOW = 1
R_MEDI = 2
R_HIGH = 3
R_FULL = 4

# percussion styles
P_STICK = 0
P_ACCENT = 1
P_BASS = 2
P_HIGH = 3
P_LOW = 4
P_RIDE = 5
P_SNARE = 6

# specific array indices
NUM_OF_BEATS_INDX = 0
INSTRUMENT_ID_INDX = 1
INSTRUMENT_MIDI_INDX = 2
INSTRUMENT_TXT_INDX = 0
INSTRUMENT_TYPE_INDX = 3
INSTRUMENT_TYPE_2_INDX = 4
INSTRUMENT_SPEED_INDX = 5
INSTRUMENT_LOW_INDX = 6
INSTRUMENT_HIGH_INDX = 7
INSTRUMENT_AUTODAMP_INDX = 8
RHYTHM_TRACKS_INDX = 1
RHYTHM_BEAT_INDX = 0
RHYTHM_PAT_INDX = 1
SCALE_DEFINITION_INDX = 1
SCALE_LEN_INDX = 0
SCALE_COUNT_INDX = 1
SCALE_START_INDX = 2
SCALE_NOTE_INDX = 3
SCALE_HARMONY_TYPES_INDX = 4
ORIGINAL_BAR_NUM_INDX = 3
CREATE_TYPE_INDX = 4

# track_info indices
TRACK_INFO_MELO_OR_PERC_INDX = 0
TRACK_INFO_INSTRU_DEF_INDX = 1
TRACK_INFO_INSTRU_PAUSE_INDX = 2
TRACK_INFO_RHYTHM_INDX = 3
TRACK_INFO_CONNECT_INDX = 4

# constants for bar_statistics columns
USED_HOW_OFTEN = 0  # how often is the bar used within the composition
GROUP_IDENTIFIER = 1  # global number of bar starting a group of bars
CREATE_TYPE_IDENTIFIER = 2  # create type of bar
HARMONY_IDENTIFIER = 3  # harmony type of bar

""" track number + PLAYED_IN_TRACK gives column index of column which defines if a specific bar is actually
   played or paused in a track """

PLAYED_IN_TRACK = 4

# constants for rhythm creation
ACC_UNDEFINED = -999
RY_POS = 0
RY_ACC = 1
RY_LEV = 2
RY_LEN = 3
AUTODAMP_PERC = -2
AUTODAMP_MELO = -1

RM_REPEAT = 1
RM_NO_CONTINUE = 2
RM_HARMONY_TRACK = 3
RM_SOLO_PATTERN = 4
RM_TRACK_RHYTHM = 5
RM_VARI_TRACK_RHYTHM = 6
RM_PAUSE = 7
RM_MELODY = 8
RM_HARMONY_TRACK_NEW_HARMO = 9
RM_HARMONY_TRACK_LAST_HARMO = 10
RM_HARMONY_TRACK_NEW_HARMO_TYPE = 11

CONNECT_LEGATO = 1
CONNECT_STANDARD = 2
CONNECT_STACCATO = 3
CONNECT_AUTODAMP = 4

# harmony track identifier
HARMONY_TRACK = -2

FIRST_BAR_OF_PART = -3
BEAT_RHYTHM = -4
BEAT_MELODY = -5

# humanize constant
HUMANIZE_MAX_IN_MS = 14  # default 14

# melody creation constants
NO_PREV_TONE = -999
NOT_IN_SCALE = 999
DISHARMONIC_LIMIT = 10
FIRST_PREVIOUS_TONE = 0
SECOND_PREVIOUS_TONE = 1

END_PAUSE_IN_S = 4

# MIDI constants
MIDI_BANK_SELECT = 0
MIDI_CHANNEL_VOLUME = 7
MIDI_BALANCE = 8
MIDI_PAN = 10
MIDI_REVERB = 91
MIDI_CHORUS = 93

NO_USABLE_TONE_LENGTH = -1

ADAPT_PARTS_MAX_TRIES = 200
CREATE_SUB_LEVEL_MAX_TRIES = 100
CREATE_LEVEL_1_MAX_TRIES = 12

# notes
NOTE_C = 0
NOTE_CIS = 1
NOTE_D = 2
NOTE_DIS = 3
NOTE_E = 4
NOTE_F = 5
NOTE_FIS = 6
NOTE_G = 7
NOTE_GIS = 8
NOTE_A = 9
NOTE_BFLAT = 10
NOTE_B = 11


# harmony types
HARMONY_PREFER_MAJOR = -1
HARMONY_PREFER_MINOR = -2
HARMONY_AVOID_MAJMIN = -3
HARMONY_ANY = -4
HARMONY_PREFER_MAJOR_VAR = -5
HARMONY_PREFER_MINOR_VAR = -6
