import itertools
import math

import VolumeComparison as vc

title = "Oribital rendenvous travelling salesman problem"
prompt = """
You are an AI in charge of navigating a spaceship in orbit.

You are currently at {PARAM_C} and the mission timer just got set to a 0 second epoch.

You are given a list of {PARAM_A} space stations in orbit, and have to plan a path for a spaceship 
to visit all of them. You need to calculate this route exactly and should use all relevant tools available to you.

Your goal is to minimise Delta-V used for this journey, not time or distance. If a new route takes an extra decade 
and travels a billion more km around the earth, but it saves a drop of fuel, it is a better route.

You may assume:
- The spacecraft is a point mass.
- All coordiantes are Earth-centred inertial (GCRF/J2000) coordinates.
- Your spaceship mass does not change as fuel is expended, and all thrusts are instantaneous.
- Your engine has no maximum impulse and your spacecraft's burns have no maximum delta-V.
- All units are SI except distances, which are in km.
- Rendevous are of duration that is short enough to be considered instantaneous.
- Rndevous does not transfer momentum between spacecraft.
- Two craft must pass within .1km of each other with relative speeds < 0.005km/s in order to successfully rendezvous.
- The earth is a perfect sphere with radius 6371km.
- The moon, sun, and rest of the solar system do not affect the spacecraft.
- The atmosphere does not affect any spacecraft above 100km altitude. Below 100km the spacecraft is destroyed instantly.

Here are the orbits you need to visit: (Of the format [Pos X, Y, Z, Vel X, Y, Z] at the same epoch as your mission timer T=0)
"""

ORBITS = [
    [4579.848378, 5233.075386, 578.192725, -5.209886, 4.167153, 3.551514],
    [5315.246203, -4099.931110, -1906.074155, 1.612607, 4.727540, -5.671965],
    [7078.137000, 0.000000, 0.000000, 0.000000, -1.122156, 7.419911],
    [-3589.068500, 6216.448994, 0.000000, -6.453475, -3.725916, 0.000000],
    [-5021.137307, -2809.845016, 4456.930482, 1.463799, -6.765963, -2.616458],
    [-3789.068500, 0.000000, -6562.859155, -0.000000, -7.252499, -0.000000],
    [-6607.161632, -1921.218246, 3836.584185, 3.874056, -2.671117, 5.334098],
    [-53.281442, -4752.411653, -6655.348928, 4.056966, -4.639096, 3.280179],
    [-7661.829065, -1642.577396, 2820.670269, -2.051378, -1.486347, -6.437742],
    [-1362.468620, 5363.320462, -4332.803085, -6.670648, -3.059719, -1.689831],
    [698.351195, 4409.062340, 5411.795735, -7.451344, -0.667695, 1.703402],
    [-6812.399084, -2955.215678, 1228.168165, 1.667802, -2.013636, 6.765994],
    [7171.882633, 1642.558199, -2648.480780, 2.132941, -0.582761, 6.718964],
    [-6296.298087, -3635.169395, 0.000000, 3.710336, -6.337245, 0.000000],
    [3704.605826, -5239.103802, -3704.605826, 3.912812, 5.072421, -3.912812],
    [3237.525397, 6547.776945, 3508.943089, -5.419795, 3.998320, -1.555682],
    [-1489.187862, -1517.679292, 7169.484087, 2.195551, 6.705530, 1.875509],
    [7073.990791, 54.146209, -875.248289, 0.056803, 7.421118, 0.918197],
    [-7641.080900, 1287.333574, 675.329658, 0.506509, -0.720443, 7.104271],
    [-1845.998197, -6653.941516, -3451.314228, 4.305530, 1.936911, -5.512077],
    [-1489.187862, -1517.679292, 7169.484087, 2.195551, 6.705530, 1.875509],
    [7073.990791, 54.146209, -875.248289, 0.056803, 7.421118, 0.918197],
    [-7641.080900, 1287.333574, 675.329658, 0.506509, -0.720443, 7.104271],
    [-1845.998197, -6653.941516, -3451.314228, 4.305530, 1.936911, -5.512077]
]

def generateOrbitList(length: int) -> list:
    return "\n".join(["Station " + str(i) + ": " + str(orbit) for i, orbit in enumerate(ORBITS[0:length])])

MISSION_LENGTHS = [2, 4, 6, 8, 10, 14, 17, 19]

def prepareSubpassPrompt(index: int) -> str:
    paramC = str(ORBITS[-1][0:3]) + " km (in a LEO orbit " + \
        str(round(math.sqrt(ORBITS[-1][0]**2 + ORBITS[-1][1]**2 + ORBITS[-1][2]**2) - 6371, 2)) + \
        " km above the earths surface) travelling with velocity " + str(ORBITS[-1][3:6]) + " km/s"

    if index == 0: 
        return prompt.format(
            PARAM_A=MISSION_LENGTHS[0], 
            PARAM_C=paramC) + \
                "\n" + generateOrbitList(MISSION_LENGTHS[0])
    if index == 1: 
        return prompt.format(
            PARAM_A=MISSION_LENGTHS[1], 
            PARAM_C=paramC) + \
                "\n" + generateOrbitList(MISSION_LENGTHS[1])
    if index == 2: 
        return prompt.format(
            PARAM_A=MISSION_LENGTHS[2], 
            PARAM_C=paramC) + \
                "\n" + generateOrbitList(MISSION_LENGTHS[2])
    if index == 3: 
        return prompt.format(
            PARAM_A=MISSION_LENGTHS[3], 
            PARAM_C=paramC) + \
                "\n" + generateOrbitList(MISSION_LENGTHS[3])
    if index == 4: 
        return prompt.format(
            PARAM_A=MISSION_LENGTHS[4], 
            PARAM_C=paramC) + \
                "\n" + generateOrbitList(MISSION_LENGTHS[4])
    if index == 5: 
        return prompt.format(
            PARAM_A=MISSION_LENGTHS[5], 
            PARAM_C=paramC) + \
                "\n" + generateOrbitList(MISSION_LENGTHS[5])

    if index == 6: 
        return prompt.format(
            PARAM_A=MISSION_LENGTHS[6], 
            PARAM_C=paramC) + \
                "\n" + generateOrbitList(MISSION_LENGTHS[6])

    if index == 7: 
        return prompt.format(
            PARAM_A=MISSION_LENGTHS[7], 
            PARAM_C=paramC) + \
                "\n" + generateOrbitList(MISSION_LENGTHS[7])
    raise StopIteration

structure = {
    "type": "object",
    "properties": {
        "reasoning": {
            "type": "string",
            "description": "Reasoning for the answer and how your engine burns were calculated."
        },
        "engineBurns": {
            "type": "array",
            "items": {
                    "type": "object",
                    "properties": {
                        "time": {
                            "type": "number",
                            "description": "Mission time in seconds of the burn's midpoint."
                        },
                        "acceleration": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            },
                            "description": "Acceleration in km/s^2 (vector in X, Y, Z). Fuel use is calculated from the magnitude."
                        }
                    },
                    "propertyOrdering": [
                        "time",
                        "acceleration"
                    ],
                    "required": [
                        "time",
                        "acceleration"
                    ],
                    "additionalProperties": False
                }
        },
        "rendevouses": {
            "type": "array",
            "items": {
                    "type": "object",
                    "properties": {
                        "position": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            },
                            "description": "XYZ position (in km earth-centred inertial) of the rendevous"
                        },
                        "velocity": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            },
                            "description": "XYZ velocity (in km/s) of the rendevous"
                        },
                        "time": {
                            "type": "number",
                            "description": "Mission time of the rendevous in seconds"
                        },
                        "station": {
                            "type": "integer",
                            "description": "Which space station we're rendezvous with"
                        }
                    },
                    "propertyOrdering": [
                        "position",
                        "velocity",
                        "time",
                        "station"
                    ],
                    "required": [
                        "position",
                        "velocity",
                        "time",
                        "station"
                    ],
                    "additionalProperties": False
                },
                "description": "Rendevous points"
            }
    },
    "propertyOrdering": [
        "engineBurns",
        "rendevouses",
        "reasoning"
    ],
    "required": [
        "engineBurns",
        "rendevouses",
        "reasoning"
    ],
    "additionalProperties": False
}

subpassParamSummary = [
    "Spacecraft and 2 stations.",
    "Spacecraft and 4 stations.",
    "Spacecraft and 6 stations.",
    "Spacecraft and 8 stations.",
    "Spacecraft and 10 stations.",
    "Spacecraft and 14 stations.",
    "Spacecraft and 17 stations.",
    "Spacecraft and 19 stations.",
]

# Standard gravitational parameter for Earth (km^3/s^2)
MU = 398600.4418

def stumpff_c(z):
    """Stumpff function C(z)"""
    if z > 1e-6:
        return (1 - math.cos(math.sqrt(z))) / z
    elif z < -1e-6:
        return (1 - math.cosh(math.sqrt(-z))) / z
    else:
        return 0.5 - z/24 + z*z/720

def stumpff_s(z):
    """Stumpff function S(z)"""
    if z > 1e-6:
        sz = math.sqrt(z)
        return (sz - math.sin(sz)) / (sz * sz * sz)
    elif z < -1e-6:
        sz = math.sqrt(-z)
        return (math.sinh(sz) - sz) / (sz * sz * sz)
    else:
        return 1/6 - z/120 + z*z/5040

