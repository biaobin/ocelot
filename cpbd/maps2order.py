__author__ = 'Sergey Tomin'

from numpy import cos, sin, sqrt, zeros, eye, tan, dot, empty_like, array, transpose, linspace
from ocelot.common.globals import *

"""
differential equation:

t_nnn'' + kx**2*t_nnn = f_nnn

here index nnn means (1,2,3,4,5,6) = (x, x', y, y', s, delta)

# h = 1/r0 - curvature
# k1 = 1/Bro*dBy/dx - gradient
# k2 = 1/Bro*d^2(By)/dx^2 - sextupole component
# h1 - derivative of h
# h11 - derivative of h1
# cx1, sx1, cy1 ... - derivative of cx, sx, cy, ... and so on
# cx = cos(kx*s)
# sx = sin(kx*s)/kx
# dx = h/kx2*(1. - cx)
# cy = cos(ky*s)
# sy = sin(ky*s)/ky

Defenition:
Brown -> OCELOT
n = ky**2/h**2
beta = K2/h**3

# Green's function for X is Gx(t, tau) = 1/kx*sin(kx*(t - tau))

f111 = -(h**3 + K2 - 2*h*ky**2)*cx**2 + 1./2.*h*kx**4*sx*2 - kx**3*cx*sx*h'
f112 = - 2 * kx * (h**3 + K2 - 2 * h * ky**2) * cx * sx - h * kx**2 * cx * sx + (cx**2 - kx**2 * sx**2)*h'
f116 = (2*h^2 -ky^2)* cx + 2 *(h^3+K2-2 *h *ky^2) *cx* dx-h^2*kx^2 *sx^2 + (h *kx *cx *sx-dx* kx^2*sx)* h'
f122 = 1/2* h* cx^2 + h^3* (-1-K2/h^3+(2 ky^2)/h^2) *sx^2 + sx *sx* h'
f126 = h^2 *(2-ky^2/h^2) sx+h^2 *cx* sx + 2 h^3 (-1-K2/h^3+(2 ky^2)/h^2) *dx* sx + (cx dx +h sx^2) h'
f166 = -h + dx*h^2*(2-ky^2/h^2) + dx^2*h^3*(-1-K2/h^3+(2 ky^2)/h^2) + 1/2*h*(dx')^2 + dx*dx'* h'
f133 = -(1/2)* h*ky4*sy^2 - ky2*cy* sy*h' + 1/2*cy^2*(2*K2 - h*ky^2+h'') = |h' = 0, h'' = 0 | = -(1/2)* h*ky2 + cy**2*K2
f134 = h*ky2*cy*sy + (cy2 - sy2*ky2)*h' + cy*sy*(2*k2 - h*ky2 + h'')
f144 = -(1/2)*h*cy2 + cy*sy*h' + (sy2*(2*K2 - h*ky2 + h''))/2 =|h' = 0, h'' = 0 | =  -(1/2) *h +sy^2*K2

# Green's function for Y is Gy(t, tau) = 1/ky*sin(ky*(t - tau))

f313 = 2*(K2 - ky2*h)*cx*cy + h*kx2*ky2*sx*sy + (kx^2 *cy *sx-ky^2 *cx* sy) h'
f314 = -h kx^2 cy sx+2 h^3 (K2/h^3-ky^2/h^2) cx sy+(cx cy+kx^2 sx sy) h'
f323 = 2 h^3 (K2/h^3-ky^2/h^2) cy sx-h ky^2 cx sy+(-cx cy-ky^2 sx sy) h'
f324 = h cx cy+2 h^3 (K2/h^3-ky^2/h^2) sx sy + (cy sx-cx sy) h'
f336 = ky^2 cy+2 h^3 (K2/h^3-ky^2/h^2) dx cy-h^2 ky^2 sx sy-(h cy sx+ky^2 dx sy) h'
f346 = h^2 cy sx+ky^2 sy+2 h^3 (K2/h^3-ky^2/h^2) dx sy-(-dx cy+h sx sy) h'

Integration:

I111 = Gx * cx**2 = ((2. + cx)*dx)/(3*h)
I122 = Gx * sx**2 = dx**2/3./h**2
I112 = Gx * cx*sx = sx*dx/(3.*h)
I11  = Gx * cx    = s*sx/2.
I116 = Gx * cx*dx = h/kx2*(cx - cx**2) = h/kx2*(I11 - I111)
I12  = Gx * sx    = 1./2./kx2*(sx - s*cx/2.)
I126 = Gx * sx*dx = h/kx2*(sx - sx*cx) = h/kx2*(I12 - I112)
I10  = Gx         = dx/h
I16  = Gx * dx    = h/kx2*(dx/h - s*sx/2)
I166 = Gx * dx**2 = h2/kx4*(1 - 2*cx + cx**2) = h2/kx4*(I10 - 2*I11 + I111)
I144 = Gx * sy**2 = (sy2 - 2*dx/h)/(kx2 - 4*ky2)
I133 = Gx * cy**2 = dx/h + ky2*(2*dx/h - sy2)/(kx2 - 4*ky2)
I134 = Gx * cy*sy = (sy*cy - sx)/(kx2 - 4.*ky2)
I313 = Gy * cx*cy = (kx2*cy*dx/h - 2*ky2*sx*sy)/(kx2 - 4 *ky2)
I324 = Gy * sx*sy = (kx2*cy*dx/h - 2*ky2*sx*sy)/(kx2 - 4*ky2)
I314 = Gy * cx*sy = (2*cy*sx - (1 + cx)*sy)/(kx2 - 4*ky2)
I323 = Gy * sx*cy = ((1 - 2*ky2*dx/h)*sy - cy*sx)/ (kx2 - 4*ky2)
I33  = Gy * cy    = s*sy/2.
I336 = Gy * dx*cy = h/kx2*(I33 - I313)
I34  = Gy * sy    = (sy - s*cy)/(2*ky2)
I346 = Gy * dx*sy = h/kx2*(I34 - I314)
"""


