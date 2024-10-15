#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

#=======================================================================
# FONCTIONS DE GENERATION ET D'ENREGISTREMENT
#=======================================================================

def generate_signal(signal_type, N, amplitude, filename):
    """
    Génère des points pour différents types de signaux (sinusoïde, carré, triangle, dent de scie),
    les met en forme et les enregistre dans un fichier.

    Args:
        signal_type (str): Type du signal ('sin', 'square', 'triangle', 'sawtooth').
        N (int): Nombre de points à générer.
        amplitude (int): Amplitude pour la quantification en entier.
        filename (str): Nom du fichier pour l'enregistrement des données.
    """
    theta = np.linspace(0., 2 * np.pi, N)

    if signal_type == 'sin':
        signal_f32 = np.sin(theta)
    elif signal_type == 'square':
        signal_f32 = signal.square(theta)
    elif signal_type == 'triangle':
        signal_f32 = signal.sawtooth(theta, 0.5)  # Rapport cyclique 0.5 pour le triangle
    elif signal_type == 'sawtooth':
        signal_f32 = signal.sawtooth(theta)
    else:
        raise ValueError(f"Signal type '{signal_type}' not supported")

    signal_int = np.round(amplitude * signal_f32)  # Quantification en entier

    # Sauvegarde des données dans un fichier
    with open(filename, "a") as fd:
        fd.write(f"float32_t {signal_type}_f32[{N}]=\n{{\n")
        for val in signal_f32:
            fd.write(f"{val},\n")
        fd.write("};\n\n")

        fd.write(f"int16_t {signal_type}_int[{N}]=\n{{\n")
        for val in signal_int:
            fd.write(f"{int(val)},\n")
        fd.write("};\n\n")

    return theta, signal_f32, signal_int

def plot_signals(theta, signal_f32, signal_int, signal_type):
    """
    Affiche les signaux en virgule flottante et en entier.

    Args:
        theta (array): Tableau des angles (ou des temps).
        signal_f32 (array): Signal en virgule flottante.
        signal_int (array): Signal en entier (quantifié).
        signal_type (str): Type du signal (utilisé pour l'affichage).
    """
    plt.figure(figsize=(10, 6))
    
    plt.subplot(211)
    plt.grid()
    plt.plot(theta, signal_f32, label=f"{signal_type} float")
    plt.ylabel(f"${signal_type}(\Theta)$")
    plt.xlabel("$\Theta$")
    plt.legend()
    
    plt.subplot(212)
    plt.grid()
    plt.plot(theta, signal_int, label=f"{signal_type} int")
    plt.ylabel(f"${signal_type}(\Theta)$ (quantified)")
    plt.xlabel("$\Theta$")
    plt.legend()

    plt.suptitle(f"Signal {signal_type.capitalize()}")
    plt.show()

#=======================================================================
# MAIN PROGRAMME
#=======================================================================

N = 1000  # Nombre de points
amplitude = 2**14  # Amplitude pour la quantification en entier
filename = "signals.txt"

# Nettoyer le fichier avant d'écrire les nouveaux signaux
with open(filename, "w") as fd:
    fd.truncate(0)

# Génération et affichage de la sinusoïde
theta, sinus_f32, sinus_int = generate_signal('sin', N, amplitude, filename)
plot_signals(theta, sinus_f32, sinus_int, 'sin')

# Génération et affichage du signal carré
theta, square_f32, square_int = generate_signal('square', N, amplitude, filename)
plot_signals(theta, square_f32, square_int, 'square')

# Génération et affichage du signal triangle
theta, triangle_f32, triangle_int = generate_signal('triangle', N, amplitude, filename)
plot_signals(theta, triangle_f32, triangle_int, 'triangle')

# Génération et affichage du signal dent de scie
theta, sawtooth_f32, sawtooth_int = generate_signal('sawtooth', N, amplitude, filename)
plot_signals(theta, sawtooth_f32, sawtooth_int, 'sawtooth')