def solve_universal_kepler(r0_mag, vr0, alpha, dt, mu=MU, tol=1e-10, max_iter=50):
    """
    Solve the universal Kepler equation for chi (universal anomaly).
    
    r0_mag: initial radius magnitude
    vr0: initial radial velocity (r0 dot v0 / r0_mag)
    alpha: reciprocal of semi-major axis (1/a), negative for hyperbolic
    dt: time of flight
    mu: gravitational parameter
    """
    # Initial guess for chi
    sqrt_mu = math.sqrt(mu)
    chi = sqrt_mu * abs(alpha) * dt  # Works for elliptical
    
    if abs(alpha) < 1e-10:  # Parabolic
        # Use different initial guess for parabolic
        h_mag = r0_mag * math.sqrt(mu / r0_mag)  # Approximate
        chi = sqrt_mu * dt / r0_mag
    
    for _ in range(max_iter):
        z = alpha * chi * chi
        C = stumpff_c(z)
        S = stumpff_s(z)
        
        chi2 = chi * chi
        chi3 = chi2 * chi
        
        F = r0_mag * vr0 / sqrt_mu * chi2 * C + (1 - alpha * r0_mag) * chi3 * S + r0_mag * chi - sqrt_mu * dt
        dF = r0_mag * vr0 / sqrt_mu * chi * (1 - z * S) + (1 - alpha * r0_mag) * chi2 * C + r0_mag
        
        delta_chi = F / dF
        chi = chi - delta_chi
        
        if abs(delta_chi) < tol:
            break
    
    return chi

def orbitalParamsAndTimeToCartesian(x, y, z, v_x, v_y, v_z, t, mu=MU):
    """
    Propagate an orbital state forward in time using two-body dynamics.
    
    Given initial position (x, y, z) in km and velocity (v_x, v_y, v_z) in km/s,
    compute the position and velocity after time t seconds.
    
    Uses the universal variable formulation (Stumpff functions) which handles
    all orbit types: elliptical, parabolic, and hyperbolic.
    
    Returns: (x_new, y_new, z_new, vx_new, vy_new, vz_new) position and velocity after time t
    """
    if t == 0:
        return (x, y, z, v_x, v_y, v_z)
    
    # Initial position and velocity vectors
    r0 = (x, y, z)
    v0 = (v_x, v_y, v_z)
    
    # Magnitudes
    r0_mag = math.sqrt(x*x + y*y + z*z)
    v0_mag = math.sqrt(v_x*v_x + v_y*v_y + v_z*v_z)
    
    # Radial velocity
    vr0 = (x*v_x + y*v_y + z*v_z) / r0_mag
    
    # Specific orbital energy
    energy = v0_mag*v0_mag / 2 - mu / r0_mag
    
    # Semi-major axis (negative for hyperbolic)
    if abs(energy) < 1e-10:
        alpha = 0  # Parabolic
    else:
        a = -mu / (2 * energy)
        alpha = 1 / a
    
    # Solve universal Kepler equation
    chi = solve_universal_kepler(r0_mag, vr0, alpha, t, mu)
    
    # Compute Stumpff functions
    psi = alpha * chi * chi
    C = stumpff_c(psi)
    S = stumpff_s(psi)
    
    chi2 = chi * chi
    chi3 = chi2 * chi
    sqrt_mu = math.sqrt(mu)
    
    # Lagrange coefficients f and g
    f = 1 - chi2 / r0_mag * C
    g = t - chi3 / sqrt_mu * S
    
    # New position
    x_new = f * x + g * v_x
    y_new = f * y + g * v_y
    z_new = f * z + g * v_z
    
    # New radius magnitude
    r_mag = math.sqrt(x_new*x_new + y_new*y_new + z_new*z_new)
    
    # Lagrange coefficients f_dot and g_dot for velocity
    f_dot = sqrt_mu / (r0_mag * r_mag) * chi * (psi * S - 1)
    g_dot = 1 - chi2 / r_mag * C
    
    # New velocity
    vx_new = f_dot * x + g_dot * v_x
    vy_new = f_dot * y + g_dot * v_y
    vz_new = f_dot * z + g_dot * v_z
    
    return [x_new, y_new, z_new, vx_new, vy_new, vz_new]


def hohmann_transfer_delta_v(r1, r2, mu=MU):
    """
    Calculate the delta-v for an optimal Hohmann transfer between two coplanar circular orbits.
    
    Args:
        r1: radius of initial circular orbit (km)
        r2: radius of final circular orbit (km)
        mu: gravitational parameter (km^3/s^2)
    
    Returns:
        (delta_v1, delta_v2, delta_v_total, transfer_time)
        - delta_v1: delta-v for first burn (km/s)
        - delta_v2: delta-v for second burn (km/s)
        - delta_v_total: total delta-v (km/s)
        - transfer_time: time of flight for transfer (s)
    """
    # Circular velocities
    v1_circ = math.sqrt(mu / r1)
    v2_circ = math.sqrt(mu / r2)
    
    # Transfer orbit semi-major axis
    a_transfer = (r1 + r2) / 2
    
    # Velocities on transfer orbit at periapsis and apoapsis
    # Using vis-viva: v^2 = mu * (2/r - 1/a)
    v_transfer_periapsis = math.sqrt(mu * (2/r1 - 1/a_transfer))
    v_transfer_apoapsis = math.sqrt(mu * (2/r2 - 1/a_transfer))
    
    # Delta-v for each burn
    if r2 > r1:
        # Transfer to higher orbit
        delta_v1 = v_transfer_periapsis - v1_circ  # Prograde burn at r1
        delta_v2 = v2_circ - v_transfer_apoapsis   # Prograde burn at r2
    else:
        # Transfer to lower orbit
        delta_v1 = v1_circ - v_transfer_apoapsis   # Retrograde burn at r1
        delta_v2 = v_transfer_periapsis - v2_circ  # Retrograde burn at r2
    
    delta_v_total = abs(delta_v1) + abs(delta_v2)
    
    # Transfer time is half the orbital period of the transfer ellipse
    transfer_time = math.pi * math.sqrt(a_transfer**3 / mu)
    
    return (abs(delta_v1), abs(delta_v2), delta_v_total, transfer_time)


