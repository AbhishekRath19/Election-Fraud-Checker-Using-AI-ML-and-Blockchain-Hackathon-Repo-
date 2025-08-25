import os  # env config
import json  # save/load abi & address
import secrets  # random salts
from fastapi import FastAPI, HTTPException  # simple API
from pydantic import BaseModel  # request schema
from web3 import Web3  # Ethereum client
from eth_account import Account  # tx signing
from eth_utils import keccak  # commitment hashing
from solcx import compile_standard, install_solc  # compile Solidity from Python
from nacl.public import SealedBox, PublicKey  # encryption (Curve25519/XSalsa20-Poly1305)
from nacl.encoding import HexEncoder  # key encoding
# ...existing code...

# ===== Config =====
GANACHE_URL = os.getenv("GANACHE_URL", "http://localhost:7545") # local Ganache RPC
PRIVATE_KEY = os.getenv("PRIVATE_KEY") or "0x3d21fc98f79a99ce0e4a4c2d28d8176eb2a1cc70f2bb04460c5233baf4f838e7"  # backend signer (from Ganache)
AUTHORITY_PUBKEY_HEX = os.getenv("AUTHORITY_PUBKEY_HEX")  # NaCl public key for encryption (hex)
SERVER_NULLIFIER_SALT = os.getenv("SERVER_NULLIFIER_SALT", "change-me-super-secret")  # server salt
CONTRACT_JSON = "election_deploy.json"  # where we cache abi/address between runs
CONTRACT_SOURCE_PATH = os.getenv("CONTRACT_SOURCE_PATH", "contracts/Election.sol")  # solidity path
SOLC_VERSION = "0.8.20"  # must match pragma

app = FastAPI()  # FastAPI app

# ===== Web3 setup =====
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))  # connect to Ganache
if not w3.is_connected():
    raise RuntimeError("Cannot connect to Ganache at " + GANACHE_URL)  # fail early
print("Connected to Ganache at", GANACHE_URL)

account = Account.from_key(PRIVATE_KEY)  # our tx signer
# ...existing code...

import os  # env config
import json  # save/load abi & address
import secrets  # random salts
from fastapi import FastAPI, HTTPException  # simple API
from pydantic import BaseModel  # request schema
from web3 import Web3  # Ethereum client
from eth_account import Account  # tx signing
from eth_utils import keccak  # commitment hashing
from solcx import compile_standard, install_solc  # compile Solidity from Python
from nacl.public import SealedBox, PublicKey  # encryption (Curve25519/XSalsa20-Poly1305)
from nacl.encoding import HexEncoder  # key encoding

# ===== Config =====
GANACHE_URL = os.getenv("GANACHE_URL", "http://127.0.0.1:7545")  # local Ganache RPC
'''PRIVATE_KEY = os.getenv("PRIVATE_KEY")  # backend signer (from Ganache)''' # backend signer (from Ganache)
AUTHORITY_PUBKEY_HEX = os.getenv("AUTHORITY_PUBKEY_HEX")  # NaCl public key for encryption (hex)
SERVER_NULLIFIER_SALT = os.getenv("SERVER_NULLIFIER_SALT", "change-me-super-secret")  # server salt
CONTRACT_JSON = "election_deploy.json"  # where we cache abi/address between runs
CONTRACT_SOURCE_PATH = os.getenv("CONTRACT_SOURCE_PATH", "contracts/Election.sol")  # solidity path
SOLC_VERSION = "0.8.20"  # must match pragma

app = FastAPI()  # FastAPI app

# ===== Web3 setup =====
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))  # connect to Ganache
if not w3.is_connected():
    raise RuntimeError("Cannot connect to Ganache at " + GANACHE_URL)  # fail early

# ...existing code...

account = Account.from_key(PRIVATE_KEY)  # our tx signer

# ===== Model =====
class CastRequest(BaseModel):
    voterOpaqueId: str  # e.g., server-side ID created after AI verification; never the real GOV ID
    candidateId: int    # your frontend's selected party id

# ...existing code...
# ===== Utils =====
def load_or_deploy_contract():
    """Compile+deploy the contract (first run) or load it (subsequent runs)."""  # explain behavior
    if os.path.exists(CONTRACT_JSON):  # already deployed earlier
        with open(CONTRACT_JSON, "r") as f:
            data = json.load(f)  # load abi & address
        return w3.eth.contract(address=Web3.to_checksum_address(data["address"]), abi=data["abi"])  # return instance

    # Compile Solidity source
    install_solc(SOLC_VERSION)  # ensure compiler is present
    with open(CONTRACT_SOURCE_PATH, "r") as f:
        source = f.read()  # read Election.sol
    compiled = compile_standard({  # run solc
        "language": "Solidity",
        "sources": {"Election.sol": {"content": source}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}}
    }, solc_version=SOLC_VERSION)

    contract_interface = compiled["contracts"]["Election.sol"]["Election"]  # select contract
    abi = contract_interface["abi"]  # ABI for web3
    bytecode = contract_interface["evm"]["bytecode"]["object"]  # bytecode to deploy

    # Deploy transaction
    contract = w3.eth.contract(abi=abi, bytecode=bytecode)  # create deployable
    tx = contract.constructor().build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 6_000_000,
        "gasPrice": w3.to_wei("1", "gwei"),
    })  # build constructor tx

    # ...existing code...
    signed = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)  # sign
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)  # send
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)  # wait mined
# ...existing code...

