# Constellation optimisation: results

3064 designs evaluated at screen fidelity (3 h / 120 s / 1000 points), 3014 simulated, the rest pruned analytically (coverage bound or no bus fits). Up to 2 shells, coverage floor 90%. Costs are 10-year TCO in M EUR.

## Answer

**Cheapest design with full coverage, p99 <= 100 ms (confirmed at full fidelity): 112 satellites**, `7x16@700km/87deg/star/F0 [in:rf x:rfx2]`, 10-year TCO EUR 348 M (capex EUR 134 M), p99 98 ms, worst-place p95 105 ms, bus 16U/30kg/5y.

**Knee of the confirmed 3-objective front: 105 satellites**, `7x15@700km/87deg/star/F0 [in:rf x:rfx2]`, TCO EUR 333 M, p99 100 ms, coverage 100.0%.

## Cheapest design per service tier (full fidelity: 24 h / 60 s / 2000 points)

| tier                           |   sats |   planes | shells                                              | buses       |   tco_meur |   capex_meur |   coverage_mean |   coverage_worst_point |   max_gap_min |   min_sats_in_view |   latency_p50_ms |   latency_p99_ms |   worst_point_p95_ms |
|:-------------------------------|-------:|---------:|:----------------------------------------------------|:------------|-----------:|-------------:|----------------:|-----------------------:|--------------:|-------------------:|-----------------:|-----------------:|---------------------:|
| full coverage                  |     96 |        6 | 6x16@800km/87deg/star/F3 [in:rf x:none]             | 12U/23kg/5y |      256.4 |        89.9  |          1      |                 1      |             0 |                  1 |            75.13 |           109.7  |                118.6 |
| full coverage, p99 <= 150 ms   |     96 |        6 | 6x16@800km/87deg/star/F3 [in:rf x:none]             | 12U/23kg/5y |      256.4 |        89.9  |          1      |                 1      |             0 |                  1 |            75.13 |           109.7  |                118.6 |
| full coverage, p99 <= 120 ms   |     96 |        6 | 6x16@800km/87deg/star/F3 [in:rf x:none]             | 12U/23kg/5y |      256.4 |        89.9  |          1      |                 1      |             0 |                  1 |            75.13 |           109.7  |                118.6 |
| full coverage, p99 <= 100 ms   |    112 |        7 | 7x16@700km/87deg/star/F0 [in:rf x:rfx2]             | 16U/30kg/5y |      348.2 |       134.2  |          1      |                 1      |             0 |                  1 |            71.95 |            98.33 |                105.1 |
| full coverage, p99 <= 90 ms    |    306 |       17 | 17x18@500km/87deg/delta/F2 [in:optical x:opticalx2] | 16U/32kg/5y |     1211   |       546.8  |          1      |                 1      |             0 |                  2 |            65.66 |            84.75 |                 89.8 |
| coverage >= 99%, p99 <= 150 ms |     80 |        5 | 5x16@800km/87deg/star/F2 [in:rf x:none]             | 12U/23kg/5y |      223.2 |        74.92 |          0.9972 |                 0.984  |             3 |                  0 |            77.66 |           116.4  |                124.3 |
| coverage >= 99%, p99 <= 100 ms |    105 |        7 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2]             | 16U/30kg/5y |      332.7 |       127.1  |          1      |                 0.9993 |             1 |                  0 |            72.78 |            99.53 |                106.1 |
| coverage >= 95%, p99 <= 150 ms |     75 |        5 | 5x15@700km/97.6deg/star/F1 [in:rf x:none]           | 12U/23kg/5y |      214.6 |        71.09 |          0.9548 |                 0.8896 |            27 |                  0 |            77.47 |           117.2  |                125.3 |

## Pareto front: cost vs latency vs coverage (full fidelity: 24 h / 60 s / 2000 points)

