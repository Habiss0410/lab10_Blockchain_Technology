import json
import os
import urllib.request

RPC_URL = os.environ.get("RPC_URL", "https://ethereum-rpc.publicnode.com")
PAIR = os.environ.get("PAIR", "0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc")
DEC0 = int(os.environ.get("DEC0", "6"))
DEC1 = int(os.environ.get("DEC1", "18"))
GET_RESERVES = "0x0902f1ac"  

# Số liệu MẪU 
FALLBACK_RAW = (
    hex(20_000_000 * 10**6)[2:].zfill(64)
    + hex(8_000 * 10**18)[2:].zfill(64)
    + hex(0)[2:].zfill(64)
)


def eth_call(to, data):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_call",
                       "params": [{"to": to, "data": data}, "latest"]}).encode()
    req = urllib.request.Request(RPC_URL, body, {"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        out = json.load(resp)
    if "error" in out:
        raise RuntimeError(out["error"])
    return out["result"]


try:
    raw = eth_call(PAIR, GET_RESERVES)[2:]
    source = f"LIVE từ {RPC_URL}"
except Exception as e:
    raw = FALLBACK_RAW
    source = f"DỰ PHÒNG (số liệu mẫu, RPC không dùng được: {type(e).__name__})"

reserve0 = int(raw[0:64], 16)    # token0
reserve1 = int(raw[64:128], 16)  # token1

print(f"Nguồn dữ liệu : {source}")
print(f"Pair          : {PAIR}")
print(f"reserve0 (raw): {reserve0}")
print(f"reserve1 (raw): {reserve1}")
print(f"reserve0 / 10**{DEC0} = {reserve0 / 10**DEC0:,.4f}")
print(f"reserve1 / 10**{DEC1} = {reserve1 / 10**DEC1:,.4f}")
price_weth_in_usdc = (reserve0 / 1e6) / (reserve1 / 1e18)
print(f"Giá spot 1 WETH = {price_weth_in_usdc:,.2f} USDC")
print(f"(nếu quên chia decimals: tỷ số thô = {reserve0 / reserve1:.3e} — sai lệch 10^{DEC1 - DEC0} lần)")
