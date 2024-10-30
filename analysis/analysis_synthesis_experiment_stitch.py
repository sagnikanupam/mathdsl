import sys
sys.path.append("../")
import os

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from src.analysis_utilities import SynthesisExperimentAnalyzer
from src.config_builder import ExperimentType

sns.set_theme(style="whitegrid", font_scale=1.25, rc={'figure.figsize':(12, 8)})
EXPERIMENT_NAME = "mathai_paper/"
DOMAIN = "math"
COMPUTE_LIKELIHOODS = True

FIGURES_DIR = os.path.join("figures", EXPERIMENT_NAME)
FIGURES_DOMAIN_DIR = os.path.join("figures", EXPERIMENT_NAME, DOMAIN)
os.makedirs(FIGURES_DOMAIN_DIR, exist_ok=True)
analyzer = SynthesisExperimentAnalyzer(experiment_name=EXPERIMENT_NAME, experiment_types=["dreamcoder"], allow_incomplete_results=True, domains = ['math', 'lemma', 'conpole'], compute_likelihoods=COMPUTE_LIKELIHOODS, batch_size = 95, seeds = [111,],)
df_runtime = analyzer.get_runtime_metrics()
print(df_runtime)
print(df_runtime.groupby(["domain", "experiment_type", "model_type", "model_fn", "split"]).time_elapsed.agg("mean"))
bp = sns.barplot(data=df_runtime.query("model_fn == 'infer_programs_for_tasks'"), y="experiment_type", x="time_elapsed", hue="split")
bp.figure.savefig("mathai_paper_mathdsl_lemma_bar_plot.png")
df_results = analyzer.get_synthesis_summary()
df_results["domain"].mask(df_results["domain"] == "math", "MathDSL", inplace=True)
df_results["domain"].mask(df_results["domain"] == "lemma", "LemmaDSL", inplace=True)
df_results["domain"].mask(df_results["domain"] == "conpole", "ConPoLeDSL", inplace=True)
print(df_results)
rel = sns.relplot(data=df_results, kind="line", col="split", x="iteration", y="percent_solved", hue="domain", markers=True, col_order=["train", "test"],)
rel.savefig('mathai_paper_mathdsl_lemma_rel_plot.png')
