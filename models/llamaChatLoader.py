from llama_cpp import Llama
from models import LLMResponse, ModelLoader
from utils import log

class LlamaModelLoader(ModelLoader):
    def __init__(self,  contextWindowSize: int = 9182, verbose: bool = False, gpu_layers: int = 30):
        self.llm = None
        self.gpu_layers = gpu_layers
        self.verbose = verbose
        self.contextSize = contextWindowSize

    def load(self, modelPath) -> bool:
        self.llm = Llama(model_path=modelPath, verbose=self.verbose, n_ctx=self.contextSize, n_gpu_layers=self.gpu_layers)
        return self.llm is not None

    def model(self) -> Llama:
        return self.llm

class LLamaChatSession():
    default_system_message = "Below is an instruction that describes a task. Write a response that appropriately completes the request."

    def __init__(self, model_loader: LlamaModelLoader, tokens: int = 32768, streamFunction = None, system_message: str = default_system_message):
        self.llm = model_loader
        self.tokens = tokens
        self.streamFunc = streamFunction
        self.clear_history(system_message)
        self.stop_chars = ["Q:", "[INST]", "[/INST]"]  # Stop generating just before the model would generate a new question
        self._canceled = False 

    #   Performs better in terms of getting a short and correct answer. But its dry.
    def answer(self, question: str) -> LLMResponse:
        try:
            msgs = self._create_question(question)

            stream = self.llm.model().create_chat_completion(
                messages = msgs,
                max_tokens= self.tokens,
                stop=self.stop_chars,
                stream=self.streamFunc != None
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
                        text = self._apply_patches(cnt)
                        completeText += text
                        completeTextUnpatched += cnt
                        self.streamFunc(text)
            else:
                completeText = self._apply_patches(stream["choices"][0]["message"]["content"])

            # cache the respon part into the history
            self.history.append(self._create_responsePart(completeTextUnpatched))

            return LLMResponse(stream, completeText.strip())
        except Exception as e:
            return LLMResponse(None, f"{e}")
    
    def cancel(self) -> None:
        self._canceled = True

    def clear_history(self, system: str = default_system_message) -> None:
        self.history = [{ "role": "system", "content": system}]
    
    def _create_question(self, question: str):
        obj = []
        
        userPart = self._create_user_part(question)
        aiPart = self._create_responsePart("")

        obj = self.history + [
            userPart, 
            aiPart
        ]
        
        self.history.append(userPart)
        #self.history.append(aiPart) <-- the history part is injected upon the answer response

        return obj
    
    def _create_user_part(self, question: str):
        return {
            "role": "user",
            "content": f"### Instruction:{question}"
        }

    def _create_responsePart(self, value: str):
        return {
            "role": "assistant",
            "content": f"### Response:{value}"
        }

    def _apply_patches(self, value: str) -> str:
        # llama 7b 4bit
        tmp = value.replace("### Instruction:", "")
        tmp = tmp.replace("### Response:", "")
        # open hermes model 
        tmp = tmp.replace("<0x0A>", "\n")
        # general
        tmp = tmp.replace("###", "")
        return tmp