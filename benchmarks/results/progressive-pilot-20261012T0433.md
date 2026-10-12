# Progressive search development pilot

Four difficult development cases selected from the existing triage, seed 0, up to 512 passes, 80M queries, 60 s cooperative deadline. Each compared with its own finished 64-pass baseline. More work, not an equal-budget G2/G4 comparison. No held-out cases.

The first 64 repacking passes and their finishing trials match the previous implementation exactly on all four cases. Longer runs retain that incumbent, finish each further block of 64 passes and respect the same shared work/deadline controls. The API permits at most 1,024 passes.

| Job | Previous material | New material | Reduction | Completed passes | Stop | Seconds |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| b-jakobs1-strip-sheet | 0.80005708 | 0.78040378 | 2.4565% | 512 | complete | 6.328 |
| b-blaz1-nest-mb-given | 11.66667427 | 11.66667427 | 0.0000% | 424 | work_limit | 20.906 |
| b-marques-strip-sheet | 1.14423841 | 1.09616149 | 4.2017% | 512 | complete | 14.047 |
| m-garment-bruce-1 | 0.21639156 | 0.21639156 | 0.0000% | 512 | complete | 25.484 |

All four outputs pass the independent checker. Jakobs1 and Marques improve; Blaz1 and Bruce retain their 64-pass result. The Blaz1 query cap stops an incomplete next pass and returns the valid incumbent. Bruce already reaches its new result within 64 passes, improving on the earlier six-pass maker pilot; longer search adds no gain on that job.

The complete four-job history is retained; no unsuccessful attempt was replaced. This small, selected, single-seed pilot does not establish the population quality or speed gates.

[All layouts, histories, timings, baselines and hashes](progressive-pilot-20261012T0433.json).
