# V2 harness draft R0

Open the YAML in WireViz or read the generated HTML/SVG diagrams in `exports/`.
Every connection is proposed/untraced. Logical names (including POS_TBD and
RET_TBD) are functions, not verified physical pins. No cable length, conductor
gauge, part number or colour is inferred. The blue adapter's red/black leads
were visible in the photos; polarity remains unverified.

H01-H09 correspond to the power schematic's functional paths. H10-H13 cover
the historically described sensors and feedback. F1 and S1 return paths represent
bypass functions, not verified fuse/switch contacts. Power feed/order and branch
protection need review. Separate logical IN/OUT connector IDs represent module
interfaces; no measured module-internal connection is asserted.

The following are deliberately unresolved rather than guessed:

- Uno external supply entry and USB power relationship.
- Pi-to-Uno USB cable and device recognition; use a complete USB data cable,
  not hand-wired guessed USB connector pins.
- ESC-to-motor, receiver/BEC and servo pinouts.
- OLED/camera installation and any voltage/temperature sensing.
- HC-SR04 trigger/echo, LED and buzzer Uno digital pin assignments.

The standard Uno A4/A5 I2C functions are a proposed use, not a traced V2 connection.
Breakout power tolerance and bus pull-up voltage must be established separately.
LED series resistance and buzzer driver/type are not yet selected.

Generated BOMs are **diagram inventories**, not purchasing or assembly BOMs.
`connector_register.csv` and `connection_register.csv` keep missing physical
details explicit. Establish those details before creating a build harness.

Rebuild with Python + PyYAML + WireViz 0.4.1 and Graphviz `dot` on PATH:

```text
python scripts/v2/build_wiring.py
wireviz -f hpst -o hardware/v2/wiring/exports hardware/v2/wiring/v2_power_harness.yml
wireviz -f hpst -o hardware/v2/wiring/exports hardware/v2/wiring/v2_sensor_harness.yml
```
