import math

FEE = 0.003


def get_amount_out(dx, x, y, fee=FEE):
    dx_eff = dx * (1 - fee)          
    return y * dx_eff / (x + dx_eff)  


def impermanent_loss(r):
    """r = P_after / P_before. IL <= 0 và IL(r) == IL(1/r)."""
    return 2 * math.sqrt(r) / (1 + r) - 1


def swap_table():
    x0, y0 = 100_000, 200_000
    k0 = x0 * y0
    spot0 = y0 / x0
    print(f"Lab 10.1 — Constant-product AMM (x*y = k) with a {FEE*100:.2f}% fee")
    print(f"  pool start: X={x0:,}  Y={y0:,}  k={k0:,}  spot={spot0:.6f} Y/X  (fee={FEE*100:.2f}%)")
    print(f"  {'dx (X in)':>10} {'dy (Y out)':>12} {'exec price':>11} {'new spot':>10} {'price impact':>13} {'k after':>20}")
    for dx in (100, 1_000, 5_000, 10_000, 50_000):
        dy = get_amount_out(dx, x0, y0)
        x1, y1 = x0 + dx, y0 - dy      
        new_spot = y1 / x1
        impact = (new_spot / spot0 - 1) * 100
        print(f"  {dx:>10,} {dy:>12,.4f} {dy/dx:>11.6f} {new_spot:>10.6f} {impact:>10.2f} %  {x1*y1:>18,.1f}")
    return x0, y0


def il_table():
    print("\nLab 10.2 — Impermanent loss IL(r) = 2*sqrt(r)/(1+r) - 1")
    print("  r = P_after/P_before    IL vs HODL (rounded)")
    print("  " + "-" * 52)
    for r in (1.25, 1.5, 2, 3, 4, 5):
        il = impermanent_loss(r)
        print(f"  {r:<6}  {il*100:>9.4f}%   {abs(il)*100:.1f}%")
    print("  " + "-" * 52)

    print("\n  Machine-checking IL against the classic table:")
    checks = [(1.25, 0.62), (2, 5.72), (4, 20.00), (5, 25.46), (0.5, 5.72)]
    for r, expected in checks:
        got = abs(impermanent_loss(r)) * 100
        ok = abs(got - expected) < 0.01
        note = " (symmetry)" if r == 0.5 else ""
        print(f"  [{'OK ' if ok else 'FAIL'}] IL({r:g}) = {got:.3f}% expected ~{expected:.2f}%{note}")
        assert ok, f"IL({r}) lệch: {got}"
    assert abs(impermanent_loss(2) - impermanent_loss(0.5)) < 1e-12
    print("  All IL assertions passed. (IL(2)=IL(0.5) confirms symmetry.)")


def plot_curve(x0, y0):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    k = x0 * y0
    xs = [x0 * (0.4 + i * 0.02) for i in range(1, 90)]
    plt.plot(xs, [k / x for x in xs])
    plt.scatter([x0], [y0])
    plt.xlabel("X"); plt.ylabel("Y"); plt.title("x*y = k")
    plt.savefig("amm_curve.png", dpi=120)
    print("\nĐã lưu amm_curve.png")


if __name__ == "__main__":
    x0, y0 = swap_table()
    il_table()
    plot_curve(x0, y0)
