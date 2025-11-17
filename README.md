# SWAT-MODFLOW Recharge Mapping Tools
# Great Miami River Watershed (GMRW) Model

```
================================================================================
             SWAT-MODFLOW RECHARGE MAPPING UTILITY v1.0
================================================================================
            Great Miami River Watershed Groundwater Model
                    Recharge Mapped to IBOUND Array
================================================================================

 SWAT-MODFLOW3.exe is a coupled surface water-groundwater model that links
 the SWAT (Soil & Water Assessment Tool) and MODFLOW-NWT models to simulate
 interactions between surface water and groundwater systems.

--------------------------------------------------------------------------------
                        MODEL CONFIGURATION SUMMARY
--------------------------------------------------------------------------------

 Model Domain............: Great Miami River Watershed (GMRW)
 Grid Dimensions.........: 197 rows x 135 columns
 Active Cells (IBOUND=1).: 11,029 cells
 Inactive Cells (IBOUND=0): 15,566 cells
 Total Grid Cells........: 26,595 cells

 Recharge Configuration..: Spatially distributed (mapped to IBOUND)
 Recharge Rate...........: 0.001000 m/day
 Recharge Applied To.....: Active cells only

--------------------------------------------------------------------------------
                          REPOSITORY CONTENTS
--------------------------------------------------------------------------------

 Python Scripts:
   ✓ map_recharge_to_ibound.py      - Main recharge mapping script
   ✓ verify_recharge_mapping.py     - Verification and validation tool

 MODFLOW Input Files:
   ✓ modflow_GMRW.bas               - Basic Package (IBOUND array)
   ✓ modflow_GMRW.rch               - Recharge Package (mapped)
   ✓ modflow_GMRW.rch_original      - Original recharge file (backup)
   ✓ modflow_GMRW.dis               - Discretization Package
   ✓ modflow_GMRW.wel               - Well Package
   ✓ modflow_GMRW.drn               - Drain Package
   ✓ modflow_GMRW.riv               - River Package
   ✓ modflow_GMRW.upw               - Upstream Weighting Package
   ✓ modflow_GMRW.nwt               - Newton Solver Package
   ✓ modflow_GMRW.oc                - Output Control

 Visualization Outputs:
   ✓ GMRW_recharge_map.png          - Standard resolution map (300 dpi)
   ✓ GMRW_recharge_map_highres.png  - High resolution map (600 dpi)

 SWAT Files:
   ✓ file.cio                       - SWAT master input file
   ✓ basins.bsn, *.hru, *.sub       - SWAT subbasin and HRU files
   ✓ output.std, output.rch         - SWAT output files

 Linkage Files:
   ✓ swatmf_link.txt                - SWAT-MODFLOW linkage configuration
   ✓ swatmf_dhru2grid.txt           - DHRUs to MODFLOW grid mapping
   ✓ swatmf_river2grid.txt          - River cells to grid mapping
   ✓ swatmf_out_*                   - SWAT-MODFLOW output files

--------------------------------------------------------------------------------
                          USAGE INSTRUCTIONS
--------------------------------------------------------------------------------

 STEP 1: Map Recharge to IBOUND
 ================================
 
 Run the mapping script to create spatially distributed recharge:
 
   $ python map_recharge_to_ibound.py
 
 Output:
   - Creates: modflow_GMRW_mapped.rch
   - Generates: GMRW_recharge_map.png (visualization)
   - Statistics: Active vs. inactive cell recharge distribution

 STEP 2: Verify Recharge Mapping
 =================================
 
 Validate that recharge is correctly mapped:
 
   $ python verify_recharge_mapping.py
 
 Verification checks:
   ✓ Dimension matching (IBOUND vs. Recharge arrays)
   ✓ Inactive cells have zero recharge
   ✓ Active cells have assigned recharge value
   ✓ Random spot checks for mapping accuracy

 STEP 3: Run SWAT-MODFLOW Model
 ================================
 
 Execute the coupled model:
 
   $ SWAT-MODFLOW3.exe
 
 The model will:
   - Read spatially distributed recharge from modflow_GMRW.rch
   - Apply recharge only to active watershed cells
   - Simulate groundwater-surface water interactions

--------------------------------------------------------------------------------
                        RECHARGE MAPPING DETAILS
--------------------------------------------------------------------------------

 BEFORE MAPPING (Original):
 ===========================
 - Recharge Type: CONSTANT 0.001
 - Applied To: All grid cells (including inactive boundaries)
 - Issue: Recharge applied outside watershed boundary
 
 AFTER MAPPING (Current):
 =========================
 - Recharge Type: INTERNAL ARRAY (spatially distributed)
 - Applied To: Active cells only (IBOUND = 1)
 - Benefit: Recharge constrained to watershed boundary
 
 Mapping Algorithm:
 ------------------
   FOR each cell (i,j) in model grid:
     IF IBOUND(i,j) = 1 THEN
       RECHARGE(i,j) = 0.001000  ! Active cell
     ELSE
       RECHARGE(i,j) = 0.000000  ! Inactive boundary
     END IF
   END FOR

--------------------------------------------------------------------------------
                        VISUALIZATION OUTPUTS
--------------------------------------------------------------------------------

 The recharge maps show three views:

 LEFT PANEL: IBOUND Map
   - Gray areas  = Inactive cells (outside watershed)
   - Green areas = Active cells (within watershed)
   - Shows model domain extent

 MIDDLE PANEL: Recharge Distribution
   - Gray boundary = Inactive cells (no recharge)
   - Blue colors   = Active cells with recharge
   - Colorbar shows recharge rate (m/day)

 RIGHT PANEL: Combined View
   - Gray = Inactive boundary
   - Blue = Active cells with recharge applied
   - Final verification of spatial distribution

--------------------------------------------------------------------------------
                        PYTHON REQUIREMENTS
--------------------------------------------------------------------------------

 Required Packages:
   - numpy       >= 1.19.0
   - matplotlib  >= 3.3.0

 Installation:
   $ pip install numpy matplotlib

 Or using conda:
   $ conda install numpy matplotlib

--------------------------------------------------------------------------------
                        MODEL STATISTICS
--------------------------------------------------------------------------------

 Grid Configuration:
   Number of Rows................: 197
   Number of Columns.............: 135
   Total Cells...................: 26,595
   
 IBOUND Analysis:
   Active Cells (IBOUND = 1).....: 11,029 (41.47%)
   Inactive Cells (IBOUND = 0)...: 15,566 (58.53%)
   
 Recharge Summary:
   Cells Receiving Recharge......: 11,029
   Recharge Rate (active cells)..: 0.001000 m/day
   Recharge Rate (inactive cells): 0.000000 m/day
   Total Recharge Volume.........: 11.029 m³/day
   Mean Recharge (non-zero)......: 0.001000 m/day

--------------------------------------------------------------------------------
                        VERIFICATION STATUS
--------------------------------------------------------------------------------

 ✓ DIMENSION CHECK........: PASSED
   - IBOUND shape: (197, 135)
   - Recharge shape: (197, 135)
   
 ✓ MAPPING VERIFICATION...: PASSED
   - All inactive cells have recharge = 0.0
   - All active cells have recharge > 0.0
   
 ✓ SPOT CHECK.............: PASSED (10/10 samples correct)
   
 ✓ OUTPUT FILES...........: GENERATED
   - modflow_GMRW.rch (mapped recharge)
   - GMRW_recharge_map.png (visualization)
   
 ✓ BACKUP.................: CREATED
   - modflow_GMRW_original.rch (original file preserved)

================================================================================
                        ALL SYSTEMS READY
================================================================================

 The SWAT-MODFLOW model is configured with spatially distributed recharge
 that respects the watershed boundary (IBOUND array). Recharge is applied
 only to active cells within the Great Miami River Watershed domain.

 Repository URL: https://github.com/HadiZamaniS/SWAT-MODFLOW-GMRW

 For questions or issues, please open a GitHub issue or contact the
 repository maintainer.

================================================================================
             END OF SWAT-MODFLOW RECHARGE MAPPING UTILITY
================================================================================
```

## Quick Start

```bash
# Clone the repository
git clone https://github.com/HadiZamaniS/SWAT-MODFLOW-GMRW.git
cd SWAT-MODFLOW-GMRW

# Run recharge mapping
python map_recharge_to_ibound.py

# Verify mapping
python verify_recharge_mapping.py

# Run SWAT-MODFLOW model
./SWAT-MODFLOW3.exe
```

## Files Modified

- `modflow_GMRW.rch` - Updated with spatially distributed recharge mapped to IBOUND

## Author

- **Repository**: HadiZamaniS
- **Date**: November 2025
- **Model**: SWAT-MODFLOW v3
- **Study Area**: Great Miami River Watershed (GMRW)

## License

This project contains SWAT-MODFLOW model input and configuration files for research purposes.

