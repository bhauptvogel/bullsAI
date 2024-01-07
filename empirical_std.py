import numpy as np

DATA = {5.0: 20.26879062704435, 4.9901803607214426: 20.250455264088615, 4.980360721442886: 20.270966503463814, 4.9705410821643286: 20.34972561010018, 4.960721442885771: 20.340785257994064, 4.9509018036072145: 20.434128395196836, 4.941082164328657: 20.42570883309326, 4.9312625250501005: 20.42957491519701, 4.921442885771543: 20.52260370865486, 4.911623246492986: 20.630835209284385, 4.901803607214429: 20.598531462255014, 4.891983967935872: 20.634269186117173, 4.882164328657314: 20.71590752807776, 4.872344689378758: 20.730983705494307, 4.8625250501002: 20.7548983486987, 4.852705410821644: 20.810069162019683, 4.842885771543086: 20.86590575583141, 4.833066132264529: 20.93915349634097, 4.823246492985972: 20.94354202229861, 4.813426853707415: 20.9339493483515, 4.803607214428857: 20.996804781296664, 4.793787575150301: 21.115765688657113, 4.783967935871743: 21.11599360806553, 4.774148296593187: 21.136783359630503, 4.764328657314629: 21.10625747330653, 4.754509018036072: 21.218169057242065, 4.744689378757515: 21.244104687528218, 4.734869739478958: 21.272940664909935, 4.7250501002004: 21.306891273270907, 4.715230460921844: 21.356740324509833, 4.705410821643286: 21.415374991045326, 4.69559118236473: 21.503453842075295, 4.685771543086172: 21.55062588106535, 4.675951903807615: 21.558003212192446, 4.666132264529058: 21.572393476357583, 4.656312625250501: 21.58867024747022, 4.6464929859719435: 21.64017313323584, 4.636673346693387: 21.74176324879717, 4.6268537074148295: 21.80666386899628, 4.617034068136273: 21.865510079397097, 4.6072144288577155: 21.82588362950737, 4.597394789579158: 21.882352461215387, 4.5875751503006015: 21.953032976524266, 4.577755511022044: 21.979865667374547, 4.567935871743487: 22.01353287026342, 4.55811623246493: 22.056484375379814, 4.548296593186373: 22.082409909384445, 4.538476953907816: 22.109244234617112, 4.528657314629259: 22.184700894802987, 4.518837675350701: 22.308996347049703, 4.509018036072145: 22.307290082417186, 4.499198396793587: 22.329943694531792, 4.48937875751503: 22.405126980127314, 4.479559118236473: 22.39267014695588, 4.469739478957916: 22.447272510997305, 4.459919839679358: 22.466131495720525, 4.450100200400802: 22.57136612288932, 4.440280561122244: 22.56564783931267, 4.430460921843688: 22.64342417560665, 4.42064128256513: 22.692309754326775, 4.410821643286573: 22.74461336915448, 4.401002004008016: 22.807230386588284, 4.391182364729459: 22.875414456875593, 4.381362725450902: 22.90368982135037, 4.371543086172345: 22.943149624174087, 4.361723446893787: 22.97137872312188, 4.351903807615231: 23.006889564910107, 4.342084168336673: 23.033857448672055, 4.332264529058116: 23.152799665709498, 4.322444889779559: 23.109413746465254, 4.312625250501002: 23.180004624763246, 4.302805611222444: 23.306842049235293, 4.292985971943888: 23.29918061714764, 4.28316633266533: 23.31552294534031, 4.273346693386774: 23.354528814942856, 4.263527054108216: 23.40652559513202, 4.253707414829659: 23.487435554754352, 4.243887775551102: 23.550746026987795, 4.234068136272545: 23.554278786215043, 4.224248496993988: 23.615337931210895, 4.214428857715431: 23.672584609137747, 4.2046092184368735: 23.705461075915856, 4.194789579158317: 23.804153429966142, 4.1849699398797595: 23.84226668547888, 4.175150300601202: 23.87089124078417, 4.1653306613226455: 23.922445773416957, 4.155511022044088: 24.0123869511352, 4.145691382765531: 23.983005146553346, 4.135871743486974: 24.089355075664553, 4.126052104208417: 24.18368966802973, 4.11623246492986: 24.153774094779223, 4.106412825651303: 24.214257201127065, 4.096593186372745: 24.340239552586326, 4.086773547094189: 24.330399675858533, 4.076953907815631: 24.375256484586092, 4.067134268537075: 24.449637555397654, 4.057314629258517: 24.538560054380586, 4.04749498997996: 24.56279789046197, 4.037675350701402: 24.573750094761206, 4.027855711422846: 24.70087403112253, 4.018036072144288: 24.702081417860146, 4.008216432865732: 24.750125559074174, 3.9983967935871743: 24.77491750907773, 3.9885771543086173: 24.869592550473413, 3.9787575150300603: 24.863543531238996, 3.968937875751503: 24.875587439478487, 3.959118236472946: 24.991126468018876, 3.949298597194389: 25.077815692062174, 3.9394789579158314: 25.140865175981745, 3.929659318637275: 25.19214320725407, 3.9198396793587174: 25.226668773638547, 3.9100200400801604: 25.243846221757284, 3.9002004008016034: 25.389705994022265, 3.890380761523046: 25.312128776758374, 3.880561122244489: 25.429018546439792, 3.870741482965932: 25.44371120635979, 3.8609218436873745: 25.567577206223262, 3.851102204408818: 25.58567664480994, 3.8412825651302605: 25.60173763341342, 3.8314629258517034: 25.674161794685904, 3.8216432865731464: 25.799740143173537, 3.811823647294589: 25.78428569197702, 3.802004008016032: 25.9340206030186, 3.792184368737475: 25.958880291778897, 3.7823647294589176: 26.037883012472484, 3.772545090180361: 26.0966535016526, 3.7627254509018035: 26.108099850649022, 3.7529058116232465: 26.14053044726164, 3.7430861723446895: 26.231358635255162, 3.733266533066132: 26.3428054021859, 3.723446893787575: 26.287034864105102, 3.713627254509018: 26.397410798503213, 3.7038076152304606: 26.44348992654494, 3.6939879759519036: 26.545662343767184, 3.6841683366733466: 26.5604592072066, 3.674348697394789: 26.550185457885313, 3.6645290581162326: 26.685769263593173, 3.654709418837675: 26.75618295921324, 3.644889779559118: 26.760880708801093, 3.635070140280561: 26.78701909727213, 3.6252505010020037: 26.96430225355012, 3.6154308617234467: 27.021033537208513, 3.6056112224448897: 27.106852939635214, 3.5957915831663323: 27.127946707285936, 3.5859719438877757: 27.155923627678938, 3.5761523046092183: 27.277573779976304, 3.5663326653306613: 27.291762207573132, 3.5565130260521043: 27.319141417200107, 3.546693386773547: 27.47830920919138, 3.53687374749499: 27.496295486258454, 3.527054108216433: 27.55383941846531, 3.5172344689378754: 27.571827393723233, 3.507414829659319: 27.686145523432305, 3.4975951903807614: 27.718993203981743, 3.4877755511022044: 27.788642140776446, 3.4779559118236474: 27.86864205347718, 3.46813627254509: 27.92305653529125, 3.458316633266533: 28.015439157817575, 3.448496993987976: 28.119922265252836, 3.4386773547094185: 28.132173480577652, 3.428857715430862: 28.226735378503612, 3.4190380761523045: 28.312297167437066, 3.4092184368737475: 28.3439757048755, 3.3993987975951905: 28.406143018040623, 3.389579158316633: 28.456765731787794, 3.379759519038076: 28.45752836990986, 3.369939879759519: 28.60229825760636, 3.3601202404809616: 28.669230310653866, 3.350300601202405: 28.716565669824575, 3.3404809619238476: 28.713928447127877, 3.3306613226452906: 28.9173440814745, 3.3208416833667336: 28.966206195000726, 3.311022044088176: 28.9542578852687, 3.301202404809619: 29.015620304350616, 3.291382765531062: 29.155312361254023, 3.2815631262525047: 29.21607835346477, 3.271743486973948: 29.31562423351962, 3.2619238476953907: 29.33006139281437, 3.2521042084168337: 29.39624371412502, 3.2422845691382767: 29.54111065707766, 3.2324649298597192: 29.568900363012354, 3.2226452905811622: 29.649519258660284, 3.2128256513026052: 29.644781796669307, 3.2030060120240478: 29.785746805643328, 3.193186372745491: 29.842649696400365, 3.1833667334669338: 29.951262677992972, 3.1735470941883768: 30.0602569471149, 3.1637274549098198: 30.064406384460124, 3.1539078156312623: 30.166907534567578, 3.1440881763527053: 30.24314321102723, 3.1342685370741483: 30.300851497867164, 3.124448897795591: 30.401147782838233, 3.114629258517034: 30.508964052905952, 3.104809619238477: 30.527630942566912, 3.0949899799599194: 30.62501791855838, 3.085170340681363: 30.72050526761911, 3.0753507014028054: 30.82009457900675, 3.0655310621242484: 30.878726714878542, 3.0557114228456914: 30.98130953720455, 3.045891783567134: 30.975034625624986, 3.036072144288577: 31.073322255949886, 3.02625250501002: 31.172161193951894, 3.0164328657314625: 31.248667986552334, 3.006613226452906: 31.23929468349129, 2.9967935871743485: 31.475622491408814, 2.9869739478957915: 31.542056450766808, 2.9771543086172345: 31.600682479423188, 2.967334669338677: 31.679318227682806, 2.95751503006012: 31.740317986520395, 2.947695390781563: 31.9046903880791, 2.937875751503006: 31.92896142217306, 2.9280561122244486: 31.965441856053985, 2.9182364729458916: 32.013730755540394, 2.9084168336673346: 32.16291174228023, 2.8985971943887776: 32.22393108160358, 2.88877755511022: 32.37067851520833, 2.878957915831663: 32.416709919323736, 2.869138276553106: 32.53655059793129, 2.859318637274549: 32.664914683514326, 2.8494989979959917: 32.680692506946585, 2.8396793587174347: 32.806886752622965, 2.8298597194388777: 32.91612665739738, 2.8200400801603207: 32.99038092597234, 2.8102204408817633: 33.128509728331885, 2.8004008016032063: 33.23381675408908, 2.7905811623246493: 33.2658303232421, 2.7807615230460923: 33.343585921963, 2.770941883767535: 33.48091859718671, 2.761122244488978: 33.57054910493085, 2.751302605210421: 33.65927017707265, 2.741482965931864: 33.70189019216709, 2.7316633266533064: 33.847711638694335, 2.7218436873747494: 33.98775297626031, 2.7120240480961924: 34.04099366957804, 2.7022044088176354: 34.20407021285734, 2.692384769539078: 34.24046754018833, 2.682565130260521: 34.39522281416247, 2.672745490981964: 34.495378887858635, 2.662925851703407: 34.56008317740669, 2.6531062124248495: 34.644077636947685, 2.6432865731462925: 34.788881651184255, 2.6334669338677354: 34.91039122733457, 2.6236472945891784: 35.0019525507673, 2.613827655310621: 35.11696921468797, 2.604008016032064: 35.18504383961924, 2.594188376753507: 35.25291198729937, 2.58436873747495: 35.47474641436217, 2.5745490981963925: 35.50539388893969, 2.5647294589178355: 35.6098130947768, 2.5549098196392785: 35.74441530588725, 2.5450901803607215: 35.84880954333584, 2.535270541082164: 36.039558865005084, 2.525450901803607: 36.12161968830674, 2.51563126252505: 36.22990485420208, 2.505811623246493: 36.28492690840889, 2.4959919839679356: 36.44507923692334, 2.4861723446893786: 36.50590015289324, 2.4763527054108216: 36.73796809644951, 2.466533066132264: 36.83693198824928, 2.456713426853707: 36.85744279328573, 2.44689378757515: 37.10057226541481, 2.437074148296593: 37.134379977945294, 2.4272545090180357: 37.31311148254407, 2.4174348697394787: 37.45851851664611, 2.4076152304609217: 37.516283572062704, 2.3977955911823647: 37.679428302443654, 2.3879759519038073: 37.823341817797576, 2.3781563126252503: 37.97126353689658, 2.3683366733466933: 38.01069261454224, 2.3585170340681363: 38.24509532824102, 2.348697394789579: 38.31580235092787, 2.338877755511022: 38.474651475270264, 2.329058116232465: 38.65193855024105, 2.319238476953908: 38.75082271516513, 2.3094188376753504: 38.90757676508061, 2.2995991983967934: 39.11980443198063, 2.2897795591182364: 39.21474507373082, 2.2799599198396794: 39.29511035804446, 2.270140280561122: 39.52101246073559, 2.260320641282565: 39.60259844050312, 2.250501002004008: 39.7790789160652, 2.240681362725451: 39.94616981918842, 2.2308617234468935: 40.0651934499548, 2.2210420841683365: 40.175828753683, 2.2112224448897795: 40.31985146563558, 2.2014028056112225: 40.5248357539319, 2.191583166332665: 40.76561508416485, 2.181763527054108: 40.88595004953945, 2.171943887775551: 41.02236473984756, 2.162124248496994: 41.23530177021662, 2.1523046092184366: 41.3879411986386, 2.1424849699398796: 41.45813839666702, 2.1326653306613226: 41.735890761010104, 2.1228456913827656: 41.88003913750933, 2.113026052104208: 42.00962716994899, 2.103206412825651: 42.231361100298486, 2.093386773547094: 42.38076097700493, 2.083567134268537: 42.60371093406461, 2.0737474949899797: 42.67353390430422, 2.0639278557114227: 42.83922376220263, 2.0541082164328657: 43.16291372948523, 2.0442885771543087: 43.237495432809155, 2.0344689378757512: 43.40818961853062, 2.0246492985971942: 43.6973410318186, 2.0148296593186372: 43.880322124318376, 2.00501002004008: 44.043431239802594, 1.9951903807615228: 44.21533378505918, 1.9853707414829658: 44.32028252248525, 1.9755511022044088: 44.60335362590174, 1.9657314629258518: 44.86298881195259, 1.9559118236472943: 45.03925841821447, 1.9460921843687373: 45.19679646140023, 1.9362725450901803: 45.338479612987, 1.9264529058116233: 45.66122076376451, 1.9166332665330659: 45.79390798803249, 1.9068136272545089: 46.13314106139064, 1.8969939879759519: 46.279272036517334, 1.8871743486973949: 46.420191791674476, 1.8773547094188374: 46.74782007247483, 1.8675350701402804: 46.89879075950357, 1.8577154308617234: 47.13654244418093, 1.847895791583166: 47.390098436596084, 1.838076152304609: 47.6169386172578, 1.828256513026052: 47.82652610442046, 1.818436873747495: 48.04828219873153, 1.8086172344689375: 48.40912074238142, 1.7987975951903805: 48.52473227215276, 1.7889779559118235: 48.708007946688255, 1.7791583166332665: 49.052854173149235, 1.769338677354709: 49.257309554388, 1.759519038076152: 49.56802446592571, 1.749699398797595: 49.674446257409585, 1.739879759519038: 50.00928277803061, 1.7300601202404806: 50.311477792164276, 1.7202404809619236: 50.47858391476263, 1.7104208416833666: 50.87927699680391, 1.7006012024048096: 51.144093128264586, 1.6907815631262522: 51.35323764464575, 1.6809619238476952: 51.58430272928352, 1.6711422845691382: 51.919034388723745, 1.6613226452905812: 52.18483518940889, 1.6515030060120237: 52.516736905585155, 1.6416833667334667: 52.67838900231087, 1.6318637274549097: 53.01700787364786, 1.6220440881763527: 53.38560139014495, 1.6122244488977953: 53.46721619483146, 1.6024048096192383: 53.89742415647774, 1.5925851703406813: 54.17216544717583, 1.5827655310621243: 54.546154948580266, 1.5729458917835668: 54.692556175247816, 1.5631262525050098: 55.06157348679588, 1.5533066132264528: 55.388883598438206, 1.5434869739478958: 55.76021556953127, 1.5336673346693384: 55.94289687477355, 1.5238476953907814: 56.26252831972912, 1.5140280561122244: 56.752199028226684, 1.5042084168336673: 57.044171126783034, 1.49438877755511: 57.39769634032289, 1.484569138276553: 57.72457374441329, 1.474749498997996: 58.09913874977785, 1.464929859719439: 58.3436563326455, 1.4551102204408815: 58.80206637516408, 1.4452905811623245: 59.14539562887599, 1.4354709418837674: 59.41519815596004, 1.4256513026052104: 59.76499048280721, 1.415831663326653: 60.15927340337886, 1.406012024048096: 60.57527058577694, 1.396192384769539: 60.75467643525757, 1.386372745490982: 61.27627285549674, 1.3765531062124245: 61.579203029856316, 1.3667334669338675: 61.906247921792676, 1.3569138276553105: 62.37166865674654, 1.3470941883767535: 62.73048211536893, 1.337274549098196: 63.12422929834477, 1.327454909819639: 63.40719097814985, 1.317635270541082: 63.97859644025227, 1.307815631262525: 64.36258682606382, 1.2979959919839676: 64.78827198727156, 1.2881763527054106: 65.13493033850327, 1.2783567134268536: 65.61521207803449, 1.2685370741482966: 66.12482692980178, 1.2587174348697392: 66.45915488352198, 1.2488977955911822: 66.93653803755643, 1.2390781563126252: 67.2953257192154, 1.2292585170340677: 67.73714078728686, 1.2194388777555107: 68.088938032203, 1.2096192384769537: 68.63137003503178, 1.1997995991983967: 69.11005002163428, 1.1899799599198393: 69.59402493497004, 1.1801603206412823: 69.95621977241706, 1.1703406813627253: 70.56924900442431, 1.1605210420841683: 70.97344225811895, 1.1507014028056108: 71.40029469799367, 1.1408817635270538: 71.78887916220314, 1.1310621242484968: 72.34024184749417, 1.1212424849699398: 72.86422269808068, 1.1114228456913824: 73.28450242799343, 1.1016032064128254: 73.85543215477514, 1.0917835671342684: 74.48054588296023, 1.0819639278557114: 74.91265448275882, 1.072144288577154: 75.41621718121624, 1.062324649298597: 75.82601732038569, 1.05250501002004: 76.2991256163437, 1.042685370741483: 76.85040566509005, 1.0328657314629255: 77.45741621440877, 1.0230460921843685: 77.9954654554786, 1.0132264529058115: 78.52845911397365, 1.0034068136272545: 79.0018689609285, 0.993587174348697: 79.67154145359409, 0.9837675350701405: 80.02787120982502, 0.973947895791583: 80.71073932540392, 0.9641282565130256: 81.19977467474227, 0.954308617234469: 81.84835032019282, 0.9444889779559116: 82.26137958576078, 0.9346693386773541: 82.9431580862959, 0.9248496993987976: 83.61681220220744, 0.9150300601202401: 84.07656502927185, 0.9052104208416836: 84.6341943826184, 0.8953907815631261: 85.25863461115374, 0.8855711422845687: 85.82495217567971, 0.8757515030060121: 86.44021421522575, 0.8659318637274547: 87.01675449874703, 0.8561122244488972: 87.63181595554052, 0.8462925851703407: 88.25215924319772, 0.8364729458917832: 88.83294784377468, 0.8266533066132267: 89.48212577134622, 0.8168336673346692: 90.18671018295154, 0.8070140280561118: 90.67379997654194, 0.7971943887775552: 91.34633992796326, 0.7873747494989978: 92.03937585111845, 0.7775551102204403: 92.75701189560368, 0.7677354709418838: 93.34166870013806, 0.7579158316633263: 93.977416298861, 0.7480961923847698: 94.62187626255209, 0.7382765531062123: 95.39756537282626, 0.7284569138276549: 96.06275820128809, 0.7186372745490983: 96.7289665765782, 0.7088176352705409: 97.35443102554264, 0.6989979959919834: 98.16359616620684, 0.6891783567134269: 98.95860080220696, 0.6793587174348694: 99.54911488801804, 0.6695390781563129: 100.22428295857597, 0.6597194388777554: 101.07745130564395, 0.649899799599198: 101.93594961372254, 0.6400801603206414: 102.70704671595983, 0.630260521042084: 103.39586251945288, 0.6204408817635265: 104.254596377109, 0.61062124248497: 105.20963090672178, 0.6008016032064125: 105.84347790089046, 0.5909819639278551: 106.80540177765899, 0.5811623246492985: 107.62078404728621, 0.5713426853707411: 108.53491201305269, 0.5615230460921845: 109.42559636919503, 0.5517034068136271: 110.29286238321066, 0.5418837675350696: 111.37838585759953, 0.5320641282565131: 112.21539387216292, 0.5222444889779556: 113.2415792342386, 0.5124248496993982: 114.16030657059645, 0.5026052104208416: 115.30232353637356, 0.49278557114228416: 116.31119637580089, 0.4829659318637276: 117.40234626691846, 0.47314629258517016: 118.46160718046234, 0.4633266533066127: 119.54321926098429, 0.45350701402805615: 120.58025782823904, 0.4436873747494987: 121.7333424315302, 0.43386773547094126: 122.9779948689476, 0.4240480961923847: 124.25684643184445, 0.41422845691382726: 125.470717415575, 0.4044088176352707: 126.66037416318652, 0.39458917835671325: 128.0745997239262, 0.3847695390781558: 129.3351648912875, 0.37494989979959925: 130.92719428864714, 0.3651302605210418: 132.1601738243026, 0.35531062124248436: 133.73539209282433, 0.3454909819639278: 135.1496644500035, 0.33567134268537036: 136.55992786283142, 0.3258517034068138: 138.18927192542753, 0.31603206412825635: 139.8159077728301, 0.3062124248496989: 141.5354603073397, 0.29639278557114235: 143.12167231158548, 0.2865731462925849: 144.85824662065875, 0.27675350701402746: 146.51487711116823, 0.2669338677354709: 148.41244955044954, 0.25711422845691345: 150.00074364488452, 0.2472945891783569: 151.94763334465534, 0.23747494989979945: 153.6876081798202, 0.227655310621242: 155.4305478071928, 0.21783567134268544: 157.20327349450548, 0.208016032064128: 158.93742418381618, 0.19819639278557055: 160.5370014015984, 0.188376753507014: 161.93393704895107, 0.17855711422845655: 163.22793012587414, 0.1687374749499: 164.33220536363638, 0.15891783567134254: 165.25853918181818, 0.1490981963927851: 165.87719827272727, 0.13927855711422854: 166.40377963636365, 0.1294589178356711: 166.69870163636364, 0.11963927855711365: 166.87881872727274, 0.10981963927855709: 166.96893799999998, 0.1: 166.98831}

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

