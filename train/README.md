# Train Opus-MT models

This folder includes make targets for training NMT models using MarianNMT and OPUS data. More details are given in the [Makefile](Makefile) but documentation needs to be improved. Also, the targets require a specific environment and right now only work well on the CSC HPC cluster in Finland.


## Structure

Essential files for making new models:

* `Makefile`: top-level makefile
* `Makefile.env`: system-specific environment (now based on CSC machines)
* `Makefile.config`: essential model configuration
* `Makefile.data`: data pre-processing tasks
* `Makefile.doclevel`: experimental document-level models
* `Makefile.tasks`: tasks for training specific models and other things (this frequently changes)
* `Makefile.dist`: make packages for distributing models (CSC ObjectStorage based)
* `Makefile.slurm`: submit jobs with SLURM

Run this if you want to train a model, for example for translating English to French:

```
make SRCLANG=en TRGLANG=fr train
```

To evaluate the model with the automatically generated test data (from the Tatoeba corpus as a default) run:

```
make SRCLANG=en TRGLANG=fr eval
```

For multilingual (more than one language on either side) models run, for example:

```
make SRCLANG="de en" TRGLANG="fr es pt" train
make SRCLANG="de en" TRGLANG="fr es pt" eval
```

Note that data pre-processing should run on CPUs and training/testing on GPUs. To speed up things you can process data sets in parallel using the jobs flag of make, for example using 8 threads:

```
make -j 8 SRCLANG=en TRGLANG=fr data
```




## Upload to Object Storage


```
swift upload OPUS-MT --changed --skip-identical name-of-file
swift post OPUS-MT --read-acl ".r:*"
```

