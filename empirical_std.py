import numpy as np

DATA = {4.9899999999999975: 20.324971495976538, 4.979999999999997: 20.28350873121527, 4.969999999999997: 20.33391692592527, 4.959999999999997: 20.400000852096632, 4.9499999999999975: 20.436750596889482, 4.939999999999997: 20.471182854518442, 4.929999999999997: 20.52274227866968, 4.919999999999997: 20.558933998779853, 4.9099999999999975: 20.66984165106518, 4.899999999999997: 20.64430408252682, 4.889999999999997: 20.685340929765054, 4.879999999999997: 20.708733209506576, 4.869999999999997: 20.791496750521176, 4.859999999999998: 20.754348925210998, 4.849999999999997: 20.806679725344736, 4.839999999999997: 20.84591770351324, 4.829999999999997: 20.884267667951697, 4.819999999999998: 20.954350067564476, 4.809999999999997: 21.02365122565585, 4.799999999999997: 21.022218018050086, 4.789999999999997: 21.07647144703956, 4.779999999999998: 21.10516263353217, 4.769999999999997: 21.129274204460685, 4.759999999999997: 21.22418253958998, 4.749999999999997: 21.282815774229405, 4.7399999999999975: 21.274652405438488, 4.729999999999998: 21.313125153392637, 4.719999999999997: 21.359270608619973, 4.709999999999997: 21.422748175869227, 4.6999999999999975: 21.495805995817445, 4.689999999999998: 21.485847080505074, 4.679999999999997: 21.53776184486852, 4.669999999999997: 21.535728342261248, 4.6599999999999975: 21.668598740829612, 4.649999999999998: 21.625927634227867, 4.639999999999997: 21.737591699574036, 4.629999999999997: 21.768610754108188, 4.619999999999997: 21.821011298426352, 4.609999999999998: 21.82809991885781, 4.599999999999997: 21.913079823550458, 4.589999999999997: 21.947070575863332, 4.579999999999997: 21.979133020162376, 4.569999999999998: 21.989997013254683, 4.559999999999998: 22.090116011156468, 4.549999999999997: 22.119688356595063, 4.539999999999997: 22.196584128544504, 4.529999999999998: 22.19372520843056, 4.519999999999998: 22.262218344340845, 4.509999999999997: 22.324868115745907, 4.499999999999997: 22.303356273373417, 4.4899999999999975: 22.373777071015652, 4.479999999999998: 22.465090990528477, 4.469999999999997: 22.530622662118805, 4.459999999999997: 22.514073413208777, 4.4499999999999975: 22.60403067116761, 4.439999999999998: 22.634937003544596, 4.429999999999997: 22.683406873278912, 4.419999999999997: 22.673632202307175, 4.4099999999999975: 22.751089791837135, 4.399999999999998: 22.787610730204097, 4.389999999999998: 22.855383153318268, 4.379999999999997: 22.9059110406463, 4.369999999999997: 22.934380194255727, 4.359999999999998: 22.983328294019113, 4.349999999999998: 23.035740564168016, 4.339999999999997: 23.063996576365586, 4.329999999999997: 23.151394329874773, 4.319999999999998: 23.163103759074705, 4.309999999999998: 23.220916736161904, 4.299999999999997: 23.2897907871961, 4.289999999999997: 23.365000415233368, 4.279999999999998: 23.380258545902123, 4.269999999999998: 23.425881129305097, 4.259999999999998: 23.458240234671788, 4.249999999999997: 23.504717264644167, 4.2399999999999975: 23.617659481202235, 4.229999999999998: 23.62122144438867, 4.219999999999998: 23.64896790518038, 4.209999999999997: 23.674272170106104, 4.1999999999999975: 23.79612008275752, 4.189999999999998: 23.840160103438162, 4.179999999999998: 23.84869139031626, 4.169999999999997: 23.914665698515545, 4.1599999999999975: 23.947795531300354, 4.149999999999998: 24.04292561048925, 4.139999999999998: 24.043727684262944, 4.129999999999997: 24.080169151635733, 4.119999999999997: 24.18849821740056, 4.109999999999998: 24.211651919828807, 4.099999999999998: 24.324394935707822, 4.089999999999998: 24.30046657858217, 4.079999999999998: 24.383032814026787, 4.069999999999998: 24.414562735381075, 4.059999999999998: 24.44119290255598, 4.049999999999998: 24.495479055998704, 4.039999999999998: 24.572237199645894, 4.029999999999998: 24.637967316413196, 4.019999999999998: 24.702728191161125, 4.009999999999998: 24.76381886871313, 3.9999999999999982: 24.74721879037812, 3.989999999999998: 24.850200887111114, 3.979999999999998: 24.916975270089846, 3.969999999999998: 24.940860112369386, 3.959999999999998: 25.00627976168678, 3.949999999999998: 25.056806395063266, 3.939999999999998: 25.113256351817977, 3.9299999999999984: 25.186019649630936, 3.919999999999998: 25.255695427620914, 3.9099999999999984: 25.28974705006187, 3.899999999999998: 25.381075950828553, 3.8899999999999983: 25.384609640567145, 3.879999999999998: 25.450531020875104, 3.8699999999999983: 25.473798803715194, 3.859999999999998: 25.540980119727394, 3.8499999999999983: 25.661259934076597, 3.839999999999998: 25.683190311650062, 3.8299999999999983: 25.771511304988326, 3.819999999999998: 25.752344102594236, 3.8099999999999983: 25.859287694846216, 3.799999999999998: 25.926909480896555, 3.7899999999999983: 25.99124303194259, 3.779999999999998: 26.021180636021537, 3.7699999999999982: 26.075184781199248, 3.7599999999999985: 26.140792786609616, 3.7499999999999982: 26.21175209423971, 3.7399999999999984: 26.266788193717282, 3.729999999999998: 26.28532344636332, 3.7199999999999984: 26.397383200757623, 3.709999999999998: 26.462723010775782, 3.6999999999999984: 26.48443905770463, 3.689999999999998: 26.52049729549179, 3.6799999999999984: 26.597872558764188, 3.669999999999998: 26.641079796401485, 3.6599999999999984: 26.706505334339735, 3.649999999999998: 26.769407306961185, 3.6399999999999983: 26.861798673783447, 3.629999999999998: 26.895992382537717, 3.6199999999999983: 26.984851430220044, 3.6099999999999985: 27.06107682521019, 3.5999999999999983: 27.063458652838445, 3.5899999999999985: 27.14066324752094, 3.5799999999999983: 27.24875644572881, 3.5699999999999985: 27.311258524833946, 3.5599999999999983: 27.33281772910832, 3.5499999999999985: 27.383341349805022, 3.5399999999999983: 27.48489711508458, 3.5299999999999985: 27.5150231112662, 3.5199999999999982: 27.65696308720041, 3.5099999999999985: 27.679107623986475, 3.4999999999999982: 27.734307423355784, 3.4899999999999984: 27.77691249457194, 3.479999999999998: 27.8772177065765, 3.4699999999999984: 27.916533683620273, 3.4599999999999986: 27.99317527607192, 3.4499999999999984: 28.15277637713709, 3.4399999999999986: 28.184189334146506, 3.4299999999999984: 28.170986917671833, 3.4199999999999986: 28.263400630876465, 3.4099999999999984: 28.382280970004018, 3.3999999999999986: 28.355766177673623, 3.3899999999999983: 28.453295009702387, 3.3799999999999986: 28.56102938490059, 3.3699999999999983: 28.63482842480279, 3.3599999999999985: 28.630907424313207, 3.3499999999999983: 28.706798495674153, 3.3399999999999985: 28.814094110083527, 3.3299999999999983: 28.893280434796758, 3.3199999999999985: 28.917768252003103, 3.3099999999999983: 29.017580410825648, 3.2999999999999985: 29.073168814546516, 3.2899999999999987: 29.195965548902578, 3.2799999999999985: 29.256881058504927, 3.2699999999999987: 29.35534706883957, 3.2599999999999985: 29.371206675309153, 3.2499999999999987: 29.464794557999127, 3.2399999999999984: 29.52740621349269, 3.2299999999999986: 29.628354847276494, 3.2199999999999984: 29.687529095954105, 3.2099999999999986: 29.731422055000547, 3.1999999999999984: 29.81558316133947, 3.1899999999999986: 29.900110834894562, 3.1799999999999984: 29.979866254642516, 3.1699999999999986: 30.053807336762333, 3.1599999999999984: 30.150486630272383, 3.1499999999999986: 30.21142824547844, 3.1399999999999983: 30.253607165402048, 3.1299999999999986: 30.399593598359242, 3.1199999999999988: 30.421598896366856, 3.1099999999999985: 30.537096945925136, 3.0999999999999988: 30.603580669661365, 3.0899999999999985: 30.67188591195346, 3.0799999999999987: 30.73808759185645, 3.0699999999999985: 30.843970029437745, 3.0599999999999987: 30.9076169026028, 3.0499999999999985: 31.051108500810386, 3.0399999999999987: 31.09422483213629, 3.0299999999999985: 31.174737788131726, 3.0199999999999987: 31.304768711749436, 3.0099999999999985: 31.287463198630793, 2.9999999999999987: 31.391408841643734, 2.9899999999999984: 31.482016988270832, 2.9799999999999986: 31.560384329368503, 2.969999999999999: 31.648091255627918, 2.9599999999999986: 31.751355843659518, 2.949999999999999: 31.83989189570033, 2.9399999999999986: 31.91560619900562, 2.929999999999999: 32.02359975005449, 2.9199999999999986: 32.04186270214681, 2.909999999999999: 32.17941405209066, 2.8999999999999986: 32.278447872296084, 2.889999999999999: 32.39427586898165, 2.8799999999999986: 32.424749254209345, 2.8699999999999988: 32.589676865287814, 2.8599999999999985: 32.64815934942128, 2.8499999999999988: 32.758339796192985, 2.8399999999999985: 32.808770786269825, 2.8299999999999987: 32.90588800357789, 2.819999999999999: 33.01271072491623, 2.8099999999999987: 33.09827176513153, 2.799999999999999: 33.22657978722611, 2.7899999999999987: 33.24078316718566, 2.779999999999999: 33.42785437784449, 2.7699999999999987: 33.496389048966996, 2.759999999999999: 33.531337726501334, 2.7499999999999987: 33.68300554616227, 2.739999999999999: 33.747439091985335, 2.7299999999999986: 33.850154170122956, 2.719999999999999: 33.96399138778469, 2.7099999999999986: 34.08949377092119, 2.699999999999999: 34.189154427546256, 2.6899999999999986: 34.27099348675574, 2.679999999999999: 34.44433542805662, 2.6699999999999986: 34.51057465795949, 2.659999999999999: 34.61982855386429, 2.649999999999999: 34.71647360296351, 2.639999999999999: 34.82370503819638, 2.629999999999999: 34.88911789003001, 2.6199999999999988: 35.00637474278394, 2.609999999999999: 35.123163984498056, 2.5999999999999988: 35.224818499004385, 2.589999999999999: 35.387941003884876, 2.5799999999999987: 35.49052197387215, 2.569999999999999: 35.58480798823976, 2.5599999999999987: 35.65118617150604, 2.549999999999999: 35.86705192420126, 2.5399999999999987: 35.935436989072535, 2.529999999999999: 36.04432875970576, 2.5199999999999987: 36.197456132315416, 2.509999999999999: 36.28281692136725, 2.4999999999999987: 36.434846595110926, 2.489999999999999: 36.56070497940781, 2.479999999999999: 36.59976700298795, 2.469999999999999: 36.797613759261516, 2.459999999999999: 36.94260587959248, 2.449999999999999: 37.0565751833609, 2.439999999999999: 37.14426671838635, 2.429999999999999: 37.23652104929372, 2.419999999999999: 37.398629388589306, 2.409999999999999: 37.56534397519862, 2.399999999999999: 37.63218139484692, 2.389999999999999: 37.7946683930241, 2.379999999999999: 37.90522953783396, 2.3699999999999988: 38.114270005514456, 2.359999999999999: 38.12437191462032, 2.3499999999999988: 38.33846715340657, 2.339999999999999: 38.470088897661256, 2.329999999999999: 38.621598457729164, 2.319999999999999: 38.71146997709629, 2.309999999999999: 38.895666639319494, 2.299999999999999: 39.009563698482395, 2.289999999999999: 39.143677622872445, 2.279999999999999: 39.37098573458973, 2.269999999999999: 39.48262502368981, 2.259999999999999: 39.54881727086831, 2.249999999999999: 39.75653440342579, 2.239999999999999: 39.95534314128607, 2.229999999999999: 40.07766215621161, 2.219999999999999: 40.269115084249634, 2.209999999999999: 40.39605470678614, 2.199999999999999: 40.558352707484474, 2.189999999999999: 40.701603788709456, 2.1799999999999993: 40.989734883871826, 2.169999999999999: 41.04244207966787, 2.1599999999999993: 41.198013006406384, 2.149999999999999: 41.4119869560475, 2.1399999999999992: 41.52134585394411, 2.129999999999999: 41.73254495234904, 2.119999999999999: 41.89096618630312, 2.109999999999999: 42.063586840767776, 2.099999999999999: 42.283100921870385, 2.089999999999999: 42.3333044126331, 2.079999999999999: 42.52584995160393, 2.069999999999999: 42.80166015069605, 2.059999999999999: 42.976263161697, 2.049999999999999: 43.1340132951906, 2.039999999999999: 43.361363087729075, 2.029999999999999: 43.54059810999848, 2.019999999999999: 43.725215914754585, 2.009999999999999: 43.8746017071495, 1.9999999999999991: 44.12977799914575, 1.989999999999999: 44.21317170513953, 1.979999999999999: 44.52693073606584, 1.969999999999999: 44.665331332297384, 1.959999999999999: 44.87016043721281, 1.949999999999999: 45.051864166401046, 1.939999999999999: 45.27315701395312, 1.9299999999999993: 45.50439884656565, 1.9199999999999993: 45.72372504934212, 1.9099999999999993: 45.94818520682173, 1.8999999999999992: 46.12917691955439, 1.8899999999999992: 46.33813773461449, 1.8799999999999992: 46.602439085277766, 1.8699999999999992: 46.79349132264134, 1.8599999999999992: 47.02117524386971, 1.8499999999999992: 47.2689357947715, 1.8399999999999992: 47.49703143961013, 1.8299999999999992: 47.70559098697463, 1.8199999999999992: 48.03164751938428, 1.8099999999999992: 48.17436800152833, 1.7999999999999992: 48.45827370825286, 1.7899999999999991: 48.6434134283136, 1.7799999999999994: 48.92476605109027, 1.7699999999999994: 49.15471961202262, 1.7599999999999993: 49.39886550187316, 1.7499999999999993: 49.68030957008507, 1.7399999999999993: 49.929693218291035, 1.7299999999999993: 50.222686641597654, 1.7199999999999993: 50.47011903500594, 1.7099999999999993: 50.727559427826826, 1.6999999999999993: 51.03598896394891, 1.6899999999999993: 51.29859988582965, 1.6799999999999993: 51.58661475164081, 1.6699999999999993: 51.795235490720046, 1.6599999999999993: 52.10537348619936, 1.6499999999999992: 52.44148660203416, 1.6399999999999992: 52.66524270876716, 1.6299999999999992: 53.05251037924331, 1.6199999999999992: 53.20361390698343, 1.6099999999999994: 53.55661756433093, 1.5999999999999994: 53.85758323608194, 1.5899999999999994: 54.19183700515097, 1.5799999999999994: 54.479387119722496, 1.5699999999999994: 54.794789471480755, 1.5599999999999994: 55.07681113505619, 1.5499999999999994: 55.37383773916333, 1.5399999999999994: 55.70130343980323, 1.5299999999999994: 55.97465931306621, 1.5199999999999994: 56.32470450472281, 1.5099999999999993: 56.67416332150933, 1.4999999999999993: 57.01649320368844, 1.4899999999999993: 57.432621092366205, 1.4799999999999993: 57.79242875433172, 1.4699999999999993: 58.110881648372775, 1.4599999999999995: 58.39084254637366, 1.4499999999999995: 58.69270971559377, 1.4399999999999995: 59.08469679533703, 1.4299999999999995: 59.45925483144187, 1.4199999999999995: 59.78987367156203, 1.4099999999999995: 60.28405691589227, 1.3999999999999995: 60.586616951381146, 1.3899999999999995: 60.925951633873524, 1.3799999999999994: 61.33197419056096, 1.3699999999999994: 61.74202110504092, 1.3599999999999994: 62.107065580119446, 1.3499999999999994: 62.51649630081741, 1.3399999999999994: 62.837479392474776, 1.3299999999999994: 63.352791865545086, 1.3199999999999994: 63.69311955002433, 1.3099999999999994: 64.05614787977491, 1.2999999999999994: 64.53331447789274, 1.2899999999999996: 64.98255757465658, 1.2799999999999996: 65.31244767900225, 1.2699999999999996: 65.72310343854129, 1.2599999999999996: 66.19593053951628, 1.2499999999999996: 66.62049412123459, 1.2399999999999995: 67.05921548673066, 1.2299999999999995: 67.49168128495734, 1.2199999999999995: 67.89254212841648, 1.2099999999999995: 68.3987065801292, 1.1999999999999995: 68.83495676907103, 1.1899999999999995: 69.26792030785575, 1.1799999999999995: 69.80618760191786, 1.1699999999999995: 70.27606216837944, 1.1599999999999995: 70.78995383091298, 1.1499999999999995: 71.13154999714948, 1.1399999999999997: 71.70528784461433, 1.1299999999999997: 72.14541009875575, 1.1199999999999997: 72.6486958626259, 1.1099999999999997: 73.12485871079237, 1.0999999999999996: 73.65078174555238, 1.0899999999999996: 74.18247723758705, 1.0799999999999996: 74.70336532044593, 1.0699999999999996: 75.24439107872577, 1.0599999999999996: 75.7837348318169, 1.0499999999999996: 76.2126106780057, 1.0399999999999996: 76.78112025043288, 1.0299999999999996: 77.33194856980376, 1.0199999999999996: 77.80121812265624, 1.0099999999999996: 78.37615294930715, 0.9999999999999996: 78.98346433093138, 0.9899999999999995: 79.45663831722119, 0.9799999999999995: 80.01249618189213, 0.9699999999999995: 80.64530269810629, 0.9599999999999995: 81.28591067702487, 0.9499999999999995: 81.78339420912143, 0.9399999999999996: 82.31173206601007, 0.9299999999999996: 82.86795641232465, 0.9199999999999996: 83.56385220478242, 0.9099999999999996: 84.09104601550503, 0.8999999999999996: 84.79798753014501, 0.8899999999999996: 85.40572440390939, 0.8799999999999996: 85.9320858822865, 0.8699999999999996: 86.6059077251059, 0.8599999999999995: 87.19459487219473, 0.8499999999999996: 87.91120491148168, 0.8399999999999996: 88.45966256928779, 0.8299999999999996: 89.09229186597445, 0.8199999999999996: 89.75284325709026, 0.8099999999999996: 90.3025165682527, 0.7999999999999996: 91.12817240722889, 0.7899999999999996: 91.62330290123327, 0.7799999999999997: 92.31047216355581, 0.7699999999999997: 93.0139063492343, 0.7599999999999997: 93.65304535953317, 0.7499999999999997: 94.51969426447066, 0.7399999999999997: 95.20645124883265, 0.7299999999999996: 95.82661176300724, 0.7199999999999996: 96.59944091494016, 0.7099999999999996: 97.2174471878876, 0.6999999999999996: 98.12868141923083, 0.6899999999999997: 98.79265514646816, 0.6799999999999997: 99.61915156085675, 0.6699999999999997: 100.33603395011363, 0.6599999999999997: 101.20982947234707, 0.6499999999999997: 101.85196761021774, 0.6399999999999997: 102.81175961392235, 0.6299999999999997: 103.62813019002441, 0.6199999999999998: 104.50601349817642, 0.6099999999999998: 105.39818960960517, 0.5999999999999998: 106.21329281848705, 0.5899999999999997: 107.18833099286883, 0.5799999999999997: 108.16355690652746, 0.5699999999999997: 108.92306572628576, 0.5599999999999997: 109.96120222061761, 0.5499999999999998: 110.82471684035366, 0.5399999999999998: 111.89849428699353, 0.5299999999999998: 112.95104603543292, 0.5199999999999998: 114.02541559841272, 0.5099999999999998: 115.05258807671355, 0.4999999999999998: 116.07173058311159, 0.48999999999999977: 117.16689956633144, 0.47999999999999976: 118.28771789697983, 0.46999999999999986: 119.4368626007081, 0.45999999999999985: 120.55786563857941, 0.44999999999999984: 121.80165887269163, 0.43999999999999984: 123.01371147409577, 0.4299999999999998: 124.22518990285356, 0.4199999999999998: 125.45479584936265, 0.4099999999999998: 126.73925021250993, 0.3999999999999998: 127.94232375474407, 0.3899999999999999: 129.31323135074632, 0.3799999999999999: 130.6054588929998, 0.3699999999999999: 131.96917497410251, 0.3599999999999999: 133.47436248929475, 0.34999999999999987: 134.79554223138393, 0.33999999999999986: 136.34825810724993, 0.32999999999999985: 137.86314239777286, 0.3199999999999999: 139.38442774472585, 0.30999999999999994: 141.02493206863028, 0.29999999999999993: 142.5613021641079, 0.2899999999999999: 144.29451423162132, 0.2799999999999999: 145.9986431821561, 0.2699999999999999: 147.78043207144327, 0.2599999999999999: 149.5542951230167, 0.24999999999999992: 151.39535590485985, 0.23999999999999994: 153.2951720331066, 0.22999999999999995: 155.04945522527473, 0.21999999999999995: 156.8325304915085, 0.20999999999999996: 158.6269892017982, 0.19999999999999996: 160.2144038646354, 0.18999999999999995: 161.71714393856146, 0.17999999999999997: 163.06498400499498, 0.16999999999999998: 164.18157136363638, 0.15999999999999998: 165.1596903636364, 0.14999999999999997: 165.83030163636366, 0.13999999999999999: 166.37413713636366, 0.13: 166.69243154545455, 0.12: 166.87837845454544, 0.11: 166.956914, 0.1: 166.989145}


def find_closest_values(y_val):
    lower = None
    higher = None
    for x, y in DATA.items():
        if y < y_val:
            lower = (x, y)
        elif y > y_val and higher is None:
            higher = (x, y)
            break

    return lower, higher

def interpolate(y_val, lower, higher):
    if lower is None or higher is None:
        return None
    x1, y1 = lower
    x2, y2 = higher
    return x1 + (x2 - x1) * ((y_val - y1) / (y2 - y1))

def emperical_std(average):
    lower, higher = find_closest_values(average)
    return interpolate(average, lower, higher)


# new_y = np.linspace(20, 167, 10000)

# estimated_x_values = []
# for val in new_y:
#     estimated_x = emperical_std(val, data)
#     estimated_x_values.append(estimated_x)

# Plot the best fitting model
# plt.figure(figsize=(10, 5))
# plt.plot(estimated_x_values, new_y, label='Estimated')
# plt.plot(np.array(list(data.keys())), np.array(list(data.values())), label='Data Points')
# plt.title('Best Fit Model')
# plt.legend()
# plt.show()

