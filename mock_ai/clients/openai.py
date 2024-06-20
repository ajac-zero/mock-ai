from random import randint
from time import time
from typing import Iterable, Union
from uuid import uuid4

from mock_ai.bottled_responses import chat_completions
from mock_ai.types.openai.completions import (
    ChatCompletion,
    ChatCompletionMessage,
    Choice,
    CompletionUsage,
)
from mock_ai.types.openai.messages import ChatCompletionMessageParam
from mock_ai.types.openai.stream import (
    ChatCompletionChunk,
    ChoiceDelta,
    Stream,
)
from mock_ai.types.openai.stream import (
    Choice as StreamChoice,
)


class OpenAI:
    @property
    def chat(self):
        return self

    @property
    def completions(self):
        return self

    def create(
        self,
        model: str,
        messages: Iterable[ChatCompletionMessageParam],
        stream: bool = False,
    ) -> Union[ChatCompletion, Stream[ChatCompletionChunk]]:
        number = randint(0, len(chat_completions) - 1)
        content = chat_completions[number]

        prompt_tokens = 0
        completion_tokens = len(content)

        match stream:
            case False:
                completion = ChatCompletion(
                    id=uuid4().hex,
                    choices=[
                        Choice(
                            finish_reason="stop",
                            index=0,
                            logprobs=None,
                            message=ChatCompletionMessage(
                                content=content, role="assistant", tool_calls=None
                            ),
                        )
                    ],
                    created=int(time()),
                    model=model,
                    object="chat.completion",
                    service_tier="default",
                    system_fingerprint="mock",
                    usage=CompletionUsage(
                        completion_tokens=completion_tokens,
                        prompt_tokens=prompt_tokens,
                        total_tokens=prompt_tokens + completion_tokens,
                    ),
                )

                return completion

            case True:
                id = uuid4().hex
                created = int(time())

                for char in content:
                    chunk = ChatCompletionChunk(
                        id=id,
                        choices=[
                            StreamChoice(
                                delta=ChoiceDelta(
                                    content=char, role="assistant", tool_calls=None
                                ),
                                finish_reason="stop",
                                index=0,
                            )
                        ],
                        created=created,
                        model=model,
                        object="chat.completion.chunk",
                        service_tier="default",
                        system_fingerprint="mock",
                        usage=None,
                    )

                    yield chunk
