# DawnDock 1.0.0

The first public release.

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

Download `DawnDock-Setup-1.0.0.exe` below and run it. It installs for you
alone, needs no administrator rights, and registers an uninstaller.

Windows may warn about an unknown publisher: the installer is not yet signed
with a code-signing certificate. Choose **More info**, then **Run anyway**.

SHA-256 of the installer:

```
7148ab203bdf030de18dddb702275d4f726ae5f9215b298b6f031c885ec687ed
```

## Known limitations

- A receptor with an unusual modified linking residue can fail preparation.
  1OYT in the Astex set is one such case.
- The installer is not code-signed yet, so Windows shows a publisher warning.
- Virtual screening has not been benchmarked. The figures above are redocking
  accuracy, which is a different question from ranking actives against decoys.

## Licence

Free for academic, nonprofit, educational and personal research. Commercial use
needs written permission. Not open source. See `LICENSE.txt`.
