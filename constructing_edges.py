import Rhino.Geometry as rg
import random
import math

def construct_directed_pt_with_length(pt_a, pt_b, scale = 50.0, noise_delta = .2):
    multiplier = rnd_multiplier(scale, noise_delta)
    dir_v = construct_direction(pt_a, pt_b)

    return rg.Point3d(pt_a + multiplier * dir_v)

def construct_direction(pt_a, pt_b):
    v = rg.Vector3d(pt_b - pt_a)
    v.Unitize()

    return v

def construct_midpoint(pt_a, pt_b):
    return rg.Point3d( (pt_a + pt_b) * .5 )

def project_point(pt_a, plane = rg.Plane.WorldXY):
    return plane.ClosestPoint(pt_a)

def rnd_multiplier(base, noise_delta):
    return base * (1.0 + .5 * random.random() * noise_delta)

def construct_single_pln(pt_a, pt_b):
    return rg.Plane(pt_a, rg.Vector3d(pt_b - pt_a) )

def construct_mulitple_plns(pt_a, pt_bs, top = False):
    b_pt = rg.Point3d(0,0,0)
    for pt_b in pt_bs:
        b_pt += pt_b

    b_pt /= len(pt_bs)
    v_b = rg.Vector3d(b_pt - pt_a)
    
    plns = []
    for pt_b in pt_bs:
        o_pt = pt_b if top else pt_a
            
        plns.append(construct_pln_2vs(
            o_pt,
            rg.Vector3d(pt_b - pt_a),
            v_b
        ))

    return plns

def construct_pln_2vs(pt_a, v_a, v_b):
    v_a, v_b = rg.Vector3d(v_a), rg.Vector3d(v_b)
    v_a.Unitize()
    v_b.Unitize()
    
    if v_a.IsParallelTo(v_b, .001) and not( v_a.IsParallelTo(rg.Plane.WorldXY.XAxis) ):
        pln = rg.Plane(pt_a, v_a)
    elif v_a.IsParallelTo(v_b, .001):
        pln = rg.Plane.WorldYZ
    else:
        pln_ref = rg.Plane(pt_a, v_a, v_b)
        pln = rg.Plane(pt_a, pln_ref.YAxis, pln_ref.ZAxis)

    return pln

def points_in_plane(pln = rg.Plane.WorldXY, width = 12.0, noise = .2, phase = None, phase_noise = .2, cnt = 4):
    pts = []
    alfa = math.pi * 2.0 / cnt

    phase = .0 * math.pi if phase is None else phase

    for i in range(cnt):
        loc_alfa = phase + i * alfa + rnd_multiplier(alfa, phase_noise)
        _x, _y = math.cos(loc_alfa), math.sin(loc_alfa)
        w_val = rnd_multiplier(width, noise)
        
        pts.append(rg.Point3d(
            pln.XAxis * w_val * _x + 
            pln.YAxis * w_val * _y +
            pln.Origin
        ))

    return pts

def construct_top_faces(pt_a, pt_bs, h_top = 50.0, w_bot = 12.0):
    return [points_in_plane(pln, width = w_bot) for pln in construct_mulitple_plns(
        pt_a, pt_bs, True
    )]

def face_single_bot_pt(pt_a, pt_b, h_top = 50.0, w_bot = 12.0, phase = 0.0):
    return [points_in_plane(
        pln = construct_mulitple_plns(pt_a, [pt_b], True)[0],
        width = w_bot
    )]

def face_pair_bot_pts(pt_a, pt_bs, h_top = 50.0, w_bot = 12.0):
    return [points_in_plane(pln, width = w_bot) for pln in construct_mulitple_plns(
        pt_a, pt_bs, True
    )]

def face_3or_more_top_pts(pt_a, pt_bs, h_top = 50.0, w_bot = 12.0):
    return [points_in_plane(pln, width = w_bot) for pln in construct_mulitple_plns(
        pt_a, pt_bs, True
    )]

def construct_top_pts(pt_a, pt_bs, h_top = 50.0, w_bot = 12.0):
    if len(pt_bs) > 0:
        return construct_top_faces(pt_a, pt_bs, h_top = 50.0, w_bot = 12.0)
    else:
        return None
    # if len(pt_bs) == 1:
    #     return face_single_top_pt(pt_a, pt_bs, h_top = 50.0, w_bot = 12.0)
    # elif len(pt_bs) == 2:
    #     return face_pair_top_pts(pt_a, pt_bs, h_top = 50.0, w_bot = 12.0)
    # elif len(pt_bs) == 0:
    #     return None
    # else:
    #     return face_3or_more_top_pts(pt_a, pt_bs, h_top = 50.0, w_bot = 12.0)

def construct_bottom_faces(pt_a, pt_bs):
    if len(pt_bs) < 1:
        return None
    elif len(b_pts) == 1:
        return face_single_bot_pt(pt_a, pt_b, h_top = 50.0, w_bot = 12.0, phase = 0.0)
    else:


