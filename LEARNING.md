# LEARNING.md - Technical Project Summary for CV

## Project Overview

This project implements a novel cryptographic key generation system using physiological signals, specifically Electrocardiography (ECG), as a biometric identifier. The core objective is to create a secure and reproducible cryptographic key for authentication in Wireless Body Area Networks (WBANs). The system leverages a Bloom filter, a probabilistic data structure, to achieve this. The implementation is based on the research paper "Using Bloom Filter to Generate a Physiological Signal-Based Key for Wireless Body Area Networks."

## Tech Stack and Key Technologies

*   **Programming Language:** Python
*   **Data Structures:** Bloom Filter
*   **Cryptography:** Hashing (SHA-1), HMAC
*   **Signal Processing:** ECG signal analysis (Inter-Pulse Interval calculation)

## Notable Libraries

*   **hashlib:** Used for cryptographic hashing, specifically SHA-1, to generate digests for the Bloom filter and for key generation.
*   **hmac:** Used for creating Hash-based Message Authentication Codes (HMACs) to ensure the integrity and authenticity of messages exchanged during the key agreement protocol.
*   **bitarray:** Provides an efficient way to handle bit arrays, which is the core data structure for the Bloom filter.
*   **matplotlib:** Used for plotting ECG signals, which is crucial for visualizing and debugging the signal processing part of the project.
*   **numpy:** Utilized for numerical operations, particularly in signal processing for handling arrays and performing calculations like cross-correlation and averaging.
*   **wfdb:** The Waveform Database (WFDB) package is used to read and process physiological signals from databases like PhysioNet, which is essential for working with real-world ECG data.

## Major Achievements and Skills Demonstrated

*   **Designed and implemented a biometric-based cryptographic key generation system.** This demonstrates the ability to translate a research paper into a functional implementation.
*   **Implemented a Bloom filter from scratch.** This showcases a strong understanding of probabilistic data structures and their applications in security.
*   **Developed a key agreement protocol using HMACs.** This highlights experience in designing and implementing secure communication protocols.
*   **Performed ECG signal processing to extract biometric features.** This involved reading and analyzing physiological signals to extract the Inter-Pulse Interval (IPI) as a unique identifier.
*   **Integrated multiple libraries to create a cohesive system.** This demonstrates the ability to work with various tools and technologies to achieve a complex goal.

## Skills Gained/Reinforced

*   **Biometric Cryptography:** Deepened understanding of using physiological signals for security applications.
*   **API Design:** While not a traditional API, the modular structure of the code demonstrates an understanding of how to design and interconnect different components.
*   **Data Structures and Algorithms:** Practical application of Bloom filters and other data structures.
*   **Cryptographic Protocols:** Hands-on experience with key agreement protocols and HMACs.
*   **Signal Processing:** Gained practical experience in processing and analyzing biomedical signals.
*   **Python Programming:** Advanced my Python skills by implementing a complex, multi-faceted project.
