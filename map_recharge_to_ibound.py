import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def read_ibound_from_bas(bas_file):
    """
    Read IBOUND array from MODFLOW BAS file
    """
    with open(bas_file, 'r') as f:
        lines = f.readlines()
    
    # Find the line with IBOUND
    ibound_start = None
    for i, line in enumerate(lines):
        if 'IBOUND layer 1' in line:
            ibound_start = i + 1
            break
    
    if ibound_start is None:
        raise ValueError("Could not find IBOUND in BAS file")
    
    # Read IBOUND array
    ibound = []
    for i in range(ibound_start, len(lines)):
        line = lines[i].strip()
        if line.startswith('#') or line.startswith('-999') or line.startswith('INTERNAL'):
            break
        if line:
            values = [int(float(x)) for x in line.split()]
            ibound.append(values)
    
    return np.array(ibound)

def create_recharge_array(ibound, recharge_rate=0.001):
    """
    Create recharge array based on IBOUND
    Recharge is applied only where IBOUND = 1 (active cells)
    """
    recharge = np.zeros_like(ibound, dtype=float)
    recharge[ibound == 1] = recharge_rate
    
    return recharge

def write_rch_file(rch_file, recharge_array, irchcb=40):
    """
    Write MODFLOW RCH file with spatially distributed recharge
    """
    nrow, ncol = recharge_array.shape
    
    with open(rch_file, 'w') as f:
        f.write("# Great Miami River Watershed groundwater flow model\n")
        f.write("# Recharge (RCH) input file - mapped to IBOUND\n")
        f.write(f"3 {irchcb}\t\t\t\t# NRCHOP, IRCHCB\n")
        f.write("0 0\n")
        f.write("INTERNAL 1 (FREE) -1\t\t# RECH (L/T)\n")
        
        # Write recharge array
        for row in recharge_array:
            line = ' '.join([f'{val:.6f}' for val in row])
            f.write(line + '\n')