|   sats |   planes | shells                                                                                             | buses                          |   tco_meur |   capex_meur |   coverage_mean |   coverage_worst_point |   max_gap_min |   min_sats_in_view |   latency_p50_ms |   latency_p99_ms |   worst_point_p95_ms |
|-------:|---------:|:---------------------------------------------------------------------------------------------------|:-------------------------------|-----------:|-------------:|----------------:|-----------------------:|--------------:|-------------------:|-----------------:|-----------------:|---------------------:|
|     40 |        4 | 4x10@1200km/87deg/star/F2 [in:none x:none]                                                         | 12U/21kg/4.01y                 |      158.5 |        31.36 |          0.9151 |                0.04236 |           167 |                  0 |            96.68 |           397.1  |               438.6  |
|     50 |        5 | 5x10@800km/87deg/star/F2 [in:optical x:none]                                                       | 16U/28kg/5y                    |      201.4 |        67.49 |          0.9448 |                0.8583  |             9 |                  0 |            84.13 |           123.8  |               134.5  |
|     75 |        5 | 5x15@600km/87deg/star/F2 [in:rf x:none]                                                            | 12U/23kg/5y                    |      214.3 |        70.93 |          0.906  |                0.7833  |            29 |                  0 |            76.04 |           115.6  |               125.4  |
|     75 |        5 | 5x15@700km/97.6deg/star/F0 [in:rf x:none]                                                          | 12U/23kg/5y                    |      214.6 |        71.09 |          0.9567 |                0.8917  |            28 |                  0 |            77.42 |           117.2  |               125    |
|     75 |        5 | 5x15@700km/97.6deg/star/F2 [in:rf x:none]                                                          | 12U/23kg/5y                    |      214.6 |        71.09 |          0.9565 |                0.8924  |            27 |                  0 |            77.4  |           117.1  |               124.5  |
|     75 |        5 | 5x15@700km/97.6deg/star/F2 [in:rf x:none]                                                          | 12U/23kg/5y                    |      214.6 |        71.09 |          0.9565 |                0.8924  |            27 |                  0 |            77.4  |           117.1  |               124.5  |
|     80 |        5 | 5x16@800km/87deg/star/F2 [in:rf x:none]                                                            | 12U/23kg/5y                    |      223.2 |        74.92 |          0.9972 |                0.984   |             3 |                  0 |            77.66 |           116.4  |               124.3  |
|     80 |        5 | 5x16@800km/87deg/star/F1 [in:rf x:none]                                                            | 12U/23kg/5y                    |      223.2 |        74.92 |          0.9953 |                0.9743  |             3 |                  0 |            77.68 |           116.3  |               124.3  |
|     80 |        5 | 5x16@800km/87deg/star/F2 [in:rf x:none]                                                            | 12U/23kg/5y                    |      223.2 |        74.92 |          0.9972 |                0.984   |             3 |                  0 |            77.66 |           116.4  |               124.3  |
|     85 |        5 | 5x17@800km/87deg/star/F2 [in:rf x:none]                                                            | 12U/23kg/5y                    |      231.7 |        78.66 |          0.9983 |                0.9875  |             3 |                  0 |            77.07 |           115.4  |               123    |
|     90 |        5 | 5x18@700km/87deg/star/F2 [in:rf x:none]                                                            | 12U/23kg/5y                    |      240   |        82.31 |          0.976  |                0.9125  |            13 |                  0 |            75.79 |           114.2  |               121.9  |
|     96 |        6 | 6x16@800km/87deg/star/F3 [in:rf x:none]                                                            | 12U/23kg/5y                    |      256.4 |        89.9  |          1      |                1       |             0 |                  1 |            75.13 |           109.7  |               118.6  |
|    102 |        6 | 6x17@800km/87deg/star/F3 [in:rf x:none]                                                            | 12U/23kg/5y                    |      266.6 |        94.39 |          1      |                1       |             0 |                  1 |            74.5  |           108.5  |               117.6  |
|    100 |        5 | 5x20@600km/97.6deg/star/F0 [in:rf x:opticalx2/4]                                                   | 12U/24kg/5y                    |      277.7 |       100.2  |          0.928  |                0.8347  |            39 |                  0 |            73.82 |           107.4  |               115    |
|    112 |        7 | 7x16@600km/97.6deg/star/F0 [in:rf x:rfx2/4]                                                        | 12U/23kg/5y                    |      295.5 |       107.8  |          0.9977 |                0.9931  |             3 |                  0 |            72.44 |           106.5  |               113.8  |
|    102 |        6 | 6x17@550km/97.6deg/star/F1 [in:rf x:rfx2]                                                          | 16U/30kg/5y                    |      319.4 |       120.8  |          0.9594 |                0.9111  |            25 |                  0 |            72.3  |           102.4  |               108.8  |
|    105 |        7 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2]                                                            | 16U/30kg/5y                    |      332.7 |       127.1  |          1      |                0.9993  |             1 |                  0 |            72.78 |            99.53 |               106.1  |
|    112 |        7 | 7x16@600km/87deg/star/F0 [in:rf x:rfx2]                                                            | 16U/30kg/5y                    |      347.6 |       133.9  |          0.998  |                0.9882  |             2 |                  0 |            71.26 |            98.15 |               104.6  |
|    112 |        7 | 7x16@700km/87deg/star/F0 [in:rf x:rfx2]                                                            | 16U/30kg/5y                    |      348.2 |       134.2  |          1      |                1       |             0 |                  1 |            71.95 |            98.33 |               105.1  |
|    126 |        7 | 7x18@700km/97.6deg/star/F0 [in:rf x:rfx2]                                                          | 16U/30kg/5y                    |      379.3 |       148.4  |          1      |                0.9993  |             1 |                  0 |            70.78 |            97.32 |               103.2  |
|    160 |        8 | 8x20@600km/97.6deg/star/F0 [in:rf x:rfx2]                                                          | 16U/30kg/5y                    |      459.9 |       185.3  |          1      |                0.9993  |             1 |                  0 |            68.43 |            93.33 |               100.8  |
|    180 |        9 | 9x20@550km/97.6deg/star/F1 [in:rf x:rfx2]                                                          | 16U/30kg/5y                    |      510.2 |       208.4  |          1      |                0.9993  |             1 |                  0 |            67.61 |            91.83 |               101.5  |
|    180 |        9 | 9x20@600km/97.6deg/star/F1 [in:rf x:rfx2]                                                          | 16U/30kg/5y                    |      510.3 |       208.4  |          1      |                1       |             0 |                  1 |            67.85 |            91.77 |               100.4  |
|    200 |       10 | 10x20@550km/97.6deg/star/F0 [in:optical x:rfx2]                                                    | 16U/31kg/5y                    |      712.9 |       307.7  |          1      |                1       |             0 |                  1 |            66.64 |            90.55 |               100.2  |
|    306 |       17 | 17x18@500km/87deg/delta/F2 [in:optical x:opticalx2]                                                | 16U/32kg/5y                    |     1211   |       546.8  |          1      |                1       |             0 |                  2 |            65.66 |            84.75 |                89.8  |
|    459 |       25 | 19x21@450km/87deg/delta/F2 [in:optical x:opticalx2] + 6x10@600km/87deg/star/F2 [in:optical x:none] | ESPA-150/75kg/5y + 12U/24kg/5y |     2756   |      1304    |          1      |                1       |             0 |                  2 |            64.58 |            83.38 |                88.31 |

