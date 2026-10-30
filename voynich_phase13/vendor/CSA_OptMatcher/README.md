# CSA_OptMatcher

This code is devoted to help paleographers and linguists in the decipherment of lost script/languages. Please, refer to the cited paper for a complete explanation of the general goals, configurations, parameters and datasets.

This package requires the installation of another package I developed, namely [EditDistanceWild](https://github.com/ftamburin/EditDistanceWild).

## For repeating the experiments on the paper:
- First you can train the system with, for example
```
    python3 CSA_OptMatcher.py -c data/linear_b-greek.cog -f data/FixNULL -n 2 -m 1 -d cuda 1> LOG 2> LOG_E
```
monitoring the training by looking at the *stderr* log 'LOG_E'. Please note that, on some systems, to guarantee a real multiprocess run you have to set "OPENBLAS_MAIN_FREE=1" in your shell environment.

- The program prints on *stdout* all the tested solutions by the CSA process, thus, sorting them using the file 'LOG' we can get the lowest-energy solution and test it by the command
```
    python3 CSA_OptMatcher.py -c data/linear_b-greek.cog -f data/FixNULL -n 2 -m 1 -d cuda -o "[34, 44, ..., 20, 72]"
```

Tested on:
- python 3.7
- pytorch 1.10.2

If you use this code or datasets please cite:
```
@ARTICLE{10.3389/frai.2025.1581129,
  AUTHOR={Tamburini, Fabio },
  TITLE={On automatic decipherment of lost ancient scripts relying on combinatorial optimisation and coupled simulated annealing},
  JOURNAL={Frontiers in Artificial Intelligence},
  VOLUME={Volume 8 - 2025},
  YEAR={2025},
  URL={https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1581129},
  DOI={10.3389/frai.2025.1581129},
  ISSN={2624-8212},
}
```
In case of problems contact me at <fabio.tamburini@unibo.it>.
