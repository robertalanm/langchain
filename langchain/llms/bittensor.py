import bittensor as bt

import asyncio

from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any


class BittensorLLM(LLM):
    """Wrapper around Bittensor Prompting Subnetwork. 
This Python file implements the BittensorLLM class, a wrapper around the Bittensor Prompting Subnetwork for easy integration into language models. The class provides a query method to receive responses from the subnetwork for a given user message and an implementation of the _call method to return the best response. The class can be initialized with various parameters such as the wallet name and chain endpoint.
    
    Example:
        .. code-block:: python

            from langchain.llms import BittensorLLM
            btllm = BittensorLLM(wallet_name="text-davinci-003")
    """

    # config: 'bt.config' = _config()
    netuid: int = 21
    chain_endpoint: str = 'wss://test.finney.opentensor.ai'
    network: str = "finney"
    wallet_name: str = 'default'
    hotkey_name: str = 'default'
    wallet: 'bt.wallet' = None
    subtensor: 'bt.subtensor' = None
    metagraph: 'bt.metagraph' = None
    timeout: int = 12

    def __init__(self, **data):
        super().__init__(**data)
        self.wallet = bt.wallet( name=self.wallet_name, hotkey=self.hotkey_name )
        self.subtensor = bt.subtensor ( chain_endpoint=self.chain_endpoint, network=self.network )
        self.metagraph = self.subtensor.metagraph(self.netuid) if self.metagraph == None else self.metagraph

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"wallet_name": self.wallet_name, "hotkey_name": self.hotkey_name}

    @property
    def _llm_type(self) -> str:
        return "BittensorLLM"

    
    async def query(self, user_message: str):
        try:
            coroutines = []
            for uid in self.metagraph.uids.tolist():
                coroutines.append(self.call_uid(uid, user_message))

            all_responses = await asyncio.gather(*coroutines)
            return all_responses
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            return ['error']
        
    async def call_uid(self, uid: int, user_message: str) -> str:
        endpoint = self.metagraph.endpoint_objs[uid]
        module = bt.text_prompting(endpoint=endpoint, wallet=self.wallet)
        response = await module.async_forward(roles=['user'], messages=[user_message], timeout=self.timeout)
        return response.response

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Call the LLM with the given prompt and stop tokens."""

        responses_per_uid = asyncio.run(self.query(prompt))
        # get rid of all None responses
        responses_per_uid = list(filter(None, responses_per_uid))
        # print(responses_per_uid)

        # TODO: sort responses by score
        # return the first response
        return responses_per_uid[0]

    