def lambert_solve(r1_vec, r2_vec, tof, mu=MU, prograde=True, tol=1e-10, max_iter=50):
    """
    Solve Lambert's problem: find the orbit connecting two position vectors
    in a given time of flight.
    
    Args:
        r1_vec: initial position vector (x, y, z) in km
        r2_vec: final position vector (x, y, z) in km
        tof: time of flight in seconds
        mu: gravitational parameter (km^3/s^2)
        prograde: if True, assume prograde transfer; if False, retrograde
        tol: convergence tolerance
        max_iter: maximum iterations
    
    Returns:
        (v1_vec, v2_vec) - velocity vectors at r1 and r2 (km/s)
        Returns None if no solution found
    """
    # Magnitudes
    r1 = math.sqrt(r1_vec[0]**2 + r1_vec[1]**2 + r1_vec[2]**2)
    r2 = math.sqrt(r2_vec[0]**2 + r2_vec[1]**2 + r2_vec[2]**2)
    
    # Cross product r1 x r2 for direction
    cross_z = r1_vec[0]*r2_vec[1] - r1_vec[1]*r2_vec[0]
    
    # Compute delta true anomaly
    cos_dnu = (r1_vec[0]*r2_vec[0] + r1_vec[1]*r2_vec[1] + r1_vec[2]*r2_vec[2]) / (r1 * r2)
    cos_dnu = max(-1, min(1, cos_dnu))  # Clamp for numerical stability
    
    # Determine direction based on prograde/retrograde
    if prograde:
        if cross_z >= 0:
            sin_dnu = math.sqrt(1 - cos_dnu**2)
        else:
            sin_dnu = -math.sqrt(1 - cos_dnu**2)
    else:
        if cross_z < 0:
            sin_dnu = math.sqrt(1 - cos_dnu**2)
        else:
            sin_dnu = -math.sqrt(1 - cos_dnu**2)
    
    dnu = math.atan2(sin_dnu, cos_dnu)
    
    # Geometry parameter A
    A = math.sqrt(r1 * r2) * sin_dnu / math.sqrt(1 - cos_dnu) if abs(1 - cos_dnu) > 1e-10 else 0
    
    if abs(A) < 1e-10:
        return None  # Degenerate case (180 degree transfer)
    
    # Initial guess for z (related to semi-major axis)
    z = 0.0
    
    # Newton iteration to solve for z
    sqrt_mu = math.sqrt(mu)
    
    for _ in range(max_iter):
        C = stumpff_c(z)
        S = stumpff_s(z)
        
        # y parameter
        y = r1 + r2 + A * (z * S - 1) / math.sqrt(C)
        
        if y < 0:
            # Adjust z if y becomes negative
            z = z * 0.5
            continue
        
        sqrt_y = math.sqrt(y)
        
        # chi (universal anomaly related)
        chi = sqrt_y / math.sqrt(C)
        
        # Time of flight equation
        F = (y / C)**1.5 * S + A * sqrt_y - sqrt_mu * tof
        
        # Derivative dF/dz
        if abs(z) < 1e-10:
            dF = math.sqrt(2) / 40 * y**1.5 + A/8 * (math.sqrt(y) + A * math.sqrt(1/(2*y)))
        else:
            dF = (y/C)**1.5 * (1/(2*z) * (C - 3*S/(2*C)) + 3*S**2/(4*C)) + \
                 A/8 * (3*S/C * sqrt_y + A * math.sqrt(C/y))
        
        # Newton step
        z_new = z - F / dF
        
        if abs(z_new - z) < tol:
            z = z_new
            break
        z = z_new
    
    # Recompute final values
    C = stumpff_c(z)
    S = stumpff_s(z)
    y = r1 + r2 + A * (z * S - 1) / math.sqrt(C)
    
    if y < 0:
        return None
    
    # Lagrange coefficients
    f = 1 - y / r1
    g = A * math.sqrt(y / mu)
    g_dot = 1 - y / r2
    
    # Velocity vectors
    v1_vec = ((r2_vec[0] - f * r1_vec[0]) / g,
              (r2_vec[1] - f * r1_vec[1]) / g,
              (r2_vec[2] - f * r1_vec[2]) / g)
    
    v2_vec = ((g_dot * r2_vec[0] - r1_vec[0]) / g + v1_vec[0] * (1 - g_dot * f) / g_dot if abs(g_dot) > 1e-10 else 
              (g_dot * r2_vec[0] - r1_vec[0]) / g,
              (g_dot * r2_vec[1] - r1_vec[1]) / g + v1_vec[1] * (1 - g_dot * f) / g_dot if abs(g_dot) > 1e-10 else
              (g_dot * r2_vec[1] - r1_vec[1]) / g,
              (g_dot * r2_vec[2] - r1_vec[2]) / g + v1_vec[2] * (1 - g_dot * f) / g_dot if abs(g_dot) > 1e-10 else
              (g_dot * r2_vec[2] - r1_vec[2]) / g)
    
    # Simpler v2 calculation using f_dot
    f_dot = math.sqrt(mu / y) * (z * S - 1) / (r1 * r2) * A / g if abs(g) > 1e-10 else 0
    v2_vec = (f_dot * r1_vec[0] + g_dot * v1_vec[0],
              f_dot * r1_vec[1] + g_dot * v1_vec[1],
              f_dot * r1_vec[2] + g_dot * v1_vec[2])
    
    return (v1_vec, v2_vec)


