import numpy as np
import random as rnd
import math

def anc_status(samples_quantity, measurements_per_sample):
    anc_status = np.empty((samples_quantity, measurements_per_sample), int)

    for i in range(samples_quantity):
        for j in range(0, measurements_per_sample, 4):
            anc_status[i][j] = 0
            anc_status[i][j+1] = 0
            anc_status[i][j+2] = 1
            anc_status[i][j+3] = 1

    return anc_status

def measured_noise(background_noise_mean, background_noise_deviation, delta_spl, generated_noise_spl, samples_quantity, measurements_per_sample):
    measured_noise = np.empty((samples_quantity, measurements_per_sample), float)

    for i in range(samples_quantity):
        for j in range(measurements_per_sample):
            background_noise_spl = rnd.gauss(background_noise_mean, background_noise_deviation)

            if (j % 2 == 0):
                measured_noise[i][j] = background_noise_spl # Solo ruido de fondo
            else:
                measured_noise[i][j] = 10 * math.log10(10 ** (background_noise_spl / 10) + 10 ** (generated_noise_spl / 10)) # Ruido de fondo + señal de ruido emitida

    return measured_noise

def perceived_noise(samples_quantity, measurements_per_sample, anc_status, measured_noise, background_noise_max):
    perceived_noise = np.empty((samples_quantity, measurements_per_sample), int)
    values = [1, 2]

    for i in range(samples_quantity):
        for j in range(measurements_per_sample):
            if (anc_status[i][j] == 1 or measured_noise[i][j] <= background_noise_max):
                weights = [0.8, 0.2] # Si la ANC está encendida o se mide poco ruido, es más probable que escuche con poco ruido
            else:
                weights = [0.1, 0.9] # Si la ANC está apagada y se mide mucho ruido, es más probable que escuche con mucho ruido

            perceived_noise[i][j] = rnd.choices(values, weights)[0]

    return perceived_noise


def perceived_quality(samples_quantity, measurements_per_sample, anc_status):
    perceived_quality = np.empty((samples_quantity, measurements_per_sample), int)
    values = [1, 2]

    for i in range(samples_quantity):
        for j in range(measurements_per_sample):
            if (anc_status[i][j] == 1):
                weights = [0.6, 0.4] # Si la ANC está encendida, es más probable que escuche con baja calidad
            else:
                weights = [0.3, 0.7] # Si la ANC está apagada, es más probable que escuche con alta calidad

            perceived_quality[i][j] = rnd.choices(values, weights)[0]

    return perceived_quality

def list_outliers(anc_status, measured_noise, perceived_noise, background_noise_max, samples_quantity, measurements_per_sample):
    strike_1 = [] # Sensibles
    strike_2 = [] # Sordos
    outliers = [] # Sensibles y sordos (absurdo)

    for i in range(samples_quantity):
        for j in range(measurements_per_sample):
            if (perceived_noise[i][j] == 2 and measured_noise[i][j] <= background_noise_max and anc_status[i][j] == 0): # Si percibe mucho ruido y solo hay ruido de fondo y la anc está apagada
                if (i not in outliers): # No agregar dos veces
                    strike_1.append(i) # Potencial outlier

    for i in range(samples_quantity):
        for j in range(measurements_per_sample):
            if (perceived_noise[i][j] == 1 and background_noise_max < measured_noise[i][j] and anc_status[i][j] == 0): # Si percibe poco ruido cuando hay ruido generado y la anc está apagada
                if (i not in outliers): # No agregar dos veces
                    strike_2.append(i) # Potencial outlier

    for i in range(samples_quantity):
        if (i in strike_1 and i in strike_2):
            outliers.append(i) # Es outlier

    return outliers

def remove_outliers(outliers_list, samples_array):
    if (len(outliers_list) == 0):
        return samples_array

    samples_quantity = len(samples_array)
    valids_quantity = len(samples_array) - len(outliers_list)
    measurements_per_sample = len(samples_array[0])
    valids_array = np.empty((valids_quantity, measurements_per_sample), int)
    aux = 0

    for i in range(samples_quantity):
        if i in outliers_list:
            aux -= 1
        else:
            for j in range(measurements_per_sample):
                valids_array[aux][j] = samples_array[i][j]

        aux += 1

    return valids_array

def ravel_noise(anc_status_valid, perceived_noise_valid, measured_noise_valid, background_noise_max):
    valids_quantity = len(perceived_noise_valid)
    measurements_per_sample = len(perceived_noise_valid[0])

    # Concatenar las mediciones (con ruido generado) de todos los participantes en una lista

    anc_status_cross = []
    perceived_noise_cross = []

    for i in range(valids_quantity):
        for j in range(measurements_per_sample):
            if (background_noise_max < measured_noise_valid[i][j]): # Solo si hay ruido generado (casos pares)
                perceived_noise_cross.append(perceived_noise_valid[i][j])
                anc_status_cross.append(anc_status_valid[i][j])

    # Asignar nombres descriptivos al estado de ANC

    anc_status_meaning = []

    for i in range(len(anc_status_cross)):
        if (anc_status_cross[i] == 0):
            anc_status_meaning.append("Apagado")
        else:
            anc_status_meaning.append("Encendido")

    # Asignar nombres descriptivos al ruido percibido

    perceived_noise_meaning = []

    for i in range(len(perceived_noise_cross)):
        if (perceived_noise_cross[i] == 1):
            perceived_noise_meaning.append("Poco")
        else:
            perceived_noise_meaning.append("Mucho")

    return anc_status_meaning, perceived_noise_meaning

def ravel_quality(anc_status_valid, perceived_quality_valid, measured_noise_valid, background_noise_max):
    valids_quantity = len(perceived_quality_valid)
    measurements_per_sample = len(perceived_quality_valid[0])

    # Concatenar las mediciones (sin ruido generado) de todos los participantes en una lista

    anc_status_cross = []
    perceived_quality_cross = []

    for i in range(valids_quantity):
        for j in range(measurements_per_sample):
            if (measured_noise_valid[i][j] < background_noise_max): # Solo si no ruido generado (casos impares)
                perceived_quality_cross.append(perceived_quality_valid[i][j])
                anc_status_cross.append(anc_status_valid[i][j])

    # Asignar nombres descriptivos al estado de ANC

    anc_status_meaning = []

    for i in range(len(anc_status_cross)):
        if (anc_status_cross[i] == 0):
            anc_status_meaning.append("Apagado")
        else:
            anc_status_meaning.append("Encendido")

    # Asignar nombres descriptivos al ruido percibido

    perceived_noise_meaning = []

    for i in range(len(perceived_quality_cross)):
        if (perceived_quality_cross[i] == 1):
            perceived_noise_meaning.append("Baja")
        else:
            perceived_noise_meaning.append("Alta")

    return anc_status_meaning, perceived_noise_meaning