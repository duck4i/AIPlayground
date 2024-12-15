from models import KnownModel, ModelFamily, ModelInfo

class ModelRegistry():

    models = {
        #   LLaMA
        KnownModel.llama7b : ModelInfo
        (
            "LLaMA v2 7B 4bit",
            ModelFamily.llama, 
            ["https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf?download=true"]
        ),
        KnownModel.openHermes : ModelInfo
        (
            "OpenHermes 2.5 Neural Chat 7b 4bit",
            ModelFamily.mistral, 
            ["https://huggingface.co/TheBloke/OpenHermes-2.5-neural-chat-7B-v3-2-7B-GGUF/resolve/main/openhermes-2.5-neural-chat-7b-v3-2-7b.Q4_K_M.gguf?download=true"]
        ),
        
        #   LLaVA
        KnownModel.llava1pt57b : ModelInfo
        (
            "LLaVA 1.5 7B 4bit",
            ModelFamily.llava,
            [
                "https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/ggml-model-q5_k.gguf",
                "https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/mmproj-model-f16.gguf"
            ]
        ),
        KnownModel.llava1pt513b : ModelInfo
        (
            "LLaVA 1.5. 13B 4bit",
            ModelFamily.llava,
            [
                "https://huggingface.co/mys/ggml_llava-v1.5-13b/resolve/main/ggml-model-q4_k.gguf",
                "https://huggingface.co/mys/ggml_llava-v1.5-13b/resolve/main/mmproj-model-f16.gguf"
            ]
        ),
        KnownModel.bakllava : ModelInfo
        (
            "BaKLLaVA 1 4bit",
            ModelFamily.llava,
            [
                "https://huggingface.co/AI-Engine/BakLLaVA1-MistralLLaVA-7B-GGUF/resolve/main/BakLLaVA1-MistralLLaVA-7B.q5_K_M.gguf",
                "https://huggingface.co/AI-Engine/BakLLaVA1-MistralLLaVA-7B-GGUF/resolve/main/BakLLaVA1-clip-mmproj-model-f16.gguf"
            ]
        ),

        KnownModel.qwen2pt5500m: ModelInfo
        (
            "Qwen 2.5 500m",
            ModelFamily.qwen,
            [
                "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-fp16.gguf?download=true"
            ]
        ),

        KnownModel.hermes33pt5: ModelInfo
        (
            "Hermes 3 3.5B",
            ModelFamily.llama,
            [
                "https://huggingface.co/NousResearch/Hermes-3-Llama-3.2-3B-GGUF/resolve/main/Hermes-3-Llama-3.2-3B.Q6_K.gguf?download=true"
            ]
        ),

        #   experimental / incomplete
        #   https://huggingface.co/billborkowski/llava-NousResearch_Nous-Hermes-2-Vision-GGUF
        KnownModel.hermesVision : ModelInfo
        (
            "Hermes Vision OpenNous 2",
            ModelFamily.mistral,
            [
                "https://huggingface.co/billborkowski/llava-NousResearch_Nous-Hermes-2-Vision-GGUF/resolve/main/NousResearch_Nous-Hermes-2-Vision-GGUF_Q4_0.gguf",
                "https://huggingface.co/billborkowski/llava-NousResearch_Nous-Hermes-2-Vision-GGUF/resolve/main/mmproj-model-f16.gguf"
            ]
        ),

        #   experimental / incomplete
        KnownModel.codeLlama7b: ModelInfo
        (
            "CodeLLaMA 7b 4bit",
            ModelFamily.llama, 
            ["https://huggingface.co/TheBloke/CodeLlama-7B-GGUF/resolve/main/codellama-7b.Q4_K_M.gguf"]
        ),

        #   experimental / incomplete
        KnownModel.leetCode7b: ModelInfo
        (
            "LeetCodeWizzard v1.1 7B 4bit",
            ModelFamily.none,
            ["https://huggingface.co/Nan-Do/LeetCodeWizard_7B_V1.1-GGUF/resolve/main/LeetCodeWizard_7B_V1.1.Q4_1.gguf?download=true"]
        )
    }