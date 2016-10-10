#!/usr/bin/env python

import sys, os

from math import *
from random import *
from time import sleep

import numpy

import cairo


from argv import Argv
argv = Argv()


def getc(theta):
    #print theta,
    theta %= 2*pi
    #print theta,
    theta = 8*(theta / (2*pi))
    #print theta,
    theta = int(round(theta))
    #prin_ theta
    c = '_/|\\'[theta%4]
    return c


def show(A):
    for row in A:
        for theta in row:
            print getc(theta),
        print


#from pyx import canvas, path, deco, trafo, style, text, color, unit, epsfile, deformer
#rgb = color.rgb
#rgbfromhexstring = color.rgbfromhexstring
#
#red, green, blue, yellow = (rgb.red,
#    rgbfromhexstring("#008000"),
#    rgb.blue, rgb(0.75, 0.75, 0)) 
#
#blue = rgb(0., 0., 0.8)
#lred = rgb(1., 0.4, 0.4)
#lgreen = rgb(0.4, 0.8, 0.2)
#
#text.set(mode="latex") 
##text.set(docopt="10pt")
#text.preamble(r'\usepackage{amsfonts}')
##text.preamble(r"\def\I{\mathbb{I}}")
#    
#
#def render(A, fname):
#
#    c = canvas.canvas()
#
#    print dir(c)
#    c.writePNGfile(fname)
#




def energy(A, i, j):
    n = len(A)
    H = 0.
    theta = A[i, j]
    for i1 in [(i-1)%n, (i+1)%n]:
        H += 1-cos(theta - A[i1, j])
    for j1 in [(j-1)%n, (j+1)%n]:
        H += 1-cos(theta - A[i, j1])
    return H

def delta(theta1, theta0):
    best = None
    for s in (-2*pi, 0, 2*pi):
      for t in (-2*pi, 0, 2*pi):
        r = theta1+s - (theta0+t)
        if best is None or abs(r)<abs(best):
            best = r
    return best

def get_wind(A, i, j):
    w = 0.
    n = len(A)
    theta = A[(i+1)%n, j]
    for (di, dj) in [(+1, +1), (+0, +1), (-1, +1), (-1, +0), (-1, -1), (+0, -1), (+1, -1), (+1, 0)]:
        theta1 = A[(i+di)%n, (j+dj)%n]
        w += delta(theta1, theta)
        theta = theta1
    return w
    

