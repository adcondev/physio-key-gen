# Learning & Achievements Log

## Project Overview
**Physio-Key-Gen** is a cryptographic security project that implements a **Key Agreement Protocol** for Wireless Body Area Networks (WBAN). It uses **Electrocardiogram (ECG)** signals—specifically the **Inter-Pulse Interval (IPI)**—as a biometric source to generate shared cryptographic keys between two sensors without transmitting the raw biometric data. The system leverages **Bloom Filters** for efficient and secure set reconciliation to find common features between two sensors observing the same physiological signal.

## Tech Stack and Key Technologies
*   **Language:** Python 3
*   **Scientific Computing:** NumPy, Matplotlib
*   **Biomedical Signal Processing:** WFDB (Waveform Database)
*   **Cryptography:** `hashlib` (SHA-1), `hmac`
*   **Data Structures:** `bitarray`

## Notable Libraries
*   **`wfdb`**: Used to read and process standard ECG records from the MIT-BIH Arrhythmia Database. It was crucial for simulating real-world sensor data.
*   **`bitarray`**: Essential for the efficient implementation of the Bloom Filter, allowing for bit-level manipulation to store biometric feature hashes.
*   **`hashlib` & `hmac`**: Used to implement the security primitives (SHA-1 for hashing features and HMAC for message authentication and integrity verification).

## Major Achievements and Skills Demonstrated
*   **Biometric Key Generation**: Designed and implemented a protocol to generate stable cryptographic keys from noisy physiological data (ECG IPIs).
*   **Probabilistic Data Structures**: Implemented a **Bloom Filter** from scratch to efficiently exchange biometric feature sets with tunable false positive probabilities.
*   **Signal Processing Pipeline**: Built a pipeline to filter raw ECG signals, detect QRS complexes, and calculate Inter-Pulse Intervals (IPI) with floating-point precision.
*   **Secure Protocol Design**: Implemented a challenge-response style protocol using **HMAC** to verify that both parties established the same key without revealing the key itself.
*   **Simulation of WBAN**: Simulated a two-node network (Sensor S and Sensor R) to demonstrate the feasibility of the key agreement scheme.

## Skills Gained/Reinforced
*   **Cryptography & Network Security**: Applied knowledge of key agreement, hashing, and message authentication codes.
*   **Biometrics**: Understanding of physiological signals (ECG) and their application in security (Cancelable Biometrics).
*   **Algorithm Implementation**: Practical experience with Bloom Filters and set intersection algorithms.
*   **Python Data Science Stack**: Proficiency with NumPy for vectorization and Matplotlib for signal visualization.
