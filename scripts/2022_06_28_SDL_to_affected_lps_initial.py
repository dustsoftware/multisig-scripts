from helpers import CHAIN_IDS, MULTISIG_ADDRESSES, SDL_ADDRESSES
from ape_safe import ApeSafe
from brownie import accounts, network
from eth_utils import to_wei

from scripts.utils import confirm_posting_transaction


def main():
    """Send the 6.7m SDL to affected LPs according to https://snapshot.org/#/saddlefinance.eth/proposal/0xf27b07ef7025aa23edb2a84d56825511ea7adff8d6164cd09a23c63c42cdc01a"""

    print(f"You are using the '{network.show_active()}' network")
    deployer = accounts.load("deployer")  # prompts for password
    multisig = ApeSafe(MULTISIG_ADDRESSES[CHAIN_IDS["MAINNET"]])

    refunds = {
        "0xa0f75491720835b36edc92d06ddc468d201e9b73": to_wei(1552781.39214474, "ether"),
        "0x38ee5f5a39c01cb43473992c12936ba1219711ab": to_wei(1508913.00981469, "ether"),
        "0x38f9abd4bd8947da035abf51fc21244108a81ca6": to_wei(1132442.54883665, "ether"),
        "0x0ea4a285e1353f490ec7f473ab3174cac71cf79a": to_wei(1132219.93569692, "ether"),
        "0x6ef3f0ff397c3de367c6ca2cc3e6b6955e7993a5": to_wei(183256.672290299, "ether"),
        "0x6a73204db71f8e054bf9a0680b02ae96f700b595": to_wei(181265.62698562, "ether"),
        "0x5eea118e75f247014c6d0e990f02a0c254edc852": to_wei(151319.065792276, "ether"),
        "0x2b9d8f558e02753ed7d4d97dedfad662c02af3cb": to_wei(150998.563444325, "ether"),
        "0x0bb31c6278d58cff41b7e8ed3b20f76424fd69ad": to_wei(150936.201534769, "ether"),
        "0xc7d2a419f8f2eaa06b3811cf7faaa7440dcf96b7": to_wei(150888.579725597, "ether"),
        "0xae1e5c84b73136a49efb70a15149c350015391ed": to_wei(113255.253248794, "ether"),
        "0xe2d079278c0f4959199136f8db11c645d69a292b": to_wei(113234.843908429, "ether"),
        "0xffd4dae0d7d8ddb6f408dca0a47763ae3a57f4ce": to_wei(62280.638160798, "ether"),
        "0x9c7d894a29f97636b66dea646a1ae2f9c83a2830": to_wei(54450.629479509, "ether"),
        "0x77956a9d1b9901bbe4cfc2ed37db17500fbe7b0c": to_wei(37688.12936225, "ether"),
        "0x02ef8147e2d0997cca48d99f01bad846d16558fa": to_wei(30168.0509875, "ether"),
        "0xc7193c01f43257f3fe4c8f86784fcaa578a9e2b1": to_wei(24138.9591695, "ether"),
        "0xd716ad4f10eade5af4ed10006678f49bd2e6624f": to_wei(7545.4015315, "ether"),
        "0x99eb33756a2eaa32f5964a747722c4b59e6af351": to_wei(3214.8607335, "ether"),
        "0x2a1eaf114f2c23d30ef571d6e84fcbeb2f6f4e62": to_wei(1509.903056, "ether"),
        "0x46866d274e6d9015c5fdc098ce270803e11e3ef4": to_wei(829.988099, "ether"),
        "0x2d5d79753bb8e02ca1ce8ece0aa55288f8c8d840": to_wei(414.9940495, "ether"),
        "0xb5e46afa9596cb6f44d2fcb6dbd2096dbe35396c": to_wei(75.9582305, "ether"),
        "0x74f8744020f5900a2c3a3289c6c2182f56a6901f": to_wei(20.7935375, "ether"),
    }
    total = sum(refunds.values())
    print(f"Total amount to be refunded: {total} SDL")
    sdl_contract = multisig.contract(SDL_ADDRESSES[CHAIN_IDS["MAINNET"]])
    for address, amount in refunds.items():
        sdl_contract.transfer(address, amount)

    # combine history into multisend txn
    safe_tx = multisig.multisend_from_receipts()
    safe_tx.safe_nonce = 41

    # sign with private key
    safe_tx.sign(deployer.private_key)
    multisig.preview(safe_tx)

    confirm_posting_transaction(multisig, safe_tx)