# Also in the /cast endpoint:
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)  # sign with backend key
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)  # broadcast
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)  # wait mined for demo UX
# ...existing code...

    instance = w3.eth.contract(address=receipt.contractAddress, abi=abi)  # live instance

    # Persist ABI + address for reuse
    with open(CONTRACT_JSON, "w") as f:
        json.dump({"abi": abi, "address": receipt.contractAddress}, f)  # save deployment info

    return instance  # return the contract instance

contract = load_or_deploy_contract()  # ready to use

def make_nullifier(voter_opaque_id: str) -> bytes:
    """nullifierHash = keccak256(opaqueId || serverSalt) — prevents double voting without identity leakage."""  # doc
    return keccak(text=voter_opaque_id + SERVER_NULLIFIER_SALT)  # return 32-byte hash

def make_commitment(candidate_id: int, salt32: bytes) -> bytes:
    """commitment = keccak256(candidateId || salt) — proves later the ciphertext encodes this choice."""  # doc
    packed = candidate_id.to_bytes(32, "big") + salt32  # 32-byte candidate + 32-byte salt
    return keccak(packed)  # keccak256 bytes

def encrypt_ballot(candidate_id: int, salt32: bytes) -> bytes:
    """Encrypt JSON payload with authority's public key using NaCl SealedBox."""  # doc
    payload = json.dumps({
        "candidateId": candidate_id,
        "saltHex": salt32.hex()
    }).encode("utf-8")  # serialize vote
    pub = PublicKey(AUTHORITY_PUBKEY_HEX, encoder=HexEncoder)  # load authority pubkey
    sealed = SealedBox(pub).encrypt(payload)  # anonymous sealed box (no sender priv key needed)
    return sealed  # ciphertext bytes

# ===== Routes =====
@app.post("/cast")
def cast(req: CastRequest):
    """Called by frontend after verification & selection — writes encrypted ballot to chain."""  # doc
    # Generate per-vote randomness
    salt32 = secrets.token_bytes(32)  # 32-byte random salt for commitment binding

    # Compute primitives
    nullifier_hash = make_nullifier(req.voterOpaqueId)  # prevents double voting
    commitment = make_commitment(req.candidateId, salt32)  # binds to choice
    ciphertext = encrypt_ballot(req.candidateId, salt32)  # encrypted payload

    # Build submitBallot tx
    tx = contract.functions.submitBallot(
        Web3.to_bytes(hexstr=nullifier_hash.hex()),   # bytes32 nullifierHash
        Web3.to_bytes(hexstr=commitment.hex()),       # bytes32 commitment
        ciphertext                                    # bytes calldata ciphertext
    ).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 2_000_000,
        "gasPrice": w3.to_wei("1", "gwei"),
    })  # transaction config

    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)  # sign with backend key
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)  # broadcast
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)  # wait mined for demo UX

    # Find the BallotSubmitted event to return index & timestamp
    logs = contract.events.BallotSubmitted().process_receipt(receipt)  # decode logs
    index = logs[0]["args"]["index"] if logs else None  # ballot index if present

    return {
        "txHash": tx_hash.hex(),           # real transaction hash to show on UI
        "ballotIndex": index,              # index into on-chain ballots array
        "commitment": commitment.hex(),    # for audits / future reveal
        "timestamp": receipt["blockNumber"]  # simple anchor; you can lookup block timestamp
    }  # response JSON

@app.get("/tx/{tx_hash}")
def tx_status(tx_hash: str):
    """Simple status endpoint for 'Verify My Vote' button."""  # doc
    try:
        receipt = w3.eth.get_transaction_receipt(tx_hash)  # fetch from chain
        return {
            "status": int(receipt.status),        # 1 = success, 0 = failed
            "blockNumber": receipt.blockNumber,   # where it landed
            "gasUsed": receipt.gasUsed            # for curiosity
        }  # return a small status object
    except Exception:
        raise HTTPException(status_code=404, detail="Transaction not found")  # errors

@app.get("/ballot/{index}")
def ballot(index: int):
    """Read back the stored commitment + ciphertext (still private) by index."""  # doc
    commit, cipher, sender, ts = contract.functions.getBallot(index).call()  # call view fn
    return {
        "commitment": commit.hex(),       # hex-encoded keccak256
        "ciphertextHex": cipher.hex(),    # encrypted payload (nonsensical to anyone w/o key)
        "sender": sender,                 # EOA that sent tx
        "timestamp": ts                   # on-chain timestamp
    }  # response JSON