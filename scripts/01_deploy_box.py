from scripts.helpful_scripts import get_account_v2, encode_function_data
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy, Contract, config

def main():
    account = get_account_v2()
    # implementation contract
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"]
    )

    # proxy admin (us), optional
    proxy_admin = ProxyAdmin.deploy({"from":account})

    # initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()

    # proxy contract
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000}
    )
    print(f"Proxy deployed to {proxy} ! You can now upgrade it to BoxV2!")
    # here we use proxy address instead
    # so that proxy delegates the function calls to the box contract
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    # now we can call box functions from the proxy
    tx = proxy_box.store(1, {"from": account})
    # add wait to prevent ConnectionResetError
    tx.wait(1)
    print(f"Here is the initial value in the Box: {proxy_box.retrieve()}")