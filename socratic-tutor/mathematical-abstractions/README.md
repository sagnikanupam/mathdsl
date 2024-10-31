# LEMMA: Bootstrapping High-Level Mathematical Reasoning with Learned Symbolic Abstractions

In this project, we want to learn mathematical abstractions from formal solutions generated algorithmically. These are some of the research questions we can explore:

1. Are there expressive patterns in these solutions? How should we represent and uncover them?
2. Can we recognize what operations these patterns carry out in terms of intuitive actions? For instance, "evaluating a large sub-expression" involves invoking evaluation operations often, whereas or "cancelling two equal terms" might involve repeatedly using commutativity and associativity until the terms are grouped together, then invoking a cancelation action.
3. If we rewrite long solutions in terms of the learned patterns, do they look natural?
4. Can these abstractions help us solve increasingly complex mathematical problems?

We explore questions 1-3 with a [dataset of ConPoLe solutions to equations](https://drive.google.com/drive/folders/1smRbVlZRNQi1OpiOhvWQ7fGA1dsgu0DI?usp=share_link).
Question 4 requires integrating the patterns in the learning algorithm, which was accomplished in [this fork](https://github.com/uranium11010/socratic-tutor/tree/2374d4a795cba3f9151ad95b68a81dac455c51d6)
of the original ConPoLe repository.

The paper can be found [here](https://arxiv.org/abs/2211.08671).

## Types of abstractions

`abstractions.py` contains interfaces for two kinds of abstraction that incorporate slightly different information in the abstraction:
* `tree_rel_pos`: Specifies a sequence of axioms and the relative positions of application in the expression tree.
* `ax_seq`: Specifies a sequence of axioms
They can be understood as "projection functions" that project a sequence of actions onto the space of abstractions by removing information
in the actions that we're not interested in.

## Abstraction algorithms

`compress.py` contains implementations of 7 algorithms for discovering abstractions from a data set of ConPoLe solutions.
Here, we only describe the two that made it to the final paper.
* `iap_logn`:
  1. Represent each solution as a sequence of actions (i.e., states are ignored.)
  2. Count the frequency of every possible abstraction in all solutions. Recall that an abstraction is just a contiguous sequence of actions in a solution,
but with all parameters removed (`ax_seq` abstractions) or with parameters replaced with information about relative positions of axiom application (`tree_rel_pos`
abstractions).
  3. Rank these abstractions by how much they decrease the objective (see paper).
  4. Save the top abstraction
  5. Create a rewrite rule (sequence of axioms -> new abstract action).
  6. Rewrite solutions using this new abstraction, and go back to Step 2.
  7. The loop ends when the top abstraction in Step 4 no longer decreases the objective.

* `iap_rand`: (for ablation studies) This is like `iap_logn`, except we don't greedily choose the top abstractions that decrease the objective the most.
Instead, abstractions are chosen at random.

## Running the code

All implementations use Python 3. There are no requirements additional to the Python standard library.

After cloning the repository, download the ConPoLe datset found [here](https://drive.google.com/drive/folders/1smRbVlZRNQi1OpiOhvWQ7fGA1dsgu0DI?usp=share_link).
The files in the Google Drive folder should be downloaded to a folder named `data/` under the root of this repository.


Running the following command discovers abstractions from a dataset of ConPoLe solutions:
```
compress.py [-h] [--config CONFIG_FILE] [--sol-data SOL_DATA] [--file FILE] [--sol-file SOL_FILE] [--use NUM_USE] [--store NUM_STORE]
                   [--num-ex-sol NUM_EX_SOL] [-s] [--iter ITER] [--thres THRES] [--top K] [--abs-type {ax_seq,dfs_idx_rel_pos,tree_rel_pos}]
                   [--compressor {iap,iap_rand,iap_heur,iap_ent,iap_logn,iap_trie,iap_dtrie}] [--peek] [-v] [--debug]
```
* `--config`: Configuration file. Allowed configurations include (but are not restricted to) the command line options below but with dashes replaced by underscores.
Configurations conflicting with options given through the command line override them.
* `--sol-data`: Path to data of solutions from which abstractions are found, if custom data were to be used.
* `--file`: Path to store the abstractions (should end in `.json` or `.pkl`)
* `--sol-file`: Path to store the abstracted solutions (should end in `.pkl`)
* `--use`: How many solutions to learn abstractions from (default: all in the file of solutions provided, i.e., 80k, or 8k if `-s` is specified)
* `--store`: How many abstracted solutions to store (default: all solutions abstracted from those in the file of solutions provided)
* `--num-ex-sol`: Number of example abstracted solutions to print to the terminal (default: `0`)
* `-s`: Specfying this option will use the small data set of 8k solutions for discovering abstractions, as opposed to the regular data set of 80k solutions
* `--iter`: Number of iterations of abstraction to perform (default: `1`)
* `--thres`: Threshold frequency (average number of occurrences per solution) for `iap` algorithm or theshold score for `iap_heur` algorithm.
* `--top K`: Take the top K abstractions. (*Note:* One should specify only one of `--top` and `--thres`.)
* `--abs-type {ax_seq,dfs_idx_rel_pos,tree_rel_pos}`: Type of abstraction
* `--compressor {iap,iap_rand,iap_heur,iap_ent,iap_logn,iap_trie,iap_dtrie}`: Type of algorithm for discovering abstractions. The final algorithm
presented in the paper is `iap_logn`.
* `--peek`: If using `ax_seq` abstractions with `IterAbsPairs`, specifying this option allows you to take a peek at the frequencies of different relative position for an abstraction.
* `-v` (verbose): Specifying this option will print the discovered abstractions along with their frequencies/scores and an example occurrence for each abstraction. Not specifying the option will only print the abstractions with their frequencies/scores.

Example configuration files are found under [`configs/`](configs/). Note that these examples store abstractions into directory
`abstractions/` and abstracted solutions into directory `abs_sols/`. These directories do not exist and therefore should be created
beforehand.

Here's an example that uses one of the provided configuration files.
```
mkdir abstractions abs_sols
python compress.py --config configs/iap_logn_tree_rel_pos_config.json
```
It uses the `iap_logn` algorithm with `tree_rel_pos` abstractions. This configuration file also shows how you can set the
maximum length of abstractions to be found by setting `max_abs_len`. It is 2 in this example configuration file.
(Simply remove this configuration in order not to limit the maximum length of abstractions.)

Here's an example that uses command line options. It discovers and saves the top 8 `tree_rel_pos` abstractions using the `iap` algorithm.
```
mkdir abstractions
python compress.py --file abstractions/IAP-80k-8len2-tree.json --top 8 --tree
```