def t_nnn(L, h, k1, k2):
    """
    :param L:
    :param angle:
    :param k1:
    :param k2:
    :return:

    here is used the following set of variables:
    x, dx/ds, y, dy/ds, delta_l, dp/p0
    """

    h2 = h*h
    h3 = h2*h
    kx2 = (k1 + h*h)
    ky2 = -k1
    kx4 = kx2*kx2
    ky4 = ky2*ky2
    kx = sqrt(kx2 + 0.j)
    ky = sqrt(ky2 + 0.j)
    cx = cos(kx*L).real
    sx = (sin(kx*L)/kx).real if kx != 0 else L
    cy = cos(ky*L).real

    sy = (sin(ky*L)/ky).real if ky != 0 else L

    sx2 = sx*sx
    sy2 = sy*sy
    L2 = L*L
    L3 = L2*L
    L4 = L3*L
    L5 = L4*L
    dx = h/kx2*(1. - cx) if kx != 0. else L*L*h/2.
    dx_h = (1. - cx)/kx2 if kx != 0. else L*L/2.

    # Integrals
    denom = kx2 - 4.*ky2
    I111 = 1./3.*(sx2 + dx_h)                          #  I111 = Gx * cx**2
    I122 = dx_h*dx_h/3.                                #  I122 = Gx * sx**2
    I112 = sx*dx_h/3.                                  #  I112 = Gx * cx*sx
    I11  = L*sx/2.                                     #  I11  = Gx * cx
    I10  = dx_h                                        #  I10  = Gx
    I33  = L*sy/2.                                     #  I33  = Gy * cy
    I34  = (sy - L*cy)/(2.*ky2) if ky !=0. else L3/6.  #  I34  = Gy * sy
    I211 = sx/3.*(1. + 2.*cx)
    I222 = 2.*dx_h*sx/3.
    I212 = 1./3.*(2*sx2 - dx_h)
    I21  = 1./2.*(L*cx + sx)
    I22  = I11
    I20  = sx
    I43  = 0.5*(L*cy + sy)
    I44  = I33

    #I5xx = h*Integrate(I1xx, dx)
    I512 = h*dx_h*dx_h/6
    I51  = L*dx/2.

    if kx != 0:
        I116 = h/kx2*(I11 - I111)                     #  I116 = Gx * cx*dx
        I12  = 0.5/kx2*(sx - L*cx)                    #  I12  = Gx * sx
        I126 = h/kx2*(I12 - I112)                     #  I126 = Gx * sx*dx
        I16  = h/kx2*(dx_h - L*sx/2.)                 #  I16  = Gx * dx
        I166 = h2/kx4*(I10 - 2*I11 + I111)            #  I166 = Gx * dx**2
        I216 = h/kx2*(I21 - I211)
        I226 = h/kx2*(I22 - I212)
        I26  = h /(2.*kx2)*(sx - L*cx)
        I266 = h2/kx4*(I20 - 2.*I21 + I211)

        I511 = h*(3.*L - 2.*sx - sx*cx)/(6.*kx2)
        I522 = h*(3.*L - 4*sx + sx*cx)/(6.*kx4)
        I516 = h/kx2*(I51 - I511)
        I52  =  (dx - 4.*L*sx)/(2.*kx2)
        I526 = h/kx2*(I52 - I512)
        I50  = h*(L - sx)/kx2
        I566 = h2/kx4*(I50 - 2*I51 + I511)
        I56  = (h2*(L*(1. + cx) - 2.*sx))/(2.*kx4)

    else:
        I116 = h*L4/24.                               #  I116 = Gx * cx*dx
        I12  = L3/6.                                  #  I12  = Gx * sx
        I126 = h*L5/40.                               #  I126 = Gx * sx*dx
        I16  = h*L4/24.                               #  I16  = Gx * dx
        I166 = h2*L5*L/120.                           #  I166 = Gx * dx**2
        I216 = h*L3/6.
        I226 = h*L4/8.
        I26  = h*L3/6.
        I266 = h2*L5/20.

        I511 = h*L3/6.
        I522 = h*L5/60.
        I516 = h2*L5/120.
        I52  = h*L4/24.
        I526 = h2*L5*L/240.
        I50  = h*L3/6.
        I566 = h2*h*L5*L2/840.
        I56  = h2*L5/120.

    if kx != 0 and ky != 0:
        I144 = (sy2 - 2.*dx_h)/denom                         #  I144 = Gx * sy**2
        I133 = dx_h - ky2*(sy2 - 2.*dx_h)/denom              #  I133 = Gx * cy**2
        I134 = (sy*cy - sx)/denom                            #  I134 = Gx * cy*sy
        I313 = (kx2*cy*dx_h - 2.*ky2*sx*sy)/denom            #  I313 = Gy * cx*cy
        I324 = (2.*cy*dx_h - sx*sy)/denom                    #  I324 = Gy * sx*sy
        I314 = (2.*cy*sx - (1. + cx)*sy)/denom               #  I314 = Gy * cx*sy
        I323 = (sy - cy*sx - 2.*ky2*sy*dx_h)/denom           #  I323 = Gy * sx*cy = (2*ky2/kx2*(1 + cx)*sy - cy*sx)/denom + sy/kx2
        #derivative of Integrals
        I244 = 2.*(cy*sy - sx)/denom
        I233 = sx + 2.*ky2*(cy*sy - sx)/denom
        I234 = (kx2*dx_h - 2.*ky2*sy2)/denom
        I413 = ((kx2 - 2.*ky2)*cy*sx - ky2*sy*(1. + cx))/denom
        I424 = (cy*sx - cx*sy - 2.*ky2*sy*dx_h)/denom
        I414 = ((kx2 - 2.*ky2)*sx*sy - (1. - cx)*cy)/denom
        I423 = (cy*dx_h*(kx2 - 2*ky2) - ky2*sx*sy)/denom      #  I423 = I323' = ((2.*ky2)/kx2*(1 + cx)*cy - cx*cy - ky2*sx*sy)/denom + cy/kx2

    else:
        I144 = L4/12.                                          #  I144 = Gx * sy**2
        I133 = L2/2.                                           #  I133 = Gx * cy**2
        I134 = L3/6.                                           #  I134 = Gx * cy*sy
        I313 = L2/2.                                           #  I313 = Gy * cx*cy
        I324 = L4/12.                                          #  I324 = Gy * sx*sy
        I314 = L3/6.                                           #  I314 = Gy * cx*sy
        I323 = L3/6.                                           #  I323 = Gy * sx*cy
        I244 = L3/3.
        I233 = L
        I234 = L2/2.
        I413 = L
        I424 = L3/3.
        I414 = L2/2.
        I423 = L2/2.

    if kx == 0 and ky != 0:
        I336 = (h*L*(3.*L*cy + (2.*ky2*L2 - 3.)*sy))/(24.*ky2)
        I346 = (h*((3. - 2.*ky2*L2)*L*cy + 3.*(ky2*L2 - 1.)*sy))/(24.*ky4)
        I436 = I346
        I446 = (h*L*(-3.*L*cy + (3. + 2.*ky2*L2)*sy))/(24.*ky2)

        I533 = (h*(3.*L + 2.*ky2*L3 - 3.*sy*cy))/(24.*ky2)
        I534 = (h*(L2 - sy2))/(8.*ky2)
        I544 = (h*(-3.*L + 2.*ky2*L3 + 3.*sy*cy))/(24.*ky4)

    elif kx == 0 and ky == 0:
        I336 = (h*L4)/24.
        I346 = (h*L5)/40.
        I436 = (h*L3)/6.
        I446 = (h*L4)/8.

        I533 = h*L3/6.
        I534 = h*L4/24.
        I544 = h*L5/60.

    else:
        I336 = h/kx2*(I33 - I313)                                  #  I336 = Gy * dx*cy
        I346 = h/kx2*(I34 - I314)                                  #  I346 = Gy * dx*sy
        I436 = h/kx2*(I43 - I413)
        I446 = h/kx2*(I44 - I414)

        I533 = (h*(denom*L - 2.*(denom + 2.*ky2)*sx + kx2*cy*sy))/(2.*denom*kx2)
        I534 = (h*sy2 - 2*dx)/(2*denom)
        I544 = (sy2 - 2*dx_h)/denom

    K2 = k2/2.
    coef1 = 2.*ky2*h - h3 - K2
    coef3 = 2.*h2 - ky2

    t111 =    coef1*I111 + h*kx4*I122/2.
    t112 = 2.*coef1*I112 - h*kx2*I112
    t116 = 2.*coef1*I116 + coef3*I11 - h2*kx2*I122
    t122 =    coef1*I122 + 0.5*h*I111
    t126 = 2.*coef1*I126 + coef3*I12 + h2*I112
    t166 =    coef1*I166 + coef3*I16 + 0.5*h3*I122 - h*I10
    t133 =       K2*I133 - ky2*h*I10/2.
    t134 =    2.*K2*I134
    t144 =       K2*I144 - h*I10/2.

    t211 =    coef1*I211 + h*kx4*I222/2.
    t212 = 2.*coef1*I212 - h*kx2*I212
    t216 = 2.*coef1*I216 + coef3*I21 - h2*kx2*I222
    t222 =    coef1*I222 + 0.5*h*I211
    t226 = 2.*coef1*I226 + coef3*I22 + h2*I212
    t266 =    coef1*I266 + coef3*I26 + 0.5*h3*I222 - h*I20
    t233 =       K2*I233 - ky2*h*I20/2.
    t234 =    2.*K2*I234
    t244 =       K2*I244 - h*I20/2.

    coef2 = 2*(K2 - ky2*h)

    t313 = coef2*I313 + h*kx2*ky2*I324
    t314 = coef2*I314 - h*kx2*I323
    t323 = coef2*I323 - h*ky2*I314
    t324 = coef2*I324 + h*I313
    t336 = coef2*I336 + ky2*I33 - h2*ky2*I324
    t346 = coef2*I346 + h2*I323 + ky2*I34

    t413 = coef2*I413 + h*kx2*ky2*I424
    t414 = coef2*I414 - h*kx2*I423
    t423 = coef2*I423 - h*ky2*I414
    t424 = coef2*I424 + h*I413
    t436 = coef2*I436 - h2*ky2*I424 + ky2*I43
    t446 = coef2*I446 + h2*I423 + ky2*I44

    # Coordinates transformation from Curvilinear to a Cartesian
    cx_1 = -kx2*sx
    sx_1 = cx
    cy_1 = -ky2*sy
    sy_1 = cy
    dx_1 = h*sx
    T = zeros((6,6,6))
    T[0, 0, 0] = t111
    T[0, 0, 1] = t112 + h*sx
    T[0, 0, 5] = t116
    T[0, 1, 1] = t122
    T[0, 1, 5] = t126
    T[0, 5, 5] = t166
    T[0, 2, 2] = t133
    T[0, 2, 3] = t134
    T[0, 3, 3] = t144

    T[1, 0, 0] = t211 - h*cx*cx_1
    T[1, 0, 1] = t212 + h*sx_1 - h*(sx*cx_1 + cx*sx_1)
    T[1, 0, 5] = t216 - h*(dx*cx_1 + cx*dx_1)
    T[1, 1, 1] = t222 - h*sx*sx_1
    T[1, 1, 5] = t226 - h*(sx*dx_1 + dx*sx_1)
    T[1, 5, 5] = t266 - dx*h*dx_1
    T[1, 2, 2] = t233
    T[1, 2, 3] = t234
    T[1, 3, 3] = t244

    T[2, 0, 2] = t313
    T[2, 0, 3] = t314 + h*sy
    T[2, 1, 2] = t323
    T[2, 1, 3] = t324
    T[2, 2, 5] = t336
    T[2, 3, 5] = t346

    T[3, 0, 2] = t413 - h*cx*cy_1
    T[3, 0, 3] = t414 + (1 - cx)*h*sy_1
    T[3, 1, 2] = t423 - h*sx*cy_1
    T[3, 1, 3] = t424 - h*sx*sy_1
    T[3, 2, 5] = t436 - h*dx*cy_1
    T[3, 3, 5] = t446 - h*dx*sy_1
    """
    Path length difference
    linear = cx*h*x0 + h*sx*x0' + dx*h*dp;
    nonlinear = (h*T111 + 1/2*(cx')^2)*x0^2 + (h*T112 + cx'*sx')*x0*x0' + (h*T116 + cx'*dx')*x0*dp
                +(h*T122 + 1/2*(sx')^2)*(x0')^2 + (h*T126 + dx'*sx')*dp*x0' + (h*T166 + 1/2*(dx')^2)*dp^2
                +(h*T133 + 1/2*(cy')^2)*y0^2 + (h*T134 + cy'*sy')*y0*y0' + (h*T144 + 1/2*(sy')^2)*(y0')^2
    dl = Integrate(linear*ds + nonlinear*ds)
    """

    t511 =    coef1*I511 + h*kx4*I522/2.
    t512 = 2.*coef1*I512 - h*kx2*I512
    t516 = 2.*coef1*I516 + coef3*I51 - h2*kx2*I522
    t522 =    coef1*I522 + 0.5*h*I511
    t526 = 2.*coef1*I526 + coef3*I52 + h2*I512
    t566 =    coef1*I566 + coef3*I56 + 0.5*h3*I522 - h*I50
    t533 =       K2*I533 - ky2*h*I50/2.
    t534 =    2.*K2*I534
    t544 =       K2*I544 - h*I50/2.
    #print "asfd = ", L,  coef1, I522, (L + sx*cx)/4.
    i566 = h2*(L - sx*cx)/(4.*kx2) if kx != 0 else h2*L3/6.

    T511 = t511 + 1/4.*kx2*(L - cx*sx)
    T512 = t512 - (1/2.)*kx2*sx2 + h*dx
    T516 = t516 + h*(sx*cx - L)/2.
    T522 = t522 + (L + sx*cx)/4.
    T526 = t526 + h*sx2/2.
    T566 = t566 + i566
    T533 = t533 + 1/4.*ky2*(L - sy*cy )
    T534 = t534 - 1/2.*ky2*sy2
    T544 = t544 + (L + sy*cy)/4.

    T[4, 0, 0] = T511
    T[4, 0, 1] = T512
    T[4, 0, 5] = T516
    T[4, 1, 1] = T522
    T[4, 1, 5] = T526
    T[4, 5, 5] = T566
    T[4, 2, 2] = T533
    T[4, 2, 3] = T534
    T[4, 3, 3] = T544
    """
    print "T511 = ", T511
    print "T512 = ", T512
    print "T516 = ", T516
    print "T522 = ", T522
    print "T526 = ", T526
    print "T566 = ", T566
    print "T533 = ", T533
    print "T534 = ", T534
    print "T544 = ", T544



    print "t111 = ", t111
    print "t112 = ", t112
    print "t116 = ", t116
    print "t122 = ", t122
    print "t126 = ", t126
    print "t166 = ", t166
    print "t133 = ", t133
    print "t134 = ", t134
    print "t144 = ", t144
    print "t211 = ", t211
    print "t212 = ", t212
    print "t216 = ", t216
    print "t222 = ", t222
    print "t226 = ", t226
    print "t266 = ", t266
    print "t233 = ", t233
    print "t234 = ", t234
    print "t244 = ", t244
    print "t313 = ", t313
    print "t314 = ", t314
    print "t323 = ", t323
    print "t324 = ", t324
    print "t336 = ", t336
    print "t346 = ", t346
    print "t413 = ", t413
    print "t414 = ", t414
    print "t423 = ", t423
    print "t424 = ", t424
    print "t436 = ", t436
    print "t446 = ", t446
    """
    return T


