from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    deploy_mocks,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    # pass price feed address to fundme contract
    # if on a persistent network (rinkeby), use associated address. Otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:  # development=local
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:  # on development chain there is no contract in the first place --> deploy own version (mock)
        deploy_mocks()
        # use address of most recently deployed Mock
        price_feed_address = MockV3Aggregator[-1].address
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  # [verify] also possible but could lead into index error
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
