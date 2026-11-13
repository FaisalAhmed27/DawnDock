# DawnDock

**DawnDock: a multi-engine GUI application for molecular docking with deep learning-based scoring**

DawnDock runs five docking engines from one window and scores poses with a
convolutional neural network, not only with a classical scoring function. Load a
protein, pick a pocket, dock one ligand or a library, and read the poses,
scores and contacts in a 3D view. No command line.

> Developed by Sk. Faisal Ahmed. Distributed by Dawn of Bioinformatics Ltd., the 1st Bioinformatics
> Company in Bangladesh.

## Download

Get the installer from the [Releases page](../../releases/latest).

| | |
|---|---|
| **Installer** | `DawnDock-Setup-1.0.0.exe` (298 MB) |
| **Requires** | Windows 10 or 11, 64-bit. No administrator rights. |
| **Disk space** | About 1 GB once installed |
| **Also needed** | Nothing. No Python, no compiler, no separate toolkit. |

Windows may warn about an unknown publisher the first time, because the
installer is not yet signed with a paid code-signing certificate. Choose
**More info**, then **Run anyway**. You can check the download first:

```powershell
Get-FileHash .\DawnDock-Setup-1.0.0.exe -Algorithm SHA256
```

It should read `7148ab203bdf030de18dddb702275d4f726ae5f9215b298b6f031c885ec687ed`.

Each release is also signed with an Ed25519 key. `verify_authorship.py` and the
published public key check both the installer and the authorship statement.

## The five engines

| Engine | Scoring |
|---|---|
| **GNINA** | Smina's search, then a convolutional neural network rescores every pose |
| **Smina** | A Vina fork with extra scoring functions |
| **AutoDock Vina** | The standard engine, and the one most papers cite |
| **AutoDock 4** | Precomputed grids and a genetic algorithm, with pose clustering |
| **LeDock** | Simulated annealing, scored against crystal poses |

AutoDock Vina and AutoDock 4 are included and work immediately. Smina, GNINA
and LeDock run through WSL and are fetched from inside the program when you ask
for them.

## How well does it do

On the **Astex Diverse Set**, run in this project with identical boxes and
ligand preparation across every engine:

| | Within 2 A RMSD of the crystal pose |
|---|---|
| **GNINA** (neural network) | **80.5%** (66 of 82) |
| Smina | 56.1% (46 of 82) |
| AutoDock 4 | 52.4% (43 of 82) |
| AutoDock Vina | 52.4% (44 of 84) |
| LeDock | 50.0% (42 of 84) |

85 complexes were attempted; the counts are over those that produced a pose.
The per-complex results are in [`docs/benchmark-data/`](docs/benchmark-data),
so the figures can be recomputed rather than taken on trust.

This compares the engines DawnDock ships against each other. It is not a
comparison with any other docking program.

## Documentation

The [user manual](docs/DawnDock_User_Manual_v1.0.0.pdf) has a quick-run
tutorial that takes a first-time user through one complete docking, and a
reference guide to every panel and setting. Its screenshots come from the
running program.

## Licence

DawnDock is **free for academic, nonprofit, educational and personal
research**. Commercial use needs written permission first. It is licensed
rather than sold, and **it is not open source**, which is why no source code is
published here.

The open-source components it builds on stay under their own licences.
[`THIRD-PARTY-NOTICES.txt`](THIRD-PARTY-NOTICES.txt) lists every one with its
full licence text. Qt and Meeko are LGPL and the annex to
[`LICENSE.txt`](LICENSE.txt) grants the rights that licence requires. AutoDock 4
and AutoGrid 4 are GPL-2.0, included as unmodified separate programs.

## Citing

See [`CITATION.cff`](CITATION.cff). Please also cite the engine you actually
used; DawnDock runs these programs, it does not replace them, and their authors
deserve the credit. The manual lists the references.

## A note on what docking can tell you

A docking score is an estimate from a scoring function. It is not a measured
binding free energy and it does not reliably predict potency. Poses, scores and
rankings are predictions and can be wrong. DawnDock is a research tool, not a
medical device, and must not be used for diagnosis, treatment or any clinical
decision.

## Contact

dawn.of.bioinformatics@gmail.com · https://dawnofbioinformatics.com