def fringe_ent(h, k1, e, h_pole=0., gap=0., fint=0.):

    sec_e = 1./cos(e)
    sec_e2 = sec_e*sec_e
    sec_e3 = sec_e2*sec_e
    tan_e = tan(e)
    tan_e2 = tan_e*tan_e
    phi = fint*h*gap*sec_e*(1. + sin(e)**2)
    R = eye(6)
    R[1,0] = h*tan_e
    R[3,2] = -h*tan(e - phi)
    #print R

    T = zeros((6,6,6))
    T[0, 0, 0] = -h/2.*tan_e2
    T[0, 2, 2] = h/2.*sec_e2
    T[1, 0, 0] = h/2.*h_pole*sec_e3 + k1*tan_e
    T[1, 0, 1] = h*tan_e2
    T[1, 0, 5] = -h*tan_e
    T[1, 2, 2] = (-k1 + h*h/2. + h*h*tan_e2)*tan_e - h/2.*h_pole*sec_e3
    T[1, 2, 3] = -h*tan_e2
    T[2, 0, 2] = h*tan_e2
    T[3, 0, 2] = -h*h_pole*sec_e3 - 2*k1*tan_e
    T[3, 0, 3] = -h*tan_e2
    T[3, 1, 2] = -h*sec_e2
    T[3, 2, 5] = h*tan_e - h*phi/cos(e - phi)**2
    return R, T

