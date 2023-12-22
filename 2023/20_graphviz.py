
gr = []

with open("20.input") as f:
    gr.append("digraph mygraph {")
    for l in f:
        line = l.rstrip().split()
        i = line[0]
        if i.startswith(("%", "&")):
            gr.append(f"  {i[1:]} [label=\"{i}\"];")
            i = i[1:]
        for o in line[1:]:
            gr.append(f"  {i} -> {o}")

    gr.append("}")

for l in gr:
    print(l)
