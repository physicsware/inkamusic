# coding=utf-8
"""

Inka Algorithmic Music
Creates fully arranged algorithmic instrumental music.
Copyright (C) 2018  Udo Wollschläger

This file contains static html code used for web interface

"""


def get_html_source(html_id):
    """returns static html code used for web interface"""

    if html_id == 0:
        txt = """
            <!doctype html>
            <html lang="en">
            <head>

            <title>Inkamusic</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <meta name="description" content="Creates algorithmic music based on artificial composition rules">
            <meta name="keywords" content="algorithmic music,artificial music,algorithmic composition,artificial composition,artificial composer,software generated music,computer generated music">
            <meta name="msapplication-TileColor" content="#da532c">
            <meta name="msapplication-config" content="/static/browserconfig.xml">
            <meta name="theme-color" content="#ffffff">

            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
            <link rel="stylesheet" href="/static/algomusic.css?version=13">
            <link rel="apple-touch-icon" sizes="180x180" href="/static/apple-touch-icon.png">
            <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
            <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
            <link rel="manifest" href="/static/site.webmanifest">
            <link rel="mask-icon" href="/static/safari-pinned-tab.svg" color="#5bbad5">
            <link rel="shortcut icon" href="/static/favicon.ico">

            <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
            """  # noqa: E501

    elif html_id == 1:

        txt = """
            <script>
            $(document).ready(function() {
                $('[data-toggle="tooltip"]').tooltip();
                var aid = document.getElementById("spinny");
                aid.src="/static/empty.gif" ;
                $("#generatemusic").click(function(e) {
                    var aid = document.getElementById("spinny");
                    aid.src="/static/spinball.gif";
                    $.post("/generate", {
                        "sel_instrumentation": $("select[name='sel_instrumentation']").val(),
                        "sel_percussion": $("select[name='sel_percussion']").val(),
                        "sel_scales": $("select[name='sel_scales']").val(),
                        "sel_rhythms": $("select[name='sel_rhythms']").val(),
                        "sel_lengthmin": $("select[name='sel_lengthmin']").val(),
                        "sel_lengthsec": $("select[name='sel_lengthsec']").val(),
                        "sel_speed": $("select[name='sel_speed']").val(),
                        "seed_check": $("input[name='seed_check']:checked").val(),
                        "seed_val": $("input[name='seed_val']").val(),
                        "instru_id_check": $("input[name='instru_id_check']:checked").val(),
                        "instru_id_val": $("input[name='instru_id_val']").val(),
                    })
                    .done(function(string_seed) {
                        string=string_seed.substring(0,23);
                        seed=string_seed.substring(23,32);
                        instru_id=string_seed.substring(32);
                        var aid = document.getElementById("spinny");
                        aid.src="/static/empty.gif" ;
                        var aid = document.getElementById("seedvalue");
                        aid.value=parseInt(seed);
                        var aid = document.getElementById("instru_idvalue");
                        aid.value=parseInt(instru_id);
                        var aid = document.getElementById("downloadbutton");
                        aid.href="/static/midi/"+string+".mid";
                        aid.download=string+".mid"
                        aid.hidden=false;
                    });
                    e.preventDefault();
                });
            });
            </script>
        """

    elif html_id == 2:
        txt = """
            <style>
            body {{background-color: #FFFFFF;}}
            </style>
            </head>
            <body>
            <div class="container bg-1">
        """

    elif html_id == 3:
        txt = """ <div class="row">"""
        txt += """<div class="col-md-3">"""
        txt += """<span>"""
        txt += '<img src="/static/inkalogo.png" alt="Inka Algorithmic Music" width=128 height=84>'
        txt += """</span>"""
        txt += """</div>"""
        txt += """<div class="col-md-9 pt-3 pull-right">"""
        txt += """<span>"""
        txt += """</span>"""
        txt += """</div>"""
        txt += """</div>"""

    elif html_id == 4:
        txt = """<div class="row justify-content-start">"""

        txt += """<div class="col-auto d-flex align-items-center">"""
        txt += """<button id="generatemusic" class="btn btn-primary  btn-sm mr-1" >Create</button>"""
        txt += """<a hidden id="downloadbutton" class="btn btn-outline-success btn-sm mr-1" """
        txt += """href="x" download="x">Open MIDI file</a>"""

        # spinning wheel
        txt += """<img  src="/static/empty.gif"  height="40" width="10" />"""
        txt += """<div id="spinning" ><img id="spinny" src="/static/empty.gif"  alt="Spinning" /></div>"""
        txt += """</div>"""
        txt += """</div>"""
        txt += """
        <div class="row justify-content-between">"""

        txt += """</div>"""

    elif html_id == 5:
        txt = """<div class="col-auto">"""

    elif html_id == 6:
        txt = """</div>"""
        txt += """</div>"""
        txt += """</div></body></html>"""

    return txt
