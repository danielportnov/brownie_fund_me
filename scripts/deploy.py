from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3

def deploy_fund_me():
    account = get_account()
    tx_from = {"from": account}
    # pass the price feed address to our fund me contract

    # if we are on persistent network like rinkeby use associated
    # otherwise, deploy mocks

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # allows you to add addresses for diff networks like Kovan or Mainnet
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
    else:
        # we are in a dev chain
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        tx_from, 
        publish_source=config["networks"][network.show_active()].get("verify"))

    print(f"Contract deployed to {fund_me.address}")
    return fund_me

def main():
    deploy_fund_me()