def general_transfer_delta_v(r1_vec, v1_vec, r2_vec, v2_vec, tof=None, mu=MU):
    """
    Calculate the delta-v for a transfer between two arbitrary orbital states.
    
    Uses Lambert's problem to find the optimal transfer orbit for a given time of flight.
    If tof is None, estimates a reasonable transfer time and searches for minimum delta-v.
    
    Args:
        r1_vec: initial position (x, y, z) in km
        v1_vec: initial velocity (vx, vy, vz) in km/s
        r2_vec: target position (x, y, z) in km
        v2_vec: target velocity (vx, vy, vz) in km/s
        tof: time of flight (s). If None, searches for optimal.
        mu: gravitational parameter (km^3/s^2)
    
    Returns:
        (delta_v1, delta_v2, delta_v_total, tof_used)
        - delta_v1: departure delta-v magnitude (km/s)
        - delta_v2: arrival delta-v magnitude (km/s)
        - delta_v_total: total delta-v (km/s)
        - tof_used: time of flight used (s)
        
        Returns None if no solution found.
    """
    r1 = math.sqrt(r1_vec[0]**2 + r1_vec[1]**2 + r1_vec[2]**2)
    r2 = math.sqrt(r2_vec[0]**2 + r2_vec[1]**2 + r2_vec[2]**2)
    
    if tof is not None:
        # Solve for specific time of flight
        result = lambert_solve(r1_vec, r2_vec, tof, mu)
        if result is None:
            return None
        
        v1_transfer, v2_transfer = result
        
        # Delta-v magnitudes
        dv1 = (v1_transfer[0] - v1_vec[0], v1_transfer[1] - v1_vec[1], v1_transfer[2] - v1_vec[2])
        dv2 = (v2_vec[0] - v2_transfer[0], v2_vec[1] - v2_transfer[1], v2_vec[2] - v2_transfer[2])
        
        delta_v1 = math.sqrt(dv1[0]**2 + dv1[1]**2 + dv1[2]**2)
        delta_v2 = math.sqrt(dv2[0]**2 + dv2[1]**2 + dv2[2]**2)
        
        return (delta_v1, delta_v2, delta_v1 + delta_v2, tof)
    
    # Search for optimal time of flight
    # Use Hohmann-like estimate as starting point
    a_transfer_est = (r1 + r2) / 2
    tof_hohmann = math.pi * math.sqrt(a_transfer_est**3 / mu)
    
    # Search range: 0.5x to 3x Hohmann time
    best_dv = float('inf')
    best_result = None
    
    # Coarse search
    for factor in [0.5, 0.7, 0.85, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0]:
        tof_try = tof_hohmann * factor
        
        for prograde in [True, False]:
            result = lambert_solve(r1_vec, r2_vec, tof_try, mu, prograde=prograde)
            if result is None:
                continue
            
            v1_transfer, v2_transfer = result
            
            dv1 = (v1_transfer[0] - v1_vec[0], v1_transfer[1] - v1_vec[1], v1_transfer[2] - v1_vec[2])
            dv2 = (v2_vec[0] - v2_transfer[0], v2_vec[1] - v2_transfer[1], v2_vec[2] - v2_transfer[2])
            
            delta_v1 = math.sqrt(dv1[0]**2 + dv1[1]**2 + dv1[2]**2)
            delta_v2 = math.sqrt(dv2[0]**2 + dv2[1]**2 + dv2[2]**2)
            total_dv = delta_v1 + delta_v2
            
            if total_dv < best_dv:
                best_dv = total_dv
                best_result = (delta_v1, delta_v2, total_dv, tof_try)
    
    return best_result


