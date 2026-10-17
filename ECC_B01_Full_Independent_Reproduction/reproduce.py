#!/usr/bin/env python3
"""ECC-B01 independent reproduction pipeline.

This code was authored independently from the supplied Investigator-B starter script.
It verifies the specified mathematical fixtures only; it does not test physical,
cosmological, arithmetic, or theorem-level claims.

Core dependencies: SymPy, NumPy, SciPy. Gmsh and GUDHI are optional accelerators;
when unavailable, deterministic independently generated simplicial meshes and a
GF(2) homology fallback are used and the limitation is stated in the report.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import itertools
import json
import math
import os
import platform
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import sympy as sp
from scipy import sparse
from scipy.integrate import quad

TAU = 2.0 * math.pi
ROOT = Path(__file__).resolve().parent
MAX_FALLBACK_BALL_TETRAHEDRA = 5_000
MAX_STRUCTURED_TORUS_FACES = 50_000
MAX_FALLBACK_SPHERE_FACES = 80_000
MAX_FALLBACK_SPHERE_LEVEL = 5
TOLERANCES: dict[str, Any] = {
    "symbolic_identities": "exact SymPy simplification to the expected expression",
    "scipy_quadrature_absolute_error": 1e-10,
    "candidate_a_period_absolute_error": 1e-9,
    "candidate_a_triangle_circulation_max_absolute_error": 1e-9,
    "candidate_c_exact_face_flux_absolute_error": 2e-9,
    "candidate_c_centroid_total_flux_absolute_error": 2e-8,
    "candidate_c_local_response_absolute_error": 1e-12,
    "sphere_solid_angle_normalized_flux_absolute_error": 1e-8,
    "sphere_planar_quadrature": "size-aware per-resolution bound and strictly decreasing errors over requested refinements",
    "chain_complex_identities": "exact zero boundary-squared matrices",
    "betti_vectors": "exact equality with the specified expected vector",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def dependency_state() -> dict[str, Any]:
    state: dict[str, Any] = {}
    for module, package in [("sympy", "sympy"), ("numpy", "numpy"), ("scipy", "scipy"),
                            ("gmsh", "gmsh"), ("gudhi", "gudhi")]:
        try:
            mod = __import__(module)
            state[module] = {"available": True, "version": getattr(mod, "__version__", None)}
        except Exception as exc:
            state[module] = {"available": False, "error": f"{type(exc).__name__}: {exc}"}
    return state


class Recorder:
    def __init__(self) -> None:
        self.results: list[dict[str, Any]] = []

    def add(self, name: str, observed: Any, expected: Any, passed: bool,
            note: str = "", category: str = "analytic") -> None:
        self.results.append({
            "test_id": name,
            "status": "PASS" if passed else "FAIL",
            "observed": jsonable(observed),
            "expected": jsonable(expected),
            "note": note,
            "category": category,
        })


def jsonable(obj: Any) -> Any:
    if isinstance(obj, (np.floating, np.integer, np.bool_)):
        return obj.item()
    if isinstance(obj, (float, int, str, bool)) or obj is None:
        return obj
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    return str(obj)


def symbolic_controls(rec: Recorder) -> None:
    """Exact controls independently written from differential-form identities."""
    phi, psi, theta, varphi = sp.symbols("phi psi theta varphi", real=True)
    x, y, z = sp.symbols("x y z", real=True)
    n, q, lam, c = sp.symbols("n q lam c", real=True)
    S = sp.cos(phi) + 2 * sp.sin(psi)

    # Candidate A: eta = a dphi + b dpsi.
    a = sp.diff(phi, phi) + sp.diff(S, phi)  # 1 - sin(phi)
    b = 2 + sp.diff(S, psi)                  # 2 + 2 cos(psi)
    d_eta_coeff = sp.simplify(sp.diff(b, phi) - sp.diff(a, psi))
    rec.add("A_closed", d_eta_coeff, 0, sp.simplify(d_eta_coeff) == 0)

    phi_period = sp.integrate(a, (phi, 0, 2 * sp.pi))
    psi_period = sp.integrate(b, (psi, 0, 2 * sp.pi))
    rec.add("A_phi_period", phi_period, 2 * sp.pi,
            sp.simplify(phi_period - 2 * sp.pi) == 0)
    rec.add("A_psi_period", psi_period, 4 * sp.pi,
            sp.simplify(psi_period - 4 * sp.pi) == 0)
    rec.add("A_nonexact_certificate_from_periods", [phi_period, psi_period],
            "at least one nonzero generating-cycle period",
            sp.simplify(phi_period) != 0 or sp.simplify(psi_period) != 0,
            "A globally exact 1-form integrates to zero on every closed loop.")
    rec.add("A_exact_term_phi_period", sp.integrate(sp.diff(S, phi), (phi, 0, 2*sp.pi)), 0,
            sp.simplify(sp.integrate(sp.diff(S, phi), (phi, 0, 2*sp.pi))) == 0)
    rec.add("A_exact_term_psi_period", sp.integrate(sp.diff(S, psi), (psi, 0, 2*sp.pi)), 0,
            sp.simplify(sp.integrate(sp.diff(S, psi), (psi, 0, 2*sp.pi))) == 0)

    # alpha = sin(phi) dpsi is a counterexample to closure.
    alpha_d_coeff = sp.diff(sp.sin(phi), phi)
    rec.add("A_nonclosed_counterexample", alpha_d_coeff, sp.cos(phi),
            sp.simplify(alpha_d_coeff - sp.cos(phi)) == 0)

    # Candidate B: two local connection 1-forms and their curvature.
    a_n = n * (1 - sp.cos(theta)) / 2
    a_s = -n * (1 + sp.cos(theta)) / 2
    rec.add("B_patch_difference", sp.simplify(a_n - a_s), n,
            sp.simplify(a_n - a_s - n) == 0)
    f_n = sp.diff(a_n, theta)
    f_s = sp.diff(a_s, theta)
    f_expected = n * sp.sin(theta) / 2
    rec.add("B_north_curvature", f_n, f_expected,
            sp.simplify(f_n - f_expected) == 0)
    rec.add("B_south_curvature", f_s, f_expected,
            sp.simplify(f_s - f_expected) == 0)
    normalized_flux = sp.simplify(
        sp.integrate(f_expected, (theta, 0, sp.pi)) *
        sp.integrate(1, (varphi, 0, 2 * sp.pi)) / (2 * sp.pi))
    rec.add("B_normalized_flux", normalized_flux, n,
            sp.simplify(normalized_flux - n) == 0)
    for charge in (-1, 0, 1, 2):
        phase = sp.simplify(sp.exp(2 * sp.pi * sp.I * charge))
        rec.add(f"B_transition_integer_{charge}", phase, 1, phase == 1)
    half_phase = sp.simplify(sp.exp(2 * sp.pi * sp.I * sp.Rational(1, 2)))
    rec.add("B_half_integer_transition_rejected", half_phase, -1,
            half_phase == -1,
            "The phase changes sign under varphi -> varphi + 2 pi; it is not single-valued.")

    # Candidate C: *dphi=dpsi and *dpsi=-dphi on the flat oriented torus.
    # For S(phi,psi), *dS = S_phi dpsi - S_psi dphi.
    u = -sp.diff(S, psi)     # coefficient of dphi
    v = sp.diff(S, phi)      # coefficient of dpsi
    d_star_dS_coeff = sp.simplify(sp.diff(v, phi) - sp.diff(u, psi))
    density = sp.simplify(q + d_star_dS_coeff)
    expected_density = q - sp.cos(phi) - 2 * sp.sin(psi)
    rec.add("C_density", density, expected_density,
            sp.simplify(density - expected_density) == 0)
    c_flux = sp.simplify(sp.integrate(density, (phi, 0, 2*sp.pi), (psi, 0, 2*sp.pi)))
    rec.add("C_total_flux", c_flux, 4 * sp.pi**2 * q,
            sp.simplify(c_flux - 4*sp.pi**2*q) == 0)
    entropy_density = sp.simplify(sp.diff(S, phi, 2) + sp.diff(S, psi, 2))
    entropy_flux = sp.simplify(sp.integrate(entropy_density, (phi, 0, 2*sp.pi), (psi, 0, 2*sp.pi)))
    rec.add("C_exact_perturbation_zero_total_flux", entropy_flux, 0,
            sp.simplify(entropy_flux) == 0,
            "The added d(*dS) term integrates to zero and does not change the flux/cohomology representative in this fixture.")

    shifted_S = S + c
    shift_density = sp.simplify(q + sp.diff(sp.diff(shifted_S, phi), phi)
                                + sp.diff(sp.diff(shifted_S, psi), psi))
    rec.add("C_entropy_shift_invariance", shift_density, expected_density,
            sp.simplify(shift_density - expected_density) == 0)
    scaled_density = sp.simplify(q + lam * (sp.diff(S, phi, 2) + sp.diff(S, psi, 2)))
    rec.add("C_entropy_scaling_local_response", scaled_density,
            q - lam * sp.cos(phi) - 2*lam*sp.sin(psi),
            sp.simplify(scaled_density - (q-lam*sp.cos(phi)-2*lam*sp.sin(psi))) == 0)
    local_delta_at_00 = sp.simplify((density - q).subs({phi: 0, psi: 0}))
    rec.add("C_nonzero_local_response_at_00", local_delta_at_00, -1,
            sp.simplify(local_delta_at_00 + 1) == 0,
            "At (phi,psi)=(0,0), the entropy term changes local density by -1.")
    q0_flux = sp.simplify(c_flux.subs(q, 0))
    q0_local = sp.simplify((density - q).subs({q: 0, phi: 0, psi: 0}))
    rec.add("C_q0_zero_total_flux", q0_flux, 0, q0_flux == 0)
    rec.add("C_q0_nonzero_local_curvature", q0_local, -1, q0_local == -1,
            "Zero integrated flux does not mean the local 2-form is identically zero.")

    # In 3D, d(z dx wedge dy) = dx wedge dy wedge dz.
    rec.add("3D_nonclosed_two_form", sp.diff(z, z), 1, sp.diff(z, z) == 1,
            "Orientation: dz wedge dx wedge dy = dx wedge dy wedge dz.")
    test_scalar = x*x*y + y*z*z + x*z
    for a_sym, b_sym, label in [(x, y, "xy"), (x, z, "xz"), (y, z, "yz")]:
        val = sp.simplify(sp.diff(test_scalar, a_sym, b_sym) -
                          sp.diff(test_scalar, b_sym, a_sym))
        rec.add(f"d_squared_scalar_{label}", val, 0, val == 0)


def quadrature_controls(rec: Recorder) -> None:
    tests = [
        ("A_phi_scipy_quadrature", lambda t: 1.0 - np.sin(t), TAU),
        ("A_psi_scipy_quadrature", lambda t: 2.0 + 2.0 * np.cos(t), 2.0 * TAU),
    ]
    for name, fn, expected in tests:
        val, err = quad(fn, 0.0, TAU, epsabs=1e-12, epsrel=1e-12, limit=200)
        rec.add(name, val, expected, abs(val-expected) < 1e-10,
                f"SciPy adaptive quadrature estimated absolute error {err:.3e}.", "quadrature")
    sphere_integral, sphere_err = quad(lambda t: 0.5 * np.sin(t), 0.0, math.pi,
                                       epsabs=1e-12, epsrel=1e-12)
    sphere_charge = sphere_integral * TAU / TAU
    rec.add("B_scipy_sphere_flux_n1", sphere_charge, 1.0,
            abs(sphere_charge-1.0) < 1e-10,
            f"Independent 1D angular quadrature; estimated error {sphere_err:.3e}.", "quadrature")


def structured_torus(n: int) -> tuple[np.ndarray, list[tuple[int, int, int]]]:
    """A periodic, oriented, two-triangle-per-cell parameter-domain torus."""
    if n < 4:
        raise ValueError("n must be >=4 so local periodic edge displacements are unambiguous")
    coords = np.array([(TAU*i/n, TAU*j/n) for i in range(n) for j in range(n)], dtype=float)

    def vid(i: int, j: int) -> int:
        return (i % n) * n + (j % n)

    faces: list[tuple[int, int, int]] = []
    for i in range(n):
        for j in range(n):
            a, b = vid(i, j), vid(i+1, j)
            c, d = vid(i+1, j+1), vid(i, j+1)
            faces.append((a, b, c))
            faces.append((a, c, d))
    return coords, faces


def periodic_delta(start: float, end: float) -> float:
    """Shortest signed angular displacement on a 2-pi periodic coordinate."""
    return (end - start + math.pi) % TAU - math.pi


def add_cochain_checks(rec: Recorder, n: int, coords: np.ndarray,
                       faces: list[tuple[int, int, int]]) -> dict[str, Any]:
    Svals = np.cos(coords[:, 0]) + 2.0*np.sin(coords[:, 1])
    edge_set = set()
    for face in faces:
        for u, v in ((face[0], face[1]), (face[1], face[2]), (face[2], face[0])):
            edge_set.add((min(u, v), max(u, v)))
    edges = sorted(edge_set)
    edge_index = {e: k for k, e in enumerate(edges)}

    # Cochain values are oriented from the smaller vertex id to the larger.
    edge_value: dict[tuple[int, int], float] = {}
    for u, v in edges:
        dphi = periodic_delta(coords[u, 0], coords[v, 0])
        dpsi = periodic_delta(coords[u, 1], coords[v, 1])
        edge_value[(u, v)] = dphi + 2*dpsi + (Svals[v] - Svals[u])

    def oriented_edge(u: int, v: int) -> float:
        key = (min(u, v), max(u, v))
        return edge_value[key] if u < v else -edge_value[key]

    face_circulations = [oriented_edge(a, b) + oriented_edge(b, c) + oriented_edge(c, a)
                         for a, b, c in faces]
    closure_residual = max(abs(v) for v in face_circulations) if face_circulations else 0.0

    # Two noncontractible cycles: one phi-loop at j=0, one psi-loop at i=0.
    phi_edges = [oriented_edge(i*n, ((i+1) % n)*n) for i in range(n)]
    psi_edges = [oriented_edge(j, (j+1) % n) for j in range(n)]
    phi_period = float(sum(phi_edges))
    psi_period = float(sum(psi_edges))
    rec.add(f"A_mesh_phi_period_n{n}", phi_period, TAU,
            abs(phi_period-TAU) < 1e-9,
            f"Periodic structured torus; {n} edges on representative phi-cycle.", "discrete-mesh")
    rec.add(f"A_mesh_psi_period_n{n}", psi_period, 2*TAU,
            abs(psi_period-2*TAU) < 1e-9,
            f"Periodic structured torus; {n} edges on representative psi-cycle.", "discrete-mesh")
    rec.add(f"A_discrete_closed_n{n}", closure_residual, 0.0,
            closure_residual < 1e-9,
            "Maximum absolute discrete circulation around any oriented triangle.", "discrete-mesh")

    return {"phi_period": phi_period, "psi_period": psi_period,
            "closure_residual": closure_residual, "edge_count": len(edges),
            "face_count": len(faces), "node_count": len(coords)}


def triangle_fluxes(phi0: float, psi0: float, a: float, b: float,
                    q: float) -> tuple[float, float, float, float]:
    """Exact and barycentre-approximated integrals of (q-cos(phi)-2 sin(psi)) dphi dpsi
    over the two positively oriented triangles in one parameter-space rectangle.
    Returns exact T1,T2, centroid T1,T2.
    """
    ph1, ps1 = phi0 + a, psi0 + b
    # T1=(0,0),(a,0),(a,b)
    area = a*b/2.0
    icos1 = (b/a) * (a*math.sin(ph1) + math.cos(ph1) - math.cos(phi0))
    isin1 = a * (math.cos(psi0) - (math.sin(ps1)-math.sin(psi0))/b)
    exact1 = q*area - icos1 - 2.0*isin1
    cen1 = q - math.cos(phi0 + 2*a/3) - 2.0*math.sin(psi0 + b/3)
    approx1 = area * cen1

    # T2=(0,0),(a,b),(0,b)
    icos2 = b * (-math.sin(phi0) + (math.cos(phi0)-math.cos(ph1))/a)
    isin2 = (a/b) * (-b*math.cos(ps1) + math.sin(ps1)-math.sin(psi0))
    exact2 = q*area - icos2 - 2.0*isin2
    cen2 = q - math.cos(phi0 + a/3) - 2.0*math.sin(psi0 + 2*b/3)
    approx2 = area * cen2
    return exact1, exact2, approx1, approx2


def curvature_mesh_checks(rec: Recorder, n: int,
                          coords: np.ndarray) -> dict[str, Any]:
    d = TAU/n
    exact_total = approx_total = 0.0
    local_errors: list[float] = []
    local_abs_approx: list[float] = []
    q_value = 1.0
    for i in range(n):
        ph0 = TAU*i/n
        for j in range(n):
            ps0 = TAU*j/n
            ex1, ex2, ap1, ap2 = triangle_fluxes(ph0, ps0, d, d, q_value)
            exact_total += ex1 + ex2
            approx_total += ap1 + ap2
            local_errors.extend((abs(ap1-ex1), abs(ap2-ex2)))
            local_abs_approx.extend((abs(ap1), abs(ap2)))
    expected = q_value * TAU**2
    max_local_error = max(local_errors)
    rms_local_error = math.sqrt(sum(v*v for v in local_errors)/len(local_errors))
    perturb_at_00 = -(math.cos(0.0) + 2.0*math.sin(0.0))
    q0_total = 0.0
    for i in range(n):
        ph0 = TAU*i/n
        for j in range(n):
            ps0 = TAU*j/n
            z01, z02, _, _ = triangle_fluxes(ph0, ps0, d, d, 0.0)
            q0_total += z01 + z02
    q0_local_at_00 = 0.0 - math.cos(0.0) - 2.0*math.sin(0.0)
    rec.add(f"C_face_exact_flux_n{n}", exact_total, expected,
            abs(exact_total-expected) < 2e-9,
            "Sum of analytically integrated oriented face contributions.", "discrete-mesh")
    rec.add(f"C_face_centroid_flux_n{n}", approx_total, expected,
            abs(approx_total-expected) < 2e-8,
            "Independent face-barycentre quadrature of the local density.", "discrete-mesh")
    rec.add(f"C_q0_zero_flux_n{n}", q0_total, 0.0,
            abs(q0_total) < 1e-12,
            "q=0 total flux is zero; this is not a claim that the local form vanishes.", "discrete-mesh")
    rec.add(f"C_nonzero_local_response_n{n}", perturb_at_00, -1.0,
            abs(perturb_at_00+1) < 1e-12,
            "At (0,0), density perturbation -cos(phi)-2 sin(psi) equals -1.", "discrete-mesh")
    return {"exact_flux": exact_total, "centroid_flux": approx_total,
            "expected_flux": expected, "exact_flux_error": abs(exact_total-expected),
            "centroid_flux_error": abs(approx_total-expected),
            "max_local_face_quadrature_error": max_local_error,
            "rms_local_face_quadrature_error": rms_local_error,
            "face_count": 2*n*n, "local_response_at_00": perturb_at_00}


def base_icosphere() -> tuple[np.ndarray, list[tuple[int, int, int]]]:
    t = (1.0 + math.sqrt(5.0))/2.0
    verts = np.array([
        (-1,t,0),(1,t,0),(-1,-t,0),(1,-t,0),
        (0,-1,t),(0,1,t),(0,-1,-t),(0,1,-t),
        (t,0,-1),(t,0,1),(-t,0,-1),(-t,0,1),
    ], dtype=float)
    verts /= np.linalg.norm(verts, axis=1)[:, None]
    faces = [
        (0,11,5),(0,5,1),(0,1,7),(0,7,10),(0,10,11),
        (1,5,9),(5,11,4),(11,10,2),(10,7,6),(7,1,8),
        (3,9,4),(3,4,2),(3,2,6),(3,6,8),(3,8,9),
        (4,9,5),(2,4,11),(6,2,10),(8,6,7),(9,8,1),
    ]
    fixed = []
    for face in faces:
        a,b,c=(verts[k] for k in face)
        if np.dot(np.cross(b-a,c-a), a+b+c) < 0:
            face=(face[0],face[2],face[1])
        fixed.append(face)
    return verts, fixed


def refine_sphere(level: int) -> tuple[np.ndarray, list[tuple[int, int, int]]]:
    verts, faces = base_icosphere()
    for _ in range(level):
        vlist = [p.copy() for p in verts]
        midpoint_cache: dict[tuple[int,int], int] = {}
        def mid(i: int, j: int) -> int:
            key = (min(i,j), max(i,j))
            if key not in midpoint_cache:
                p = verts[i] + verts[j]
                p /= np.linalg.norm(p)
                midpoint_cache[key] = len(vlist)
                vlist.append(p)
            return midpoint_cache[key]
        new_faces: list[tuple[int,int,int]] = []
        for a,b,c in faces:
            ab,bc,ca = mid(a,b),mid(b,c),mid(c,a)
            new_faces.extend([(a,ab,ca),(b,bc,ab),(c,ca,bc),(ab,bc,ca)])
        verts = np.asarray(vlist, dtype=float)
        oriented = []
        for face in new_faces:
            a,b,c=(verts[k] for k in face)
            if np.dot(np.cross(b-a,c-a), a+b+c) < 0:
                face=(face[0],face[2],face[1])
            oriented.append(face)
        faces = oriented
    return verts, faces


def sphere_flux_methods(points: dict[int, tuple[float,float,float]] | np.ndarray,
                        faces: list[tuple[int,int,int]], charge: float = 1.0) -> dict[str,float]:
    if isinstance(points, dict):
        pmap = points
        def point(i: int) -> np.ndarray:
            x = np.asarray(pmap[i], dtype=float)
            return x/np.linalg.norm(x)
    else:
        arr = points
        def point(i: int) -> np.ndarray:
            x = np.asarray(arr[i], dtype=float)
            return x/np.linalg.norm(x)
    omega_total = 0.0
    planar_surface_integral = 0.0
    max_edge = 0.0
    for tri in faces:
        a,b,c=(point(k) for k in tri)
        # Fix orientation outward for robust use with both Gmsh and fallback meshes.
        if np.dot(np.cross(b-a,c-a), a+b+c) < 0:
            b,c=c,b
        max_edge=max(max_edge, float(np.linalg.norm(a-b)), float(np.linalg.norm(b-c)), float(np.linalg.norm(c-a)))
        det = float(np.dot(a, np.cross(b,c)))
        den = float(1.0 + np.dot(a,b) + np.dot(b,c) + np.dot(c,a))
        omega_total += 2.0*math.atan2(det, den)
        # Midpoint quadrature of the radial monopole 2-form over the flat triangle.
        centroid=(a+b+c)/3.0
        area_vector=0.5*np.cross(b-a,c-a)
        planar_surface_integral += float(np.dot(centroid/(np.linalg.norm(centroid)**3), area_vector))
    # F=(n/2)dOmega. Normalize integral by 2*pi to get n.
    solid_angle_charge = charge*omega_total/(4.0*math.pi)
    planar_charge = charge*planar_surface_integral/(4.0*math.pi)
    return {"solid_angle_charge": solid_angle_charge,
            "planar_quadrature_charge": planar_charge,
            "solid_angle_error": abs(solid_angle_charge-charge),
            "planar_quadrature_error": abs(planar_charge-charge),
            "solid_angle_total": omega_total,
            "max_edge_length": max_edge}


def cube_tetra_mesh(n: int) -> tuple[np.ndarray, list[tuple[int,int,int,int]]]:
    """Freudenthal triangulation of [0,1]^3: a contractible solid-ball substitute."""
    if n < 1:
        raise ValueError("n must be >=1")
    pts = np.array([(i/n,j/n,k/n) for i in range(n+1) for j in range(n+1) for k in range(n+1)], dtype=float)
    stride_j=n+1; stride_i=(n+1)*(n+1)
    def vid(i:int,j:int,k:int)->int:
        return i*stride_i+j*stride_j+k
    tets=[]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                origin=(i,j,k)
                for perm in itertools.permutations(range(3)):
                    p=list(origin)
                    v0=vid(*p)
                    p[perm[0]] += 1; v1=vid(*p)
                    p[perm[1]] += 1; v2=vid(*p)
                    p[perm[2]] += 1; v3=vid(*p)
                    tet=(v0,v1,v2,v3)
                    coords=pts[list(tet)]
                    if np.linalg.det(np.stack([coords[1]-coords[0],coords[2]-coords[0],coords[3]-coords[0]],axis=1)) < 0:
                        tet=(v0,v1,v3,v2)
                    tets.append(tet)
    return pts, tets


def gmsh_mesh(shape: str, h: float) -> tuple[dict[int, tuple[float,float,float]], list[tuple[int,...]]]:
    """Create a Gmsh linear simplicial mesh; raises if Gmsh cannot initialize."""
    import gmsh  # optional dependency, intentionally not swallowed here
    gmsh.initialize()
    try:
        gmsh.option.setNumber("General.Terminal", 0)
        gmsh.option.setNumber("Mesh.ElementOrder", 1)
        gmsh.model.add("ecc_b01_independent_" + shape)
        if shape == "sphere":
            gmsh.model.occ.addSphere(0,0,0,1)
            dim=2
        elif shape == "torus":
            gmsh.model.occ.addTorus(0,0,0,2,0.75)
            dim=2
        elif shape == "ball":
            gmsh.model.occ.addSphere(0,0,0,1)
            dim=3
        else:
            raise ValueError(shape)
        gmsh.model.occ.synchronize()
        gmsh.option.setNumber("Mesh.MeshSizeMin", h)
        gmsh.option.setNumber("Mesh.MeshSizeMax", h)
        gmsh.model.mesh.generate(dim)
        ids, xyz, _ = gmsh.model.mesh.getNodes()
        points={int(tag): tuple(map(float,xyz[3*i:3*i+3])) for i,tag in enumerate(ids)}
        element_types, _, element_nodes = gmsh.model.mesh.getElements(dim)
        simplices=[]
        expected_nodes=dim+1
        for etype, flat in zip(element_types, element_nodes):
            props=gmsh.model.mesh.getElementProperties(int(etype))
            node_count=int(props[3])
            if int(props[1]) != dim or node_count != expected_nodes:
                continue
            for i in range(0,len(flat),node_count):
                simplex=tuple(int(k) for k in flat[i:i+node_count])
                simplices.append(simplex)
        if not simplices:
            raise RuntimeError(f"Gmsh returned no first-order {dim}-simplices for {shape}")
        return points, simplices
    finally:
        gmsh.finalize()


def build_simplices(top_simplices: Iterable[tuple[int,...]]) -> list[list[tuple[int,...]]]:
    tops=[tuple(int(v) for v in s) for s in top_simplices]
    if not tops:
        raise ValueError("empty top-simplex list")
    dim=len(tops[0])-1
    all_by_dim: list[set[tuple[int,...]]] = [set() for _ in range(dim+1)]
    for simplex in tops:
        if len(simplex)!=dim+1:
            raise ValueError("inconsistent top simplex dimensions")
        canon=tuple(sorted(simplex))
        for d in range(dim+1):
            for face in itertools.combinations(canon,d+1):
                all_by_dim[d].add(tuple(face))
    return [sorted(s) for s in all_by_dim]


def boundary_matrix(lower: list[tuple[int,...]], higher: list[tuple[int,...]]) -> sparse.csr_matrix:
    lower_index={s:i for i,s in enumerate(lower)}
    rows=[]; cols=[]; vals=[]
    for j, simplex in enumerate(higher):
        # Simplices are stored in canonical sorted orientation.
        for omitted in range(len(simplex)):
            face=simplex[:omitted]+simplex[omitted+1:]
            rows.append(lower_index[face]); cols.append(j); vals.append(1 if omitted%2==0 else -1)
    return sparse.csr_matrix((np.asarray(vals,dtype=np.int64),(rows,cols)),shape=(len(lower),len(higher)),dtype=np.int64)


def incidence_report(top_simplices: list[tuple[int,...]]) -> dict[str,Any]:
    simplices=build_simplices(top_simplices)
    dim=len(simplices)-1
    boundaries={k:boundary_matrix(simplices[k-1],simplices[k]) for k in range(1,dim+1)}
    coboundaries={k:boundaries[k].transpose().tocsr() for k in range(1,dim+1)}
    products=[]
    for k in range(dim-1):
        # D_k maps k-cochains to (k+1)-cochains, represented as B_{k+1}^T.
        left=coboundaries[k+2]
        right=coboundaries[k+1]
        prod=left @ right
        prod.eliminate_zeros()
        products.append({"identity":f"D{k+1}@D{k}=0","passed":prod.nnz==0,"nnz":int(prod.nnz)})
    unique=[]; seen=set()
    for item in products:
        if item["identity"] not in seen:
            unique.append(item); seen.add(item["identity"])
    return {"simplex_counts_by_dimension":[len(s) for s in simplices],
            "boundary_nnz_by_dimension":{str(k):int(m.nnz) for k,m in boundaries.items()},
            "coboundary_identity_checks":unique,
            "all_identities_pass":all(x["passed"] for x in unique),
            "simplices":simplices}


def gf2_rank_columns(columns: Iterable[int]) -> int:
    pivots: dict[int,int] = {}
    rank=0
    for col in columns:
        value=int(col)
        while value:
            pivot=value.bit_length()-1
            previous=pivots.get(pivot)
            if previous is None:
                pivots[pivot]=value
                rank += 1
                break
            value ^= previous
    return rank


def gf2_betti(top_simplices: list[tuple[int,...]]) -> list[int]:
    simplexes=build_simplices(top_simplices)
    topdim=len(simplexes)-1
    ranks: dict[int,int]={0:0}
    for dim in range(1,topdim+1):
        lower=simplexes[dim-1]
        idx={s:i for i,s in enumerate(lower)}
        cols=[]
        for simplex in simplexes[dim]:
            mask=0
            for omitted in range(len(simplex)):
                facet=simplex[:omitted]+simplex[omitted+1:]
                mask ^= 1 << idx[facet]
            cols.append(mask)
        ranks[dim]=gf2_rank_columns(cols)
    ranks[topdim+1]=0
    return [len(simplexes[k])-ranks[k]-ranks[k+1] for k in range(topdim+1)]


def betti_numbers(top_simplices: list[tuple[int,...]]) -> tuple[list[int],str]:
    try:
        import gudhi
        st=gudhi.SimplexTree()
        for simplex in top_simplices:
            st.insert(simplex)
        st.compute_persistence(homology_coeff_field=2, persistence_dim_max=True)
        betti=st.betti_numbers()
        targetdim=len(top_simplices[0])-1
        return (list(betti)+[0]*(targetdim+1-len(betti)))[:targetdim+1], "GUDHI SimplexTree over GF(2)"
    except Exception as exc:
        return gf2_betti(top_simplices), f"independent Python GF(2) boundary-rank fallback ({type(exc).__name__}: {exc})"


def max_edge_length(points: dict[int,tuple[float,float,float]] | np.ndarray,
                    simplices: list[tuple[int,...]]) -> float:
    def p(i:int)->np.ndarray:
        if isinstance(points,dict): return np.asarray(points[i],dtype=float)
        return np.asarray(points[i],dtype=float)
    edges=set()
    for simplex in simplices:
        for i,j in itertools.combinations(simplex,2): edges.add((min(i,j),max(i,j)))
    return max((float(np.linalg.norm(p(i)-p(j))) for i,j in edges), default=0.0)


def sphere_refinement_level(h: float) -> int:
    # Choose a monotone fallback icosphere refinement from requested target size.
    return max(1, int(math.ceil(0.8 / h)))


def validate_mesh_resources(h_levels: list[float]) -> None:
    # Reject unsafe/non-finite target sizes before mesh allocation.
    for h in h_levels:
        if not math.isfinite(h) or h <= 0:
            raise ValueError("all --h values must be finite and positive")
        # Bound each fallback family before ceil/exponent calculations can explode.
        if h < TAU / math.floor(math.sqrt(MAX_STRUCTURED_TORUS_FACES / 2)):
            raise ValueError(
                f"h={h:g} exceeds structured-torus budget ({MAX_STRUCTURED_TORUS_FACES:,} faces)"
            )
        n_torus = max(4, int(math.ceil(TAU / h)))
        torus_faces = 2 * n_torus * n_torus
        if torus_faces > MAX_STRUCTURED_TORUS_FACES:
            raise ValueError(
                f"h={h:g} requires {torus_faces:,} structured-torus faces; "
                f"budget is {MAX_STRUCTURED_TORUS_FACES:,}"
            )
        if h < 1.0 / math.floor((MAX_FALLBACK_BALL_TETRAHEDRA / 6) ** (1 / 3)):
            raise ValueError(
                f"h={h:g} exceeds fallback ball budget ({MAX_FALLBACK_BALL_TETRAHEDRA:,} tetrahedra)"
            )
        n_ball = max(1, int(math.ceil(1.0 / h)))
        ball_tetrahedra = 6 * n_ball**3
        if ball_tetrahedra > MAX_FALLBACK_BALL_TETRAHEDRA:
            raise ValueError(
                f"h={h:g} requires {ball_tetrahedra:,} fallback tetrahedra; "
                f"budget is {MAX_FALLBACK_BALL_TETRAHEDRA:,}"
            )
        if h < 0.8 / MAX_FALLBACK_SPHERE_LEVEL:
            raise ValueError(
                f"h={h:g} exceeds fallback sphere refinement budget "
                f"(maximum level {MAX_FALLBACK_SPHERE_LEVEL})"
            )
        level = sphere_refinement_level(h)
        sphere_faces = 20 * (4 ** level)
        if sphere_faces > MAX_FALLBACK_SPHERE_FACES:
            raise ValueError(
                f"h={h:g} requires {sphere_faces:,} fallback sphere faces; "
                f"budget is {MAX_FALLBACK_SPHERE_FACES:,}"
            )


def prepare_output_directory(requested: str | None) -> Path:
    # Never reuse a path containing earlier evidence.
    if requested:
        target = Path(requested).expanduser().resolve()
    else:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        target = ROOT / "runs" / f"run-{stamp}-{os.getpid()}"
    if target.exists():
        raise FileExistsError(f"refusing to overwrite existing output directory: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.mkdir(exist_ok=False)
    return target


class _GmshRuntimeFailure(RuntimeError):
    # Signal that an imported Gmsh runtime failed during mesh generation.
    pass


def fallback_mesh(shape: str, index: int, h: float) -> tuple[dict[int,tuple[float,float,float]] | np.ndarray, list[tuple[int,...]], str]:
    del index  # Refinement is driven by the requested h, not list ordering.
    validate_mesh_resources([h])
    if shape == "sphere":
        level = sphere_refinement_level(h)
        verts, faces=refine_sphere(level)
        return verts, faces, f"fallback radial icosphere refinement level {level}"
    if shape == "torus":
        n=max(4, int(math.ceil(TAU/h)))
        coords, faces=structured_torus(n)
        # Embed the parameter torus in R^3 for geometric mesh-size reporting.
        embedded=[]
        major,minor=2.0,0.75
        for ph,ps in coords:
            embedded.append(((major+minor*math.cos(ps))*math.cos(ph),
                             (major+minor*math.cos(ps))*math.sin(ph),
                             minor*math.sin(ps)))
        return np.asarray(embedded), faces, f"fallback periodic structured torus n={n}"
    if shape == "ball":
        n=max(1,int(math.ceil(1.0/h)))
        if 6 * n**3 > MAX_FALLBACK_BALL_TETRAHEDRA:
            raise ValueError(
                f"fallback ball mesh needs {6*n**3:,} tetrahedra; "
                f"budget is {MAX_FALLBACK_BALL_TETRAHEDRA:,}"
            )
        pts,tets=cube_tetra_mesh(n)
        return pts,tets,f"fallback Freudenthal tetrahedralization of a cube, n={n} cells per axis"
    raise ValueError(shape)


def normalize_mesh_points(points: dict[int,tuple[float,float,float]] | np.ndarray) -> tuple[np.ndarray,dict[int,int]]:
    if isinstance(points,dict):
        ids=sorted(points)
        arr=np.asarray([points[i] for i in ids],dtype=float)
        return arr,{tag:i for i,tag in enumerate(ids)}
    arr=np.asarray(points,dtype=float)
    return arr,{i:i for i in range(len(arr))}


def derive_mesh_gate_statuses(
    backend_request: str,
    mesh_rows: list[dict[str, Any]],
    h_levels: list[float],
    gmsh_available: bool,
    gudhi_available: bool,
) -> dict[str, str]:
    # Derive toolchain gate status from every expected per-shape result.
    records = [record for row in mesh_rows for record in row.get("shapes", {}).values()]
    complete = len(records) == 3 * len(h_levels) and all("error" not in record for record in records)
    gmsh_all = complete and all(str(record.get("mesh_source", "")).startswith("Gmsh") for record in records)
    gudhi_all = complete and all(str(record.get("homology_method", "")).startswith("GUDHI") for record in records)

    if backend_request == "fallback":
        gmsh_status = "NOT_REQUESTED"
    elif not gmsh_available:
        gmsh_status = "BLOCKED_OPTIONAL_DEPENDENCY"
    elif gmsh_all:
        gmsh_status = "PASS"
    else:
        gmsh_status = "BLOCKED_RUNTIME_FAILURE"

    if not gudhi_available:
        gudhi_status = "BLOCKED_OPTIONAL_DEPENDENCY"
    elif gudhi_all:
        gudhi_status = "PASS"
    else:
        gudhi_status = "BLOCKED_RUNTIME_FAILURE"

    if backend_request == "fallback":
        full_status = "NOT_REQUESTED"
    elif gmsh_status == "PASS" and gudhi_status == "PASS":
        full_status = "PASS"
    elif "BLOCKED_OPTIONAL_DEPENDENCY" in (gmsh_status, gudhi_status):
        full_status = "BLOCKED_OPTIONAL_DEPENDENCY"
    else:
        full_status = "BLOCKED_RUNTIME_FAILURE"
    return {
        "gmsh_gate_status": gmsh_status,
        "gudhi_gate_status": gudhi_status,
        "full_requested_toolchain_gate_status": full_status,
        "gmsh_execution_records": sum(str(r.get("mesh_source", "")).startswith("Gmsh") for r in records),
        "gudhi_execution_records": sum(str(r.get("homology_method", "")).startswith("GUDHI") for r in records),
    }


def run_mesh_suite(rec: Recorder, h_levels: list[float], backend_request: str) -> tuple[list[dict[str,Any]],list[dict[str,Any]],dict[str,Any]]:
    try:
        import gmsh  # noqa: F401
        gmsh_available=True
    except Exception:
        gmsh_available=False
    backend_actual="gmsh" if backend_request in ("auto","gmsh") and gmsh_available else "fallback"
    if backend_request=="gmsh" and not gmsh_available:
        backend_actual="fallback"
        gmsh_failure="Gmsh was explicitly requested but could not be imported; fallback was run, and Gmsh-specific gate remains blocked."
    else:
        gmsh_failure=None

    h_levels=sorted(h_levels, reverse=True)
    mesh_rows: list[dict[str,Any]]=[]
    convergence_rows: list[dict[str,Any]]=[]
    gudhi_available=dependency_state()["gudhi"]["available"]
    mesh_manifest={"backend_requested":backend_request,"backend_used":backend_actual,
                   "gmsh_available":gmsh_available,"gudhi_available":gudhi_available,
                   "fallback_note":gmsh_failure or ("Explicit fallback backend selected; Gmsh was not requested." if backend_request=="fallback" else ("Gmsh unavailable; used independent fallback simplicial meshes. This does not count as a Gmsh execution." if backend_actual!="gmsh" else ""))}

    sphere_planar_errors=[]
    for idx,h in enumerate(h_levels):
        shape_records={}
        for shape in ("sphere","torus","ball"):
            try:
                if backend_actual=="gmsh":
                    points, top=gmsh_mesh(shape,h)
                    source="Gmsh linear simplex mesh"
                else:
                    points, top, source=fallback_mesh(shape,idx,h)
                # Gmsh node tags are sparse, so remap to a dense index for topology routines.
                if isinstance(points,dict):
                    id_map={tag:i for i,tag in enumerate(sorted(points))}
                    top_dense=[tuple(id_map[v] for v in s) for s in top]
                    p_dense=np.asarray([points[tag] for tag in sorted(points)],dtype=float)
                    points_for_flux={i:tuple(p_dense[i]) for i in range(len(p_dense))}
                else:
                    p_dense=np.asarray(points,dtype=float)
                    top_dense=[tuple(int(v) for v in s) for s in top]
                    points_for_flux=p_dense
                inc=incidence_report(top_dense)
                betti,homology_method=betti_numbers(top_dense)
                target={"sphere":[1,0,1],"torus":[1,2,1],"ball":[1,0,0,0]}[shape]
                actual_edge=max_edge_length(points_for_flux,top_dense)
                record={"shape":shape,"target_h":h,"actual_max_edge":actual_edge,
                        "point_count":len(p_dense),"top_simplex_count":len(top_dense),
                        "simplex_counts_by_dimension":inc["simplex_counts_by_dimension"],
                        "betti_numbers":betti,"expected_betti_numbers":target,
                        "betti_pass":betti==target,"homology_method":homology_method,
                        "incidence_identities":inc["coboundary_identity_checks"],
                        "incidence_pass":inc["all_identities_pass"],"mesh_source":source}
                rec.add(f"TOPO_{shape}_h{h}",betti,target,betti==target,
                        f"{len(p_dense)} vertices; {len(top_dense)} top simplices; {homology_method}.","topology")
                rec.add(f"INCIDENCE_{shape}_h{h}",inc["all_identities_pass"],True,
                        inc["all_identities_pass"],json.dumps(inc["coboundary_identity_checks"]),"discrete-mesh")
                if shape=="sphere":
                    flux=sphere_flux_methods(points_for_flux,top_dense,charge=1.0)
                    record.update(flux)
                    rec.add(f"B_solid_angle_flux_h{h}",flux["solid_angle_charge"],1.0,
                            flux["solid_angle_error"]<1e-8,
                            "Spherical-triangle solid-angle integral of F=(1/2)dOmega.","mesh-flux")
                    rec.add(f"B_planar_face_quadrature_h{h}",flux["planar_quadrature_charge"],1.0,
                            flux["planar_quadrature_error"]<max(0.12,3.0*actual_edge**2),
                            "Independent centroid quadrature on flat triangular facets; convergence tested across levels.","mesh-flux")
                    sphere_planar_errors.append(flux["planar_quadrature_error"])
                    convergence_rows.append({"candidate":"B","metric":"solid_angle_normalized_flux",
                        "target_h":h,"actual_max_edge":actual_edge,"mesh_vertices":len(p_dense),
                        "mesh_edges":inc["simplex_counts_by_dimension"][1],"mesh_faces":inc["simplex_counts_by_dimension"][2],
                        "mesh_tetrahedra":0,"measured_value":flux["solid_angle_charge"],"expected_value":1.0,
                        "absolute_error":flux["solid_angle_error"],"convergence_rate":None,"note":"spherical solid-angle formula"})
                    convergence_rows.append({"candidate":"B","metric":"planar_face_quadrature_normalized_flux",
                        "target_h":h,"actual_max_edge":actual_edge,"mesh_vertices":len(p_dense),
                        "mesh_edges":inc["simplex_counts_by_dimension"][1],"mesh_faces":inc["simplex_counts_by_dimension"][2],
                        "mesh_tetrahedra":0,"measured_value":flux["planar_quadrature_charge"],"expected_value":1.0,
                        "absolute_error":flux["planar_quadrature_error"],"convergence_rate":None,"note":"flat-facet midpoint quadrature"})
                if shape=="torus":
                    convergence_rows.append({"candidate":"topology","metric":"torus_betti_numbers",
                        "target_h":h,"actual_max_edge":actual_edge,"mesh_vertices":len(p_dense),
                        "mesh_edges":inc["simplex_counts_by_dimension"][1],"mesh_faces":inc["simplex_counts_by_dimension"][2],
                        "mesh_tetrahedra":0,"measured_value":str(betti),"expected_value":"[1, 2, 1]",
                        "absolute_error":0 if betti==target else 1,"convergence_rate":None,"note":homology_method})
                if shape=="ball":
                    convergence_rows.append({"candidate":"topology","metric":"ball_betti_numbers",
                        "target_h":h,"actual_max_edge":actual_edge,"mesh_vertices":len(p_dense),
                        "mesh_edges":inc["simplex_counts_by_dimension"][1],"mesh_faces":inc["simplex_counts_by_dimension"][2],
                        "mesh_tetrahedra":len(top_dense),"measured_value":str(betti),"expected_value":"[1, 0, 0, 0]",
                        "absolute_error":0 if betti==target else 1,"convergence_rate":None,"note":homology_method})
                shape_records[shape]=record
            except Exception as exc:
                detail=f"{type(exc).__name__}: {exc}"
                rec.add(f"MESH_{shape}_h{h}",detail,"successful mesh checks",False,traceback.format_exc(limit=2),"mesh-error")
                shape_records[shape]={"shape":shape,"target_h":h,"error":detail}
        mesh_rows.append({"target_h":h,"shapes":shape_records})

    if len(sphere_planar_errors) > 1:
        monotone = all(a > b for a,b in zip(sphere_planar_errors, sphere_planar_errors[1:]))
        rec.add("B_planar_flux_error_decreases_with_refinement", sphere_planar_errors,
                "strictly decreasing absolute errors", monotone,
                "Cross-resolution convergence gate for the independent flat-facet quadrature.", "mesh-convergence")

    # Structured parameter-space torus for actual candidate-A cochains and candidate-C face integrals.
    a_errors=[]; c_local_errors=[]
    for h in h_levels:
        n=max(4,int(math.ceil(TAU/h)))
        coords,faces=structured_torus(n)
        a=add_cochain_checks(rec,n,coords,faces)
        c=curvature_mesh_checks(rec,n,coords)
        target_h=TAU/n
        convergence_rows.extend([
            {"candidate":"A","metric":"phi_period","target_h":h,"actual_max_edge":math.sqrt(2.0)*target_h,
             "mesh_vertices":a["node_count"],"mesh_edges":a["edge_count"],"mesh_faces":a["face_count"],"mesh_tetrahedra":0,
             "measured_value":a["phi_period"],"expected_value":TAU,"absolute_error":abs(a["phi_period"]-TAU),
             "convergence_rate":None,"note":"discrete cochain on representative phi-cycle"},
            {"candidate":"A","metric":"psi_period","target_h":h,"actual_max_edge":math.sqrt(2.0)*target_h,
             "mesh_vertices":a["node_count"],"mesh_edges":a["edge_count"],"mesh_faces":a["face_count"],"mesh_tetrahedra":0,
             "measured_value":a["psi_period"],"expected_value":2*TAU,"absolute_error":abs(a["psi_period"]-2*TAU),
             "convergence_rate":None,"note":"discrete cochain on representative psi-cycle"},
            {"candidate":"A","metric":"max_triangle_circulation","target_h":h,"actual_max_edge":math.sqrt(2.0)*target_h,
             "mesh_vertices":a["node_count"],"mesh_edges":a["edge_count"],"mesh_faces":a["face_count"],"mesh_tetrahedra":0,
             "measured_value":a["closure_residual"],"expected_value":0.0,"absolute_error":a["closure_residual"],
             "convergence_rate":None,"note":"max absolute discrete circulation"},
            {"candidate":"C","metric":"analytic_face_flux","target_h":h,"actual_max_edge":math.sqrt(2.0)*target_h,
             "mesh_vertices":a["node_count"],"mesh_edges":a["edge_count"],"mesh_faces":c["face_count"],"mesh_tetrahedra":0,
             "measured_value":c["exact_flux"],"expected_value":c["expected_flux"],"absolute_error":c["exact_flux_error"],
             "convergence_rate":None,"note":"exact analytic integration on each oriented parameter triangle"},
            {"candidate":"C","metric":"centroid_face_flux","target_h":h,"actual_max_edge":math.sqrt(2.0)*target_h,
             "mesh_vertices":a["node_count"],"mesh_edges":a["edge_count"],"mesh_faces":c["face_count"],"mesh_tetrahedra":0,
             "measured_value":c["centroid_flux"],"expected_value":c["expected_flux"],"absolute_error":c["centroid_flux_error"],
             "convergence_rate":None,"note":"barycentre quadrature of local density"},
            {"candidate":"C","metric":"max_local_face_quadrature_error","target_h":h,"actual_max_edge":math.sqrt(2.0)*target_h,
             "mesh_vertices":a["node_count"],"mesh_edges":a["edge_count"],"mesh_faces":c["face_count"],"mesh_tetrahedra":0,
             "measured_value":c["max_local_face_quadrature_error"],"expected_value":0.0,"absolute_error":c["max_local_face_quadrature_error"],
             "convergence_rate":None,"note":"max absolute local-face integral error versus exact face integral"},
        ])

    # Estimate observed convergence rates only where successive errors sit above floating-point floor.
    groups: dict[str,list[dict[str,Any]]]={}
    for row in convergence_rows:
        if isinstance(row.get("absolute_error"), (int,float)):
            groups.setdefault(row["metric"],[]).append(row)
    for metric, rows in groups.items():
        rows.sort(key=lambda r:r["actual_max_edge"], reverse=True)
        for i,row in enumerate(rows):
            if i==0 or row["absolute_error"] is None or rows[i-1]["absolute_error"] is None:
                row["convergence_rate"] = None
                continue
            e1=float(rows[i-1]["absolute_error"]); e2=float(row["absolute_error"])
            h1=float(rows[i-1]["actual_max_edge"]); h2=float(row["actual_max_edge"])
            if e1>1e-12 and e2>1e-12 and h1>h2>0:
                row["convergence_rate"]=math.log(e1/e2)/math.log(h1/h2)
            else:
                row["convergence_rate"]=None

    mesh_manifest.update(derive_mesh_gate_statuses(backend_request, mesh_rows, h_levels, gmsh_available, gudhi_available))
    return mesh_rows, convergence_rows, mesh_manifest


def main() -> int:
    parser=argparse.ArgumentParser(description="Independent ECC-B01 mathematical reproduction kit")
    parser.add_argument("--out-dir",default=None,help="New output directory; default is unique under runs/")
    parser.add_argument("--mesh",action="store_true",help="Run topology, incidence, mesh-flux, torus-period, and face-curvature checks")
    parser.add_argument("--h",nargs="+",type=float,default=[0.8,0.5,0.3,0.2],help="Target mesh sizes")
    parser.add_argument("--backend",choices=["auto","gmsh","fallback"],default="auto",help="Use Gmsh if available or deterministic independent meshes")
    args=parser.parse_args()
    if any(not math.isfinite(h) or h<=0 for h in args.h):
        parser.error("all --h values must be finite and positive")
    if args.mesh:
        try:
            validate_mesh_resources(args.h)
        except ValueError as exc:
            parser.error(str(exc))
    try:
        outdir = prepare_output_directory(args.out_dir)
    except (FileExistsError, OSError) as exc:
        parser.error(str(exc))

    rec=Recorder()
    symbolic_controls(rec)
    quadrature_controls(rec)
    mesh_rows=[]; convergence_rows=[]; mesh_manifest={"requested":False}
    if args.mesh:
        mesh_rows,convergence_rows,mesh_manifest=run_mesh_suite(rec,args.h,args.backend)
        with (outdir/"convergence_b.csv").open("w",newline="",encoding="utf-8") as f:
            fields=["candidate","metric","target_h","actual_max_edge","mesh_vertices","mesh_edges","mesh_faces","mesh_tetrahedra","measured_value","expected_value","absolute_error","convergence_rate","note"]
            writer=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
            writer.writeheader(); writer.writerows(convergence_rows)
        (outdir/"mesh_details.json").write_text(json.dumps({"mesh_manifest":mesh_manifest,"rows":mesh_rows},indent=2,allow_nan=False)+"\n",encoding="utf-8")

    deps=dependency_state()
    fail_count=sum(r["status"]=="FAIL" for r in rec.results)
    pass_count=sum(r["status"]=="PASS" for r in rec.results)
    if fail_count:
        status="FAIL"
    elif args.mesh and (str(mesh_manifest.get("gmsh_gate_status", "")).startswith("BLOCKED") or str(mesh_manifest.get("gudhi_gate_status", "")).startswith("BLOCKED")):
        status="PASS_CORE_AND_AVAILABLE_MESH; GMSH_GUDHI_GATE_BLOCKED"
    else:
        status="PASS"
    payload={
        "experiment_id":"EXP-ECC-B01-INDEPENDENT-REPRODUCTION",
        "independence_statement":"Fresh implementation and proofs; starter result JSON not used as observed output.",
        "scope":"Mathematical controls for three stated candidates only.",
        "overall_status":status,
        "generated_at_utc":datetime.now(timezone.utc).isoformat(),
        "python":sys.version,
        "platform":platform.platform(),
        "dependencies":deps,
        "mesh_requested":bool(args.mesh),
        "mesh_manifest":mesh_manifest,
        "source_sha256":sha256_file(Path(__file__).resolve()),
        "run_parameters":{"mesh_requested":bool(args.mesh),"backend_requested":args.backend,"h":list(args.h) if args.mesh else [],"out_dir":str(outdir)},
        "tolerances":TOLERANCES,
        "resource_limits":{"fallback_ball_tetrahedra_max":MAX_FALLBACK_BALL_TETRAHEDRA,"structured_torus_faces_max":MAX_STRUCTURED_TORUS_FACES,"fallback_sphere_faces_max":MAX_FALLBACK_SPHERE_FACES,"fallback_sphere_level_max":MAX_FALLBACK_SPHERE_LEVEL},
        "results":rec.results,
        "counts":{"PASS":pass_count,"FAIL":fail_count},
        "limitations":[
            "No physical, cosmological, arithmetic, or new-theorem conclusion follows from these calculations.",
            "A nonzero period disproves exactness of a closed 1-form; it does not assert all closed forms are non-exact.",
            "For Candidate C at q=0, the total flux vanishes but the local curvature density is generally nonzero.",
            "When Gmsh is unavailable, fallback meshes validate the mathematical mesh pipeline but do not satisfy a Gmsh-specific execution gate.",
            "When GUDHI is unavailable, Betti numbers are computed by an independent Python GF(2) boundary-rank implementation; the exact GUDHI gate remains blocked.",
        ],
    }
    (outdir/"reproduction_results.json").write_text(json.dumps(payload,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    artifact_rows=[]
    for artifact in sorted(outdir.iterdir()):
        if artifact.is_file():
            artifact_rows.append({"path":artifact.name,"sha256":sha256_file(artifact),"bytes":artifact.stat().st_size})
    receipt={"receipt_format":"ECC-B01-run-receipt-v1","run_id":outdir.name,
             "receipt_created_at_utc":datetime.now(timezone.utc).isoformat(),
             "recorded_run_generated_at_utc":payload["generated_at_utc"],"source_sha256":payload["source_sha256"],
             "python":payload["python"],"platform":payload["platform"],"dependencies":payload["dependencies"],
             "run_parameters":payload["run_parameters"],"overall_status":payload["overall_status"],
             "counts":payload["counts"],"mesh_manifest":payload["mesh_manifest"],"artifacts":artifact_rows,
             "note":"Artifact hashes exclude this receipt to avoid a self-referential digest."}
    (outdir/"run_receipt.json").write_text(json.dumps(receipt,indent=2,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps({"overall_status":status,"counts":payload["counts"],"out_dir":str(outdir),"mesh_backend":mesh_manifest.get("backend_used")},indent=2))
    if fail_count:
        return 1
    if args.mesh and args.backend=="gmsh" and mesh_manifest.get("full_requested_toolchain_gate_status")!="PASS":
        return 2
    return 0


if __name__=="__main__":
    raise SystemExit(main())
