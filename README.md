# Physio Key Gen 🔐

Implementation of "Using Bloom Filter to Generate a Physiological Signal-Based Key for Wireless Body Area Networks" - A novel approach to biometric cryptography using physiological signals.

## Overview

This project implements a cryptographic key generation system that uses physiological signals (ECG) combined with Bloom filters to create secure, reproducible keys for Wireless Body Area Networks (WBANs).

## Features

- 📊 **Signal Processing**: ECG signal analysis
- 🔍 **Feature Extraction**: Automated physiological feature detection
- 🌸 **Bloom Filters**: Probabilistic data structure for key generation
- 🔒 **Key Generation**: Reproducible cryptographic keys from biometrics

## Algorithm Overview

1. **Signal Preprocessing**: Noise reduction and normalization
2. **Feature Extraction**: R-peak detection, HRV analysis
3. **Quantization**: Convert features to discrete values
4. **Bloom Filter**: Insert quantized features
5. **Key Derivation**: Generate key from filter state

## Research Papers
    1. Goldberger AL, Amaral LAN, Glass L, Hausdorff JM, Ivanov PCh, Mark RG, Mietus JE, Moody GB, Peng C-K, Stanley HE. PhysioBank, PhysioToolkit, and PhysioNet: Components of a New Research Resource for Complex Physiologic Signals (2003). Circulation. 101(23):e215-e220.
    2. Moody GB, Mark RG. The impact of the MIT-BIH Arrhythmia Database. IEEE Eng in Med and Biol 20(3):45-50 (May-June 2001). (PMID: 11446209).
    3. Using Bloom Filter to Generate a Physiological Signal-Based Key for Wireless Body Area Networks(Yao et al, 2019).
    4. Key Establishment Protocol for a Patient Monitoring System Based on PUF and PKG(Diaz).
    5. Alfred J. Menezes, Paul C. Van Oorschot, Scott A. Vanstone. "Handbook of applied cryptography". CRC Press, 1997.

## License

MIT License
