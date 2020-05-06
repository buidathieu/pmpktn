import subprocess, os

def start_print_job(filepath, delete=True):
    subprocess.run(['gs', '-sPapersize=A5',
                    '-sDEVICE=mswinpr2',
                    '-sOutputFile=%printer%Canon LBP2900',
                    '-dBATCH', '-dNOPAUSE',
                    filepath])
    if delete:
        os.remove(filepath)