def fringe_ext(h, k1, e, h_pole=0., gap=0., fint=0.):

    sec_e = 1./cos(e)
    sec_e2 = sec_e*sec_e
    sec_e3 = sec_e2*sec_e
    tan_e = tan(e)
    tan_e2 = tan_e*tan_e
    phi = fint*h*gap*sec_e*(1. + sin(e)**2)
    R = eye(6)

    R[1,0] = h*tan_e
    R[3,2] = -h*tan(e - phi)
    #print R

    T = zeros((6,6,6))
    T[0,0,0] = h/2.*tan_e2
    T[0,2,2] = -h/2.*sec_e2
    T[1,0,0] = h/2.*h_pole*sec_e3 - (-k1 + h*h/2.*tan_e2)*tan_e
    T[1,0,1] = -h*tan_e2
    T[1,0,5] = -h*tan_e
    T[1,2,2] = (-k1 - h*h/2.*tan_e2)*tan_e - h/2.*h_pole*sec_e3
    T[1,2,3] = h*tan_e2
    T[2,0,2] = -h*tan_e2
    T[3,0,2] = -h*h_pole*sec_e3 +(-k1 + h*h*sec_e2)*tan_e
    T[3,0,3] = h*tan_e2
    T[3,1,2] = h*sec_e2
    T[3,2,5] = h*tan_e - h*phi/cos(e - phi)**2
    return R, T

