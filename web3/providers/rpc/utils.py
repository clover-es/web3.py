import asyncio
from typing import Sequence, Type

import requests
from pydantic import BaseModel

from web3.types import RPCEndpoint


REQUEST_RETRY_ALLOWLIST = [
    "admin",
    "miner",
    "net",
    "txpool",
    "testing",
    "evm",
    "eth_protocolVersion",
    "eth_syncing",
    "eth_coinbase",
    "eth_mining",
    "eth_hashrate",
    "eth_chainId",
    "eth_gasPrice",
    "eth_accounts",
    "eth_blockNumber",
    "eth_getBalance",
    "eth_getStorageAt",
    "eth_getProof",
    "eth_getCode",
    "eth_getBlockByNumber",
    "eth_getBlockByHash",
    "eth_getBlockTransactionCountByNumber",
    "eth_getBlockTransactionCountByHash",
    "eth_getUncleCountByBlockNumber",
    "eth_getUncleCountByBlockHash",
    "eth_getTransactionByHash",
    "eth_getTransactionByBlockHashAndIndex",
    "eth_getTransactionByBlockNumberAndIndex",
    "eth_getTransactionReceipt",
    "eth_getTransactionCount",
    "eth_getRawTransactionByHash",
    "eth_call",
    "eth_estimateGas",
    "eth_createAccessList",
    "eth_maxPriorityFeePerGas",
    "eth_newBlockFilter",
    "eth_newPendingTransactionFilter",
    "eth_newFilter",
    "eth_getFilterChanges",
    "eth_getFilterLogs",
    "eth_getLogs",
    "eth_uninstallFilter",
    "eth_getCompilers",
    "eth_getWork",
    "eth_sign",
    "eth_signTypedData",
    "eth_sendRawTransaction",
    "personal_importRawKey",
    "personal_newAccount",
    "personal_listAccounts",
    "personal_listWallets",
    "personal_lockAccount",
    "personal_unlockAccount",
    "personal_ecRecover",
    "personal_sign",
    "personal_signTypedData",
]


def check_if_retry_on_failure(
    method: RPCEndpoint,
    allowlist: Sequence[str] = None,
) -> bool:
    if allowlist is None:
        allowlist = REQUEST_RETRY_ALLOWLIST

    if method in allowlist or method.split("_")[0]:
        return True
    else:
        return False


class ExceptionRetryConfiguration(BaseModel):
    errors: Sequence[Type[BaseException]] = (
        ConnectionError,
        requests.HTTPError,
        asyncio.Timeout,
        requests.Timeout,
    )
    retries: int = 5
    backoff_factor: float = 0.5
    method_allowlist: Sequence[str] = REQUEST_RETRY_ALLOWLIST