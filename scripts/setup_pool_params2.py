#!/usr/bin/python3

from brownie import *
from brownie.network.contract import InterfaceContainer
from brownie.network.state import _add_contract, _remove_contract

import shared
from munch import Munch

'''deploys = Munch.fromDict({
    "bZxProtocol": True,
    "PriceFeeds": True,
    "SwapsImpl": True,
    "ProtocolMigration": True,
    "ProtocolSettings": True,
    "LoanSettings": True,
    "LoanOpenings": True,
    "LoanMaintenance": True,
    "LoanClosings": True,
})'''

'''
"0x0afBFCe9DB35FFd1dFdF144A788fa196FD08EFe9", # iETH
"0xA1e58F3B1927743393b25f261471E1f2D3D9f0F6", # iSAI
"0xd40C0e7230c5bde65B61B5EDDc3E973f76Aff252", # iDAI

"0xd0A1E359811322d97991E03f863a0C30C2cF029C", # WETH
"0xC4375B7De8af5a38a93548eb8453a498222C4fF2", # SAI
"0x4F96Fe3b7A6Cf9725f59d353F723c1bDb64CA6Aa", # DAI
'''
def main():
    thisNetwork = network.show_active()

    if thisNetwork == "development":
        acct = accounts[0]
    elif thisNetwork == "mainnet" or thisNetwork == "mainnet-fork":
        acct = accounts.load('deployer1')
        bzx = Contract.from_abi("bzx", address="0xD8Ee69652E4e4838f2531732a46d1f7F584F0b7f", abi=interface.IBZx.abi, owner=acct)
    elif thisNetwork == "kovan":
        acct = accounts.load('testnet_admin')
        bzx = Contract.from_abi("bzx", address="0x5cfba2639a3db0D9Cc264Aa27B2E6d134EeA486a", abi=interface.IBZx.abi, owner=acct)
    else:
        acct = accounts.load('testnet_admin')
    print("Loaded account",acct)

    constants = shared.Constants()
    addresses = shared.Addresses()

    if thisNetwork == "kovan":
        itokens = {
            "fWETH": "0xe3d99c2152Fc8eA5F87B733706FAA241C37592f1", # ifWETH
            "WBTC": "0xF6a0690f22da5464924A28a8198E8ecA69ffc47e", # iWBTC
            "USDC": "0x021C5923398168311Ff320902BF8c8C725B4F288", # iUSDC
        }

        tokens = {
            "fWETH": "0xfBE16bA4e8029B759D3c5ef8844124893f3ae470", # fWETH
            "WBTC": "0x5aE55494Ccda82f1F7c653BC2b6EbB4aD3C77Dac", # WBTC
            "USDC": "0xB443f30CDd6076b1A5269dbc08b774F222d4Db4e", # USDC
        }

        collateralTokens = [
            "0xfBE16bA4e8029B759D3c5ef8844124893f3ae470", # WETH
            "0x5aE55494Ccda82f1F7c653BC2b6EbB4aD3C77Dac", # WBTC
            "0xB443f30CDd6076b1A5269dbc08b774F222d4Db4e", # USDC
        ]

        config = [
            ### token1, token2, Liquidation_Markdown, Initial_Margin, Margin_Maintenance
            "fWETH,WBTC,12000000000000000000,35000000000000000000,30000000000000000000",
            "fWETH,USDC,5000000000000000000,20000000000000000000,15000000000000000000",
            "WBTC,USDC,12000000000000000000,35000000000000000000,30000000000000000000",
        ]

    elif thisNetwork == "mainnet" or thisNetwork == "mainnet-fork":

        itokens = {
            "DAI": "0x6b093998d36f2c7f0cc359441fbb24cc629d5ff0", # iDAI
            "ETH": "0xb983e01458529665007ff7e0cddecdb74b967eb6", # iETH
            "USDC": "0x32e4c68b3a4a813b710595aeba7f6b7604ab9c15", # iUSDC
            "WBTC": "0x2ffa85f655752fb2acb210287c60b9ef335f5b6e", # iWBTC
            "KNC": "0x687642347a9282be8fd809d8309910a3f984ac5a", # iKNC
            "MKR": "0x9189c499727f88f8ecc7dc4eea22c828e6aac015", # iMKR
            "BZRX": "0x18240bd9c07fa6156ce3f3f61921cc82b2619157", # iBZRX
            "LINK": "0x463538705e7d22aa7f03ebf8ab09b067e1001b54", # iLINK
            "YFI": "0x7f3fe9d492a9a60aebb06d82cba23c6f32cad10b", # iYFI
            "USDT": "0x7e9997a38a439b2be7ed9c9c4628391d3e055d48", # iUSDT
            "UNI": "0x0a625FceC657053Fe2D9FFFdeb1DBb4e412Cf8A8", # iUNI
            "AAVE": "0x0cae8d91E0b1b7Bd00D906E990C3625b2c220db1", # iAAVE
        }

        tokens = {
            "DAI": "0x6b175474e89094c44da98b954eedeac495271d0f", # DAI
            "ETH": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", # ETH
            "USDC": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", # USDC
            "WBTC": "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", # WBTC
            "KNC": "0xdd974d5c2e2928dea5f71b9825b8b646686bd200", # KNC
            "MKR": "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2", # MKR
            "BZRX": "0x56d811088235F11C8920698a204A5010a788f4b3", # BZRX
            "LINK": "0x514910771AF9Ca656af840dff83E8264EcF986CA", # LINK
            "YFI": "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e", # YFI
            "USDT": "0xdac17f958d2ee523a2206206994597c13d831ec7", # USDT
            "UNI": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", # UNI
            "AAVE": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9", # AAVE
        }


        collateralTokens = [
            "0x6b175474e89094c44da98b954eedeac495271d0f", # DAI
            "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", # ETH
            "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", # USDC
            "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599", # WBTC
            "0xdd974d5c2e2928dea5f71b9825b8b646686bd200", # KNC
            "0x9f8f72aa9304c8b593d555f12ef6589cc3a579a2", # MKR
            "0x56d811088235F11C8920698a204A5010a788f4b3", # BZRX
            "0x514910771AF9Ca656af840dff83E8264EcF986CA", # LINK
            "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e", # YFI
            "0xdac17f958d2ee523a2206206994597c13d831ec7", # USDT
            "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", # UNI
            "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9", # AAVE
        ]

        config = [
            ### token1, token2, Liquidation_Markdown, Initial_Margin, Margin_Maintenance
            "ETH,WBTC,12000000000000000000,35000000000000000000,30000000000000000000",
            "ETH,LINK,7000000000000000000,20000000000000000000,15000000000000000000",
            "ETH,YFI,7000000000000000000,20000000000000000000,15000000000000000000",
            "ETH,AAVE,7000000000000000000,20000000000000000000,15000000000000000000",
            "ETH,UNI,7000000000000000000,20000000000000000000,15000000000000000000",
            "ETH,DAI,5000000000000000000,20000000000000000000,15000000000000000000",
            "ETH,USDC,5000000000000000000,20000000000000000000,15000000000000000000",
            "ETH,USDT,5000000000000000000,20000000000000000000,15000000000000000000",
            "ETH,MKR,10000000000000000000,30000000000000000000,25000000000000000000",
            "ETH,KNC,10000000000000000000,30000000000000000000,25000000000000000000",
            "ETH,BZRX,20000000000000000000,110000000000000000000,100000000000000000000",
            "DAI,USDC,2500000000000000000,5500000000000000000,5000000000000000000",
            "DAI,USDT,2500000000000000000,5500000000000000000,5000000000000000000",
            "USDC,USDT,2500000000000000000,5500000000000000000,5000000000000000000",
            "WBTC,DAI,12000000000000000000,35000000000000000000,30000000000000000000",
            "WBTC,USDC,12000000000000000000,35000000000000000000,30000000000000000000",
            "WBTC,USDT,12000000000000000000,35000000000000000000,30000000000000000000",
            "YFI,DAI,7000000000000000000,20000000000000000000,15000000000000000000",
            "YFI,USDC,7000000000000000000,20000000000000000000,15000000000000000000",
            "YFI,USDT,7000000000000000000,20000000000000000000,15000000000000000000",
            "LINK,DAI,7000000000000000000,20000000000000000000,15000000000000000000",
            "LINK,USDC,7000000000000000000,20000000000000000000,15000000000000000000",
            "LINK,USDT,7000000000000000000,20000000000000000000,15000000000000000000",
            "AAVE,DAI,7000000000000000000,20000000000000000000,15000000000000000000",
            "AAVE,USDC,7000000000000000000,20000000000000000000,15000000000000000000",
            "AAVE,USDT,7000000000000000000,20000000000000000000,15000000000000000000",
            "UNI,DAI,7000000000000000000,20000000000000000000,15000000000000000000",
            "UNI,USDC,7000000000000000000,20000000000000000000,15000000000000000000",
            "UNI,USDT,7000000000000000000,20000000000000000000,15000000000000000000",
            "MKR,DAI,10000000000000000000,30000000000000000000,25000000000000000000",
            "MKR,USDC,10000000000000000000,30000000000000000000,25000000000000000000",
            "MKR,USDT,10000000000000000000,30000000000000000000,25000000000000000000",
            "KNC,DAI,10000000000000000000,30000000000000000000,25000000000000000000",
            "KNC,USDC,10000000000000000000,30000000000000000000,25000000000000000000",
            "KNC,USDT,10000000000000000000,30000000000000000000,25000000000000000000",
            "BZRX,DAI,20000000000000000000,150000000000000000000,145000000000000000000",
            "BZRX,USDC,20000000000000000000,150000000000000000000,145000000000000000000",
            "BZRX,USDT,20000000000000000000,150000000000000000000,145000000000000000000",
            #"ERC20,ERC20,25000000000000000000,150000000000000000000,145000000000000000000",

            "WBTC,AAVE,25000000000000000000,150000000000000000000,145000000000000000000",
            "WBTC,UNI,25000000000000000000,150000000000000000000,145000000000000000000",
            "WBTC,KNC,25000000000000000000,150000000000000000000,145000000000000000000",
            "WBTC,MKR,25000000000000000000,150000000000000000000,145000000000000000000",
            "WBTC,BZRX,25000000000000000000,150000000000000000000,145000000000000000000",
            "WBTC,LINK,25000000000000000000,150000000000000000000,145000000000000000000",
            "WBTC,YFI,25000000000000000000,150000000000000000000,145000000000000000000",

            "AAVE,WBTC,25000000000000000000,150000000000000000000,145000000000000000000",
            "AAVE,KNC,25000000000000000000,150000000000000000000,145000000000000000000",
            "AAVE,MKR,25000000000000000000,150000000000000000000,145000000000000000000",
            "AAVE,BZRX,25000000000000000000,150000000000000000000,145000000000000000000",
            "AAVE,LINK,25000000000000000000,150000000000000000000,145000000000000000000",
            "AAVE,YFI,25000000000000000000,150000000000000000000,145000000000000000000",
            "AAVE,UNI,25000000000000000000,150000000000000000000,145000000000000000000",

            "UNI,WBTC,25000000000000000000,150000000000000000000,145000000000000000000",
            "UNI,KNC,25000000000000000000,150000000000000000000,145000000000000000000",
            "UNI,MKR,25000000000000000000,150000000000000000000,145000000000000000000",
            "UNI,BZRX,25000000000000000000,150000000000000000000,145000000000000000000",
            "UNI,LINK,25000000000000000000,150000000000000000000,145000000000000000000",
            "UNI,YFI,25000000000000000000,150000000000000000000,145000000000000000000",
            "UNI,AAVE,25000000000000000000,150000000000000000000,145000000000000000000",


            "KNC,AAVE,25000000000000000000,150000000000000000000,145000000000000000000",
            "KNC,UNI,25000000000000000000,150000000000000000000,145000000000000000000",
            "KNC,WBTC,25000000000000000000,150000000000000000000,145000000000000000000",
            "KNC,MKR,25000000000000000000,150000000000000000000,145000000000000000000",
            "KNC,BZRX,25000000000000000000,150000000000000000000,145000000000000000000",
            "KNC,LINK,25000000000000000000,150000000000000000000,145000000000000000000",
            "KNC,YFI,25000000000000000000,150000000000000000000,145000000000000000000",

            "MKR,AAVE,25000000000000000000,150000000000000000000,145000000000000000000",
            "MKR,UNI,25000000000000000000,150000000000000000000,145000000000000000000",
            "MKR,KNC,25000000000000000000,150000000000000000000,145000000000000000000",
            "MKR,WBTC,25000000000000000000,150000000000000000000,145000000000000000000",
            "MKR,BZRX,25000000000000000000,150000000000000000000,145000000000000000000",
            "MKR,LINK,25000000000000000000,150000000000000000000,145000000000000000000",
            "MKR,YFI,25000000000000000000,150000000000000000000,145000000000000000000",

            "BZRX,AAVE,25000000000000000000,150000000000000000000,145000000000000000000",
            "BZRX,UNI,25000000000000000000,150000000000000000000,145000000000000000000",
            "BZRX,KNC,25000000000000000000,150000000000000000000,145000000000000000000",
            "BZRX,MKR,25000000000000000000,150000000000000000000,145000000000000000000",
            "BZRX,WBTC,25000000000000000000,150000000000000000000,145000000000000000000",
            "BZRX,LINK,25000000000000000000,150000000000000000000,145000000000000000000",
            "BZRX,YFI,25000000000000000000,150000000000000000000,145000000000000000000",

            "LINK,AAVE,25000000000000000000,150000000000000000000,145000000000000000000",
            "LINK,UNI,25000000000000000000,150000000000000000000,145000000000000000000",
            "LINK,KNC,25000000000000000000,150000000000000000000,145000000000000000000",
            "LINK,MKR,25000000000000000000,150000000000000000000,145000000000000000000",
            "LINK,BZRX,25000000000000000000,150000000000000000000,145000000000000000000",
            "LINK,WBTC,25000000000000000000,150000000000000000000,145000000000000000000",
            "LINK,YFI,25000000000000000000,150000000000000000000,145000000000000000000",

            "YFI,AAVE,25000000000000000000,150000000000000000000,145000000000000000000",
            "YFI,UNI,25000000000000000000,150000000000000000000,145000000000000000000",
            "YFI,KNC,25000000000000000000,150000000000000000000,145000000000000000000",
            "YFI,MKR,25000000000000000000,150000000000000000000,145000000000000000000",
            "YFI,BZRX,25000000000000000000,150000000000000000000,145000000000000000000",
            "YFI,LINK,25000000000000000000,150000000000000000000,145000000000000000000",
            "YFI,WBTC,25000000000000000000,150000000000000000000,145000000000000000000",
        ]
        
    else:
        return


    '''function setLiquidationIncentivePercent(
        address[] calldata loanTokens,
        address[] calldata collateralTokens,
        uint256[] calldata amounts)
        external
        onlyOwner'''

    ### handle liquidation penalty
    '''loanTokensArr = []
    collateralTokensArr = []
    amountsArr = []
    
    for t in collateralTokens:
        for u in collateralTokens:
            if t == u:
                continue

            if not (t == "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984" or t == "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9" or u == "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984" or u == "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"):
                continue

            loanTokensArr.append(t)
            collateralTokensArr.append(u)
            amountsArr.append(7000000000000000000)

    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(loanTokensArr)
    pp.pprint(collateralTokensArr)
    pp.pprint(amountsArr)
    print(len(loanTokensArr),len(collateralTokensArr),len(amountsArr))

    bzx.setLiquidationIncentivePercent(loanTokensArr, collateralTokensArr, amountsArr, {"from": acct, "gas_price": 62e9 })
    
    return'''


    #sig = web3.sha3(text="setupLoanParams((bytes32,bool,address,address,address,uint256,uint256,uint256)[],bool)").hex()[:10]
    base_data = [
        b"0x0", ## id
        False, ## active
        str(acct), ## owner
        constants.ZERO_ADDRESS, ## loanToken
        constants.ZERO_ADDRESS, ## collateralToken
        Wei("20 ether"), ## minInitialMargin
        Wei("15 ether"), ## maintenanceMargin
        0 ## fixedLoanTerm
    ]
            ## itoken -> [ stuff ]
    params = {}
    for c in config:
        spl = c.split(',')

        base_data_copy = base_data.copy()
        base_data_copy[4] = tokens[spl[1]] ## collateralToken
        base_data_copy[5] = Wei(spl[3]) ## minInitialMargin
        base_data_copy[6] = Wei(spl[4]) ## maintenanceMargin
        
        if itokens[spl[0]] not in params:
            params[itokens[spl[0]]] = []
        params[itokens[spl[0]]].append(base_data_copy)

    #import pprint
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(params)

    excludes = [
        #"0x2ffa85f655752fb2acb210287c60b9ef335f5b6e",
    ]

    for loanPoolAddress in params:
        if loanPoolAddress != "0x0a625FceC657053Fe2D9FFFdeb1DBb4e412Cf8A8" and loanPoolAddress != "0x0cae8d91E0b1b7Bd00D906E990C3625b2c220db1":
            continue

        if loanPoolAddress in excludes:
            continue

        if thisNetwork == "development":
            raise Exception("Development netowrk unsupported")
            #loanToken = acct.deploy(LoanTokenLogicStandard)
            #loanTokenSettings = acct.deploy(LoanTokenSettingsLowerAdmin)
        elif thisNetwork == "kovan":
            loanToken = Contract.from_abi("loanToken", address=loanPoolAddress, abi=LoanTokenLogicStandard.abi, owner=acct)
            loanTokenSettings = Contract.from_abi("loanToken", address="0x96305EA01086424b5E822f0B6bD01197A7768518", abi=LoanTokenSettingsLowerAdmin.abi, owner=acct)
            #loanTokenSettings = acct.deploy(LoanTokenSettingsLowerAdmin)
        elif thisNetwork == "mainnet" or thisNetwork == "mainnet-fork":
            loanToken = Contract.from_abi("loanToken", address=loanPoolAddress, abi=LoanTokenLogicStandard.abi, owner=acct)
            loanTokenSettings = Contract.from_abi("loanToken", address="0xcd273a029fB6aaa89ca9A7101C5901b1f429d457", abi=LoanTokenSettingsLowerAdmin.abi, owner=acct)
            #loanTokenSettings = acct.deploy(LoanTokenSettingsLowerAdmin)
        else:
            return

        print("\nSetting up Torque for "+loanToken.address+".")

        calldata = loanTokenSettings.setupLoanParams.encode_input(params[loanPoolAddress], True)
        
        print(calldata)
        loanToken.updateSettings(loanTokenSettings.address, calldata, { "from": acct, "gas_price": 60e9 })