def H23(vec_x, h, k1, k2, beta=1., g_inv=0.):
    """
    H2 = (px**2 + py**2)/2 + (h**2 + k1)*x**2/2 - (k1*y**2)/2 - (h*pt*x)/beta
    H3 = (h*x - ps/beta)*(px**2 + py**2)/2 + (2*h*k1 + k2)*(x**3)/6 - (h*k1 + k2)*(x*y**2)/2 - ps/(beta*gamma**2*(1. + beta))
    H23 = H2 + H3
    :param vec_x: [x, px, y, py, sigma, psigma]
    :param h: curvature
    :param k1: quadrupole strength
    :param k2: sextupole strength
    :param beta: = 1, velocity
    :param g_inv: 1/gamma, by default 0.
    :return: [x', px', y', py', sigma', psigma']
    """
    #print "H23: ", vec_x
    x = vec_x[0]
    px = vec_x[1]
    y = vec_x[2]
    py = vec_x[3]
    ps = vec_x[5]
    px2 = px*px
    py2 = py*py
    x1 = px*(1. + h*x - ps/beta)
    px1 = -(h*h + k1)*x + (h*ps)/beta + (-h*(px2 + py2) - (2.*h*k1 + k2)*x*x + (h*k1 + k2)*y*y)/2.
    y1 = py*(1. + h*x - ps/beta)
    py1 = k1*y + (h*k1 + k2)*x*y
    sigma1 = -(h*x)/beta - ((px2 + py2)/(2.*beta)) - g_inv*g_inv/(beta*(1. + beta))
    return [x1, px1, y1, py1, sigma1, 0.]