class Model(object):
    def __init__(self, n, t=0.2):
        A = numpy.zeros((n, n))
        for i in range(n):
          for j in range(n):
            i1 = i-n/2
            j1 = j-n/2
            if i1 > abs(j1):
                theta = 0.5*pi
            elif j1 > abs(i1):
                theta = 1.0*pi
            elif i1 < -abs(j1):
                theta = 1.5*pi
            else:
                theta = 0.
            A[i, j] = theta
        self.t = t
        B = A.copy()
        for i in range(n):
          for j in range(n):
            A[i, j] = B[(i+n/4)%n, (j+n/4)%n]
        #A = numpy.zeros((n, n))
        if argv.random:
            for i in range(n):
                for j in range(n):
                    A[i, j] = 2*pi*random()
            
        self.A = A
        self.H = numpy.zeros((n, n)) # energy
        self.frame = 0

    def step(self):
        A = self.A
        H = self.H
        #t = self.t
        theta = (self.frame)/200.
        t = self.t
        t = self.t = 0.6 * (1+cos(theta)) + 0.1
        #print "t=", t
        n = len(A)
        B = A.copy()
        for i in range(n):
          for j in range(n):
            theta0 = A[i, j]
            h0 = energy(A, i, j)
            A[i, j] = 2*pi * random()
            h1 = energy(A, i, j)
            p = 1.0/(1. + e**((h1-h0)/t))
            if random() <= p:
                B[i, j] = A[i, j] # accept
                H[i, j] = h1
            else:
                H[i, j] = h0
            A[i, j] = theta0
        A[:] = B
        self.frame += 1
        #print numpy.min(H), numpy.max(H)

    def render(self, ctx, w, h):
        N = argv.get("step", 5)
        for i in range(N):
            self.step()
        A = self.A
        n = len(A)
        r0 = 0.5*w/n
        r = 0.4*w/n

        ctx.set_source_rgb(0,0,0)
        ctx.rectangle(0,0,w,h)
        ctx.fill()

        h1 = h
        m = 30.
        h = h-m

        H = self.H
        for i in range(n):
          for j in range(n):
            a = H[i, j] / (2*pi)
            a = a**0.3
            x = 1.*(i+0.5)*w/n
            y = 1.*(j+0.5)*h/n
            if a>0.1:
                ctx.set_source_rgb(a, 0.2*a, 0.2*a)
                ctx.rectangle(x-r0, y-r0, 2*r0, 2*r0)
                ctx.fill()

        for i in range(n):
          for j in range(n):
            a = get_wind(A, i, j)
            #if abs(a)>0.01:
            #    print (i, j), "%.2f"%a
            if abs(a)<0.01:
                continue

            x = 1.*(i+0.5)*w/n
            y = 1.*(j+0.5)*h/n
            if a>0:
                ctx.set_source_rgb(0.0, 0.2, 1.0)
            elif a<0:
                ctx.set_source_rgb(0.3, 1.0, 0.0)
            #ctx.arc(x, y, 2*r, 0., 2*pi)
            #ctx.fill()
            ctx.rectangle(x-r0, y-r0, 2*r0, 2*r0)
            ctx.stroke()


        for i in range(n):
          for j in range(n):
            x = 1.*(i+0.5)*w/n
            y = 1.*(j+0.5)*h/n
            theta = A[i, j]
            dx = r*cos(theta)
            dy = r*sin(theta)
            ctx.set_source_rgb(1,1,1)
            ctx.move_to(x-dx, y-dy)
            ctx.line_to(x+dx, y+dy)
            ctx.stroke()

            #ctx.set_source_rgb(1,0,0)
            ctx.arc(x+dx, y+dy, 0.3*r, 0., 2*pi)
            ctx.fill()

        ctx.set_source_rgb(1,1,1)
        ctx.set_font_size(20)
        ctx.move_to(20, h+0.8*m)
        ctx.show_text("temperature: %.2f"%self.t)

#        ctx.move_to(w-150, h+0.6*m)
#        ctx.show_text("order:")
#
#        dx = numpy.cos(A)
#        dy = numpy.sin(A)
#        N = n**2
#        dx = r*dx.sum() / N
#        dy = r*dy.sum() / N
#        #norm = (dx**2 + dy**2)**0.5 + 1e-8
#        #dx = r*(dx/norm)
#        #dy = r*(dy/norm)
#        x, y = w-50, h+m/2.
#
#        ctx.set_source_rgb(1,1,1)
#        ctx.move_to(x-dx, y-dy)
#        ctx.line_to(x+dx, y+dy)
#        ctx.stroke()
#
#        ctx.set_source_rgb(1,0,0)
#        ctx.arc(x+dx, y+dy, 0.2*r, 0., 2*pi)
#        ctx.stroke()

            


def main():

    n = argv.get("n", 4)
    t = argv.get("t", 0.1)
    model = Model(n, t)

    _seed = argv.get("seed")
    if _seed is not None:
        print "seed:", _seed
        seed(_seed)

    if argv.skip:
        for i in range(argv.skip):
            model.step()

    W, H = 640, 640
    if argv.frames:
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
        ctx = cairo.Context(surface)
        for i in range(argv.frames):
            model.render(ctx, W, H)
            surface.write_to_png("frames/%.4d.png"%i)
            print ".",;sys.stdout.flush()

    else:
        import render
        render.display(model.render, W, H)



if __name__ == "__main__":
    main()


