import numpy as np

def read_ibound_from_bas(bas_file):
    """Read IBOUND array from MODFLOW BAS file"""
    with open(bas_file, 'r') as f:
        lines = f.readlines()
    
    ibound_start = None
    for i, line in enumerate(lines):
        if 'IBOUND layer 1' in line:
            ibound_start = i + 1
            break
    
    if ibound_start is None:
        raise ValueError("Could not find IBOUND in BAS file")
    
    ibound = []
    for i in range(ibound_start, len(lines)):
        line = lines[i].strip()
        if line.startswith('#') or line.startswith('-999') or line.startswith('INTERNAL'):
            break
        if line:
            values = [int(float(x)) for x in line.split()]
            ibound.append(values)
    
    return np.array(ibound)

def read_recharge_from_rch(rch_file):
    """Read recharge array from MODFLOW RCH file"""
    with open(rch_file, 'r') as f:
        lines = f.readlines()
    
    # Find where recharge array starts
    rch_start = None
    for i, line in enumerate(lines):
        if 'RECH' in line or 'INTERNAL' in line:
            rch_start = i + 1
            break
    
    if rch_start is None:
        raise ValueError("Could not find recharge array in RCH file")
    
    recharge = []
    for i in range(rch_start, len(lines)):
        line = lines[i].strip()
        if line.startswith('#') or not line:
            continue
        values = [float(x) for x in line.split()]
        recharge.append(values)
    
    return np.array(recharge)

def verify_mapping(ibound, recharge):
    """Verify that recharge is correctly mapped to IBOUND"""
    print("="*70)
    print("RECHARGE MAPPING VERIFICATION")
    print("="*70)
    
    # Check dimensions
    print(f"\n1. DIMENSION CHECK:")
    print(f"   IBOUND shape:   {ibound.shape}")
    print(f"   Recharge shape: {recharge.shape}")
    if ibound.shape == recharge.shape:
        print("   ✓ Dimensions match!")
    else:
        print("   ✗ ERROR: Dimensions do not match!")
        return False
    
    # Check mapping correctness
    print(f"\n2. MAPPING VERIFICATION:")
    
    # Where IBOUND = 0, recharge should be 0
    inactive_cells = (ibound == 0)
    inactive_recharge = recharge[inactive_cells]
    
    print(f"   Inactive cells (IBOUND=0): {np.sum(inactive_cells)}")
    print(f"   Recharge at inactive cells - Min: {np.min(inactive_recharge):.6f}, Max: {np.max(inactive_recharge):.6f}")
    
    if np.all(inactive_recharge == 0):
        print("   ✓ All inactive cells have recharge = 0")
    else:
        print(f"   ✗ ERROR: {np.sum(inactive_recharge != 0)} inactive cells have non-zero recharge!")
        return False
    
    # Where IBOUND = 1, recharge should be > 0
    active_cells = (ibound == 1)
    active_recharge = recharge[active_cells]
    
    print(f"\n   Active cells (IBOUND=1): {np.sum(active_cells)}")
    print(f"   Recharge at active cells - Min: {np.min(active_recharge):.6f}, Max: {np.max(active_recharge):.6f}")
    
    if np.all(active_recharge > 0):
        print(f"   ✓ All active cells have recharge > 0")
        print(f"   ✓ Recharge value: {np.unique(active_recharge)[0]:.6f}")
    else:
        print(f"   ✗ WARNING: {np.sum(active_recharge == 0)} active cells have zero recharge!")
    
    # Sample verification - show some cells
    print(f"\n3. SAMPLE CELLS (showing first 10 rows, columns 60-75):")
    print("   " + "="*60)
    print("   IBOUND values:")
    print(ibound[:10, 60:75])
    print("\n   Corresponding RECHARGE values:")
    print(recharge[:10, 60:75])
    
    # Check specific locations
    print(f"\n4. SPOT CHECK (random samples):")
    print("   " + "-"*60)
    print("   Row | Col | IBOUND | Recharge | Status")
    print("   " + "-"*60)
    
    np.random.seed(42)
    for _ in range(10):
        row = np.random.randint(0, ibound.shape[0])
        col = np.random.randint(0, ibound.shape[1])
        ib_val = ibound[row, col]
        rch_val = recharge[row, col]
        
        # Check if mapping is correct
        if ib_val == 0 and rch_val == 0:
            status = "✓ Correct"
        elif ib_val == 1 and rch_val > 0:
            status = "✓ Correct"
        else:
            status = "✗ ERROR"
        
        print(f"   {row:3d} | {col:3d} | {ib_val:6d} | {rch_val:.6f} | {status}")
    
    print("\n" + "="*70)
    print("VERIFICATION COMPLETE!")
    print("="*70)
    
    return True

def main():
    bas_file = 'modflow_GMRW.bas'
    rch_file = 'modflow_GMRW.rch'
    
    print("Reading IBOUND from BAS file...")
    ibound = read_ibound_from_bas(bas_file)
    
    print("Reading Recharge from RCH file...")
    recharge = read_recharge_from_rch(rch_file)
    
    print("\nVerifying recharge mapping...\n")
    verify_mapping(ibound, recharge)

if __name__ == "__main__":
    main()
