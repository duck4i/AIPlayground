
# AIPlayground
AIPlayground is a testing CLI for various LLMs and models.

## Downloading models
You can download the model files into the ./model_data/ directory as git will safely ignore them as they are too large to be pushed.

Check out the [ModelRegistry](models/utils/modelRegistry.py) for more info.

# Using node based UI interface
`python3 main.py UI --help`
```
                                                                                                                                                
 Usage: main.py UI [OPTIONS] COMMAND [ARGS]...                                                                                                  
                                                                                                                                                
 Show UI                                                                                                                                        
                                                                                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ show                        Displays main window                                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
# Main usage
`python3 main.py --help`
```
                                                                                                                                                
 Usage: main.py [OPTIONS] COMMAND [ARGS]...                                                                                                     
                                                                                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                      │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                               │
│ --help                        Show this message and exit.                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ UI                                   Show UI                                                                                                 │
│ download                             Download the models                                                                                     │
│ llama                                LLaMA based models loader                                                                               │
│ llava                                LLaVA family of models                                                                                  │
│ version                              Prints CLI app version.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
## download
Useful utility for downloading the model files.

`python3 main.py version --help`
```
                                                                                                                                                
 Usage: main.py version [OPTIONS]                                                                                                               
                                                                                                                                                
 Prints CLI app version.                                                                                                                        
                                                                                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
## version
`python3 main.py version --help`
```
                                                                                                                                                
 Usage: main.py version [OPTIONS]                                                                                                               
                                                                                                                                                
 Prints CLI app version.                                                                                                                        
                                                                                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
# LLaMA usage
`python3 main.py llama --help`
```
                                                                                                                                                
 Usage: main.py llama [OPTIONS] COMMAND [ARGS]...                                                                                               
                                                                                                                                                
 LLaMA based models loader                                                                                                                      
                                                                                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ chat                Chat with LLAMA                                                                                                          │
│ run                 Single pass inference for LLAMA                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
## run
Raw output one shot inference for use on the CIs

`python3 main.py llama run --help`
```
                                                                                                                                                
 Usage: main.py llama run [OPTIONS] QUESTION                                                                                                    
                                                                                                                                                
 Single pass inference for LLAMA                                                                                                                
                                                                                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    question      TEXT  [default: None] [required]                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --model                      [None|OpenHermes|LLaMA|LLaVA|LLaVA13|BakLLaVA|Qwen25Sm  [default: KnownModel.none]                              │
│                              all|Hermes3Small|HermesVision|CodeLLaMA|LeetCodeWizard                                                          │
│                              ]                                                                                                               │
│ --verbose    --no-verbose                                                            [default: no-verbose]                                   │
│ --help                                                                               Show this message and exit.                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
## chat
Chat with LLaMA model

`python3 main.py llama chat --help`
```
                                                                                                                                                
 Usage: main.py llama chat [OPTIONS] QUESTION                                                                                                   
                                                                                                                                                
 Chat with LLAMA                                                                                                                                
                                                                                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    question      TEXT  [default: None] [required]                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --model                      [None|OpenHermes|LLaMA|LLaVA|LLaVA13|BakLLaVA|Qwen25Sm  [default: KnownModel.none]                              │
│                              all|Hermes3Small|HermesVision|CodeLLaMA|LeetCodeWizard                                                          │
│                              ]                                                                                                               │
│ --verbose    --no-verbose                                                            [default: no-verbose]                                   │
│ --help                                                                               Show this message and exit.                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
# LLaVA usage
`python3 main.py llava --help`
```
                                                                                                                                                
 Usage: main.py llava [OPTIONS] COMMAND [ARGS]...                                                                                               
                                                                                                                                                
 LLaVA family of models                                                                                                                         
                                                                                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ run               Run image inference for LLaVA                                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
## run
Raw output one shot inference for use on the CIs

`python3 main.py llava run --help`
```
                                                                                                                                                
 Usage: main.py llava run [OPTIONS] QUESTION                                                                                                    
                                                                                                                                                
 Run image inference for LLaVA                                                                                                                  
                                                                                                                                                
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    question      TEXT  [default: None] [required]                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --image                      TEXT                                                    [default: (dynamic)]                                    │
│ --model                      [None|OpenHermes|LLaMA|LLaVA|LLaVA13|BakLLaVA|Qwen25Sm  [default: KnownModel.none]                              │
│                              all|Hermes3Small|HermesVision|CodeLLaMA|LeetCodeWizard                                                          │
│                              ]                                                                                                               │
│ --verbose    --no-verbose                                                            [default: no-verbose]                                   │
│ --help                                                                               Show this message and exit.                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
