import matplotlib.pyplot as plt
import pandas as pd

xlim = (0, 11)
output_file = "./f1-vs-alpha-combined.png"
plot_title = "F1 vs. alpha, by language-pair condition"
columns = ("alpha", "f1")
pair_to_result_file = {
    "en-ne": "./tuning/morfessor-baseline/en-ne/tuning-results",
    "en-si": "./tuning/morfessor-baseline/en-si/tuning-results",
    "en-all": "./tuning/morfessor-baseline/en-all/tuning-results",
}

_all_results = []

for pair, f in pair_to_result_file.items():
    df = pd.read_csv(f, sep="\t", header=None)
    df.columns = columns
    df["pair"] = pair
    _all_results.append(df)

all_results = pd.concat(_all_results)
all_results.set_index("alpha").groupby("pair").f1.plot(
    title=plot_title, xlim=xlim, legend=True
)

plt.savefig(output_file)
