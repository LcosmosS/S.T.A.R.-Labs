#!/usr/bin/env python3
"""M1-INH-E1a general-class exact algebra certificate (no cosmological data).

Independent generic-metric curvature and frozen Szekeres-Szafron algebra,
with +--- and G_ab - Lambda*g_ab = kappa*rho*u_a*u_b.
The proof document supplies the intervening tensor/constraint identities.
Requires SymPy. This is not an external mathematical peer review.
"""

import sympy as sp


def require_zero(expr, label):
    reduced = sp.cancel(expr)
    if reduced != 0:
        raise AssertionError(f"{label}: {sp.factor(reduced)}")
    print(f"PASS {label}")


def generic_metric_curvature():
    t, z, x, y = coords = sp.symbols("t z x y")
    a = sp.Function("a")(*coords)
    c = sp.Function("c")(*coords)
    metric = sp.diag(1, -a**2, -c**2, -c**2)
    inv = sp.diag(1, -1/a**2, -1/c**2, -1/c**2)
    conn = {}
    for i in range(4):
        for j in range(4):
            for k in range(j, 4):
                value = sum(
                    inv[i, ell] * (
                        sp.diff(metric[ell, k], coords[j])
                        + sp.diff(metric[ell, j], coords[k])
                        - sp.diff(metric[j, k], coords[ell])
                    ) / 2
                    for ell in range(4)
                )
                if value != 0:
                    conn[i, j, k] = conn[i, k, j] = sp.cancel(value)

    def gamma(i, j, k):
        return conn.get((i, j, k), sp.Integer(0))

    def ricci(i, j):
        value = 0
        for m in range(4):
            value += sp.diff(gamma(m, i, j), coords[m])
            value -= sp.diff(gamma(m, i, m), coords[j])
            for n in range(4):
                value += gamma(m, m, n) * gamma(n, i, j)
                value -= gamma(m, j, n) * gamma(n, i, m)
        return sp.factor(value)

    components = [ricci(i, i) for i in range(4)]
    scalar = sp.cancel(sum(inv[i, i] * components[i] for i in range(4)))
    Gtt = sp.cancel(components[0] - scalar / 2)
    Gzz = sp.cancel(-components[1]/a**2 - scalar / 2)
    transverse = (
        (sp.diff(c, x, 2) + sp.diff(c, y, 2))/c**3
        - (sp.diff(c, x)**2 + sp.diff(c, y)**2)/c**4
    )
    radial_spatial = (
        (sp.diff(a, x, 2) + sp.diff(a, y, 2))/(a*c**2)
        + 2*sp.diff(c, z, 2)/(a**2*c)
        - 2*sp.diff(a, z)*sp.diff(c, z)/(a**3*c)
        + sp.diff(c, z)**2/(a**2*c**2)
    )
    spatial_R = -2*(transverse + radial_spatial)
    H_perp = sp.diff(c, t)/c
    H_parallel = sp.diff(a, t)/a
    require_zero(
        Gtt - spatial_R/2 - H_perp**2 - 2*H_perp*H_parallel,
        "generic 4D Hamiltonian Einstein identity",
    )
    require_zero(
        Gzz - 2*sp.diff(c, t, 2)/c - H_perp**2
        + transverse + (sp.diff(c, z)/(a*c))**2,
        "generic 4D longitudinal Einstein identity",
    )


