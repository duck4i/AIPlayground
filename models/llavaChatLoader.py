from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler
from models import ModelLoader, LLMResponse
from utils import log

class LlavaModelLoader(ModelLoader):
    def __init__(self,  contextWindowSize: int = 2048, verbose: bool = False, gpu_layers: int = 30):
        self.llm = None
        self.gpu_layers = gpu_layers
        self.verbose = verbose
        self.contextSize = contextWindowSize

    def load(self, modelPath: str, clipModelPath: str) -> bool:
        self.chat_handler = Llava15ChatHandler(clip_model_path=clipModelPath, verbose=self.verbose)
        self.llm = Llama(model_path=modelPath, chat_handler=self.chat_handler, logits_all=True, chat_format="llava-1-5", verbose=self.verbose, n_ctx=self.contextSize, n_gpu_layers=self.gpu_layers)
        return self.llm is not None

    def model(self) -> Llama:
        return self.llm

class LLavaChatSession():
    default_system_message = "Below is an instruction that describes a task. Write a response that appropriately completes the request."

    def __init__(self, model_loader: LlavaModelLoader, tokens: int = 512, streamFunction = None):
        self.llm = model_loader
        self.tokens = tokens
        self.streamFunc = streamFunction
        self._canceled = False

    #   Performs better in terms of getting a short and correct answer. But its dry.
    def answer(self, question: str, image_content_base64: str, system_message: str = default_system_message) -> LLMResponse:
        try:
            stream = self.llm.model().create_chat_completion(
            messages = [
                {"role": "system", "content": system_message},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_content_base64}"}},
                        {"type" : "text", "text": {question}}
                    ]
                }
            ],
            max_tokens=self.tokens,
            )

            completeText = ""
            completeTextUnpatched = "" # this is needed because what user sees and what AI sees is different, user doesn't care about "### Instruction:" but the AI does
            if self.streamFunc: # chat mode - stream
                for output in stream:
                    if self._canceled:
                        log.info(f"Task canceled. {self}")
                        break
                    delta = output["choices"][0]["delta"]
                    if "content" in delta.keys():
                        cnt = delta["content"]
                        completeText += cnt
                        completeTextUnpatched += cnt
                        self.streamFunc(cnt)
            else:
                completeText = stream["choices"][0]["message"]["content"]

            return LLMResponse(stream, completeText.strip())
        except Exception as e:
            return LLMResponse(None, f"{e}")
        
    def answer_with_file(self, question: str, image_file_path: str) -> LLMResponse:
        import base64
        with open(image_file_path, "rb") as img_file:
            base64_data = base64.b64encode(img_file.read()).decode('utf-8')
            return self.answer(question, base64_data)
    
    def cancel(self) -> None:
        self._canceled = True
