# SWAT-MODFLOW Recharge Mapping for Great Miami River Watershed

## Overview
This repository contains SWAT-MODFLOW coupled model files for the Great Miami River Watershed (GMRW) with spatially distributed recharge mapped to IBOUND array.

## Project Description
- **Model Type**: SWAT-MODFLOW Coupled Surface-Groundwater Model
- **Watershed**: Great Miami River Watershed
- **Grid Dimensions**: 197 rows  135 columns
- **Active Cells**: 11,029 cells
- **Inactive Cells**: 15,566 cells

## Key Features
- Recharge mapped to IBOUND array (only active cells receive recharge)
- Python scripts for automated recharge mapping and visualization
- Visual maps showing recharge distribution with gray boundaries for inactive cells

## Files
- modflow_GMRW.bas - MODFLOW Basic Package file with IBOUND array
- modflow_GMRW.rch - MODFLOW Recharge Package file (spatially distributed)
- modflow_GMRW_original.rch - Original recharge file backup
- map_recharge_to_ibound.py - Script to map recharge based on IBOUND
- erify_recharge_mapping.py - Script to verify recharge mapping
- GMRW_recharge_map.png - Recharge distribution visualization
- GMRW_recharge_map_highres.png - High-resolution recharge map

## Usage

### Generate Recharge Mapping
```python
python map_recharge_to_ibound.py
```

### Verify Recharge Mapping
```python
python verify_recharge_mapping.py
```

## Recharge Configuration
- **Recharge Rate**: 0.001 m/day (applied only to active cells)
- **Inactive Cells**: 0.0 m/day (no recharge outside watershed boundary)

## Model Statistics
- Total recharge volume: 11.029 units
- Recharge applied to 11,029 active cells within watershed boundary
- Gray boundary represents 15,566 inactive cells outside the model domain

## Date
Created: November 16, 2025

## License
Research and Educational Use