def transfer_delta_v_lower_bound(r1_vec, v1_vec, r2_vec, v2_vec, mu=MU):
    """
    Compute a lower bound on the delta-v required to transfer between two orbital states.
    
    This provides a quick estimate without solving Lambert's problem, useful for
    pruning in optimization algorithms.
    
    The lower bound is based on:
    1. Minimum energy change required (vis-viva)
    2. Plane change requirement
    
    Args:
        r1_vec: initial position (x, y, z) in km
        v1_vec: initial velocity (vx, vy, vz) in km/s
        r2_vec: target position (x, y, z) in km  
        v2_vec: target velocity (vx, vy, vz) in km/s
        mu: gravitational parameter (km^3/s^2)
    
    Returns:
        Lower bound on total delta-v (km/s)
    """
    # Compute orbital energies
    r1 = math.sqrt(r1_vec[0]**2 + r1_vec[1]**2 + r1_vec[2]**2)
    r2 = math.sqrt(r2_vec[0]**2 + r2_vec[1]**2 + r2_vec[2]**2)
    v1 = math.sqrt(v1_vec[0]**2 + v1_vec[1]**2 + v1_vec[2]**2)
    v2 = math.sqrt(v2_vec[0]**2 + v2_vec[1]**2 + v2_vec[2]**2)
    
    energy1 = v1**2 / 2 - mu / r1
    energy2 = v2**2 / 2 - mu / r2
    
    # Semi-major axes (negative for hyperbolic)
    if abs(energy1) > 1e-10:
        a1 = -mu / (2 * energy1)
    else:
        a1 = float('inf')
    
    if abs(energy2) > 1e-10:
        a2 = -mu / (2 * energy2)
    else:
        a2 = float('inf')
    
    # Angular momentum vectors h = r x v
    h1 = (r1_vec[1]*v1_vec[2] - r1_vec[2]*v1_vec[1],
          r1_vec[2]*v1_vec[0] - r1_vec[0]*v1_vec[2],
          r1_vec[0]*v1_vec[1] - r1_vec[1]*v1_vec[0])
    
    h2 = (r2_vec[1]*v2_vec[2] - r2_vec[2]*v2_vec[1],
          r2_vec[2]*v2_vec[0] - r2_vec[0]*v2_vec[2],
          r2_vec[0]*v2_vec[1] - r2_vec[1]*v2_vec[0])
    
    h1_mag = math.sqrt(h1[0]**2 + h1[1]**2 + h1[2]**2)
    h2_mag = math.sqrt(h2[0]**2 + h2[1]**2 + h2[2]**2)
    
    # Angle between orbital planes
    if h1_mag > 1e-10 and h2_mag > 1e-10:
        cos_inclination = (h1[0]*h2[0] + h1[1]*h2[1] + h1[2]*h2[2]) / (h1_mag * h2_mag)
        cos_inclination = max(-1, min(1, cos_inclination))
        delta_i = math.acos(cos_inclination)
    else:
        delta_i = 0
    
    # Lower bound components:
    
    # 1. Minimum delta-v for Hohmann-like transfer (ignoring plane change)
    if a1 > 0 and a2 > 0 and a1 != float('inf') and a2 != float('inf'):
        # Use characteristic radii
        r_char1 = a1  # Could use periapsis/apoapsis for tighter bound
        r_char2 = a2
        
        # Simplified Hohmann estimate
        v_circ1 = math.sqrt(mu / r_char1) if r_char1 > 0 else 0
        v_circ2 = math.sqrt(mu / r_char2) if r_char2 > 0 else 0
        
        if r_char1 > 0 and r_char2 > 0:
            a_t = (r_char1 + r_char2) / 2
            if a_t > 0:
                v_t1 = math.sqrt(max(0, mu * (2/r_char1 - 1/a_t)))
                v_t2 = math.sqrt(max(0, mu * (2/r_char2 - 1/a_t)))
                dv_hohmann = abs(v_t1 - v_circ1) + abs(v_circ2 - v_t2)
            else:
                dv_hohmann = abs(v1 - v2)
        else:
            dv_hohmann = abs(v1 - v2)
    else:
        # Hyperbolic or parabolic - use velocity difference as rough estimate
        dv_hohmann = abs(v1 - v2) * 0.5
    
    # 2. Minimum plane change delta-v
    # Optimal plane change at highest point uses: dv = 2*v*sin(di/2)
    v_at_change = min(v1, v2)  # Conservative: use lower velocity
    dv_plane = 2 * v_at_change * math.sin(delta_i / 2) if delta_i > 0 else 0
    
    # The actual lower bound - these can be combined optimally, so we use
    # a conservative estimate (not just sum)
    # For combined plane change + transfer: dv >= sqrt(dv_h^2 + dv_p^2 - 2*dv_h*dv_p*cos(di))
    # But simpler lower bound: max of the two components
    lower_bound = max(dv_hohmann * 0.8, dv_plane * 0.5, abs(v1 - v2) * 0.3)
    
    return lower_bound

