COLLATERAL_ETH = 10
DEBT_USDC = 12_000
LIQ_THRESHOLD = 0.825
CLOSE_FACTOR = 0.5
BONUS = 0.05


def health_factor(collateral, price, debt, threshold=LIQ_THRESHOLD):
    return collateral * price * threshold / debt


def liquidation_price(collateral, debt, threshold=LIQ_THRESHOLD):
    return debt / (collateral * threshold)   # HF = 1


print("Health factor khi giá ETH rơi (10 ETH thế chấp, nợ 12,000 USDC, ngưỡng 82.5%)")
for p in (2000, 1800, 1600, 1500, 1454.55, 1450):
    hf = health_factor(COLLATERAL_ETH, p, DEBT_USDC)
    status = "an toàn" if hf >= 1 else "CÓ THỂ BỊ THANH LÝ"
    print(f"  ETH = ${p:>8,.2f}   HF = {hf:.4f}   {status}")

liq = liquidation_price(COLLATERAL_ETH, DEBT_USDC)
print(f"\nGiá thanh lý (HF = 1): ${liq:,.2f}")

price = 1450
repay = DEBT_USDC * CLOSE_FACTOR                 # thanh lý tối đa 50% nợ
seized_eth = repay * (1 + BONUS) / price         # nhận tài sản thế chấp + thưởng 5%
coll_after = COLLATERAL_ETH - seized_eth
debt_after = DEBT_USDC - repay
print(f"\nThanh lý một phần tại ETH = ${price:,} (close factor 50%, thưởng 5%):")
print(f"  người thanh lý trả      : {repay:,.2f} USDC")
print(f"  người thanh lý nhận     : {seized_eth:.4f} ETH (~${seized_eth*price:,.2f})")
print(f"  thế chấp còn lại        : {coll_after:.4f} ETH")
print(f"  nợ còn lại              : {debt_after:,.2f} USDC")
print(f"  HF sau thanh lý         : {health_factor(coll_after, price, debt_after):.4f}")
