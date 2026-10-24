# Medical Engagement Workbench presentation

Prepared 24 October 2026. Includes 16 slides, presenter notes and eight screenshot walkthrough views. The deck covers the problem, delivered workspaces, three agents, architecture, runtime controls, specifications, testing, agent harness, demonstration script and pending evaluation.

## Open or share

- [Open the HTML slides](index.html): use Previous/Next or arrow keys. Slides opens an outline; Presenter notes toggles the script; click a screenshot to enlarge it. Full screen is optional.
- [Open the PDF](presentation.pdf): 16 slides for static review or circulation.
- [Presenter notes](presenter-notes.md): suggested narrative and a six-minute application walkthrough.
- [Presentation checks](qa/presentation_checks.json): 47 checks passed, including all slide layouts, mobile overflow, standalone offline opening and PDF content/page count.

The standalone index.html embeds its screenshots and needs no external fonts or JavaScript libraries. Send it on its own for slides and the screenshot walkthrough. Send MSL_Workbench_Presentation.zip to include PDF, notes and evidence: extract the ZIP, then open index.html. Evidence text files preserve original report content; their embedded repository-relative references belong to the source repository.

## Local links

- Slides: http://localhost:8765/index.html
- Screenshot walkthrough: http://localhost:8765/index.html#demo=profile
- Working application: http://localhost:8502

Localhost links work on the presenter computer only. The screenshot walkthrough does not execute filters, retrieve new records or call OpenAI. It is a guided view of captured screens. The live app requires the Python server to be running. Public hosting remains on hold pending team confirmation.

If the presentation server is stopped, run from the prototype folder:

```powershell
./.venv/Scripts/python.exe -B -m http.server 8765 --bind 127.0.0.1 --directory presentation
```

If the application is not running, run from the prototype folder:

```powershell
./.venv/Scripts/python.exe -B -m streamlit run app.py --server.address=127.0.0.1 --server.port=8502
```

## Evidence and limits

The included snapshot records 126 automated tests, 16 fixed harness cases and eight browser checks passing. Harness scenarios overlap with unit-test behavior; these counts are not independent quality samples. No saved, human-reviewed live OpenAI completion, scientific-quality score or productivity benefit has been established. CRM is synthetic and read-only. Original public sources and MSL review remain central to the workflow.

The [manifest](presentation-manifest.json) records source and screenshot hashes. [Evidence snapshots](evidence/latest_run.txt) are copied from actual reports. Source screenshots and full specifications remain in the project repository and Obsidian vault.

## Rebuild within the repository

From the repository root:

```powershell
./prototype/.venv/Scripts/python.exe -B prototype/presentation/build_presentation.py
./prototype/.venv/Scripts/python.exe -B prototype/presentation/export_and_verify.py
```

The builder uses standard Python only. PDF/browser QA uses the existing temporary Playwright/PDF-reader tools and installed Microsoft Edge; these are not application runtime requirements. A later rebuild requires those tools to be available. Rebuild and repackage after changing slides or evidence. Editing slides.json changes the narrative; template.html defines the design and controls.

## Cover credits and palette proposals

The cover reads Prepared by, followed by Sayali Shedge, Asawari U and Roshni Srivastava in that order. HTML and PDF were rebuilt and verified.

Compare four coordinated options in the [palette gallery](palettes.html) or [comparison image](palette-previews/comparison.png): A Navy & Azure (selected), B Plum & Lavender, C Forest & Sage, D Graphite & Amber. [Individual previews](palette-previews/option-A.png) and [colour definitions/contrast calculations](palette-previews/palettes.json) are included. A is now applied to the live app, slides and PDF. B, C and D remain available as alternatives.

## Selected palette: A - Navy & Azure

Header/navy #102A43, primary/action blue #2563EB, text #172B4D, background #F4F7FC, soft panels #EFF6FF. The HTML deck, PDF, architecture diagram, Streamlit theme and embedded screenshots now match. Green completion and amber overdue indicators retain their status meanings.
