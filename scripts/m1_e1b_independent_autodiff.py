"""Independent numerical automatic-differentiation witness for frozen M1 E1b.

This is NOT independent mathematical proof, peer review, or the general E1a
derivation. Run explicitly in a disposable CPU environment:
    python -m pip install 'jax[cpu]==0.9.0.1'
    python scripts/m1_e1b_independent_autodiff.py
It performs no registry mutation and writes no science result artifacts.
"""
import json
import jax
jax.config.update("jax_enable_x64", True)
import jax.numpy as np
from jax import jacfwd


def metric(v, sector):
    """Return the diagonal M1 E1b metric with signature (+, -, -, -).

    Args:
        v: Coordinates in (t, z, x, y) order at a regular interior point.
        sector: 0 for the transverse-independent case or 1 for the varying case.

    Returns:
        A 4-by-4 JAX array of covariant metric components.
    """
    t,z,x,y = v
    m = 1.+z
    P=(2.*m)**(1./3.)*np.sinh(1.5*(t+z))**(2./3.)
    H=1./np.tanh(1.5*(t+z))
    B=1./(3.*m)
    w=np.exp(z) if sector else 1.
    q=w*w*(x*x+y*y)
    d=(1.-q)/(1.+q) if sector else 0.
    a=P*(H+B+d)
    c=2.*P*w/(1.+q)
    return np.diag(np.array([1.,-a*a,-c*c,-c*c]))


def christoffel(v, sector):
    """Return Christoffel symbols Gamma^a_bc from metric autodifferentiation.

    Args:
        v: Coordinates in (t, z, x, y) order at a regular interior point.
        sector: Metric sector, 0 or 1.

    Returns:
        A JAX array indexed by (a, b, c), with the first index contravariant.
    """
    g=metric(v,sector)
    gi=np.linalg.inv(g)
    dg=jacfwd(lambda v: metric(v,sector))(v)
    term=(np.einsum("cdb->dbc",dg)
          +np.einsum("bdc->dbc",dg)
          -np.einsum("bcd->dbc",dg))
    return 0.5*np.einsum("ad,dbc->abc",gi,term)


def einstein_mixed(v,sector):
    """Compute the mixed Einstein tensor G^a_b using JAX derivatives.

    Args:
        v: Coordinates in (t, z, x, y) order at a regular interior point.
        sector: Metric sector, 0 or 1.

    Returns:
        A 4-by-4 JAX array with the first tensor index raised.
    """
    g=metric(v,sector)
    gi=np.linalg.inv(g)
    ga=christoffel(v,sector)
    dga=jacfwd(lambda v:christoffel(v,sector))(v)
    R=(np.einsum("kabk->ab",dga)
       -np.einsum("kakb->ab",dga)
       +np.einsum("kkl,lab->ab",ga,ga)
       -np.einsum("kbl,lak->ab",ga,ga))
    scalar=np.einsum("ab,ab->",gi,R)
    return gi@(R-0.5*scalar*g)


def rho_expected(v,sector):
    """Return the analytic dust density used to check G^a_b - 3 delta^a_b.

    Args:
        v: Coordinates in (t, z, x, y) order at a regular interior point.
        sector: Metric sector, 0 or 1.

    Returns:
        The expected scalar density for the chosen sector.
    """
    t,z,x,y=v
    H=1./np.tanh(1.5*(t+z))
    B=1./(3*(1+z))
    w=np.exp(z) if sector else 1.
    q=w*w*(x*x+y*y)
    d=(1-q)/(1+q) if sector else 0.
    return 3*(H*H-1)*(B+d)/(H+B+d)


def J_expected(v,sector):
    """Return the analytic squared transverse density-gradient norm J.

    Args:
        v: Coordinates in (t, z, x, y) order at a regular interior point.
        sector: Metric sector, 0 or 1.

    Returns:
        Zero for sector 0, or the analytic transverse discriminator for sector 1.
    """
    if not sector:return 0.
    t,z,x,y=v
    P=(2*(1+z))**(1./3.)*np.sinh(1.5*(t+z))**(2./3.)
    H=1./np.tanh(1.5*(t+z))
    B=1./(3*(1+z))
    q=np.exp(2*z)*(x*x+y*y)
    d=(1-q)/(1+q)
    return 36*H*H*(H*H-1)**2*q/(P*P*(H+B+d)**4*(1+q)**2)


def run():
    """Print four numerical spot checks and assert field and gradient tolerances.

    These sampled checks provide numerical corroboration, not a proof.

    Raises:
        AssertionError: A residual or sector discriminator fails its check.
    """
    points=[(1.3,0.1,0.2,0.1),(1.8,-0.17,-0.15,0.25)]
    records=[]
    for sector in (0,1):
        for point in points:
            v=np.array(point)
            G=einstein_mixed(v,sector)
            T=G-3*np.eye(4)
            expected=np.diag(np.array([rho_expected(v,sector),0.,0.,0.]))
            residual=float(np.max(np.abs(T-expected)))
            delta=1e-4
            d=[]
            for axis in (2,3):
                shift=np.zeros(4).at[axis].set(delta)
                plus=float((einstein_mixed(v+shift,sector)-3*np.eye(4)).trace())
                minus=float((einstein_mixed(v-shift,sector)-3*np.eye(4)).trace())
                d.append((plus-minus)/(2*delta))
            c=np.sqrt(-metric(v,sector)[2,2])
            J_num=float((d[0]**2+d[1]**2)/c**2)
            J_exact=float(J_expected(v,sector))
            records.append({
                "sector":sector,
                "point":point,
                "max_field_equation_residual":residual,
                "J_numerical":J_num,
                "J_exact":J_exact,
                "abs_J_error":abs(J_num-J_exact),
            })
    print(json.dumps(records,indent=2))
    assert all(x["max_field_equation_residual"]<2e-11 for x in records)
    assert all(x["abs_J_error"]<2e-6 for x in records)
    assert all(x["J_exact"]==0 for x in records if x["sector"]==0)
    assert all(x["J_exact"]>0 for x in records if x["sector"]==1)
    print("NUMERICAL_AUTODIFF_SPOT_CHECK_PASS (not independent proof)")


if __name__=="__main__":
    run()