## RF vs optical: cheapest design per ISL technology, full coverage, p99 <= 100 ms (screen fidelity)

| isl_techs   |   sats |   planes | shells                                            | buses       |   tco_meur |   capex_meur |   coverage_mean |   coverage_worst_point |   max_gap_min |   min_sats_in_view |   latency_p50_ms |   latency_p99_ms |   worst_point_p95_ms |
|:------------|-------:|---------:|:--------------------------------------------------|:------------|-----------:|-------------:|----------------:|-----------------------:|--------------:|-------------------:|-----------------:|-----------------:|---------------------:|
| rf          |    105 |        7 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2]           | 16U/30kg/5y |      332.7 |        127.1 |               1 |                      1 |             0 |                  1 |            72.75 |            99.26 |                106.9 |
| optical/rf  |    160 |        8 | 8x20@550km/87deg/star/F1 [in:rf x:opticalx2/4]    | 12U/24kg/5y |      409.9 |        160.2 |               1 |                      1 |             0 |                  1 |            69.14 |            98.62 |                108.1 |
| optical     |    120 |        6 | 6x20@800km/87deg/star/F1 [in:optical x:opticalx1] | 16U/30kg/5y |      473.3 |        196.5 |               1 |                      1 |             0 |                  1 |            72.05 |            99.67 |                108.3 |

