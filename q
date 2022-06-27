[33mcommit cea98b463fe7dcaabfcc0fe7b706d1ef5ff7266c[m[33m ([m[1;36mHEAD -> [m[1;32mreport-generation[m[33m)[m
Author: Islam Ahmadien <islammohamed323@gmail.com>
Date:   Mon Jun 27 10:03:31 2022 +0200

    generate report pdf for "basic" version.0

[33mcommit 115ef29981bf95c5a93d15da70d37528a8491dd0[m[33m ([m[1;31morigin/master[m[33m, [m[1;31morigin/HEAD[m[33m, [m[1;32mmaster[m[33m)[m
Merge: 32f1002 45e0d5c
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Jun 26 22:20:16 2022 +0200

    Merge pull request #6 from e-ahmedwaleed/remote-cli
    
    Interstellar CLI

[33mcommit 45e0d5c06ab9c1f9ebe4091506ae93453ecd5514[m[33m ([m[1;31morigin/remote-cli[m[33m)[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Jun 26 22:18:11 2022 +0200

    dataflow analysis

[33mcommit 129f4f0041b696a96e2ff12c2508e2d4ba938241[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Jun 26 21:34:11 2022 +0200

    code reduction
    
    kill children if terminated:
    https://stackoverflow.com/questions/25542110/kill-child-process-if-parent-is-killed-in-python

[33mcommit 10c4d0ebe92addf1fd0cfeb10e08c1355bd413e4[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu Jun 2 19:31:56 2022 +0200

    reorganized
    modified .gitignore
    no output pickle file
    extracted cli logic to folder
    more clear comments in utils files
    better folder naming for interstellar
    
    max and min values:
    https://stackoverflow.com/questions/7604966/maximum-and-minimum-values-for-ints
    extract nth line:
    https://stackoverflow.com/questions/11491835/get-nth-line-of-string-in-python
    trim string:
    https://www.journaldev.com/23625/python-trim-string-rstrip-lstrip-strip

[33mcommit c0cb03d0d45d7a97c741e6955f5389c8332f4052[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Wed Jun 1 23:17:16 2022 +0200

    dataflow_explore cli ready
    better output file
    encoding problem solved

[33mcommit d534e56e011dfff178ceb6f7c69ebcdcfafe58b6[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Wed Jun 1 23:04:33 2022 +0200

    interstellar cli revived

[33mcommit 523d2feed380d92a61287a441784d45b2b784948[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Wed Jun 1 22:42:52 2022 +0200

    requirements

[33mcommit 06c30389d1fe6747ef39afa47a6fcdfb69ba6abc[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Wed Jun 1 22:17:45 2022 +0200

    fixed encoding issue
    character maps to <undefined>:
    https://stackoverflow.com/questions/27092833/unicodeencodeerror-charmap-codec-cant-encode-characters

[33mcommit 198b4ba00c63734d755b73dc87dc76c443fabb59[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Wed Jun 1 21:20:41 2022 +0200

    independent interstellar

[33mcommit 32f100208ed1b04f97bbc1edee4fecc09f0f3a3c[m
Merge: d139277 119c08a
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat May 28 23:04:47 2022 +0200

    Merge pull request #5 from e-ahmedwaleed/interstellar-expanded
    
    Interstellar Output Clarification

[33mcommit 119c08a047548340578cc50b5a5f87f0e664b9f4[m[33m ([m[1;31morigin/interstellar-expanded[m[33m)[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat May 28 22:57:24 2022 +0200

    handled dataflow_explore exception
    "parallel count has to be more than 1 for dataflow exploration" -> checked correctly
    it was fixed in a previous commit, but had to clarify so that others assertions of the same types are to be rechecked

[33mcommit a93a711bad2215fd8b71b944b75805892d8786d8[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat May 28 22:41:04 2022 +0200

    handled loop_blocking problem
    where the last level in 4_level memory had 0 energy cost,
    added a label to clarify that it was not checked.

[33mcommit d78db07635d096ed84e84f9dd66f556a2219a49b[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat May 28 22:12:25 2022 +0200

    handled memory_explore exception
    "No valid mapping point found." -> inf cost
    python exceptions:
    https://docs.python.org/3/tutorial/errors.html

[33mcommit b59ca3fef434a94580155f1da7f9f322e2c8a54a[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat May 28 20:27:32 2022 +0200

    memory-explore done
    concatenate lists:
    https://stackoverflow.com/questions/1720421/how-do-i-concatenate-two-lists-in-python

[33mcommit e9e8d1f9766cb155c026ba0bb82d07ab26147321[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat May 28 15:39:53 2022 +0200

    mem_explore: round-2
    reverted gitignore
    mem_explore output done
    uniform output representation
    deleted/commented non-useful code
    
    column extraction:
    https://stackoverflow.com/questions/903853/how-do-you-extract-a-column-from-a-multi-dimensional-array

[33mcommit 39615fc5d1aef66e8675a6ccd43bdf8f67837869[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Fri May 27 23:55:24 2022 +0200

    mem_explore: round-1
    improved gitignore
    mem_explore code cleaning
    removed unwanted columns in summary_array

[33mcommit 5f0d26bd0734192273111a3e9af67796160910a2[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Fri May 27 21:39:52 2022 +0200

    interstellar reorganized
    improved and extracted output formatting methods,
    changed '-' to '_' in folder names

[33mcommit 533ec570942cff235ef8676cb318f567f14fe519[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu May 26 22:43:45 2022 +0200

    dataflow-explore done
    array condition:
    https://stackoverflow.com/questions/45848612/python-how-to-use-conditional-statements-on-every-element-of-array-using-s
    Iterating over dict:
    https://stackoverflow.com/questions/3294889/iterating-over-dictionaries-using-for-loops
    all occurrences of a char:
    https://stackoverflow.com/questions/13009675/find-all-the-occurrences-of-a-character-in-a-string

[33mcommit 27675cbcde91016ab2f971397555d6c87f6d61ff[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu May 26 20:30:59 2022 +0200

    loop-blocking done
    list reversing:
    https://www.geeksforgeeks.org/python-reversing-list/

[33mcommit bc235cc75c320dda17753969cb9a29040a05e49b[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu May 26 15:49:56 2022 +0200

    warnings handling

[33mcommit 0cb6495bf97c1cdb32b521592b81a3abf08b2d61[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu May 26 14:59:33 2022 +0200

    energy costs expanded
    append to tuple:
    https://datagy.io/python-append-to-tuple/
    ascii art:
    https://textpaint.net/

[33mcommit 48aeee1be173d7653a4c3fc1ed4e9eb0328e4670[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Wed May 25 22:13:16 2022 +0200

    best mapping point expanded
    strings vertical alignment:
    https://stackoverflow.com/questions/57156557/how-can-i-change-align-columns-vertically-in-python
    length of number:
    https://stackoverflow.com/questions/2189800/how-to-find-length-of-digits-in-an-integer

[33mcommit fdd8f02d9081e3d95e0a1774cc68e552f3f11f7b[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Wed May 25 13:58:54 2022 +0200

    gitinore fixed

[33mcommit d1392770e820ba415928f1851ac8859741aad754[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu Apr 21 06:35:05 2022 +0200

    rgola zone
    
    Center image in README file:
    https://stackoverflow.com/questions/12090472/how-do-i-center-an-image-in-the-readme-md-file-on-github

[33mcommit dbc255f1b6bb9bd826a317c5a5ac7ac82d4cb393[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu Apr 21 06:01:24 2022 +0200

    reorganized
    phase 1 files moved back to main dir
    
    Interfaces in Python:
    https://www.godaddy.com/engineering/2018/12/20/python-metaclasses

[33mcommit 32b6cc9664a498375faacf67b77a930b6e7a7aa6[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu Apr 21 02:40:34 2022 +0200

    maro's territory
    
    Image to html:
    https://www.text-image.com/convert/

[33mcommit d6577bc08a869ddab02396628790bbe5312c3706[m[33m ([m[1;31morigin/interstellar-samples-generator[m[33m)[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu Apr 21 00:28:39 2022 +0200

    analysis done

[33mcommit 0e602535700cd403f3b44c0d6c32569d4c8f09f4[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu Mar 31 15:15:13 2022 +0200

    minimal analysis
    
    dictionary sort:
    https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

[33mcommit 3ae541da53c624d9196b25ab3518830ee1130614[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Wed Mar 30 04:21:54 2022 +0200

    empty analysis
    
    file handling:
    https://www.geeksforgeeks.org/file-handling-python
    
    sorting a set:
    https://stackoverflow.com/questions/17457793/sorting-a-set-of-values

[33mcommit 140d0c938ed2d4f155393f2fcad114721a351594[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Mon Mar 21 11:12:34 2022 +0200

    analysis preparation
    
    empty set:
    https://pythonguides.com/python-create-empty-set
    
    strike-through effect:
    https://stackoverflow.com/questions/8357203/is-it-possible-to-display-text-in-a-console-with-a-strike-through-effect

[33mcommit 83177d5c2d01e72623f35ec4cd4559156a21f259[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Tue Mar 8 16:58:14 2022 +0200

    output traversal

[33mcommit 0e148ef9ba991ebeec0104bf3fa587abfbd83762[m
Merge: b87e153 9521d81
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Wed Feb 16 18:23:30 2022 +0200

    Merge pull request #3 from e-ahmedwaleed/phase-selector-cli
    
    Global main

[33mcommit 9521d81155b70104eb2ce7b666f90c26878956b7[m[33m ([m[1;31morigin/phase-selector-cli[m[33m)[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Wed Feb 16 05:24:18 2022 +0200

    organized output

[33mcommit 002886cba6c52f1dbf59cd37fa97b13a29af6e6a[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Wed Feb 16 02:09:20 2022 +0200

    timeout
    https://stackoverflow.com/questions/1191374/using-module-subprocess-with-timeout?rq=1

[33mcommit ea8b77949f850729b293cd961cf5350159113dda[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Tue Feb 15 21:22:30 2022 +0200

    interstellar samples

[33mcommit cae872e94e1870ebb14f69b80f6140c6292e0937[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat Feb 12 23:00:56 2022 +0200

    untils file
    to separate the logic from global main file

[33mcommit 13ae8db6ec74ef62a6f255f0a7cae0ed9e64b96a[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat Feb 12 22:14:52 2022 +0200

    multithreading test
    
    Multithreading:
    https://www.geeksforgeeks.org/multithreading-python-set-1/
    Python exists():
    https://www.guru99.com/python-check-if-file-exists.html
    List all files of a directory:
    https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory

[33mcommit 454d4d34a6573b223239593d180526af13ad6ebe[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat Feb 12 21:33:35 2022 +0200

    run_python test

[33mcommit b3132206940c712fa80e0bb4590be313fdfb1bd0[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat Feb 12 18:54:39 2022 +0200

    global main

[33mcommit c02c3b19b8370193e3a1b82a0874271718d39627[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Mon Feb 7 12:14:11 2022 +0200

    tests no output

[33mcommit d06897c136ec3c8eda5736c921a5e8529d3a33cb[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Mon Feb 7 11:28:15 2022 +0200

    tests no prints

[33mcommit 78062b881296d67bfd894c36b83ea3c4fed3b9ad[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Mon Feb 7 11:04:23 2022 +0200

    better gitignore

[33mcommit 00a22f563a9129018a037064a41a1a7ce6779573[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Feb 6 18:59:00 2022 +0200

    fixed missing import modules

[33mcommit b87e1536bf783691da8b93e96a2e455b215fd36b[m
Merge: d3c30d4 15ad544
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Feb 6 18:36:07 2022 +0200

    Merge pull request #2 from e-ahmedwaleed/pre-interstellar
    
    Windows interstellar

[33mcommit 15ad54435294988b8a0694a26afb8559a4e7575e[m[33m ([m[1;31morigin/pre-interstellar[m[33m)[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Feb 6 18:31:44 2022 +0200

    runnable interstellar

[33mcommit 243f6d7e2bc992fa5754d48bf08c205ce380c0cc[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Feb 6 18:23:34 2022 +0200

    compared with original
    https://github.com/xuanyoya/Interstellar-CNN-scheduler/

[33mcommit 471e615a81e7543c4568f6e8a322eb891995eda5[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Feb 6 17:35:16 2022 +0200

    correctness tested

[33mcommit 09af054ea98eb9bc0d2ecd02cb7a8e832e344bf3[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Feb 6 15:06:34 2022 +0200

    cost_model_systolic pass

[33mcommit 106afc2cb763710fc9a9defee4e7313fa7e10d72[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Feb 6 13:18:35 2022 +0200

    to python 3

[33mcommit 570f930377b60b2c7f44648618c99c0bc480b3b9[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Feb 6 13:08:44 2022 +0200

    raw interstellar

[33mcommit 937534ee77b4b06121d94d140e8d8b3ef7c9a7bc[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Feb 6 12:47:25 2022 +0200

    reorganized
    Qt gui files included, foldering previous phase

[33mcommit d3c30d41291b2bcfed4a44704bf87b0fab3974b7[m
Merge: 660724f 502b41c
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Dec 12 20:33:04 2021 +0200

    Merge pull request #1 from e-ahmedwaleed/extractor-gui
    
    Extraction Phase

[33mcommit 502b41c5dae385f4e7151288e1794690d1197a05[m[33m ([m[1;31morigin/extractor-gui[m[33m)[m
Merge: 1e91102 0dc0db4
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Dec 12 20:27:40 2021 +0200

    Merge branch 'extractor-gui-onnx' into extractor-gui

[33mcommit 0dc0db480c29d8192852aff1bc7e06a8daabebfd[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Dec 12 20:27:09 2021 +0200

    netron bad fix

[33mcommit 65d9806fecba44a916d305b038b97a3fc096fae3[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Dec 12 19:53:29 2021 +0200

    extraction completed, but
    
    numpy full print:
    https://stackoverflow.com/questions/1987694/how-to-print-the-full-numpy-array-without-truncation

[33mcommit 8a8b87dbdd7b39a9d3c563f5b0e1779bdc08199c[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Dec 12 17:38:32 2021 +0200

    summary files
    
    open folder:
    https://www.codegrepper.com/code-examples/python/how+to+open+folder+in+python
    
    sleep:
    https://www.programiz.com/python-programming/time/sleep

[33mcommit b5c9b54abfe1aed094aea0183d56a7a3c035eaa4[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Dec 12 16:14:17 2021 +0200

    utils file

[33mcommit 52096d2d5cd5446ada8d3a1a7a51abd384df1ca4[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sun Dec 12 15:20:36 2021 +0200

    parsed, no output
    
    onnx docs:
    https://github.com/onnx/onnx/tree/master/docs
    
    model input/output dims:
    https://stackoverflow.com/questions/56734576/find-input-shape-from-onnx-file
    
    string replace:
    https://www.w3schools.com/python/ref_string_replace.asp

[33mcommit 176cd3ff5cf595db111d66a0673ce17dd3e3f9f4[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Fri Dec 10 18:58:44 2021 +0200

    tensor to onnx
    
    end2end example:
    https://github.com/onnx/tensorflow-onnx/blob/master/examples/end2end_tfhub.py
    
    cleaning after conversion:
    https://mkyong.com/python/python-how-to-delete-a-file-or-folder/

[33mcommit 19b85cad23b35f66e10183946c93e3adc9098c36[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Fri Dec 10 16:09:52 2021 +0200

    raw extract
    
    docs:
    https://github.com/onnx/onnx/blob/master/docs/IR.md#graphs
    
    how to iterate:
    https://github.com/onnx/onnx/issues/2883
    
    fabrication:
    https://note.nkmk.me/en/python-str-replace-translate-re-sub/

[33mcommit ee5da7b1df8389179e2379494437075b9fc6c240[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Fri Dec 10 11:24:10 2021 +0200

    switched to onnx
    
    better file dialog:
    https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QFileDialog.html
    
    pytorch to onnx:
    https://github.com/onnx/tutorials/blob/master/tutorials/PytorchOnnxExport.ipynb
    
    basic onnx layers iteration:
    https://stackoverflow.com/questions/52402448/how-to-read-individual-layers-weight-bias-values-from-onnx-model

[33mcommit 1e91102c30cd9612b76f80f697aa7c398be6a2ef[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu Dec 9 13:53:45 2021 +0200

    better inference examples
    
    suppress tensor warnnings:
    https://stackoverflow.com/questions/60130622/warningtensorflow-with-constraint-is-deprecated-and-will-be-removed-in-a-future
    
    handle create dir error:
    https://www.geeksforgeeks.org/create-a-directory-in-python/
    
    save/load entire model:
    https://pytorch.org/tutorials/beginner/saving_loading_models.html#save-load-entire-model

[33mcommit 6e6c7f6faf9982b60a37a5bfe967789024edb750[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu Dec 2 11:08:47 2021 +0200

    reorganized
    
    Uniform project structure and various QoL changes

[33mcommit 4e0ef9a938dafb705836e5ebee439a14a5345d91[m
Merge: a62904a f22f816
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Tue Nov 30 02:44:00 2021 +0200

    Merge branch 'extractor-gui-front' into extractor-gui

[33mcommit f22f816c4ab3349f1af9f29322d1226cf2530bed[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Tue Nov 30 02:37:40 2021 +0200

    gitignore updated

[33mcommit 9a026151f5e5957e7493ad5c777190ac37c5e0cb[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Tue Nov 30 02:36:27 2021 +0200

    general improvments
    
    easier debug (custom number of epochs), little fix and cleaner terminal:

[33mcommit 826e622f5e6c07be85627915507d3c2b3d5450fe[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Tue Nov 30 01:28:11 2021 +0200

    cleaning extra files

[33mcommit 420b62db201bfee4ffd458a8b7a1ae8dd90f6b58[m
Author: Solovic2 <islammohamed323@gmail.com>
Date:   Mon Nov 29 19:08:55 2021 +0200

    Models

[33mcommit c0b43ea720be0f5bfe3603deaccf7aa9230484dc[m
Author: Solovic2 <islammohamed323@gmail.com>
Date:   Mon Nov 29 08:11:11 2021 +0200

    Location of file from browse gui

[33mcommit a62904aea5d21b8abe673e18ea5146b92f7d5a7b[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat Nov 27 06:48:47 2021 +0200

    fixed missing import modules
    helpful:
    https://stackoverflow.com/questions/2349991/how-to-import-other-python-files

[33mcommit cceb0aaecb10b97ece042e7443f9ce176df54ca3[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat Nov 27 06:30:02 2021 +0200

    better gui shell

[33mcommit 98e3a9c724267c66c57de1e86c8e0ce689bb9056[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Sat Nov 27 00:01:23 2021 +0200

    empty gui

[33mcommit 660724fbc821f77f57d62748953a6054eb933415[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu Nov 25 06:16:38 2021 +0200

    readme added

[33mcommit 6bf65c19fda8d5e43d3ca2e910164c5816d902ab[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Thu Nov 25 05:59:29 2021 +0200

    cnn-models

[33mcommit 9dd2a55ddc1efb7dc977010259390827ccbfa167[m
Author: Ahmed Waleed <ahmedwaleed@csed22.com>
Date:   Mon Nov 22 01:20:23 2021 +0200

    raw keras model
    
    codebasics:
    https://github.com/codebasics/deep-learning-keras-tf-tutorial

[33mcommit 1c7839d99a3cdc52fa85a70300cc3192c51c8e7b[m
Author: computer-group <computer-group>
Date:   Sat Nov 20 12:11:03 2021 -0800

    clean start

[33mcommit 676ba0e302b2d0192da9345d0e111917459ba95a[m
Author: computer-group <computer-group>
Date:   Sat Nov 20 11:53:31 2021 -0800

    first commit
