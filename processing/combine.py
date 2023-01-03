def finalCoords(rssi, imu, prevCoords, rssiWeight=0.5):
    if prevCoords == None:
        prevCoords = [0, 0]
        rssiWeight = 1
    imuWeight = 1 - rssiWeight
    rssi = [(rssi[i] - prevCoords[i]) for i in range(2)]
    dx = rssi[0] * rssiWeight + imu[0] * imuWeight
    dy = rssi[1] * rssiWeight + imu[1] * imuWeight
    return [prevCoords[0] + dx, prevCoords[1] + dy]