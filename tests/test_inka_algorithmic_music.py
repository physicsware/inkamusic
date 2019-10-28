#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `inkamusic` package."""

import pytest
import inkamusic.webutilities as webutilities

def test_generate_midi():
    x = webutilities.InkaAlgorithmicMusicWebInterface()
    x.generate(sel_instrumentation='Piano + Bass',sel_percussion='Add percussion', sel_scales='6 tone (maj min)',
    sel_rhythms='Soca', sel_lengthmin='0 min',sel_lengthsec='10 s', sel_speed='normal speed', seed_val = 33016197,
    instru_id_val = 79586706)

    x.generate(sel_instrumentation='Marimba + Bass',sel_percussion='Add percussion', sel_scales='C (maj)',
    sel_rhythms='Soca', sel_lengthmin='2 min',sel_lengthsec='10 s', sel_speed='normal speed')

