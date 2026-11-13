# DawnDock 1.0.1

On a computer that had never had them, one of the CUDA libraries GNINA loads was missing from the set DawnDock fetched, so the engine would not start; the fetch now covers every library it loads, resumes instead of starting again if it is interrupted, and names any library still missing. Installing over an existing copy now keeps the engines already downloaded. The docking progress bar covers the whole run rather than only the search, so it no longer reaches 100% while GNINA is still scoring poses. Docking itself is unchanged, so results produced with 1.0.0 stand.

## What it does

Five docking engines in one window: GNINA, Smina, AutoDock Vina, AutoDock 4 and
LeDock. GNINA rescores every pose with a convolutional neural network. The whole
workflow runs without a command line: load a receptor, prepare it, add ligands
from file or SMILES, set the search box by hand or from a detected pocket, dock
one ligand or a library, then read poses, scores and interactions in a 3D view
and export the lot.

## Validation

On the Astex Diverse Set, with identical boxes and ligand preparation across
engines, neural-network scoring placed **80.5%** of ligands within 2 A RMSD of
the crystal pose (66 of 82 complexes that produced a pose), against
**52.4%** for a classical scoring function (43 of 82). Per-complex
results for all five engines are in `docs/benchmark-data/`.

## Installing

Download `DawnDock-Setup-1.0.1.exe` below and run it. It installs for you
alone, needs no administrator rights, and registers an uninstaller.

Windows may warn about an unknown publisher: the installer is not yet signed
with a code-signing certificate. Choose **More info**, then **Run anyway**.

SHA-256 of the installer:

```
6ac85686171fa845533adbd487482977bcc01a7821cb6fce1707fcabed27dd8f
```

## Known limitations

- A receptor with an unusual modified linking residue can fail preparation.
  1OYT in the Astex set is one such case.
- The installer is not code-signed yet, so Windows shows a publisher warning.
- Virtual screening has not been benchmarked. The figures above are redocking
  accuracy, which is a different question from ranking actives against decoys.

## Citing this release

> Ahmed, S. F. (2026). DawnDock: a multi-engine GUI application for molecular docking with deep learning scoring (Version 1.0.1) [Computer software]. Dawn of Bioinformatics Ltd. https://doi.org/10.5281/zenodo.24198678

The DOI points at this archived version, not at a moving target, so results
stay traceable to the build that produced them.

## Licence

Free for academic, nonprofit, educational and personal research. Commercial use
needs written permission. Not open source. See `LICENSE.txt`.
