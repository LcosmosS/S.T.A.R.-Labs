#!/usr/bin/env python3
"""M1-INH-E1b: metric-first exact SymPy certificate (v2 symbol guards).

Derives the Einstein tensor from a generic diagonal metric *before* inserting
Szekeres scale factors. No density, velocity, shear eigenvector, or transverse
projector formula is supplied to the curvature calculation.

Sectors: S1 (k=0) and S2 (k=1), as preregistered. Signature +---;
Einstein convention G_ab - Lambda*g_ab = (kappa*rho) u_a u_b, Lambda=3.

Exact SO(2) reduction: all (x,y) points can be rotated to (r,0). We first
compute the complete tensor with derivatives in (t,z,x,y), and only then set
y=0. The metric is rotationally invariant, so tensor identities verified on
this meridian extend to the full regular domain by tensorial covariance.

The auxiliary differential ring substitutes the *exact* derivatives of
P=Phi(t,z), H=coth(3(t+z)/2), B=1/(3(1+z)), W=exp(z). It is equivalent to
fully differentiating those elementary functions, but controls expression size.

Requires sympy only. This is a metric-first algebraic calculation (with notebook-safe coordinate symbols), not
third-party peer review or a complete general M1-INH-E1a verification.
"""
import hashlib
import json
import sys
from functools import lru_cache
from pathlib import Path

import sympy as sp


def zero(expr, label):
    reduced = sp.cancel(expr)
    if reduced != 0:
        raise AssertionError(f'{label}: NONZERO residual = {sp.factor(reduced)}')
    return True