from copy import copy
def verlet(vec_x, step, h, k1, k2, beta=1., g_inv=0.):
    """
    q_{n+1} = q_{n} + h * dH(p_{n}, q_{n+1})/dp
    p_{n+1} = p_{n} - h * dH(p_{n}, q_{n+1})/dq
    """
    #vec_x0 = copy(vec_x)
    x =     vec_x[0::6]
    px =    vec_x[1::6]
    y =     vec_x[2::6]
    py =    vec_x[3::6]
    sigma = vec_x[4::6]
    ps =    vec_x[5::6]
    #print "1: verlet: ", x[:3], px[:3], y[:3], py[:3], sigma[:3], ps[:3]
    x1 = (x + step*px*(1. - ps/beta))/(1. - step*h*px)
    y1 = y + step*py*(1. + h*x1 - ps/beta)
    sigma1 = sigma + step*(-(h*x1)/beta - ((px*px + py*py)/(2.*beta)) - g_inv*g_inv/(beta*(1. + beta)))
    #print "verlet: ", [x1, px, y1, py, sigma1, ps]
    vec0 = H23([x1, px, y1, py, sigma1, ps], h, k1, k2, beta, g_inv)
    #print "verlet: ", vec0
    px1 = px + step*vec0[1]
    py1 = py + step*vec0[3]
    ps1 = ps + step*vec0[5]
    #print "verlet: params : h = ", h, k1, k2
    #print "2: verlet: ", x1[:3], px1[:3], y1[:3], py1[:3], sigma1[:3], ps1[:3]
    #w = zeros(len(vec_x))
    vec_x[0::6] = x1[:]
    vec_x[1::6] = px1[:]
    vec_x[2::6] = y1[:]
    vec_x[3::6] = py1[:]
    vec_x[4::6] = sigma1[:]
    vec_x[5::6] = ps1[:]
    #vec_x[:] = w[:]
    return vec_x