def create_recharge_map(ibound, recharge_array, output_file='recharge_map.png'):
    """
    Create a visual map of recharge distribution with gray boundary
    """
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    
    # Plot 1: IBOUND map with gray boundary
    ax1 = axes[0]
    # Create custom colormap for IBOUND: gray for 0, green for 1
    cmap_ibound = mcolors.ListedColormap(['gray', 'green'])
    bounds = [-0.5, 0.5, 1.5]
    norm = mcolors.BoundaryNorm(bounds, cmap_ibound.N)
    
    im1 = ax1.imshow(ibound, cmap=cmap_ibound, norm=norm, aspect='auto', interpolation='nearest')
    ax1.set_title('IBOUND Map\n(Gray=Inactive, Green=Active)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Column', fontsize=12)
    ax1.set_ylabel('Row', fontsize=12)
    cbar1 = plt.colorbar(im1, ax=ax1, orientation='horizontal', pad=0.05, ticks=[0, 1])
    cbar1.set_label('IBOUND Status', fontsize=11)
    cbar1.ax.set_xticklabels(['Inactive (0)', 'Active (1)'])
    
    # Add grid statistics
    active = np.sum(ibound == 1)
    inactive = np.sum(ibound == 0)
    ax1.text(0.02, 0.98, f'Active: {active:,}\nInactive: {inactive:,}', 
             transform=ax1.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    # Plot 2: Recharge map with gray boundary
    ax2 = axes[1]
    # Create masked array for recharge visualization
    recharge_masked = np.ma.masked_where(ibound == 0, recharge_array)
    
    # Show inactive cells as gray background
    ax2.imshow(np.where(ibound == 0, 1, 0), cmap='gray', alpha=0.3, aspect='auto', interpolation='nearest')
    
    # Overlay recharge values
    cmap_recharge = plt.cm.Blues
    im2 = ax2.imshow(recharge_masked, cmap=cmap_recharge, aspect='auto', interpolation='nearest', vmin=0)
    ax2.set_title('Recharge Map\n(Gray boundary = Inactive cells)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Column', fontsize=12)
    ax2.set_ylabel('Row', fontsize=12)
    cbar2 = plt.colorbar(im2, ax=ax2, orientation='horizontal', pad=0.05)
    cbar2.set_label('Recharge Rate (m/day)', fontsize=11)
    
    # Add recharge statistics
    rch_cells = np.sum(recharge_array > 0)
    max_rch = np.max(recharge_array)
    mean_rch = np.mean(recharge_array[recharge_array > 0]) if rch_cells > 0 else 0
    ax2.text(0.02, 0.98, f'Cells with recharge: {rch_cells:,}\nMax: {max_rch:.6f}\nMean: {mean_rch:.6f}', 
             transform=ax2.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    
    # Plot 3: Combined map with boundary outline
    ax3 = axes[2]
    # Create RGB overlay with gray boundary
    overlay = np.ones((*ibound.shape, 3))
    
    # Gray background for inactive cells
    overlay[ibound == 0] = [0.7, 0.7, 0.7]
    
    # Blue gradient for active cells with recharge
    recharge_norm = recharge_array / np.max(recharge_array) if np.max(recharge_array) > 0 else recharge_array
    overlay[ibound == 1, 0] = 1 - recharge_norm[ibound == 1] * 0.8  # R
    overlay[ibound == 1, 1] = 1 - recharge_norm[ibound == 1] * 0.5  # G
    overlay[ibound == 1, 2] = 1  # B (full blue)
    
    ax3.imshow(overlay, aspect='auto', interpolation='nearest')
    ax3.set_title('Recharge with Gray Boundary\n(Gray=Inactive, Blue=Active w/ Recharge)', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Column', fontsize=12)
    ax3.set_ylabel('Row', fontsize=12)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='gray', alpha=0.7, label=f'Inactive Boundary: {inactive:,} cells'),
        Patch(facecolor='lightblue', alpha=1.0, label=f'Active w/ Recharge: {rch_cells:,} cells')
    ]
    ax3.legend(handles=legend_elements, loc='upper right', fontsize=10,
               bbox_to_anchor=(0.98, 0.98), framealpha=0.9)
    
    plt.suptitle('MODFLOW Recharge Distribution - Great Miami River Watershed', 
                 fontsize=16, fontweight='bold', y=1.00)
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ Recharge map saved as: {output_file}")
    
    # Also save a high-res version
    output_file_hires = output_file.replace('.png', '_highres.png')
    plt.savefig(output_file_hires, dpi=600, bbox_inches='tight')
    print(f"✓ High-resolution map saved as: {output_file_hires}")
    
    plt.close()
    print("✓ Map generation complete!")

def main():
    # File paths
    bas_file = 'modflow_GMRW.bas'
    rch_file_output = 'modflow_GMRW_mapped.rch'
    
    # Recharge rate (you can modify this value)
    recharge_rate = 0.001  # m/day or appropriate units
    
    print("Reading IBOUND from BAS file...")
    ibound = read_ibound_from_bas(bas_file)
    print(f"IBOUND dimensions: {ibound.shape}")
    print(f"Active cells (IBOUND=1): {np.sum(ibound == 1)}")
    print(f"Inactive cells (IBOUND=0): {np.sum(ibound == 0)}")
    
    print("\nCreating recharge array based on IBOUND...")
    recharge_array = create_recharge_array(ibound, recharge_rate)
    
    print(f"Cells with recharge: {np.sum(recharge_array > 0)}")
    print(f"Total recharge volume: {np.sum(recharge_array):.6f}")
    
    print(f"\nWriting new RCH file: {rch_file_output}")
    write_rch_file(rch_file_output, recharge_array)
    
    print("\nDone! The new RCH file has been created.")
    print("Replace 'modflow_GMRW.rch' with 'modflow_GMRW_mapped.rch' or rename it.")
    
    # Print statistics
    print("\n--- Statistics ---")
    print(f"Min recharge: {np.min(recharge_array):.6f}")
    print(f"Max recharge: {np.max(recharge_array):.6f}")
    print(f"Mean recharge (non-zero cells): {np.mean(recharge_array[recharge_array > 0]):.6f}")
    
    # Create visual recharge map
    print("\n--- Creating Recharge Map ---")
    create_recharge_map(ibound, recharge_array, 'GMRW_recharge_map.png')
    
    print("\n" + "="*70)
    print("ALL TASKS COMPLETED SUCCESSFULLY!")
    print("="*70)

if __name__ == "__main__":
    main()
