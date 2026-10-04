// WRONG — this is what ships inverted A/D in the wild
if (KeyA) steer -= 1;
if (KeyD) steer += 1;
yaw += steer * turnRate * dt;  // A → −yaw → nose RIGHT on chase cam
