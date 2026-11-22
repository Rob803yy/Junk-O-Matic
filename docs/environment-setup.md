# Environment and command matrix / reviewed REPO-R1

Use a separate virtual environment for the task. There is no single locked,
cross-platform tested environment for every folder. Version ranges are existing
project requirements, not a fresh dependency/security certification. No versions
were upgraded in this review; actual Pi model/OS compatibility is still open.

| Task | Dependency entry | Intended command / limit |
| --- | --- | --- |
| Current Pi logger offline replay | `software/v2/raspberry_pi/requirements.txt` | Commands below; protocol-2 fixtures only |
| Current software tests | Above plus `pytest` from drafting requirements | `python -m pytest software/v2/tests -q`; source-only checks |
| Three architecture diagrams | Pillow from `scripts/v2/requirements-drafting.txt` | `python scripts/v2/architecture_diagrams.py --check`; no regeneration/PDF |
| QET / WireViz / CAD review | `scripts/v2/requirements-drafting.txt` plus external native tools | Consult [generator matrix](../scripts/README.md); commands may overwrite sources |
| Dataset/model dashboard | Root `requirements.txt` | From repo root: `python -m streamlit run app/streamlit_app.py`; historical examples |
| Dataset directory bootstrap / inventory | PyYAML in root requirements | Bootstrap creates dirs only; scanner does not parse annotations |
| Historical V1A Pi logger | `software/raspberry_pi/requirements.txt` | Preserved reference only; not the current quick start |

Current offline replay, from repo root using Python 3.10+:

```sh
python -m venv .venv-v2
# Activate using your shell's virtual-environment command.
python -m pip install -r software/v2/raspberry_pi/requirements.txt
python software/v2/raspberry_pi/logger.py --config software/v2/raspberry_pi/config.example.yml --replay software/v2/tests/fixtures/disabled.ndjson --output-root runs
```

Use the created environment's Python after activation. PowerShell activation:
`.\.venv-v2\Scripts\Activate.ps1`; POSIX activation: `. .venv-v2/bin/activate`.
The port remains null during replay; this command does not contact hardware.
Do not confuse this environment with root `.venv` or an existing Pi deployment.

Live serial requires the verified actual device identity and a private reviewed
config, plus original-software capture and power/pin review. No upload, Pi service
installation, firmware recovery or live camera operation is part of these setup
examples. OpenCV is optional/separate; native FreeCAD/QET/Graphviz/Arduino CLI
requirements are not supplied by pip alone. Use prior receipts as historical
runtime evidence, not a guarantee a different OS/tool version behaves identically.

The legacy root dependency list includes UI and historical acquisition packages;
it does not declare the new V2 logger, drafting checks or external CAD toolchain.
No deployment or CI installation follows from installing dependencies.