## Single vs mixed altitude, full coverage, p99 <= 100 ms (screen fidelity)

| mix                              | altitudes   |   sats |   planes | shells                                                                                                 | buses                     |   tco_meur |   capex_meur |   coverage_mean |   coverage_worst_point |   max_gap_min |   min_sats_in_view |   latency_p50_ms |   latency_p99_ms |   worst_point_p95_ms |
|:---------------------------------|:------------|-------:|---------:|:-------------------------------------------------------------------------------------------------------|:--------------------------|-----------:|-------------:|----------------:|-----------------------:|--------------:|-------------------:|-----------------:|-----------------:|---------------------:|
| single shell                     | 700         |    105 |        7 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2]                                                                | 16U/30kg/5y               |      332.7 |        127.1 |               1 |                      1 |             0 |                  1 |            72.75 |            99.26 |                106.9 |
| mixed altitude                   | 700/550     |    172 |       13 | 7x16@700km/87deg/star/F0 [in:rf x:rfx2] + 6x10@550km/87deg/star/F1 [in:optical x:none]                 | 16U/30kg/5y + 12U/24kg/5y |      504.4 |        206.3 |               1 |                      1 |             0 |                  1 |            71.09 |            96.35 |                104.7 |
| mixed altitude + inter-shell ISL | 600/550     |    240 |       16 | 10x18@600km/87deg/star/F1 [in:rf x:rfx2/4] + 6x10@550km/87deg/star/F1 [in:optical x:none] +inter-shell | 16U/28kg/5y + 16U/30kg/5y |      709.9 |        302.3 |               1 |                      1 |             0 |                  1 |            68.77 |            96.86 |                106   |

## Cost sensitivity of the full coverage, p99 <= 100 ms answer (re-costed, no re-simulation)

| scenario                              |   sats | shells                                  | isl_techs   |   tco_meur |
|:--------------------------------------|-------:|:----------------------------------------|:------------|-----------:|
| baseline                              |    105 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] | rf          |      332.7 |
| optical terminal -50%                 |    105 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] | rf          |      332.7 |
| optical terminal +50%                 |    105 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] | rf          |      332.7 |
| RF terminal -50%                      |    105 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] | rf          |      311.7 |
| RF terminal +50%                      |    105 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] | rf          |      353.7 |
| launch EUR/kg -50%                    |    105 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] | rf          |      313.7 |
| launch EUR/kg +50%                    |    105 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] | rf          |      351.6 |
| per-plane cost -50%                   |    105 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] | rf          |      311.7 |
| per-plane cost +50%                   |    105 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] | rf          |      353.7 |
| dedicated launch per plane (EUR 7.5M) |    105 | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] | rf          |      500.7 |

## RF / optical crossover: winner vs optical terminal price

