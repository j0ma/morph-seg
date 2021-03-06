import matplotlib.pyplot as plt
import pandas as pd

xlim = (0, 3)
output_file = "./f1-vs-alpha-all.png"
plot_title = "F1 vs. alpha"
columns = ("alpha", "f1")
pair_to_result_file = {
    "en-ne (token)": "./tuning/morfessor-baseline/no-dampening/en-ne/tuning-results",
    "en-si (token)": "./tuning/morfessor-baseline/no-dampening/en-si/tuning-results",
    "en-all (token)": "./tuning/morfessor-baseline/no-dampening/en-all/tuning-results",
    "en-ne (type)": "./tuning/morfessor-baseline/dampening/en-ne/tuning-results",
    "en-si (type)": "./tuning/morfessor-baseline/dampening/en-si/tuning-results",
    "en-all (type)": "./tuning/morfessor-baseline/dampening/en-all/tuning-results"
}

_all_results = []

for pair, f in pair_to_result_file.items():
    df = pd.read_csv(f, sep="\t", header=None)
    df.columns = columns
    df["pair"] = pair
    _all_results.append(df)

all_results = pd.concat(_all_results)
all_results.set_index("alpha").groupby("pair").f1.plot(
    title=plot_title, xlim=xlim, legend=True, figsize=(12,6)
)
plt.legend(loc="lower right")
plt.savefig(output_file)
