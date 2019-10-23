#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `inkamusic` package."""

import pytest
import inkamusic.webutilities as webutilities

def test_file1_method1():
    x = webutilities.InkaAlgorithmicMusicWebInterface()
    x.generate(sel_instrumentation='Marimba + Bass',sel_percussion='Add percussion', sel_scales='A min maj (natural)',
    sel_rhythms='Soca', sel_lengthmin='2 min',sel_lengthsec='10 s', sel_speed='normal speed')