def sym_map(z, X, h, k1, k2, energy=0.):

    if h != 0 or k1 != 0:
        step = 0.005
    else:
        step = z
    if step > z:
        step = z
    #print z, h, k1, k2
    n = int(z/step) + 1
    gamma = energy/m_e_GeV
    g_inv = 0.
    beta = 1.
    if gamma !=0:
        g_inv = 1/gamma
        beta = sqrt(1. - g_inv*g_inv)
    z_array = linspace(0., z, num=n)
    #print z_array
    step = z_array[1] - z_array[0]
    #print len(X)
    for i in linspace(0., z, num=(n-1)):

        X = verlet(X, step, h, k1, k2, beta=beta, g_inv=g_inv)

    return X


"""
def rot_mtx(angle):
    return array([[cos(angle), 0., sin(angle), 0., 0., 0.],
                    [0., cos(angle), 0., sin(angle), 0., 0.],
                    [-sin(angle), 0., cos(angle), 0., 0., 0.],
                    [0., -sin(angle), 0., cos(angle), 0., 0.],
                    [0., 0., 0., 0., 1., 0.],
                    [0., 0., 0., 0., 0., 1.]])

def transform_vec(X, dx, dy, tilt):
    n = len(X)
    for i in range(n/6):
        X0 = X[6*i:6*(i+1)]
        X0 -= array([dx, 0.,dy,0.,0.,0.])
        X[6*i:6*(i+1)] = dot(rot_mtx(tilt), X0)
    return X

def t_apply(R, T, X, dx, dy, tilt):

    if dx != 0 or dy != 0 or tilt != 0:
        X = transform_vec(X, dx, dy, tilt)

    n = len(X)
    Xr = transpose(dot(R, transpose(X.reshape(n/6,6)))).reshape(n)
    Xt = zeros(n)
    x, px, y, py, tau, dp = X[0::6], X[1::6],X[2::6], X[3::6], X[4::6], X[5::6]

    Xt[0::6] = T[0, 0, 0]*x*x + T[0, 0, 1]*x*px + T[0, 0, 5]*x*dp + T[0, 1, 1]*px*px + T[0, 1, 5]*px*dp + \
               T[0, 5, 5]*dp*dp + T[0, 2, 2]*y*y + T[0, 2, 3]*y*py + T[0, 3, 3]*py*py

    Xt[1::6] = T[1, 0, 0]*x*x + T[1, 0, 1]*x*px + T[1, 0, 5]*x*dp + T[1, 1, 1]*px*px + T[1, 1, 5]*px*dp + \
               T[1, 5, 5]*dp*dp + T[1, 2, 2]*y*y + T[1, 2, 3]*y*py + T[1, 3, 3]*py*py

    Xt[2::6] = T[2, 0, 2]*x*y + T[2, 0, 3]*x*py + T[2, 1, 2]*px*y + T[2, 1, 3]*px*py + T[2, 2, 5]*y*dp + T[2, 3, 5]*py*dp

    Xt[3::6] = T[3, 0, 2]*x*y + T[3, 0, 3]*x*py + T[3, 1, 2]*px*y + T[3, 1, 3]*px*py + T[3, 2, 5]*y*dp + T[3, 3, 5]*py*dp

    Xt[4::6] = T[4, 0, 0]*x*x + T[4, 0, 1]*x*px + T[4, 0, 5]*x*dp + T[4, 1, 1]*px*px + T[4, 1, 5]*px*dp + \
               T[4, 5, 5]*dp*dp + T[4, 2, 2]*y*y + T[4, 2, 3]*y*py + T[4, 3, 3]*py*py

    X[:] = Xr[:] + Xt[:]

    if dx != 0 or dy != 0 or tilt != 0:
        X = transform_vec(X, -dx, -dy, -tilt)

    return X
"""

"""
def symp_kick2(X, h, k1, k2, ndivs = 1):

    beta = 1.
    gamma2_inv = 0.
    L = length/ndivs
    R_2 = R_z(L/2.)
    n = len(X)
    for i in range(ndivs):
        Xr = transpose(dot(R_2, transpose(X.reshape(n/6,6)))).reshape(n)
        Xt = zeros(n)
        x, px, y, py, tau, dp = Xr[0::6], Xr[1::6], Xr[2::6], Xr[3::6], Xr[4::6], Xr[5::6]

        px2 = px*px
        py2 = py*py

        Xt[0::6] = x + L*px*(h*x - dp/beta)
        Xt[1::6] = px + -0.5*L*(h*(px2 + py2) + (2.*h*k1 + k2)*x*x - (h*k1 + k2)*y*y)

        Xt[2::6] = y + L*py*(h*x - dp/beta)
        Xt[3::6] = py + L*(h*k1 + k2)*x*y

        Xt[4::6] = tau + L*(-(px2 + py2)/(2*beta) - gamma2_inv/(beta*(1+beta)))
        X = transpose(dot(R_2, transpose(Xt.reshape(n/6,6)))).reshape(n)
    return X
"""

