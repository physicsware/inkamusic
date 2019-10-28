# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file contains webutility functions

"""

import datetime
import string
import random
import cherrypy
import inkamusic.html_data as html_data
import inkamusic.const as const
import inkamusic.utilities as utilities
import inkamusic.create_composition as create_composition
import inkamusic.settings as settings
import inkamusic.general_midi_instruments as general_midi_instruments
import inkamusic.menu_entries as me
import inkamusic.music_parameter as mp


def check_instrumentation_ids(instrumentation):
    """checks instrumentation settings"""

    def check_entries(instr):
        for idx in instr[1]:
            if len(idx) == 2:  # not a random type
                assert (isinstance(idx[1], int) and 0 < idx[1] <= 100) \
                  or (isinstance(idx[1], list) and check_cr(idx[1]))
                found = False
                for gmi in general_midi_instruments.GM_INSTRUMENTS:
                    if gmi[1] == idx[0]:
                        found = True
                        break

                assert found, ("ID " + repr(idx) + " used in " +
                               repr(instr) + " was not found in GM_INSTRUMENTS list")

    def check_cr(cr_list):
        for i in cr_list:
            if i not in [const.CR, const.CR2, const.CR_INTRO, const.CR_ENDING, const.CRB]:
                return False
        return True
    for instr in instrumentation:
        # example instr = ['Random instrumentation', [[0]]]
        if instr:  # not a separator line
            assert len(instr) == 2, "Syntax problem (len) in " + repr(instr)
            assert type(instr[1]).__name__ == 'list', "Syntax problem (not a list) in " + repr(instr)
            assert instr[1], "Syntax problem in " + repr(instr)
            check_entries(instr)


def nonbreak(original_string):
    """replaces spaces by non breaking spaces"""
    new_string = ''
    for character in original_string:
        if character == ' ':
            new_string += '&nbsp;'
        else:
            new_string += character

    return new_string


def html_select(legend, title, option_list, sel_element):
    """generates html code for select element """
    html = ''
    html += '<h5  class =" text-dark font-weight-light text-muted">' + legend + '<br></h5>'

    html += '<select  class =" custom-select  mb-4 bg-light border border-dark" name ="' + title + '">\n'

    # example option list is: [['Add percussion', True], ["Don't add percussion", False]]
    for indx, option in enumerate(option_list):
        if not option:
            html += '<option disabled>'
            for _ in range(16):
                html += '&#9472;'
            html += '</option>\n'
        else:
            if indx == sel_element:
                sel = ' selected'
            else:
                sel = ''
            option_text = option[0]
            html += '<option value ="' + option_text + '"' + sel + '>' + nonbreak(option_text) + '</option>\n'
        indx += 1

    html += '</select> '

    return html


def html_select_length_min(legend, title, option_list, sel_element):
    """generates html code for minute/second select element """

    html = ''

    html += '<h5  class =" text-dark font-weight-light text-muted">' + legend + '<br></h5>'

    # minutes
    html += '<select id ="idlenmin" '
    html += 'class =" custom-select  mb-4 bg-light border border-dark" name ="'
    html += title + 'min">\n'

    for indx, option in enumerate(option_list):
        if not option:
            html += '<option disabled>'
            for _ in range(16):
                html += '&#9472;'
            html += '</option>\n'
        else:
            if indx == sel_element:
                sel = ' selected'
            else:
                sel = ''
            option_text = option[0]
            html += '<option value ="' + option_text + '"' + sel + '>' + nonbreak(option_text) + '</option>\n'
        indx += 1

    html += '</select> '

    return html


def html_select_length_sec(title, option_list, sel_element):
    """generates html code for minute/second select element """

    html = ''

    html += '<select id ="idlensec" '
    html += 'class =" custom-select  mb-4 bg-light border border-dark" name ="'
    html += title + 'sec">\n'

    for indx, option in enumerate(option_list):
        if not option:
            html += '<option disabled>'
            for _ in range(16):
                html += '&#9472;'
            html += '</option>\n'
        else:
            if indx == sel_element:
                sel = ' selected'
            else:
                sel = ''
            option_text = option[0]
            html += '<option value ="' + option_text + '"' + sel + '>' + nonbreak(option_text) + '</option>\n'
        indx += 1

    html += '</select> '

    return html


def get_seed_html():
    """creates seed value html code"""
    html = ''
    html += """
        <script>function set_checked()
        {document.getElementById("seed_check").checked = true;}
        </script>
        """
    html += '<h5  class =" text-dark font-weight-light text-muted" >Use seed︎<br></h5>'
    html += '<label class ="checkbox-inline mb-2">'
    html += '<input id ="seed_check" type ="checkbox"  name ="seed_check" '

    html += 'value ="1">'
    html += '</label> '

    html += '<input id ="seedvalue" onclick ="set_checked(true)" type ="number" name ="seed_val"'
    html += 'data-toggle="tooltip" title="Activate this value to fix all random decisions, except instrumentation.︎"'

    sel_element = str(get_random_seed())
    html += 'value ="' + sel_element + '">'

    return html


def get_instru_id_html():
    """creates instrumentation ID (seed) value html code"""
    html = ''
    html += """
        <script>function set_instru_checked()
        {document.getElementById("instru_id_check").checked = true;}
        </script>
        """
    html += '<h5  class =" text-dark font-weight-light text-muted" >Use instrumentation seed<br></h5>'
    html += '<label class ="checkbox-inline mb-2">'
    html += '<input id ="instru_id_check" type ="checkbox"  name ="instru_id_check" '

    html += 'value ="1">'
    html += '</label> '

    html += '<input id ="instru_idvalue" onclick ="set_instru_checked(true)" type ="number" name ="instru_id_val"'
    html += 'data-toggle="tooltip"  title="Activate this value to fix all random decisions about the instrumentation.︎"'

    sel_element = str(get_random_seed())
    html += 'value ="' + sel_element + '">'

    return html


def get_random_seed():
    """gets new seed value"""
    random.seed()
    return random.randint(10000, const.MAX_SEED)


def create_rndm_classes(seed_val, instru_id_val):
    """creates independant random classes for different parts of the composition process"""

    def get_rndm():
        """creates random number used as seed for next random class"""
        return random.randint(1, 1000000)

    rndm_class = [0 for i in range(const.NUM_RNDM_CLASSES)]

    # init seed objects
    rnd_state = random.getstate()
    rndm_class[const.RNDM_INSTRU] = utilities.Rndm(instru_id_val)
    random.setstate(rnd_state)
    rndm_class[const.RNDM_SCALE] = utilities.Rndm(seed_val)
    seed_val_next = get_rndm()
    rndm_class[const.RNDM_HARMO] = utilities.Rndm(seed_val_next)
    seed_val_next = get_rndm()
    rndm_class[const.RNDM_MELO_RHYTHM] = utilities.Rndm(seed_val_next)
    seed_val_next = get_rndm()
    rndm_class[const.RNDM_STRUCTURE] = utilities.Rndm(seed_val_next)
    seed_val_next = get_rndm()
    rndm_class[const.RNDM_BASE_RHYTHM] = utilities.Rndm(seed_val_next)
    seed_val_next = get_rndm()
    rndm_class[const.RNDM_SOLO_RHYTHM] = utilities.Rndm(seed_val_next)
    seed_val_next = get_rndm()
    rndm_class[const.RNDM_PERC_RHYTHM] = utilities.Rndm(seed_val_next)
    seed_val_next = get_rndm()
    rndm_class[const.RNDM_INSTRU_RHYTHM] = utilities.Rndm(seed_val_next)
    seed_val_next = get_rndm()
    rndm_class[const.RNDM_HARMO_DISTRI] = utilities.Rndm(seed_val_next)
    seed_val_next = get_rndm()
    rndm_class[const.RNDM_OTHER] = utilities.Rndm(seed_val_next)

    return rndm_class


def create_filename():
    """generates file name for midid file"""
    date_time = datetime.datetime.today()
    time_ext = (f'{date_time.year:04}' + f'{date_time.month:02}' + f'{date_time.day:02}' +
                f'{date_time.hour:02}' + f'{date_time.minute:02}' + f'{date_time.second:02}')

    random_file_name = time_ext + '_' + ''.join(random.sample(string.ascii_uppercase, 8))

    return random_file_name


def get_menu_html():
    """generates web interface html code"""
    html = ''

    # first menu row
    html += """<div class ="row justify-content-between">"""

    # instrumentation menu
    html += """<div class ="col-auto">"""
    html_fragment = html_select('Instruments', 'sel_instrumentation',
                                me.INSTRUMENTATION_LIST, mp.MENU_INIT[0])
    html += html_fragment
    html += """</div>"""

    # percussion menu
    html += """<div class ="col-auto">"""
    html_fragment = html_select('Percussion', 'sel_percussion', settings.get_percussion_list(), mp.MENU_INIT[1])
    html += html_fragment
    html += """</div>"""

    # end of first menu row
    html += """</div>"""

    # second menu row
    html += """<div class ="row justify-content-between">"""

    # scales and harmonies menu
    html += """<div class ="col-auto">"""
    html_fragment = html_select('Scales and Harmonies', 'sel_scales', settings.get_scales_list(), mp.MENU_INIT[2])
    html += html_fragment
    html += """</div>"""

    # rhythms menu
    html += """<div class ="col-auto">"""
    html_fragment = html_select('Rhythms', 'sel_rhythms', settings.get_rhythm_list(), mp.MENU_INIT[3])
    html += html_fragment
    html += """</div>"""

    # end of second menu row
    html += """</div>"""

    # third menu row
    html += """<div class ="row justify-content-between">"""

    # minutes and seconds
    html += """<div class = "col-auto">"""
    html_fragment = html_select_length_min('Length', 'sel_length', settings.get_length_min(), mp.MENU_INIT[4])
    html += html_fragment
    html_fragment = html_select_length_sec('sel_length', settings.get_length_sec(), mp.MENU_INIT[5])
    html += html_fragment
    html += """</div>"""

    # speed menu
    html += """<div class ="col-auto">"""
    html_fragment = html_select('Speed', 'sel_speed', settings.get_speed_list(), mp.MENU_INIT[6])
    html += html_fragment
    html += """</div>"""

    # end of third menu row
    html += """</div>"""

    return html


# pylint: disable=locally-disabled, no-self-use

class InkaAlgorithmicMusicWebInterface():
    """ This is the Inka_Algorithmic_Music web interface class
        which generates and handles the web interface.
    """

    def __init__(self):

        # create settings object
        self.menu_options = settings.Settings()

        # check consistency of entries in settings module.
        check_instrumentation_ids(me.INSTRUMENTATION_LIST)
        # to do check valid harmonies for scales

    @cherrypy.expose
    def index(self):
        """This function generates the default web page used as user interface to Inka Algorithmic Music"""

        html = ''
        html += html_data.get_html_source(0)
        html += html_data.get_html_source(1)
        html += html_data.get_html_source(2)
        html += html_data.get_html_source(3)
        html += html_data.get_html_source(4)

        html += get_menu_html()  # creates html code for all menu options

        html += html_data.get_html_source(5)

        html += get_seed_html()
        html += get_instru_id_html()

        html += html_data.get_html_source(6)

        return html

    @cherrypy.expose
    def generate(self, **kwargs):
        """This function uses the web page settings to generate a composition"""

        # check if user seed is checked in web interface and set seed_val
        if 'seed_check' in kwargs:  # user seed checked
            try:
                seed_int = int(kwargs['seed_val'])

            except ValueError:
                seed_int = get_random_seed()

            seed_val = seed_int
            if seed_val > const.MAX_SEED or seed_val < 1:
                seed_val = get_random_seed()
        else:
            seed_val = get_random_seed()

        # check if instrumentation seed is checked in web interface and set instru_id_val
        if 'instru_id_check' in kwargs:  # instrumentation seed checked
            try:
                instru_id_int = int(kwargs['instru_id_val'])

            except ValueError:
                instru_id_int = get_random_seed()

            instru_id_val = instru_id_int
            if instru_id_val > const.MAX_SEED or instru_id_val < 1:
                instru_id_val = get_random_seed()
        else:
            instru_id_val = get_random_seed()

        # initialize random value generation with seed_val

        random.seed(a=seed_val)
        if const.DEBUG_OUTPUT:
            print(' ')
            print(' ')
            print(' ***   START   ***')
            print(' ')
            print(' ')
            print('seed is', seed_val, 'and instru_id is', instru_id_val)

        # initialise random classes for different parts of the creation process
        rndm_2 = create_rndm_classes(seed_val, instru_id_val)

        # reset all settings
        self.menu_options.reset()

        # set all selections from web interface
        self.menu_options.set_web_interface_selections(kwargs)

        # define other settings which are not available in web interface
        # but are derived indirectly, typically using random numbers
        self.menu_options.set_selected_bpm(rndm_2)

        # create filename for composition
        random_file_name = create_filename()

        try:
            # use file name to identify cherrypy session
            cherrypy.session['mystring'] = random_file_name

        except AttributeError:
            pass

        # create InkaAlgorithmicMusic object
        current_composition = create_composition.InkaAlgorithmicMusic(menu_options=self.menu_options,
                                                                      rndm_2=rndm_2,
                                                                      random_file_name=random_file_name)

        # create composition
        current_composition.create_composition()

        # return name of generated file and actually used seed_val to web interface
        xxd = random_file_name + str(seed_val).zfill(9) + str(instru_id_val).zfill(9)
        return xxd
