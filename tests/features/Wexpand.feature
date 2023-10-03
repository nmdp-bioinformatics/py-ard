Feature: W expansion

  Scenario Outline:

    Given the allele as <Allele>
    When expanding to WHO then reducing to the <Level> level
    Then the expanded allele is found to be <Expanded Alleles>

    Examples:
      | Allele     | Level | Expanded Alleles |
      | DRB1*07:01 | W | DRB1*07:01:01:01/DRB1*07:01:01:02/DRB1*07:01:01:04/DRB1*07:01:01:05/DRB1*07:01:02/DRB1*07:01:03/DRB1*07:01:04/DRB1*07:01:05/DRB1*07:01:06/DRB1*07:01:07/DRB1*07:01:08/DRB1*07:01:09/DRB1*07:01:10/DRB1*07:01:11/DRB1*07:01:12/DRB1*07:01:13/DRB1*07:01:14/DRB1*07:01:15/DRB1*07:01:16/DRB1*07:01:17/DRB1*07:01:18/DRB1*07:01:19/DRB1*07:01:20/DRB1*07:01:21/DRB1*07:01:22/DRB1*07:01:23/DRB1*07:01:24/DRB1*07:01:25 |
      | DRB1*07:XX | W | DRB1*07:01:01:01/DRB1*07:01:01:02/DRB1*07:01:01:04/DRB1*07:01:01:05/DRB1*07:01:02/DRB1*07:01:03/DRB1*07:01:04/DRB1*07:01:05/DRB1*07:01:06/DRB1*07:01:07/DRB1*07:01:08/DRB1*07:01:09/DRB1*07:01:10/DRB1*07:01:11/DRB1*07:01:12/DRB1*07:01:13/DRB1*07:01:14/DRB1*07:01:15/DRB1*07:01:16/DRB1*07:01:17/DRB1*07:01:18/DRB1*07:01:19/DRB1*07:01:20/DRB1*07:01:21/DRB1*07:01:22/DRB1*07:01:23/DRB1*07:01:24/DRB1*07:01:25/DRB1*07:03/DRB1*07:04/DRB1*07:05/DRB1*07:06/DRB1*07:07/DRB1*07:08/DRB1*07:09/DRB1*07:10N/DRB1*07:11/DRB1*07:12/DRB1*07:13/DRB1*07:14/DRB1*07:15/DRB1*07:16/DRB1*07:17/DRB1*07:18/DRB1*07:19/DRB1*07:20/DRB1*07:21/DRB1*07:22/DRB1*07:23/DRB1*07:24/DRB1*07:25/DRB1*07:26N/DRB1*07:27/DRB1*07:28/DRB1*07:29/DRB1*07:30/DRB1*07:31/DRB1*07:32/DRB1*07:33/DRB1*07:34:01/DRB1*07:34:02/DRB1*07:35/DRB1*07:36/DRB1*07:37/DRB1*07:38/DRB1*07:39/DRB1*07:40/DRB1*07:41/DRB1*07:42/DRB1*07:43/DRB1*07:44/DRB1*07:45/DRB1*07:46/DRB1*07:47/DRB1*07:48/DRB1*07:49/DRB1*07:50/DRB1*07:51/DRB1*07:52/DRB1*07:53/DRB1*07:54/DRB1*07:55/DRB1*07:56/DRB1*07:57/DRB1*07:58N/DRB1*07:59/DRB1*07:60/DRB1*07:61/DRB1*07:62/DRB1*07:63/DRB1*07:64/DRB1*07:65/DRB1*07:66/DRB1*07:67/DRB1*07:68N/DRB1*07:69/DRB1*07:70/DRB1*07:71/DRB1*07:72/DRB1*07:73/DRB1*07:74/DRB1*07:75/DRB1*07:76/DRB1*07:77/DRB1*07:78/DRB1*07:79/DRB1*07:80/DRB1*07:81/DRB1*07:82/DRB1*07:83/DRB1*07:84/DRB1*07:85/DRB1*07:86/DRB1*07:87N/DRB1*07:88/DRB1*07:89/DRB1*07:90/DRB1*07:91/DRB1*07:92/DRB1*07:93/DRB1*07:94/DRB1*07:95/DRB1*07:96/DRB1*07:97/DRB1*07:98/DRB1*07:99/DRB1*07:100/DRB1*07:101N/DRB1*07:102/DRB1*07:103/DRB1*07:104/DRB1*07:105/DRB1*07:106/DRB1*07:107/DRB1*07:108/DRB1*07:109/DRB1*07:110/DRB1*07:111/DRB1*07:112/DRB1*07:113/DRB1*07:114/DRB1*07:115/DRB1*07:116/DRB1*07:117/DRB1*07:118N/DRB1*07:119/DRB1*07:120/DRB1*07:121/DRB1*07:122/DRB1*07:123 |
      | DRB1*11:01 | W | DRB1*11:01:01:01/DRB1*11:01:01:03/DRB1*11:01:01:04/DRB1*11:01:02:01/DRB1*11:01:02:02/DRB1*11:01:03/DRB1*11:01:04/DRB1*11:01:05/DRB1*11:01:06/DRB1*11:01:07/DRB1*11:01:08/DRB1*11:01:09/DRB1*11:01:10/DRB1*11:01:11/DRB1*11:01:12/DRB1*11:01:13/DRB1*11:01:14/DRB1*11:01:15/DRB1*11:01:16/DRB1*11:01:17/DRB1*11:01:18/DRB1*11:01:19/DRB1*11:01:20/DRB1*11:01:21/DRB1*11:01:22/DRB1*11:01:23/DRB1*11:01:24/DRB1*11:01:25/DRB1*11:01:26/DRB1*11:01:27/DRB1*11:01:28/DRB1*11:01:29/DRB1*11:01:30/DRB1*11:01:31/DRB1*11:01:32/DRB1*11:01:33/DRB1*11:01:34/DRB1*11:01:35/DRB1*11:01:36/DRB1*11:01:37/DRB1*11:01:38/DRB1*11:01:39/DRB1*11:01:40/DRB1*11:01:41/DRB1*11:01:42/DRB1*11:01:43 |
      | DRB1*11:02 | W | DRB1*11:02:01:01/DRB1*11:02:01:02/DRB1*11:02:01:03/DRB1*11:02:02/DRB1*11:02:03/DRB1*11:02:04/DRB1*11:02:05/DRB1*11:02:06/DRB1*11:02:07 |
      | DRB1*11:02:02 | W | DRB1*11:02:02 |
      | DRB1*11:02:01:01 | W | DRB1*11:02:01:01 |