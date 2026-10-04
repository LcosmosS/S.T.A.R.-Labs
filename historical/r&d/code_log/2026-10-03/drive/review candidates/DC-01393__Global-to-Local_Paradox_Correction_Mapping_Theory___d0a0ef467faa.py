import math


def safe_log(x, epsilon=1e-9):
    return math.log(max(abs(x), epsilon))


def Phi(discriminant, conductor, rank, regulator):
    phi = (safe_log(discriminant) / safe_log(DELTA_MAX)) * 360
    theta = (safe_log(conductor) / safe_log(N_MAX)) * 180
    z = rank * RANK_SCALING
    s = math.log(1 + regulator)
    return {"longitude": phi, "latitude": theta, "elevation_m": z, "node_size": s}