def frozen_sector_algebra():
    x, y = sp.symbols("x y")
    A, B1, B2, C, Az, B1z, B2z, Cz = sp.symbols(
        "A B1 B2 C Az B1z B2z Cz")
    E = A*(x*x+y*y) + 2*B1*x + 2*B2*y + C
    Ez = Az*(x*x+y*y) + 2*B1z*x + 2*B2z*y + Cz
    chi = 4*(A*C-B1**2-B2**2)
    chiz = 4*(Az*C+A*Cz-2*B1*B1z-2*B2*B2z)
    Ex, Ey = sp.diff(E,x), sp.diff(E,y)
    Exz, Eyz = sp.diff(Ez,x), sp.diff(Ez,y)
    lapE = sp.diff(E,x,2)+sp.diff(E,y,2)
    lapEz = sp.diff(Ez,x,2)+sp.diff(Ez,y,2)
    require_zero(Ex**2+Ey**2-E*lapE+chi,
                 "general quadratic E transverse identity")
    require_zero(2*Ex*Exz+2*Ey*Eyz-Ez*lapE-E*lapEz+chiz,
                 "z derivative of general quadratic identity")

    P,Pz,h,h_z,E0,Ez0,ch,ch_z = sp.symbols(
        "P Pz h h_z E0 Ez0 ch ch_z", nonzero=True)
    q=Ez0/E0
    nu=-q
    D=Pz+P*nu
    # These three geometrical terms follow by substituting a=h*D,
    # c=P/E into the generic spatial Ricci formula above. The polynomial
    # identities checked above eliminate all x/y dependence except E_z/E.
    transverse=-ch/P**2-(ch_z-2*ch*q)/(P*D)
    radial=-2*(h_z/h+q)/(h**2*P*D)+1/(h**2*P**2)
    scalar_3=-2*(transverse+radial)
    ricci_3_zz=(ch_z-2*ch*q)/(P*D)+2*(h_z/h+q)/(h**2*P*D)
    K=ch-1/h**2
    Kz=ch_z+2*h_z/h**3
    require_zero(
        scalar_3-(2*K/P**2+2*(Kz+2*K*nu)/(P*D)),
        "3-curvature scalar with frozen radial constraint",
    )
    require_zero(
        ricci_3_zz-(Kz+2*K*nu)/(P*D),
        "3-curvature longitudinal Ricci with frozen constraint",
    )

    Ms, Mz, Lam, V, Vz = sp.symbols("M Mz Lambda V Vz")
    # Hamiltonian G^t_t in the evolved sector, before using the
    # field equation; differentiate the first integral radially.
    Gtt = (K/P**2 + (Kz+2*K*nu)/(P*D)
           + V**2/P**2 + 2*V*(Vz+V*nu)/(P*D))
    time_first_integral = -K+2*Ms/P+Lam*P**2/3
    twice_VVz = -Kz+2*Mz/P-2*Ms*Pz/P**2+2*Lam*P*Pz/3
    derived=sp.expand(Gtt).subs(V*Vz,twice_VVz/2).subs(V**2,time_first_integral)
    require_zero(derived-Lam-(2*Mz+6*Ms*nu)/(P**2*D),
                 "general Einstein Hamiltonian density")

    xi, X = sp.symbols("xi X")
    Q=-2*Ms*X**3-K*X**2+Lam/3
    shifted_X=-2*(xi+K/12)/Ms
    g2=K**2/12
    g3=K**3/216-Lam*Ms**2/12
    require_zero((Ms**2/4)*Q.subs(X,shifted_X)
                 -(4*xi**3-g2*xi-g3),
                 "frozen X to Weierstrass cubic normalization")
    discr=g2**3-27*g3**2
    require_zero(discr-Lam*Ms**2*(K**3-9*Lam*Ms**2)/48,
                 "Weierstrass discriminant factorization")
    # Time derivative on expanding P>0, X<0 branch: dX/dt = dotP/P^2;
    # Q(X) = (dotP/P)^2, hence dt/du=P when du/dX=1/sqrt(Q).
    require_zero(
        X**4*time_first_integral.subs(P,-1/X)
        -X**2*Q,
        "X-time differential relation (dX/dt)^2 = X^2 Q(X)",
    )


def main():
    print("M1-INH-E1a: generic Einstein and frozen normal-form checks")
    generic_metric_curvature()
    frozen_sector_algebra()
    print("ALL CHECKS PASSED — not external review; E1a scope only")


if __name__ == "__main__":
    main()
