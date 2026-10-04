def phi_mapping(discriminant):
    return (math.log(abs(discriminant)) / math.log(DELTA_MAX)) * 360


def theta_mapping(conductor):
    return (math.log(abs(conductor)) / math.log(N_MAX)) * 180


def elevation_mapping(rank):
    return rank * RANK_SCALING


def Phi(discriminant, conductor, rank, regulator):
    phi = phi_mapping(discriminant)
    theta = theta_mapping(conductor)
    z = elevation_mapping(rank)
    size = math.log(1 + regulator)
    return {
        "longitude": phi,
        "latitude": theta,
        "elevation_m": z,
        "node_size": size
    }