def gradeAnswer(answer: dict, subPass: int, aiEngineName: str):
    currentTime = 0
    currentOrbit = list(ORBITS[-1])
    
    burns = answer.get("engineBurns", [])
    rendezvous = answer.get("rendevouses", [])

    burns.sort(key=lambda x: x["time"])
    rendezvous.sort(key=lambda x: x["time"])

    # Check to see if we rendevous with every station exactly once.
    rendezvousStations = set()
    for r in rendezvous:
        rendezvousStations.add(r["station"])
    if len(rendezvousStations) != MISSION_LENGTHS[subPass]:
        return 0, "Must rendezvous with every station exactly once"

    # Check to see if we rendevous with any station higher than 2000km
    for r in rendezvous:
        heightAboveEarth = round(math.sqrt(r["position"][0]**2 + r["position"][1]**2 + r["position"][2]**2) - 6371)
        if heightAboveEarth > 10000:
            return 0, "Spacecraft is planning a rendezvous at an altitude of " + \
                str(heightAboveEarth) + "km above mean sea level, which is well above LEO orbit and higher than any of these stations get."

    # Before we start the complex simulation, try to estimate the delta-v used
    roughDeltaV = 0
    for b in burns:
        roughDeltaV += math.sqrt(b["acceleration"][0]**2 + b["acceleration"][1]**2 + b["acceleration"][2]**2)

    if roughDeltaV > 15000:
        return 0, "Spacecraft is planning to use more than 15km/s of delta-v from LEO, which is enough to escape the solar system."

    if roughDeltaV > 5000:
        return 0, "Spacecraft is planning to use more than 5km/s of delta-v from LEO, which is is more than a Mars mission."

    deltaVUsed = 0
    STEP_SIZE = 10  # seconds per simulation step
    EARTH_RADIUS = 6371
    MIN_ALTITUDE = 100
    MAX_ALTITUDE = 10000 # We allow high ellipses

    # Find the end time (last event)
    allEventTimes = [b["time"] for b in burns] + [r["time"] for r in rendezvous]
    if not allEventTimes:
        return 0, "No events scheduled"
    endTime = max(allEventTimes)

    while currentTime < endTime:
        # Check altitude constraint
        altitude = math.sqrt(currentOrbit[0]**2 + currentOrbit[1]**2 + currentOrbit[2]**2) - EARTH_RADIUS
        if altitude < MIN_ALTITUDE:
            return 0, f"Spacecraft crashed! Altitude {altitude:.1f}km at T={currentTime}s is below {MIN_ALTITUDE}km"
        if altitude > MAX_ALTITUDE:
            return 0, f"Spacecraft left LEO! Altitude {altitude:.1f}km at T={currentTime}s exceeds {MAX_ALTITUDE}km"

        # Process any burns at this time
        while burns and burns[0]["time"] <= currentTime:
            burn = burns.pop(0)
            deltaV = burn["acceleration"]
            deltaVUsed += math.sqrt(deltaV[0]**2 + deltaV[1]**2 + deltaV[2]**2)
            currentOrbit[3] += deltaV[0]
            currentOrbit[4] += deltaV[1]
            currentOrbit[5] += deltaV[2]

        # Process any rendezvous at this time
        while rendezvous and rendezvous[0]["time"] <= currentTime:
            rend = rendezvous.pop(0)
            rPos = rend["position"]
            rVel = rend["velocity"]

            if abs(rPos[0] - currentOrbit[0]) > 1 or abs(rPos[1] - currentOrbit[1]) > 1 or abs(rPos[2] - currentOrbit[2]) > 1:
                return 0, "Rendezvous position does not match current orbit. SpaceCraft is at " \
                    + str(currentOrbit[0:3]) + " km but rendezvous is supposed to be at " + str(rPos) + " km"

            if abs(rVel[0] - currentOrbit[3]) > 0.05 or abs(rVel[1] - currentOrbit[4]) > 0.05 or abs(rVel[2] - currentOrbit[5]) > 0.05:
                return 0, "Rendezvous velocity does not match current orbit. SpaceCraft is travelling at " \
                    + str(currentOrbit[3:6]) + " km/s but rendezvous is supposed to be at velocity " + str(rVel) + " km/s"

            # Check station position at rendezvous time
            craftOrbit = orbitalParamsAndTimeToCartesian(*ORBITS[rend["station"]], rend["time"])

            if abs(craftOrbit[0] - rPos[0]) > 1 or abs(craftOrbit[1] - rPos[1]) > 1 or abs(craftOrbit[2] - rPos[2]) > 1:
                return 0, "Rendezvous position does not match station orbit. SpaceCraft is at " \
                    + str(currentOrbit[0:3]) + " km but station " + str(rend["station"]) + " is at " + str(craftOrbit[0:3]) + " km"

            if abs(craftOrbit[3] - rVel[0]) > 0.05 or abs(craftOrbit[4] - rVel[1]) > 0.05 or abs(craftOrbit[5] - rVel[2]) > 0.05:
                return 0, "Rendezvous velocity does not match station orbit. SpaceCraft is travelling at " \
                    + str(currentOrbit[3:6]) + " km/s but station " + str(rend["station"]) + " is at velocity " + str(craftOrbit[3:6]) + " km/s"

        # Advance simulation
        currentOrbit = list(orbitalParamsAndTimeToCartesian(*currentOrbit, STEP_SIZE))
        currentTime += STEP_SIZE

    # Now calculate the optimal delta-V
    bestDeltaV = float('inf')
    for ordering in itertools.permutations(MISSION_LENGTHS[subPass],MISSION_LENGTHS[subPass]):
        currentOrbit = ORBITS[-1]
        deltaVUsed = 0

        for destination in ordering:
            deltaVUsed += general_transfer_delta_v(
                currentOrbit[0:3], currentOrbit[3:6], 
                ORBITS[destination][0:3], ORBITS[destination][3:6])
            currentOrbit = ORBITS[destination]
        
        if deltaVUsed < bestDeltaV:
            bestDeltaV = deltaVUsed

    return bestDeltaV / deltaVUsed, "Used " + str(deltaVUsed) + " km/s, best possible " + str(bestDeltaV) + " km/s"

