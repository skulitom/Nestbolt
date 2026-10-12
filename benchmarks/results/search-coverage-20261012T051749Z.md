# Combined placement search: development coverage

All 65 development B/M jobs, seed 0, mixed search up to 1,024 passes / 80M queries / 60 s safety deadline. 0 earlier runs reused; 65 new runs. Prior Nestbolt baseline uses 64 B passes and 6 M passes; competitor reference uses three-seed 60 s medians. Work and populations differ: this is quality triage, not G1/G2/G4 acceptance. Ten held-out maker jobs remain unused.

Valid layouts: **65/65**. Against the preceding fixed-work layouts: 45 better, 18 tied, 2 worse; failed outputs are counted separately.

There are 52 finite competitor comparisons at 60 s and 13 jobs with no finite competitor. Nestbolt wins or ties 27 comparisons; 15 are more than 1% worse. Median material reduction: **0.396716%**.

Of the 9 available finite 300 s targets, 5 are reached within 30 s. Another 1 subset job has no finite competitor, and 55 jobs have no 300 s reference. Accepted-progress arrival provides an upper bound on observed time to target. Missing results never earn free wins. This subset cannot establish G4 across all sheet jobs.

| Job | Material | Change from prior | Reduction vs 60 s competitor | Passes | Stop |
| --- | ---: | ---: | ---: | ---: | --- |
| b-albano-nest-mb-free | 2.588010 | 0.913758% | -0.951699% | 839 | work_limit |
| b-albano-nest-mb-given | 2.875257 | 2.164627% | -1.075977% | 1024 | requested work complete |
| b-albano-strip-sheet | 1.773383 | 5.092655% | 0.643675% | 1024 | requested work complete |
| b-blaz1-nest-mb-free | 9.800015 | 0.000000% | -0.000155% | 196 | work_limit |
| b-blaz1-nest-mb-given | 9.766805 | 16.284586% | -0.001413% | 391 | work_limit |
| b-blaz1-strip-sheet | 3.333341 | 0.000000% | -0.000228% | 791 | work_limit |
| b-dagli-strip-sheet | 0.946742 | 0.000000% | -7.125042% | 1024 | requested work complete |
| b-fu-nest-mb-free | 3.476198 | 5.194794% | 5.194597% | 998 | work_limit |
| b-fu-nest-mb-given | 3.476198 | 5.194794% | 5.194597% | 998 | work_limit |
| b-fu-strip-sheet | 1.368429 | 0.896185% | 1.153558% | 1024 | requested work complete |
| b-jakobs1-nest-mb-free | 3.833345 | 0.000000% | 1.828976% | 515 | work_limit |
| b-jakobs1-nest-mb-given | 3.833345 | 0.000000% | -0.000300% | 515 | work_limit |
| b-jakobs1-strip-sheet | 0.780404 | 2.456487% | -11.295021% | 1024 | requested work complete |
| b-jakobs2-nest-mb-free | 3.750378 | 0.000000% | -4.661723% | 433 | work_limit |
| b-jakobs2-nest-mb-given | 3.750378 | 0.000000% | -4.661723% | 433 | work_limit |
| b-jakobs2-strip-sheet | 0.850428 | 0.524976% | -12.802497% | 940 | work_limit |
| b-mao-nest-mb-free | 1.857514 | 5.114427% | 2.787490% | 1024 | requested work complete |
| b-mao-nest-mb-given | 1.965739 | 9.470709% | 9.470391% | 1024 | requested work complete |
| b-mao-strip-sheet | 0.874959 | 2.711797% | -9.105616% | 1024 | requested work complete |
| b-marques-strip-sheet | 1.096161 | 4.201653% | -10.675563% | 1024 | requested work complete |
| b-shapes0-nest-mb-free | 6.904955 | 4.602690% | 8.225276% | 152 | work_limit |
| b-shapes0-nest-mb-given | 6.904955 | 4.602690% | 8.225276% | 152 | work_limit |
| b-shapes0-strip-sheet | 2.700238 | 1.811167% | 2.694132% | 1024 | requested work complete |
| b-shapes1-nest-mb-free | 6.904955 | 4.602690% | 8.225276% | 152 | work_limit |
| b-shapes1-nest-mb-given | 7.476206 | 1.259508% | 1.257660% | 273 | work_limit |
| b-shapes1-strip-sheet | 2.450031 | 6.671318% | -0.001246% | 652 | work_limit |
| b-shirts-nest-mb-free | 6.948890 | 3.556482% | 6.870543% | 101 | work_limit |
| b-shirts-nest-mb-given | 8.358982 | 0.000000% | -1.875094% | 160 | work_limit |
| b-shirts-strip-sheet | 2.559257 | 0.000000% | 0.149756% | 312 | work_limit |
| b-swim-nest-mb-free | 4.890754 | 1.745301% | -0.158661% | 256 | work_limit |
| b-swim-nest-mb-given | 4.926665 | 0.636290% | -6.533648% | 448 | work_limit |
| b-swim-strip-sheet | 1.744160 | 2.614031% | -2.945940% | 815 | work_limit |
| b-trousers-nest-mb-free | 2.637300 | 9.183652% | 1.101231% | 379 | work_limit |
| b-trousers-nest-mb-given | 2.942172 | 9.432497% | 9.867706% | 607 | work_limit |
| b-trousers-strip-sheet | 2.253196 | 6.315140% | -2.300289% | 604 | work_limit |
| m-box-batch-500 | 2.037549 | 0.000000% | 17.006884% | 22 | work_limit |
| m-box-desktop | 0.837064 | 0.000684% | 5.629762% | 901 | work_limit |
| m-box-long | 0.309399 | 5.027615% | 5.015887% | 1024 | requested work complete |
| m-box-mini | 0.720054 | 0.001578% | -0.566265% | 1024 | requested work complete |
| m-box-storage | 0.538885 | 0.001402% | -0.006053% | 1024 | requested work complete |
| m-box-tool | 1.431028 | 0.000000% | 3.243550% | 590 | deadline |
| m-garment-bruce-1 | 0.209923 | 5.623431% | -6.987170% | 1024 | requested work complete |
| m-garment-bruce-2 | 0.449591 | 3.821372% | -5.334773% | 406 | deadline |
| m-garment-bruce-3 | 1.095671 | 1.930731% | — | 79 | deadline |
| m-garment-teagan-1 | 0.826866 | 2.389290% | -8.415684% | 1024 | requested work complete |
| m-garment-teagan-2 | 1.966469 | 1.019731% | — | 272 | deadline |
| m-garment-teagan-3 | 4.563721 | 2.309865% | — | 83 | deadline |
| m-mechanical-batch-1000 | 1.051642 | 0.000000% | — | 8 | deadline |
| m-mechanical-cog-washers | 1.981347 | 0.000000% | 9.216641% | 113 | work_limit |
| m-mechanical-defective-stock | 2.833085 | 0.000000% | — | 38 | work_limit |
| m-mechanical-frame-inserts | 0.598540 | 0.000000% | 3.855013% | 113 | work_limit |
| m-mechanical-large-plates | 1.197022 | 0.598675% | 3.440005% | 277 | work_limit |
| m-mechanical-mixed-stock | 1.001845 | 0.000000% | 2.586999% | 46 | work_limit |
| m-mechanical-mounting-kit | 2.754289 | 1.189362% | 1.353799% | 162 | work_limit |
| m-mechanical-panel-hardware | 1.636662 | 0.000000% | 5.931207% | 85 | work_limit |
| m-mechanical-remnant-kit | 0.723607 | -1.929529% | — | 60 | work_limit |
| m-mechanical-small-brackets | 6.672542 | 2.306287% | -0.038106% | 81 | work_limit |
| m-public-gear-1 | 1.505621 | 0.005558% | — | 51 | deadline |
| m-public-gear-2 | 1.302529 | -0.149715% | — | 52 | deadline |
| m-public-gear-3 | 0.737159 | 0.000000% | — | 19 | deadline |
| m-public-gear-4 | 0.798394 | 0.134645% | — | 64 | deadline |
| m-sign-1 | 0.771045 | 4.659293% | 18.388342% | 205 | work_limit |
| m-sign-2 | 0.632778 | 1.313716% | — | 163 | deadline |
| m-sign-3 | 0.157601 | 0.823363% | — | 121 | deadline |
| m-sign-4 | 0.367831 | 2.170574% | — | 158 | deadline |

[Full-precision audit and every standalone validation report](search-coverage-20261012T051749Z.json)