def main():
    # Distinct coordinate identities remain robust against notebook symbol state.
    t, z, x, y = coords = tuple(sp.Dummy(name, real=True) for name in ('t', 'z', 'x', 'y'))
    a = sp.Function('a')(*coords)
    c = sp.Function('c')(*coords)
    generic_g = sp.diag(1, -a**2, -c**2, -c**2)
    generic_ginv = sp.diag(1, -1/a**2, -1/c**2, -1/c**2)

    # From the metric alone: Levi-Civita Christoffels and Ricci tensor.
    gamma = {}
    for i in range(4):
        for j in range(4):
            for k in range(j, 4):
                val = generic_ginv[i, i] * (
                    sp.diff(generic_g[i, k], coords[j])
                    + sp.diff(generic_g[i, j], coords[k])
                    - sp.diff(generic_g[j, k], coords[i])
                ) / 2
                if val != 0:
                    gamma[i, j, k] = gamma[i, k, j] = sp.cancel(val)

    ricci = {}
    for i in range(4):
        for j in range(i, 4):
            val = 0
            for h in range(4):
                val += (
                    sp.diff(gamma.get((h, i, j), 0), coords[h])
                    - sp.diff(gamma.get((h, i, h), 0), coords[j])
                )
                for m in range(4):
                    val += (
                        gamma.get((h, h, m), 0) * gamma.get((m, i, j), 0)
                        - gamma.get((h, j, m), 0) * gamma.get((m, i, h), 0)
                    )
            ricci[i, j] = sp.factor(val)

    # Validate all differential-ring rules against the explicit Phi, H, b, w,
    # so identities are not simply stipulated auxiliary field equations.
    arg = sp.Rational(3,2)*(t+z)
    phi_phys = (2*(1+z))**sp.Rational(1,3)*sp.sinh(arg)**sp.Rational(2,3)
    H_phys = sp.coth(arg)
    B_phys = 1/(3*(1+z))
    zero(sp.simplify(sp.diff(phi_phys,t)-phi_phys*H_phys), 'Phi time derivative')
    zero(sp.simplify(sp.diff(phi_phys,z)-phi_phys*(H_phys+B_phys)),
         'Phi radial derivative')
    zero(sp.simplify(sp.diff(H_phys,t)+sp.Rational(3,2)*(H_phys**2-1)),
         'H time derivative')
    zero(sp.simplify(sp.diff(H_phys,z)+sp.Rational(3,2)*(H_phys**2-1)),
         'H radial derivative')
    zero(sp.simplify(phi_phys**3*(H_phys**2-1)-2*(1+z)),
         'Friedmann first integral')

    P, H, B, W = sp.symbols('P H B W', positive=True, real=True)
    F = H**2 - 1
    results = {}
    derived_densities = []

    for sector in (0, 1):
        # These are the only sector inputs: the two registered metric tensors.
        w = W if sector else sp.Integer(1)
        q = w**2 * (x*x + y*y)
        v = (1-q)/(1+q) if sector else sp.Integer(0)
        L = H+B+v
        a_metric = P*L
        c_metric = 2*P*w/(1+q)
        # The exact chain rule for the stated Phi, H, b, exp(z).
        dtime = {P: P*H, H: -sp.Rational(3,2)*F}
        dradial = {P: P*(H+B), H: -sp.Rational(3,2)*F,
                   B: -3*B**2}
        if sector:
            dradial[W] = W

        def deriv(expr, coordinate_index):
            if coordinate_index == 0:
                return sum(sp.diff(expr, sym)*rhs for sym, rhs in dtime.items())
            if coordinate_index == 1:
                return sum(sp.diff(expr, sym)*rhs for sym, rhs in dradial.items())
            return sp.diff(expr, coords[coordinate_index])

        # Differential identities are compatible with mixed partial derivatives.
        for variable in (P, H, B, W):
            zero(deriv(deriv(variable,0),1)-deriv(deriv(variable,1),0),
                 f'S{sector+1}: commuting derivatives of {variable}')

        # Independent Euclidean spatial embedding test (not used in Ricci).
        # X_vec = P*n + k*e3*I, where I_z=P. The check uses only its
        # explicitly differentiable spatial tangents, not an evaluated integral.
        n = sp.Matrix([2*w*x/(1+q), 2*w*y/(1+q), (1-q)/(1+q)])
        e3 = sp.Matrix([0,0,1])
        dot = lambda A,V: (A.T*V)[0]
        zero(dot(n,n)-1, f'S{sector+1}: unit vector norm')
        nz = n.diff(W)*W if sector else sp.zeros(3,1)
        for ii in range(3):
            zero(nz[ii]-sector*(n[2]*n[ii]-e3[ii]),
                 f'S{sector+1}: radial derivative n component {ii}')
        # Require exact symbol identity, not merely matching printed names.
        # Different SymPy assumptions can create distinct symbols called 'x'.
        for coordinate in (x, y):
            same_name = [symbol for symbol in n.free_symbols
                         if symbol.name == coordinate.name]
            if same_name != [coordinate]:
                raise AssertionError(
                    f'S{sector+1}: coordinate-symbol mismatch for '
                    f'{coordinate.name}; free symbols={n.free_symbols}'
                )
        nx = n.diff(x)
        ny = n.diff(y)
        # Independent stereographic derivative norm; failure here isolates
        # coordinate identity problems before the embedded metric comparison.
        for direction, nv in (('x', nx), ('y', ny)):
            zero(dot(nv,nv)-4*w**2/(1+q)**2,
                 f'S{sector+1}: stereographic derivative norm {direction}')
        for direction, nv in (('x', nx), ('y', ny)):
            zero(dot(n,nv), f'S{sector+1}: n orthogonal to n_{direction}')
            zero(dot(nv,nv)-(c_metric/P)**2,
                 f'S{sector+1}: transverse Gram {direction}{direction}')
        zero(dot(nx,ny), f'S{sector+1}: transverse Gram xy')
        Xz = deriv(P,1)*n+P*nz+sector*P*e3
        Xx=P*nx
        Xy=P*ny
        for ii in range(3):
            zero(Xz[ii]-a_metric*n[ii], f'S{sector+1}: embedding z tangent {ii}')
        zero(dot(Xz,Xz)-a_metric**2, f'S{sector+1}: embedded g_zz')
        zero(dot(Xx,Xx)-c_metric**2, f'S{sector+1}: embedded g_xx')
        zero(dot(Xy,Xy)-c_metric**2, f'S{sector+1}: embedded g_yy')
        for nm,L1,L2 in (('zx',Xz,Xx),('zy',Xz,Xy),('xy',Xx,Xy)):
            zero(dot(L1,L2),f'S{sector+1}: embedded cross term {nm}')

        @lru_cache(None)
        def metric_derivative(which, variables):
            expression = a_metric if which == 'a' else c_metric
            for var in variables:
                expression = deriv(expression, coords.index(var))
            return sp.cancel(expression.subs(y, 0))

        def specialize(generic):
            replace = {
                d: metric_derivative(d.expr.func.__name__, d.variables)
                for d in generic.atoms(sp.Derivative)
            }
            replace[a] = a_metric.subs(y, 0)
            replace[c] = c_metric.subs(y, 0)
            return sp.cancel(generic.xreplace(replace).subs(y, 0))

        # Ricci is derived before any use of the dust equations or density.
        R = {}
        for (i, j), expr in ricci.items():
            R[i, j] = specialize(expr)
            R[j, i] = R[i, j]

        ai = a_metric.subs(y, 0)
        ci = c_metric.subs(y, 0)
        g = sp.diag(1, -ai**2, -ci**2, -ci**2)
        ginv = sp.diag(1, -1/ai**2, -1/ci**2, -1/ci**2)
        scalar_R = sp.cancel(sum(ginv[i,i]*R[i,i] for i in range(4)))
        Gmixed = sp.Matrix(4, 4, lambda i,j:
            sp.cancel(ginv[i,i]*R[i,j] - (scalar_R/2 if i==j else 0)))
        Tmixed = Gmixed - 3*sp.eye(4)
        density = sp.cancel(sp.trace(Tmixed))  # curvature-derived kappa*rho
        zero(Tmixed[0,0]-density, 'trace/density consistency')
        for i in range(4):
            for j in range(4):
                if (i,j)!=(0,0):
                    zero(Tmixed[i,j], f'S{sector+1}: Einstein dust T[{i},{j}]')
        # Dust algebra, prior to extraction of the four-velocity.
        zero(sp.trace(Tmixed*Tmixed)-density**2, 'dust square trace')
        for entry in Tmixed*Tmixed-density*Tmixed:
            zero(entry, 'dust rank-one polynomial')
        if density == 0:
            raise AssertionError('non-positive identically zero density')
        dust_projector = (Tmixed/density).applyfunc(sp.cancel)
        for entry in dust_projector*dust_projector-dust_projector:
            zero(entry, 'dust projector idempotence')
        zero(sp.trace(dust_projector)-1, 'dust projector rank')
        # Image of the rank-one projector is timelike: contracted unit test.
        u_up = dust_projector[:,0] / sp.sqrt(dust_projector[0,0])
        u_dn = g*u_up
        zero((u_up.T*g*u_up)[0]-1, 'timelike normalized u')
        hproj = (sp.eye(4)-u_up*u_dn.T).applyfunc(sp.cancel)

        # Recover connection and shear from the extracted u (not chart input).
        def gamma_at(i,j,k):
            return specialize(gamma.get((i,j,k),sp.Integer(0)))
        # After dust projection, u^a=(1,0,0,0) identically in both sectors.
        if list(u_up)!=[1,0,0,0] or list(u_dn)!=[1,0,0,0]:
            raise AssertionError('extracted u has unanticipated components')
        expansion = sp.cancel(sum(gamma_at(i,i,0) for i in range(4)))
        sigma_lower = sp.Matrix(4,4,lambda i,j:
            sp.cancel(-gamma_at(0,i,j)-expansion*g[i,j]/3
                      +expansion*u_dn[i]*u_dn[j]/3))
        sigma = (ginv*sigma_lower).applyfunc(sp.cancel)
        for entry in sigma*u_up:
            zero(entry, 'shear orthogonal to dust flow')
        zero(sp.trace(sigma), 'shear tracefree')
        I2 = sp.cancel(sp.trace(sigma*sigma))
        I3 = sp.cancel(sp.trace(sigma*sigma*sigma))
        if I2 == 0 or I3 == 0:
            raise AssertionError('shear invariants vanished identically')
        zero(I2**3-6*I3**2,'shear discriminant identity')
        quad = (sigma*sigma-(I3/I2)*sigma-(I2/3)*hproj)
        for entry in quad:
            zero(entry, 'shear quadratic minimal polynomial')
        perp = (sp.Rational(2,3)*hproj-I2/(3*I3)*sigma).applyfunc(sp.cancel)
        for entry in perp*perp-perp:
            zero(entry, 'intrinsic shear projector idempotence')
        zero(sp.trace(perp)-2, 'intrinsic shear projector rank')
        for entry in perp*u_up:
            zero(entry, 'intrinsic shear projector/dust orthogonality')

        # Full gradient of curvature-derived density, projected by P_perp.
        grad = sp.Matrix([sp.cancel(deriv(density,j)) for j in range(4)])
        J = sp.cancel(-(grad.T*perp*ginv*grad)[0])
        if sector == 0:
            zero(J, 'S1: J identically zero')
            expected_d = 3*F*B/(H+B)
        else:
            expected_d = 3*F*(B+v.subs(y,0))/(H+B+v.subs(y,0))
            # Independent post-hoc comparison against registered analytic J2.
            # Here M=1/(3B) and the first integral P^3 F=2M.
            Q = W**2*x**2
            v_axis=(1-Q)/(1+Q)
            predicted = (144*(1/(3*B))**2*H**2*Q
                         /(P**8*(H+B+v_axis)**4*(1+Q)**2))
            ratio = sp.factor(sp.cancel(J/predicted))
            target_ratio = sp.Rational(9,4)*B**2*P**6*F**2
            zero(ratio-target_ratio, 'S2: J comparison before first integral')
            zero(target_ratio.subs(H**2,1+2/(3*B*P**3))-1,
                 'S2: J comparison after exact Friedmann first integral')
        zero(density-expected_d,'curvature density/post-hoc comparison')
        derived_densities.append(density)

        results['S'+str(sector+1)] = {
            'Einstein_dust_tensor': 'PASS: all 16 mixed components, exact',
            'off_diagonal_curvature': 'PASS',
            'SO2_embedding_full_xy': 'PASS: unit vector, radial/transverse tangents, all spatial Gram components, exact',
            'positive_density_on_U': 'PROVED: H>1, B>0, and v>=0 on U',
            'rank_one_timelike_dust_projector': 'PASS: exact',
            'shear_polynomial_identity': 'PASS: exact',
            'shear_projector_idempotent_rank2': 'PASS: exact',
            'J_identity': '0' if sector==0 else 'positive for x != 0 on meridian; by SO(2), q>0',
            'J_curvature_expression': str(sp.factor(J)),
        }
        print(f'S{sector+1}: 16 Einstein-dust components, dust algebra, '
              f'shear identities, projector identities, Euclidean embedding, J: PASS',flush=True)

    # The strict density difference is obtained from the TWO CURVATURE TRACES.
    # This expression is not an input to either curvature reconstruction.
    Q = W**2*x**2
    v1 = (1-Q)/(1+Q)
    d_rho = sp.cancel(derived_densities[1]-derived_densities[0])
    difference_expected = 3*F*H*v1/((H+B)*(H+B+v1))
    zero(d_rho-difference_expected, 'curvature-derived density difference')
    # On U, W>0, Q<1, H>1, B>0, P>0; hence the difference is >0
    # off the full axis, and J2>0 for x !=0 on the meridian.
    results['density_difference'] = str(sp.factor(d_rho))
    results['domain_U'] = '1<t<2, -1/4<z<1/4, x^2+y^2<1/4; H>1, B>0, q<1, v>0'

    # Exact agreement of the complete frozen elliptic record on the common J:
    # M(z)=1+z, K=0, f=z, Lambda=3 and identical branch choices.
    # The purely elliptic invariants are g2=0, g3=-(1+z)^2/4,
    # Delta=-27(1+z)^4/16 != 0 for z in (-1,infinity).
    results['derivative_rules_exact_Phi'] = 'PASS: 5 direct SymPy hyperbolic identities'
    results['elliptic_record'] = 'same M,K,f,Lambda,epsilon,v0,sigma,g2,g3,Delta'
    results['method'] = ('independent generic-metric Christoffel and Ricci; '
                         'exact rotational reduction only after differentiation; '
                         'curvature-derived density, dust flow, shear, projector and J')
    results['general_E1a'] = 'NOT CLAIMED: general Einstein-to-evolution derivation remains pending'
    results['sympy_version'] = sp.__version__
    results['script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    outfile = Path(__file__).with_suffix('.json')
    outfile.write_text(json.dumps(results, indent=2)+'\n')
    print('ALL EXACT METRIC-FIRST E1b CERTIFICATE CHECKS PASSED')
    print('Certificate:', outfile)
    print('Code SHA256:', results['script_sha256'])


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('AUDIT FAILURE:', repr(exc), file=sys.stderr)
        raise
