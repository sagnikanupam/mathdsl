# MathDSL:  A Domain-Specific Language for Concise Mathematical Solutions Via Program Synthesis ([arXiv:2409.17490](https://arxiv.org/abs/2409.17490)) 

This repository is a fork of [LILO](https://github.com/gabegrand/lilo), and uses the DreamCoder+Stitch framework described in the LILO paper LILO: Learning Interpretable Libraries by Compressing and Documenting Code ([arxiv/2310.19791](https://arxiv.org/abs/arxiv/2310.19791)). The baseline models presented in this paper utilize the [ConPoLe](https://github.com/gpoesia/socratic-tutor) and [Lemma](https://github.com/gpoesia/socratic-tutor/tree/abstract) codebases. 

## Installation

This codebase has only been tested on Linux systems. To run LILO, you'll need an environment with:

- Python 3.7 (for backwards compatibility with DreamCoder)
- OCaml (required by DreamCoder)
- Rust (required by Stitch)

The easiest way to get this environment is to use the Docker container provided in this repository. First, install [Docker](https://docs.docker.com/get-docker/) on your local machine. Then, you can clone the repo and build the Docker container locally:

```
git clone --recurse-submodules https://github.com/gabegrand/lilo
cd lilo
docker build -t mathdsl .
docker run --name mathdsl-instance --shm-size="2gb" -it mathdsl bash
```

To run the ConPoLe and Lemma baselines, you'll need to first install [Rust](https://rustup.rs/) Then execute the following commands from the root of the repository. 

```
cd socratic-tutor
pip install -r requirements.txt
cd commoncore
cargo build --release
cd ..
ln -s commoncore/target/release/libcommoncore.so ./commoncore.so
```

Then, for generating `socratic-tutor/outputs/generatedConpoleSolutions.csv`, `cd` into `socratic-tutor` and execute:

```
python environment.py --rust --data-eval --q-function best-config/conpole/99.pt --domain equations-ct --dataset-filepath data/conpoleDatasetPrefix.csv --dataset-output outputs/generatedConpoleSolutions.csv
```

Similarly, for generating `socratic-tutor/outputs/generatedLemmaSolutions.csv`, `cd` into `socratic-tutor` and execute:

```
python environment.py --rust --data-eval --abstract best-config/lemma/A2.pkl,tree_rel_pos --q-function best-config/lemma/3-29.pt --domain equations-ct --dataset-filepath data/conpoleDatasetPrefix.csv --dataset-output outputs/generatedLemmaSolutions.csv
```

## DreamCoder + Stitch + DSL Experiments

MathDSL Experiment

```
python run_iterative_experiment.py  --experiment_name mathai_paper --experiment_type dreamcoder --domain math --encoder math --iterations 25 --global_batch_sizes 95 --enumeration_timeout 1000 --recognition_train_steps 10000 --random_seeds 111 --verbose
```

ConPoLeDSL Experiment

```
python run_iterative_experiment.py  --experiment_name mathai_paper --experiment_type dreamcoder --domain conpole --encoder conpole --iterations 25 --global_batch_sizes 95 --enumeration_timeout 1000 --recognition_train_steps 10000 --random_seeds 111 --verbose
```

LemmaDSL Experiment

```
python run_iterative_experiment.py  --experiment_name mathai_paper --experiment_type dreamcoder --domain lemma --encoder lemma --iterations 25 --global_batch_sizes 95 --enumeration_timeout 1000 --recognition_train_steps 10000 --random_seeds 111 --verbose
```

The number of tasks solved in each iteration can be discovered under `experiments_iterative/outputs/math_ai_paper/domains/<domain_name>/<iteration_number>/frontiers.json`. The graph comparing the performance of the three DreamCoder experiments using MathDSL, ConPoLeDSL, and LemmaDSL (Figure 3 in the paper) can be compared by executing `python analysis/analysis_synthesis_experiment_stitch.py`. The resulting image is stored in `mathai_paper_mathdsl_lemma_rel_plot.png`.

## C-Score Generation 

For producing C-Scores of an experiment run (with a ConPoLe baseline), replace `meta_analysis/MathDomainAnalysis/dreamcoder_stitch_<dsl_name>.json` with the appropriate `frontiers.json` file generated during the experiment from `experiments_iterative`, and then execute `python math_domain_analysis.py` after setting `EXP_NAME` to the appropriate experiment name (a full list of experiment names is described in a comment [here](https://github.com/sagnikanupam/mathdsl/blob/777bd11462d1579ac7a45dbe18f17263498a0282/math_domain_analysis.py#L457)). For example, a file generated using MathDSL should be saved as `meta_analysis/MathDomainAnalysis/dreamcoder_stitch_mathdsl.json`. The files currently in the repo with the names `meta_analysis/MathDomainAnalysis/dreamcoder_stitch_mathdsl.json`, `meta_analysis/MathDomainAnalysis/dreamcoder_stitch_conpoledsl.json`,  `meta_analysis/MathDomainAnalysis/dreamcoder_stitch_lemmadsl.json` are the `frontiers.json` files from iteration 24 (the final iteration, iterations are numbered 0-24) of the experiments using MathDSL, ConPoLeDSL, and LemmaDSL respectively. To generate teh table of results with DreamCoder permitted to have duplicate steps in the solution (Table 1), set `NO_DUPLICATES` to `False`, and set it to `True` to generate the table of results where DreamCoder solutions contain only unique steps (Table 4).

Our DreamCoder experiments are available in JSON format in `experiments_iterative/outputs/mathai_paper/domains/<domain_name>`. Our prefix-form dataset is available under `meta_analysis/MathDomainAnalysis/conpoleDatasetPrefix.csv`. The results of passing our dataset to the ConPoLe PyTorch models is available at `socratic-tutor/outputs/generatedConpoleSolutions.csv` and the results of passing the dataset to the ConPoLe model equipped with Lemma abstractions is available at `socratic-tutor/outputs/generatedLemmaSolutions.csv`.

# Citations

If you use MathDSL, please cite:

```
@inproceedings{anupam24mathdsl,
  title={MathDSL: A Domain-Specific Language for Concise Mathematical Solutions Via Program Synthesis},
  author={Anupam, Sagnik and Bowers, Maddy and Reyes, Omar Costilla and Solar-Lezama, Armando},
  booktitle={The 4th Workshop on Mathematical Reasoning and AI at NeurIPS'24}
}
```

If you use this codebase implementing MathDSL alongside DreamCoder + Stitch, please also cite:

```
@article{grand2023lilo,
  title={{LILO}: Learning Interpretable Libraries by Compressing and Documenting Code},
  author={Gabriel Grand and Lionel Wong and Matthew Bowers and Theo X. Olausson and Muxin Liu and Joshua B. Tenenbaum and Jacob Andreas},
  journal={arXiv preprint arXiv:2310.19791},
  year={2023}
}
```

If you use the ConPoLe and Lemma baselines, please also cite:

```
@inproceedings{poesia2021contrastive,
  author = {Poesia, Gabriel and Dong, WenXin and Goodman, Noah},
  booktitle = {Advances in Neural Information Processing Systems (NeurIPS)},
  title = {Contrastive Reinforcement Learning of Symbolic Reasoning Domains},
  website = {https://arxiv.org/abs/2106.09146},
  year = {2021}
} 
```

```
@article{li2022lemma,
  title={Lemma: Bootstrapping high-level mathematical reasoning with learned symbolic abstractions},
  author={Li, Zhening and Poesia, Gabriel and Costilla-Reyes, Omar and Goodman, Noah and Solar-Lezama, Armando},
  booktitle = {NeurIPS'22 MATH-AI Workshop},
  journal={arXiv preprint arXiv:2211.08671},
  year={2022}
}
```

# Acknowledgements

MathDSL is a domain-specific application of the LILO codebase, which inherits from the [LAPS](github.com/CatherineWong/laps) codebase. We gratefully acknowledge Gabriel Grand and Lionel Wong for the use of their codebases as a foundation. The `socratic-tutor` folder is derived from the [ConPoLe](https://github.com/gpoesia/socratic-tutor) and [Lemma](https://github.com/gpoesia/socratic-tutor/tree/abstract) codebases, for which we would like to acknowledge the support of Gabriel Poesia and Zhening Li.

# License

MIT License Copyright (c) 2024 Sagnik Anupam, Maddy Bowers

MIT License Copyright (c) 2023 Gabriel Grand

`socratic-tutor` reproduced here with permission from Gabriel Poesia and Zhening Li

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
