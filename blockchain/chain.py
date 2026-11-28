# Let's Build It: a blockchain you can try to cheat. No installs, just Python.
import hashlib, time

ZEROS = 4                                     # how hard mining is

# 1. A FINGERPRINT: any text in, 64 characters out. Change one letter, all 64 change.
def fingerprint(block):
    text = f"{block['number']}|{block['data']}|{block['before']}|{block['lucky']}"
    return hashlib.sha256(text.encode()).hexdigest()

# 2. MINING: keep trying lucky numbers until the fingerprint starts with zeros
def mine(block):
    block["lucky"] = 0
    while not fingerprint(block).startswith("0" * ZEROS):
        block["lucky"] += 1
    block["print"] = fingerprint(block)
    return block

# 3. THE CHAIN: every block carries the fingerprint of the block before it
def add(chain, data):
    before = chain[-1]["print"] if chain else "0" * 64
    chain.append(mine({"number": len(chain), "data": data, "before": before}))

# 4. THE CHECK: recompute every fingerprint, demand the zeros, follow the links
def check(chain):
    for block in chain:
        if fingerprint(block) != block["print"]:
            return f"BROKEN: block {block['number']} was changed"
        if not block["print"].startswith("0" * ZEROS):
            return f"BROKEN: block {block['number']} has invalid proof of work"
        if block["number"] > 0 and block["before"] != chain[block["number"] - 1]["print"]:
            return f"BROKEN: block {block['number']} does not link to block {block['number'] - 1}"
    return "all good"

if __name__ == "__main__":
    chain = []
    for data in ["start", "Ali pays Sara 10", "Sara pays Omar 4", "Omar pays Ali 7", "Ali pays Omar 2"]:
        add(chain, data)
    for block in chain:
        print(block["number"], block["print"][:16], f"lucky={block['lucky']:<7}", block["data"])
    print("check:", check(chain))

    # 5. CHEAT: change one old payment
    chain[1]["data"] = "Ali pays Sara 1000"
    print("after the cheat:", check(chain))

    # 6. CHEAT HARDER: re-mine that block so its own fingerprint is valid again
    mine(chain[1])
    print("after re-mining block 1:", check(chain))

    # 7. THE ONLY WAY: redo every block after it, while the honest chain keeps growing
    began = time.time()
    for block in chain[2:]:
        block["before"] = chain[block["number"] - 1]["print"]
        mine(block)
    print("after re-mining everything:", check(chain), f"({time.time() - began:.2f} s of work)")
