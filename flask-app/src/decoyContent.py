import pathlib

def getTimestamps(filename):
    fname = pathlib.Path(filename)
    stats = fname.stat()
    if not fname.exists(): #file deleted
        return []
    return(stats.st_ctime, stats.st_mtime, stats.st_atime)

def checkTimestamps(filename,create,modify,access):
    stats=getTimestamps(filename)
    # print(stats)
    if len(stats)==0:
        return False # archivo borrado
    (ctime, mtime, atime) = stats
    if float(create) != float(ctime):
        return False #la fecha de creación es incorrecta
    elif float(modify) != float(mtime):
        return False # la fecha de modificacion es incorrecta
    elif float(access) != float(atime):
        return False # la fecha de acceso es incorrecta
    return True

def checkDecoyFiles():
    with open("decoys.txt","r") as f:
        for line in f:
            vals = line.rstrip().split(",")
            if not checkTimestamps(vals[0], vals[1], vals[2], vals[3]):
                print(f"{vals[0]} ha sido accedido de alguna forma")
            else:
                print(f"{vals[0]}: Todo bien! :)")

checkDecoyFiles()