|   optical_eur_m_per_terminal |   sats | isl_techs   | shells                                  |   tco_meur |
|-----------------------------:|-------:|:------------|:----------------------------------------|-----------:|
|                         0.02 |    105 | rf          | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] |      332.7 |
|                         0.05 |    105 | rf          | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] |      332.7 |
|                         0.1  |    105 | rf          | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] |      332.7 |
|                         0.15 |    105 | rf          | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] |      332.7 |
|                         0.2  |    105 | rf          | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] |      332.7 |
|                         0.3  |    105 | rf          | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] |      332.7 |
|                         0.4  |    105 | rf          | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] |      332.7 |
|                         0.6  |    105 | rf          | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] |      332.7 |
|                         1    |    105 | rf          | 7x15@700km/87deg/star/F0 [in:rf x:rfx2] |      332.7 |

## Robustness of the picks (shorter run at full grid resolution)

| pick                           | scenario                            |   sats |   coverage_mean |   coverage_worst_point |   max_gap_min |   latency_p99_ms |   worst_point_p95_ms |
|:-------------------------------|:------------------------------------|-------:|----------------:|-----------------------:|--------------:|-----------------:|---------------------:|
| knee                           | baseline                            |    105 |          1      |                 0.9972 |             1 |            99.18 |               106.7  |
| knee                           | 1 satellite failed (draw 1)         |    105 |          0.9978 |                 0.9861 |             5 |           100.1  |               109.2  |
| knee                           | 1 satellite failed (draw 2)         |    105 |          0.9978 |                 0.9861 |             5 |            99.75 |               106.7  |
| knee                           | 1 satellite failed (draw 3)         |    105 |          0.9976 |                 0.9861 |             5 |            99.59 |               106.7  |
| knee                           | 1 satellite failed (draw 4)         |    105 |          0.9978 |                 0.9861 |             5 |           100.3  |               107.3  |
| knee                           | Svalbard gateway down               |    105 |          1      |                 0.9972 |             1 |            99.18 |               106.7  |
| knee                           | cross-plane lasers off above 70 deg |    105 |          1      |                 0.9972 |             1 |            99.33 |               106.7  |
| full coverage                  | baseline                            |     96 |          1      |                 1      |             0 |           109.8  |               119    |
| full coverage                  | 1 satellite failed (draw 1)         |     96 |          0.9977 |                 0.9861 |             4 |           111.1  |               121.6  |
| full coverage                  | 1 satellite failed (draw 2)         |     96 |          0.9977 |                 0.9861 |             4 |           111.4  |               144.8  |
| full coverage                  | 1 satellite failed (draw 3)         |     96 |          0.9978 |                 0.9861 |             4 |           111.2  |               119.8  |
| full coverage                  | 1 satellite failed (draw 4)         |     96 |          0.9977 |                 0.9861 |             4 |           110.6  |               119    |
| full coverage                  | Svalbard gateway down               |     96 |          1      |                 1      |             0 |           109.8  |               119    |
| full coverage                  | cross-plane lasers off above 70 deg |     96 |          1      |                 1      |             0 |           109.8  |               119    |
| full coverage, p99 <= 100 ms   | baseline                            |    112 |          1      |                 1      |             0 |            97.98 |               105.2  |
| full coverage, p99 <= 100 ms   | 1 satellite failed (draw 1)         |    112 |          0.9984 |                 0.9889 |             4 |            99    |               109.7  |
| full coverage, p99 <= 100 ms   | 1 satellite failed (draw 2)         |    112 |          0.9984 |                 0.9889 |             4 |            99.05 |               108.6  |
| full coverage, p99 <= 100 ms   | 1 satellite failed (draw 3)         |    112 |          0.9984 |                 0.9889 |             4 |            98.78 |               106.5  |
| full coverage, p99 <= 100 ms   | 1 satellite failed (draw 4)         |    112 |          0.9984 |                 0.9889 |             4 |            98.96 |               106.6  |
| full coverage, p99 <= 100 ms   | Svalbard gateway down               |    112 |          1      |                 1      |             0 |            97.98 |               105.2  |
| full coverage, p99 <= 100 ms   | cross-plane lasers off above 70 deg |    112 |          1      |                 1      |             0 |            98.07 |               105.2  |
| full coverage, p99 <= 90 ms    | baseline                            |    306 |          1      |                 1      |             0 |            84.78 |                89.81 |
| full coverage, p99 <= 90 ms    | 1 satellite failed (draw 1)         |    306 |          1      |                 1      |             0 |            84.8  |                89.81 |
| full coverage, p99 <= 90 ms    | 1 satellite failed (draw 2)         |    306 |          1      |                 1      |             0 |            84.84 |                90.11 |
| full coverage, p99 <= 90 ms    | 1 satellite failed (draw 3)         |    306 |          1      |                 1      |             0 |            84.83 |                90    |
| full coverage, p99 <= 90 ms    | 1 satellite failed (draw 4)         |    306 |          1      |                 1      |             0 |            84.81 |                90.09 |
| full coverage, p99 <= 90 ms    | Svalbard gateway down               |    306 |          1      |                 1      |             0 |            84.78 |                89.81 |
| full coverage, p99 <= 90 ms    | cross-plane lasers off above 70 deg |    306 |          1      |                 1      |             0 |            84.8  |                89.81 |
| coverage >= 99%, p99 <= 150 ms | baseline                            |     80 |          0.9972 |                 0.9722 |             3 |           116.8  |               127.5  |
| coverage >= 99%, p99 <= 150 ms | 1 satellite failed (draw 1)         |     80 |          0.9929 |                 0.9528 |             7 |           119.1  |               137.5  |
| coverage >= 99%, p99 <= 150 ms | 1 satellite failed (draw 2)         |     80 |          0.9928 |                 0.95   |             7 |           117.8  |               127.6  |
| coverage >= 99%, p99 <= 150 ms | 1 satellite failed (draw 3)         |     80 |          0.9927 |                 0.9556 |             7 |           117.6  |               129.1  |
| coverage >= 99%, p99 <= 150 ms | 1 satellite failed (draw 4)         |     80 |          0.9929 |                 0.9472 |             7 |           119.2  |               135.7  |
| coverage >= 99%, p99 <= 150 ms | Svalbard gateway down               |     80 |          0.9972 |                 0.9722 |             3 |           116.8  |               127.5  |
| coverage >= 99%, p99 <= 150 ms | cross-plane lasers off above 70 deg |     80 |          0.9972 |                 0.9722 |             3 |           116.8  |               127.5  |
| coverage >= 95%, p99 <= 150 ms | baseline                            |     75 |          0.9548 |                 0.8556 |            26 |           116.7  |               132.8  |
| coverage >= 95%, p99 <= 150 ms | 1 satellite failed (draw 1)         |     75 |          0.9481 |                 0.8306 |            26 |           117.8  |               132.8  |
| coverage >= 95%, p99 <= 150 ms | 1 satellite failed (draw 2)         |     75 |          0.9482 |                 0.8389 |            26 |           119.4  |               150.8  |
| coverage >= 95%, p99 <= 150 ms | 1 satellite failed (draw 3)         |     75 |          0.9484 |                 0.8306 |            26 |           117.7  |               132.8  |
| coverage >= 95%, p99 <= 150 ms | 1 satellite failed (draw 4)         |     75 |          0.9481 |                 0.8333 |            29 |           117.4  |               133    |
| coverage >= 95%, p99 <= 150 ms | Svalbard gateway down               |     75 |          0.9548 |                 0.8556 |            26 |           116.7  |               132.8  |
| coverage >= 95%, p99 <= 150 ms | cross-plane lasers off above 70 deg |     75 |          0.9548 |                 0.8556 |            26 |           116.7  |               132.8  |
