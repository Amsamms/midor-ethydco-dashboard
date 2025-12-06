# MIDOR-ETHYDCO Integration Project

## Project Overview
This project analyzes the petrochemical integration between MIDOR (Middle East Oil Refinery) and ETHYDCO (Egyptian Ethylene and Derivatives Company). It processes calculation data from Excel files and generates interactive HTML dashboards for different audience levels.

## Project Structure

```
integration_project/
├── venv/                          # Python virtual environment
├── MIDOR_ETHYDCO_Detailed_Calculations_rev03.xlsx  # Source data
├── create_dashboard_v2.py         # Main dashboard generator script
├── integration_dashboard_v2.html  # Generated interactive dashboard
├── .playwright-mcp/               # Screenshots from visual testing
└── CLAUDE.md                      # This file
```

## Key Files

| File | Description |
|------|-------------|
| `MIDOR_ETHYDCO_Detailed_Calculations_rev03.xlsx` | Source Excel with 11 sheets of integration calculations |
| `create_dashboard_v2.py` | Python script that generates the interactive HTML dashboard |
| `integration_dashboard_v2.html` | Output: Self-contained interactive dashboard |

## Technology Stack

- **Python 3** with virtual environment (`venv/`)
- **pandas** - Data processing
- **openpyxl** - Excel file reading
- **plotly** - Interactive charts and visualizations

## Commands

### Activate Virtual Environment
```bash
cd /home/amsamms/projects/integration_project
source venv/bin/activate
```

### Regenerate Dashboard
```bash
source venv/bin/activate && python create_dashboard_v2.py
```

### Install Dependencies (if needed)
```bash
source venv/bin/activate
pip install pandas openpyxl plotly
```

## Dashboard Features

### 4 Audience-Level Tabs
1. **Overview** - Executive summary with KPI cards, donut chart, product values
2. **Financial Analysis** - Cost-benefit analysis, detailed financial table
3. **Process Flow** - Sankey diagram, gauges, heatmap, material flow
4. **Detailed Data** - Stream details cards, product prices table

### Key Metrics
- **Total Integration Value**: $196M/year
- **Phase 1+2 (Gas Recovery)**: $100M/year - LPG, H2, C2, C5+ recovery
- **Phase 3+4 (Methanol & MTO)**: $96M/year - Methanol blending, olefins production

### Features
- Language toggle (English/Arabic) with RTL support
- Dark glassmorphism UI design
- Animated background
- Responsive layout
- Interactive Plotly charts (hover, zoom, pan)

## Data Structure (from Excel)

### Sheets in Source File
1. Molecular Conversions
2. Heat Content reference
3. Input Data
4. Stream Calculations (6 streams: Flare OLD, Flare New, Refinery Gas, PSA Purge, Sweep Gas, Penex)
5. Calc 1 - LPG & C5+ Recovery
6. Calc 2 - H2 Recovery
7. Calc 3 - C2 Balance (ETHYDCO feed)
8. Calc 5 - Methanol Synthesis
9. Calc 6 - Blend & MTO
10. Final Summary

### Key Products
- LPG (C3+C4): $91.5M/year
- Hydrogen (H2): $78.9M/year
- Propylene (MTO): $44.3M/year
- Methanol Blend: $35.8M/year
- Ethane (C2): $23.6M/year
- Ethylene (MTO): $16.2M/year
- Naphtha (C5+): $13.5M/year

## Chart Types Used

| Chart | Library | Purpose |
|-------|---------|---------|
| Donut | Plotly Pie | Phase value distribution |
| Horizontal Bar | Plotly Bar | Product values comparison |
| Grouped Bar | Plotly Bar | Cost-benefit analysis |
| Sankey | Plotly Sankey | Material & value flow |
| Gauge | Plotly Indicator | C2 coverage percentages |
| Heatmap | Plotly Heatmap | Stream component distribution |
| Pie | Plotly Pie | Methanol allocation |

## Styling Notes

### Color Palette
- Primary: `#0ea5e9` (blue)
- Secondary: `#06b6d4` (teal/cyan)
- Accent: `#f59e0b` (orange/gold)
- Success: `#22c55e` (green)
- Danger: `#ef4444` (red)
- Dark: `#0f172a`, `#1e293b`

### Fonts
- English: Inter
- Arabic: Cairo

## Testing

Visual testing was performed using Playwright MCP to capture screenshots and verify:
- Chart labels are not cut off
- All text is readable
- RTL layout works correctly for Arabic
- Charts render properly across all tabs

## Related Documents

The project includes PDF memos and questionnaires in the parent directory that provide context for the integration analysis.