def resultToNiceReport(answer, subPass, aiEngineName):
    scadOutput = "color([0,0,1]) sphere(6371, $fn=100);"


    currentTime = 0
    currentOrbit = ORBITS[-1]
    
    burns = answer.get("engineBurns", [])
    burns.sort(key=lambda x: x["time"])


    for burn in burns:
        nextTime  = burn["time"]

        while nextTime > currentTime + 10:
            currentOrbit = list(orbitalParamsAndTimeToCartesian(*currentOrbit, 10))
            currentTime += 10

            scadOutput += \
                "color([1,1,1])" + \
                "translate([" + str(currentOrbit[0]) + "," + str(currentOrbit[1]) + "," + str(currentOrbit[2]) + "]) sphere(20);\n"

        currentOrbit = list(orbitalParamsAndTimeToCartesian(*currentOrbit, nextTime - currentTime))
        currentTime = nextTime

        scadOutput += \
            "color([1,0,0])" + \
            "translate([" + str(currentOrbit[0]) + "," + str(currentOrbit[1]) + "," + str(currentOrbit[2]) + "]) sphere(50);\n"

        currentOrbit[3] += burn["acceleration"][0]
        currentOrbit[4] += burn["acceleration"][1]
        currentOrbit[5] += burn["acceleration"][2]


    # And now continue the path on the orbit we endded up in. 
    for i in range(2000):
        currentOrbit = orbitalParamsAndTimeToCartesian(*currentOrbit, 10)
        scadOutput += \
            "color([1,1,0])" + \
            "translate([" + str(currentOrbit[0]) + "," + str(currentOrbit[1]) + "," + str(currentOrbit[2]) + "]) sphere(20);\n"


    # Now draw the orbits of the things we rendezvous with.
    for i in range(MISSION_LENGTHS[subPass]):
        orbit = ORBITS[i]
        for j in range(2000):
            orbit = orbitalParamsAndTimeToCartesian(*orbit, 10)

            manhattanDistanceFromStart = abs(orbit[0] - ORBITS[i][0]) + abs(orbit[1] - ORBITS[i][1]) + abs(orbit[2] - ORBITS[i][2])

            if j > 100 and manhattanDistanceFromStart < 100: break

            scadOutput += \
                "color([0,1,0])" + \
                "translate([" + str(orbit[0]) + "," + str(orbit[1]) + "," + str(orbit[2]) + "]) sphere(20);\n"


    import os
    os.makedirs("results", exist_ok=True)
    output_path = "results/22_Visualization_" + aiEngineName + "_" + str(subPass) + ".png"
    vc.render_scadText_to_png(scadOutput, output_path)
    print(f"Saved visualization to {output_path}")


    return f"""
<a href="{os.path.basename(output_path).replace(".png", "temp.scad")}" download>
<img src="{os.path.basename(output_path)}" alt="Orbital Visualization" style="max-width: 100%;">
</a>
"""


if __name__ == "__main__":
    print(prepareSubpassPrompt(0))
    print(gradeAnswer(
        {"engineBurns":[
            {"time":285,"acceleration":[0.617,0.002,0.001]},
            {"time":300,"acceleration":[0.02,0.8100,0.001]},
            {"time":310,"acceleration":[0.003,0.001,0.5655]}],
        "rendevouses":[
            {"position":[1610.213,7608.353,-10414.022],"velocity":[0.00617,0,0],"time":570,"station":0},
            {"position":[7734.157,7089.379,-10414.022],"velocity":[1.612607,4.72754,-5.671965],"time":1500,"station":1}]},
        0,
        "Placebo"))
    print(resultToNiceReport(
        {"engineBurns":[
            {"time":285,"acceleration":[0.617,0.002,0.001]},
            {"time":300,"acceleration":[0.02,0.8100,0.001]},
            {"time":310,"acceleration":[0.003,0.001,0.5655]}],
        "rendevouses":[
            {"position":[1610.213,7608.353,-10414.022],"velocity":[0.00617,0,0],"time":570,"station":0},
            {"position":[7734.157,7089.379,-10414.022],"velocity":[1.612607,4.72754,-5.671965],"time":1500,"station":1}]},
        0,
        "Placebo"))