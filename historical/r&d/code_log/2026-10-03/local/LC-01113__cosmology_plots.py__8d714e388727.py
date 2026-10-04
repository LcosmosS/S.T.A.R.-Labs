"""
Cosmology Visualization Tools
=============================

Provides plotting utilities for comparing cosmological models.
"""

from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt


def plot_H_of_z(models, labels, zmax=2, n=200):
    z = np.linspace(0, zmax, n)
    plt.figure(figsize=(10,6))
    for model, label in zip(models, labels):
        H = np.array([model.H(zi) for zi in z])
        plt.plot(z, H, label=label, lw=2)
    plt.xlabel("Redshift z")
    plt.ylabel("H(z)")
    plt.title("Expansion History Comparison")
    plt.legend()
    plt.grid()
    plt.show()


def plot_distance_modulus(models, labels, zmax=2, n=200):
    z = np.linspace(0, zmax, n)
    plt.figure(figsize=(10,6))
    for model, label in zip(models, labels):
        mu = np.array([model.distance_modulus(zi) for zi in z])
        plt.plot(z, mu, label=label, lw=2)
    plt.xlabel("Redshift z")
    plt.ylabel("Distance Modulus μ")
    plt.title("Distance Modulus Comparison")
    plt.legend()
    plt.grid()
    plt.show()


def plot_residuals(model1, model2, label1="Model 1", label2="Model 2", zmax=2, n=200):
    z = np.linspace(0, zmax, n)
    mu1 = np.array([model1.distance_modulus(zi) for zi in z])
    mu2 = np.array([model2.distance_modulus(zi) for zi in z])
    plt.figure(figsize=(10,6))
    plt.plot(z, mu2 - mu1, lw=2)
    plt.axhline(0, color="black", lw=1)
    plt.xlabel("Redshift z")
    plt.ylabel(f"μ({label2}) - μ({label1})")
    plt.title("Distance Modulus Residuals")
    plt.grid()
    plt.show()
