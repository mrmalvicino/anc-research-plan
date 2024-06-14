import numpy as np
import random as rnd
import math

def anc_status(samples_quantity, measurements_per_sample):
    anc_status = np.empty((samples_quantity, measurements_per_sample))

    for i in range(samples_quantity):
        for j in range(0, measurements_per_sample, 4):
            anc_status[i][j] = 0
            anc_status[i][j+1] = 0
            anc_status[i][j+2] = 1
            anc_status[i][j+3] = 1

    return anc_status

def measured_noise(background_noise_mean, background_noise_deviation, delta_spl, generated_noise_spl, samples_quantity, measurements_per_sample):
    measured_noise = np.empty((samples_quantity, measurements_per_sample))

    for i in range(samples_quantity):
        for j in range(measurements_per_sample):
            background_noise_spl = rnd.gauss(background_noise_mean, background_noise_deviation)

            if (j % 2 == 0):
                measured_noise[i][j] = background_noise_spl # Solo ruido de fondo
            else:
                measured_noise[i][j] = 10 * math.log10(10 ** (background_noise_spl / 10) + 10 ** (generated_noise_spl / 10)) # Ruido de fondo + señal de ruido emitida

    return measured_noise

def perceived_noise(samples_quantity, measurements_per_sample):
    perceived_noise = np.empty((samples_quantity, measurements_per_sample))

    for i in range(samples_quantity):
        for j in range(measurements_per_sample):
            perceived_noise[i][j] = rnd.randint(1, 2)

    return perceived_noise


def perceived_quality(samples_quantity, measurements_per_sample):
    perceived_quality = np.empty((samples_quantity, measurements_per_sample))

    for i in range(samples_quantity):
        for j in range(measurements_per_sample):
            perceived_quality[i][j] = rnd.randint(1, 2)

    return perceived_quality
