"""Assemble a portable review PDF from the checked subsystem exports."""
import sys
if True:  # Historical R0 book assembler; current PDF pipeline requires revision/proofing.
    raise SystemExit("Historical R0 book builder disabled. PDFs are archived; review current sources and update the export workflow after content review.")
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from pypdf import PdfReader,PdfWriter
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'reports/v2';OUT.mkdir(parents=True,exist_ok=True)
styles=getSampleStyleSheet();story=[]
def para(t,style='BodyText'):story.append(Paragraph(t,styles[style]));story.append(Spacer(1,12))
para('LitterBuggy V2', 'Title');para('Engineering draft R0 / technical review package','Heading1')
para('Prepared 2026-11-21 in Junk-O-Matic. Owner-confirmed controller: <b>Elegoo Uno R3</b>.')
para('This book collects the review drawings in the requested order. Native editable files, firmware, Python, SQL, tests and generation scripts accompany it in the repository/archive. Start at docs/v2/README.md.')
data=[['Order','Deliverable','Included'],['1','System overview','3 diagrams.net sources + PDF/SVG'],['2','Power schematic','3-sheet native QElectroTech + PDF'],['3','Wiring','2 WireViz sources + diagrams/tables/BOMs'],['4','Mechanical assembly','5 FreeCAD files + STEP/PDF/PNG'],['5','Firmware / Pi logger','Uno source + Python/SQL/service/tests']]
t=Table(data,colWidths=[40,145,300]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#153e56')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),12),('TOPPADDING',(0,0),(-1,-1),12),('GRID',(0,0),(-1,-1),.3,colors.HexColor('#cbd5df'))]));story.append(t);story.append(Spacer(1,20))
para('How to read the draft','Heading2')
para('Historical observations, current owner confirmations and proposed details are distinguished. Dashed architecture links and schematic TBD labels identify unresolved wiring. Logical connector labels are not physical pin numbers.')
para('<b>All CAD dimensions are illustrative layout values.</b> Measured values are still null. Native solid validity and successful STEP readback do not establish physical fit, strength or a payload rating.')
para('No firmware upload, Pi installation, hardware test, drilling or fabrication was performed. Preserve the original Uno program before deploying replacement code.')
story.append(PageBreak())
para('Software and validation review','Heading1')
para('Uno R3 firmware','Heading2')
para('New source implements optional MPU-6050 raw acquisition, bounded ultrasonic timing and optional LED/passive-buzzer feedback. Default drivers are disabled because power and pins are unverified. Disabled or failed readings are null with explicit flags; there are no synthetic measurement constants or vehicle motion commands.')
para('Both default and enabled-driver/feedback variants compile for Uno on AVR Boards 1.8.8. The negative build rejects unassigned range pins. Compile-only test pin choices are not a physical wiring plan.')
para('Pi acquisition','Heading2')
para('Versioned JSON-line parsing, raw byte preservation, SQLite sessions/frames/telemetry/events/health, reconnect handling, bounded framing, receive timestamps, sequence diagnostics and graceful signal shutdown. Optional camera capture is separate and reports open/write failures. A service draft and CSV export tool are included.')
para('Completed checks','Heading2')
para('32 Python tests passed. End-to-end replay preserved byte-identical input and created an integral database and replay-labelled manifest with two valid frames and zero physical measurements. QElectroTech opened/re-saved/exported three sheets. WireViz generated both harnesses. Five native CAD documents and five STEP files reopened; native parameter propagation and tyre-centre spacing were checked.')
para('Technical review priorities','Heading2')
para('1. Trace source/return paths, protection, polarity and Pi/Uno power entry.<br/>2. Confirm sensor identities, power/logic compatibility and real pin mapping.<br/>3. Measure mounting interfaces, component placement and moving clearances.<br/>4. Preserve/capture the existing firmware and serial behaviour.<br/>5. Bench-test the new software on verified hardware before field use.')
para('Review records: docs/v2/validation.md, docs/v2/sources_and_decisions.md and reports/v2/validation.json. The original 118-item verification record remains available. Old V1A targets are not recorded as passed.')
intro=OUT/'review-introduction.pdf';SimpleDocTemplate(str(intro),pagesize=(595.28,841.89),leftMargin=50,rightMargin=50,topMargin=40,bottomMargin=40).build(story)
files=[intro,*[ROOT/f'hardware/v2/architecture/{n}.pdf' for n in ['v2_system_overview','v2_power_domains','v2_data_flow']],ROOT/'hardware/v2/electrical/v2_electrical.pdf',*[ROOT/f'hardware/v2/wiring/exports/{n}.pdf' for n in ['v2_power_harness','v2_sensor_harness']],*[ROOT/f'hardware/v2/mechanical/exports/{n}.pdf' for n in ['v2_assembly','v2_cart_mount','v2_battery_mount','v2_electronics_enclosure','v2_sensor_mounts']]]
writer=PdfWriter()
for f in files:writer.append(str(f),outline_item=f.stem)
writer.add_metadata({'/Title':'LitterBuggy V2 Engineering Draft R0','/Subject':'Technical review; unresolved connections and illustrative dimensions'})
dest=OUT/'LitterBuggy-V2-review.pdf'
with dest.open('wb') as f:writer.write(f)
print(str(dest),len(PdfReader(dest).pages),'pages')