"""


        I111 = 1./3.*(sx2 + dx_h)                                                    #  I111 = Gx * cx**2
        I122 = dx_h*dx_h/3.                                                          #  I122 = Gx * sx**2
        I112 = sx*dx_h/3.                                                            #  I112 = Gx * cx*sx
        I11  = L*sx/2.                                                               #  I11  = Gx * cx
        I116 = h/kx2*(I11 - I111)                  if kx != 0 else h*L4/24.          #  I116 = Gx * cx*dx
        I12  = 0.5/kx2*(sx - L*cx)                 if kx != 0 else L3/6.             #  I12  = Gx * sx
        I126 = h/kx2*(I12 - I112)                  if kx != 0 else h*L5/40.          #  I126 = Gx * sx*dx
        I10  = dx_h                                                                  #  I10  = Gx
        I16  = h/kx2*(dx_h - L*sx/2.)              if kx != 0 else h*L4/24.          #  I16  = Gx * dx
        I166 = h2/kx4*(I10 - 2*I11 + I111)         if kx != 0 else h2*L5*L/120.      #  I166 = Gx * dx**2
        I144 = (sy2 - 2.*dx_h)/denom               if non_drift else L4/12.          #  I144 = Gx * sy**2
        I133 = dx_h - ky2*(sy2 - 2.*dx_h)/denom    if non_drift else L2/2.           #  I133 = Gx * cy**2
        I134 = (sy*cy - sx)/denom                  if non_drift else L3/6.           #  I134 = Gx * cy*sy
        I313 = (kx2*cy*dx_h - 2.*ky2*sx*sy)/denom  if non_drift else L2/2.           #  I313 = Gy * cx*cy
        I324 = (2.*cy*dx_h - sx*sy)/denom          if non_drift else L4/12.          #  I324 = Gy * sx*sy
        I314 = (2.*cy*sx - (1. + cx)*sy)/denom     if non_drift else L3/6.           #  I314 = Gy * cx*sy
        I323 = (sy - cy*sx - 2.*ky2*sy*dx_h)/denom if non_drift else L3/6.           #  I323 = Gy * sx*cy = (2*ky2/kx2*(1 + cx)*sy - cy*sx)/denom + sy/kx2
        I33  = L*sy/2.                                                               #  I33  = Gy * cy
        I34  = (sy - L*cy)/(2.*ky2)                if ky !=0. else L3/6.             #  I34  = Gy * sy
        I336 = h/kx2*(I33 - I313)                                                    #  I336 = Gy * dx*cy
        I346 = h/kx2*(I34 - I314)                                                    #  I346 = Gy * dx*sy

        #derivative of Integrals
        I211 = sx/3.*(1. + 2.*cx)
        I222 = 2.*dx_h*sx/3.
        I212 = 1./3.*(2*sx2 - dx_h)
        I21  = 1./2.*(L*cx + sx)
        I216 = h/kx2*(I21 - I211)
        I22  = I11
        I226 = h/kx2*(I22 - I212)
        I20  = sx
        I26  = h /(2.*kx2)*(sx - L*cx)
        I266 = h2/kx4*(I20 - 2.*I21 + I211)
        I244 = 2.*(cy*sy - sx)/denom                           if non_drift else L3/3.
        I233 = sx + 2.*ky2*(cy*sy - sx)/denom                  if non_drift else L
        I234 = (kx2*dx_h - 2.*ky2*sy2)/denom                   if non_drift else L2/2.
        I413 = ((kx2 - 2.*ky2)*cy*sx - ky2*sy*(1. + cx))/denom if non_drift else L
        I424 = (cy*sx - cx*sy - 2.*ky2*sy*dx_h)/denom          if non_drift else L3/3.
        I414 = ((kx2 - 2.*ky2)*sx*sy - (1. - cx)*cy)/denom     if non_drift else L2/2.
        I423 = (cy*dx_h*(kx2 - 2*ky2) - ky2*sx*sy)/denom       if non_drift else L2/2.   #  I423 = I323' = ((2.*ky2)/kx2*(1 + cx)*cy - cx*cy - ky2*sx*sy)/denom + cy/kx2
        I43  = 0.5*(L*cy + sy)
        I436 = h/kx2*(I43 - I413)
        I44  = I33
        I446 = h/kx2*(I44 - I414)
"""



