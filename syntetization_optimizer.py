import sys
import numpy

# Run optimize_one_sequence multiple times until all subsequences have a score below threshold
def opt(dna_sequence, threshold, min_length):

    threshold = float(threshold)
    min_length = int(min_length)

    cut_list = [{"dna_sequence" : dna_sequence, "score" : compute_sequence_score(dna_sequence)}]

    while is_cut_list_unoptimized(cut_list, threshold, min_length):
        new_cut_list = []
        for cut in cut_list:
            if cut["score"] > threshold and len(cut["dna_sequence"]) > min_length*2:
                cut = optimize_one_sequence(cut, min_length)
                new_cut_list.extend(cut)
            else:
                new_cut_list.append(cut)
        cut_list = new_cut_list[:]

    l = 0
    for cut in cut_list:
        print(cut["dna_sequence"] + " : " + str(cut["score"]))

# Optimize one sequence
def optimize_one_sequence(cut_to_optimize, min_length):

    dna_sequence = cut_to_optimize["dna_sequence"]
    cuts = []
    for x in range(min_length, len(dna_sequence)-(min_length-1)):
        left_score = compute_sequence_score(dna_sequence[:-x])
        right_score = compute_sequence_score(dna_sequence[-x:])

        cuts.append([{"dna_sequence" : dna_sequence[:-x], "score": left_score}, {"dna_sequence" : dna_sequence[-x:], "score": right_score}])

    # Find the best sequences
    best_cut = [{"dna_sequence" : "", "score" : 10000}, {"dna_sequence" : "", "score" : 10000}]
    for cut in cuts:
        worst_score_in_cut = max(cut[0]["score"], cut[1]["score"])
        if (worst_score_in_cut < best_cut[0]["score"]) or (worst_score_in_cut < best_cut[1]["score"]):
            best_cut = cut

    return best_cut



# Return False if all sequences' scores are below the threshold, True otherwise
def is_cut_list_unoptimized(cut_list, threshold, min_length):
    for cut in cut_list:
        if cut["score"] > threshold and len(cut["dna_sequence"]) > min_length*2:
            return True
    return False



# Compute the composite sequence score based on multiple parameters
def compute_sequence_score(dna_sequence):

    gc_content_score = compute_gc_content(dna_sequence)
    length_score = compute_length_score(dna_sequence)

    composite_score = gc_content_score * length_score

    print(gc_content_score)
    print(length_score)

    return composite_score


# Compute the length score of the sequence
def compute_length_score(dna_sequence):
    length_score = numpy.arctan( len(dna_sequence) / 200 )
    return length_score

# Compute the GC content of a dna sequence
def compute_gc_content(dna_sequence):
    gc_content = float(dna_sequence.count("G") + dna_sequence.count("C")) / float(len(dna_sequence)) * 100.
    gc_content_score = numpy.arctan( (gc_content - 50) / 10 ) * 20
    return gc_content_score
















opt(sys.argv[1], sys.argv[2], sys.argv[3])
