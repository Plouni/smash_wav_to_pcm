import os
import sys
        

def system_command(command, debug=False):
    """
    Run command. Replace '/' with '\\' for Windows
    
    :command: command to run
    """

    if sys.platform.startswith('win') and not debug:
        # Set stdout to NUL so that it doesn't print on console
        os.system(command.replace('/', '\\\\') + ' > NUL')
    else:
        os.system(command)


def get_folder_final_info(output_path, folder_final):
    """
    :output_path: output path where .pcm will be stored
    :folder_final: name of output folder
    :return: folder_final with '/' at the end and folder_final with '-' at the end as a prefix for output .pcm 
    """
    if len(folder_final)==0:
        return output_path, folder_final
     
    if  not os.path.exists(output_path + folder_final) or not os.path.isdir(output_path + folder_final):
        os.mkdir(output_path + folder_final)
    return output_path + folder_final + '/', folder_final + '-'