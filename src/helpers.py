def load_data(filename):
    '''opens a tab separated value file, and returns a tuple of lables, and a 2D tuple of data'''
    with open(filename, "r") as f:
        labels = None
        data = []
        for x, line in enumerate(f):
            if x == 0:
                labels = line[:-1].split("\t")[38:]
                labels[0] = "text"
                labels = tuple(labels)
            else:
                l = line[:-1].split("\t")
                text = " ".join(l[1:39]).replace("\"", "")
                data.append([text] + l[39:])
        return labels, data