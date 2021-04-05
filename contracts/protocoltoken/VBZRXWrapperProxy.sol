// SPDX-License-Identifier: MIT

/**
 * Copyright 2017-2021, bZeroX, LLC. All Rights Reserved.
 * Licensed under the Apache License, Version 2.0.
 */


pragma solidity >=0.6.0 <0.8.0;

import "@openzeppelin/contracts/proxy/TransparentUpgradeableProxy.sol";


contract VBZRXWrapperProxy is TransparentUpgradeableProxy {

    constructor(address _logic, bytes memory _data) TransparentUpgradeableProxy(_logic, msg.sender, _data) {

    }
}
