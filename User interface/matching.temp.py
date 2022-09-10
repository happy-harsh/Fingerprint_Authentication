
import skelaton_process
import fpcopy


def matching_finger():
    filename = skelaton_process.finger(upload_file())
    fpcopy.finger(filename)
