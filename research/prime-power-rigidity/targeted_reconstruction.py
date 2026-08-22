#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
from math import isqrt
from typing import Sequence
Pair=tuple[int,int]
def is_square(n:int)->bool:
    if n<0:return False
    r=isqrt(n);return r*r==n
def gaussian_mul(z:Pair,w:Pair)->Pair:return(z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def gaussian_pow(z:Pair,e:int)->Pair:
    if e<0:z=(z[0],-z[1]);e=-e
    out=(1,0)
    while e:
        if e&1:out=gaussian_mul(out,z)
        z=gaussian_mul(z,z);e>>=1
    return out
def column_monomial(indices:Sequence[Sequence[int]],generators:Sequence[Pair],column:int)->Pair:
    block=(2,1,1);out=(1,0)
    for row,g in enumerate(generators):
        j=int(indices[row][column]);k=block[row]
        out=gaussian_mul(out,gaussian_pow(g,2*(k+j)))
        out=gaussian_mul(out,gaussian_pow((g[0],-g[1]),2*(k-j)))
    return out
def exact_offsets(indices,generators):return tuple(abs(column_monomial(indices,generators,c)[1]) for c in range(4))
def center_root(generators):
    n=[a*a+b*b for a,b in generators];return n[0]*n[0]*n[1]*n[2]
@dataclass(frozen=True)
class Verification:
    coupled:bool;square_embeddings:bool;positive:bool;distinct:bool;entries:tuple[int,...]
def verify_candidate(indices,generators):
    d=exact_offsets(indices,generators);coupled={d[2],d[3]}=={d[0]+d[1],abs(d[0]-d[1])};e=center_root(generators);E=e*e
    entries=tuple([E]+[E-x for x in d]+[E+x for x in d]);sq=all(is_square(E-x) and is_square(E+x) for x in d)
    return Verification(coupled,sq,all(x>0 for x in entries),len(set(entries))==9,entries)
def is_full_magic_square(indices,generators):
    v=verify_candidate(indices,generators);return v.coupled and v.square_embeddings and v.positive and v.distinct
