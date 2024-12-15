#   Generates readme file 

FILE=README.md

echo "" > $FILE # clear 

header(){
    echo "# "$1 >> $FILE
}

subheader(){
    echo "## "$1 >> $FILE
}

line(){
    echo $1"\n" >> $FILE
}

command(){
    echo '`'$1'`' >> $FILE
}

wrap(){
    echo '```' >> $FILE 
    echo "$@" >> $FILE
    echo '```' >> $FILE 
}

pair(){
    command "$1"
    wrap "$($1)"
}

#   Generate README 

header "AIPlayground"
line "AIPlayground is a testing CLI for various LLMs and models."

subheader "Downloading models"
line "You can download the model files into the ./model_data/ directory as git will safely ignore them as they are too large to be pushed."
line "Check out the [ModelRegistry](models/utils/modelRegistry.py) for more info."

#   UI
header "Using node based UI interface"
pair "python3 main.py UI --help"

#   MAIN
header "Main usage"
pair "python3 main.py --help"

subheader "download"
line "Useful utility for downloading the model files."
pair "python3 main.py version --help"

subheader "version"
pair "python3 main.py version --help"

#   LLAMA
header "LLaMA usage"
pair "python3 main.py llama --help"

subheader "run"
line "Raw output one shot inference for use on the CIs"
pair "python3 main.py llama run --help"

subheader "chat"
line "Chat with LLaMA model"
pair "python3 main.py llama chat --help"

#   LLAVA
header "LLaVA usage"
pair "python3 main.py llava --help"

subheader "run"
line "Raw output one shot inference for use on the CIs"
pair "python3 main.py llava run --help"