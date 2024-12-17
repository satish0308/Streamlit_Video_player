import subprocess

# Command structure to run Streamlit directly
# cmd = [
#     "streamlit",  # Directly call streamlit if it's in the PATH
#     "run", 
#     "d:/Upwork/4.stramlitapptobrowsethroughvideos_local/main.py"
# ]

cmd = [
    "C:/Users/hirem/anaconda3/Scripts/streamlit.exe",  # Full path to streamlit.exe
    "run", 
    "d:/Upwork/4.stramlitapptobrowsethroughvideos_local/main.py",
    "--server.port", "8508"
]

# Run the command
subprocess.Popen(cmd, shell=True)
