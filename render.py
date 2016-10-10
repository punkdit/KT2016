#!/usr/bin/env python

from math import pi, sin, cos, sqrt
import math
import sys
import wave
from time import time, sleep
import random

#random.seed(0)

import cairo
from cairo import Context

import numpy




food_for_vim_autocomplete = """
ANTIALIAS_DEFAULT       HAS_PS_SURFACE          PATH_CURVE_TO
ANTIALIAS_GRAY          HAS_QUARTZ_SURFACE      PATH_LINE_TO
ANTIALIAS_NONE          HAS_SVG_SURFACE         PATH_MOVE_TO
ANTIALIAS_SUBPIXEL      HAS_WIN32_FONT          PDFSurface
CAPI                    HAS_WIN32_SURFACE       PSSurface
CONTENT_ALPHA           HAS_XCB_SURFACE         Pattern
CONTENT_COLOR           HAS_XLIB_SURFACE        RadialGradient
CONTENT_COLOR_ALPHA     HINT_METRICS_DEFAULT    SUBPIXEL_ORDER_BGR
Context                 HINT_METRICS_OFF        SUBPIXEL_ORDER_DEFAULT
EXTEND_NONE             HINT_METRICS_ON         SUBPIXEL_ORDER_RGB
EXTEND_REFLECT          HINT_STYLE_DEFAULT      SUBPIXEL_ORDER_VBGR
EXTEND_REPEAT           HINT_STYLE_FULL         SUBPIXEL_ORDER_VRGB
Error                   HINT_STYLE_MEDIUM       SVGSurface
FILL_RULE_EVEN_ODD      HINT_STYLE_NONE         ScaledFont
FILL_RULE_WINDING       HINT_STYLE_SLIGHT       SolidPattern
FILTER_BEST             ImageSurface            Surface
FILTER_BILINEAR         LINE_CAP_BUTT           SurfacePattern
FILTER_FAST             LINE_CAP_ROUND          XlibSurface
FILTER_GAUSSIAN         LINE_CAP_SQUARE         __class__
FILTER_GOOD             LINE_JOIN_BEVEL         __delattr__
FILTER_NEAREST          LINE_JOIN_MITER         __dict__
FONT_SLANT_ITALIC       LINE_JOIN_ROUND         __doc__
FONT_SLANT_NORMAL       LinearGradient          __file__
FONT_SLANT_OBLIQUE      Matrix                  __getattribute__
FONT_WEIGHT_BOLD        OPERATOR_ADD            __hash__
FONT_WEIGHT_NORMAL      OPERATOR_ATOP           __init__
FORMAT_A1               OPERATOR_CLEAR          __name__
FORMAT_A8               OPERATOR_DEST           __new__
FORMAT_ARGB32           OPERATOR_DEST_ATOP      __path__
FORMAT_RGB16_565        OPERATOR_DEST_IN        __reduce__
FORMAT_RGB24            OPERATOR_DEST_OUT       __reduce_ex__
FontFace                OPERATOR_DEST_OVER      __repr__
FontOptions             OPERATOR_IN             __setattr__
Gradient                OPERATOR_OUT            __str__
HAS_ATSUI_FONT          OPERATOR_OVER           _cairo
HAS_FT_FONT             OPERATOR_SATURATE       cairo_version
HAS_GLITZ_SURFACE       OPERATOR_SOURCE         cairo_version_string
HAS_PDF_SURFACE         OPERATOR_XOR            version



flush get_content get_data get_device_offset get_font_options
get_format get_height get_stride get_width mark_dirty mro
create_for_data          set_device_offset
create_from_png          set_fallback_resolution
create_similar           write_to_png
finish                   



__class__                 get_font_matrix           rotate
__delattr__               get_font_options          save
__doc__                   get_group_target          scale
__getattribute__          get_line_cap              select_font_face
__hash__                  get_line_join             set_antialias
__init__                  get_line_width            set_dash
__new__                   get_matrix                set_fill_rule
__reduce__                get_miter_limit           set_font_face
__reduce_ex__             get_operator              set_font_matrix
__repr__                  get_scaled_font           set_font_options
__setattr__               get_source                set_font_size
__str__                   get_target                set_line_cap
append_path               get_tolerance             set_line_join
arc                       glyph_extents             set_line_width
arc_negative              glyph_path                set_matrix
clip                      identity_matrix           set_miter_limit
clip_extents              in_fill                   set_operator
clip_preserve             in_stroke                 set_source
close_path                line_to                   set_source_rgb
copy_clip_rectangle_list  mask                      set_source_rgba
copy_page                 mask_surface              set_source_surface
copy_path                 move_to                   set_tolerance
copy_path_flat            new_path                  show_glyphs
curve_to                  new_sub_path              show_page
device_to_user            paint                     show_text
device_to_user_distance   paint_with_alpha          stroke
fill                      pop_group                 stroke_extents
fill_extents              pop_group_to_source       stroke_preserve
fill_preserve             push_group                text_extents
font_extents              push_group_with_content   text_path
get_antialias             rectangle                 transform
get_current_point         rel_curve_to              translate
get_dash                  rel_line_to               user_to_device
get_dash_count            rel_move_to               user_to_device_distance
get_fill_rule             reset_clip                
get_font_face             restore                   

"""




class FlipRedAndBlue(object):

    """ This does not seem to appreciably slow down the animation.
    """

    def __init__(self, surface):
        self.surface = surface
        self.ctx = cairo.Context(surface)
        for name in dir(self.ctx):
            if not getattr(self, name, None):
                self.__dict__[name] = getattr(self.ctx, name)

    def set_source_rgb(self, r, g, b):
        return self.ctx.set_source_rgb(b, g, r)

    def set_source_rgba(self, r, g, b, a):
        return self.ctx.set_source_rgba(b, g, r, a)



def display(callback, w=480, h=480):

    global Context
    Context = FlipRedAndBlue

    import pygame

    depth = 4
    data = numpy.empty((w, h, depth,), dtype=numpy.uint8)
    surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, w, h)
    ctx = Context(surface)
    #print ctx.get_antialias()
    ctx.set_antialias(cairo.ANTIALIAS_GRAY)

    pygame.display.init()
    surf = pygame.display.set_mode((w,h), pygame.DOUBLEBUF)
    imsurf = pygame.image.frombuffer(data, (w,h), "RGBA")
    
    t0 = time()
    t = 0
    frame = 0
    done = False

#    bluechan = numpy.empty((w, h), dtype=numpy.uint8)

    clock = pygame.time.Clock()
    running = True

    fps = 25
    while not done:
        clock.tick(fps)

        if running:
            t = time() - t0
        else:
            t0 += time()-t0-t

        callback(ctx, w, h)

# XXX can't seem to get this right...
#        bluechan = data[:,:,2] 
#        data[:,:,2] = data[:,:,0]
#        data[:,:,0] = bluechan
        surf.blit(imsurf, (0,0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                key, mod, unicode = event.key, event.mod, event.unicode
                if key == pygame.K_ESCAPE:
                    done = True
                elif key == pygame.K_SPACE:
                    running = not running
#            elif event.type == pygame.MOUSEBUTTONDOWN:
#                #print event, dir(event)
#                graph.mouse(*event.pos)


        pygame.display.flip()
#        sleep(0.1)

        frame += 1


