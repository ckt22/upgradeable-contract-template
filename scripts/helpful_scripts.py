from ast import arg
from brownie import (
    accounts,
    config,
    network
)
import eth_utils

LOCAL_BLOCKCHAIN_ENVIRONMENTS=["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS=["mainnet-fork-dev"]

OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

def get_account_v2(index=None, id=None):
    if (index):
        return accounts[index]
    if (id):
        return accounts.load(id)
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS 
    or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

# initializer = box.store, 1
def encode_function_data(initializer=None, *args):
    """Encodes the function call so we can work with an initializer.
    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Example: `box.store`.
        Defaults to None.
        args (Any, optional):
        The arguments to pass to the initializer function
    Returns:
        [bytes]: Return the encoded bytes.
    """
    if not len(args): args = b''

    if initializer: return initializer.encode_input(*args)

    return b''

def upgrade(
    account,
    proxy,
    newimplementation_address,
    proxy_admin_contract=None,
    initializer=None,
    *args
):
    transaction = None
    if proxy_admin_contract:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                newimplementation_address,
                encoded_function_call,
                {"from": account},
            )
            transaction.wait(1)
        else:
            transaction = proxy_admin_contract.upgrade(
                proxy.address, newimplementation_address, {"from": account}
            )
            transaction.wait(1)
    else:
        # use proxy contract
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                newimplementation_address, encoded_function_call, {"from": account}
            )
        else:
            transaction = proxy.upgradeTo(newimplementation_address, {"from": account})
    return 
